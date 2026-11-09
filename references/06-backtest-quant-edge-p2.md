# 06-backtest-quant-edge — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: signal-classification

- Fuente: `agiprolabs/claude-trading-skills` → `skills/signal-classification` (MIT)
- Cuándo usarla: ML trading signal classifiers using XGBoost and LightGBM with walk-forward validation, SHAP feature importance, and threshold optimization
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/signal-classification/` (train_classifier.py, walk_forward_backtest.py)

# Signal Classification

Predict whether an asset's price will move up or down over a forward horizon using supervised machine learning classifiers. This skill covers the full pipeline: label creation, model training, walk-forward validation, feature importance analysis, and threshold optimization for trading applications.

## Why Tree-Based Models Dominate Trading ML

XGBoost and LightGBM are the workhorses of quantitative trading ML for good reason:

- **Non-linear relationships**: Financial features interact in complex, non-linear ways that trees capture naturally
- **Robust to feature scale**: No need to normalize or standardize inputs — trees split on rank order
- **Built-in feature importance**: Understand which features drive predictions without separate analysis
- **Fast training and inference**: Train on thousands of samples in seconds, predict in microseconds
- **Handle missing values**: Native support for NaN without imputation hacks
- **Regularization built in**: max_depth, min_child_weight, subsample all prevent overfitting

Linear models and deep learning have their place, but for tabular trading features with fewer than 100k samples, gradient-boosted trees consistently outperform alternatives.

## Classification Types

### Binary Classification

The simplest and most common setup. Predict whether forward returns exceed a threshold:

- **Up signal**: forward return > +1%
- **Down signal**: forward return < -1%
- **Neutral (excluded)**: -1% to +1% — drop these from training to create cleaner labels

```python
import numpy as np

def create_binary_labels(
    prices: np.ndarray, horizon: int = 24, threshold: float = 0.01
) -> np.ndarray:
    """Create binary labels from forward returns.

    Args:
        prices: Array of prices.
        horizon: Forward return lookback in bars.
        threshold: Minimum return magnitude for a label.

    Returns:
        Array of labels: 1 (up), 0 (down), NaN (neutral).
    """
    fwd_returns = np.roll(prices, -horizon) / prices - 1
    fwd_returns[-horizon:] = np.nan
    labels = np.where(fwd_returns > threshold, 1,
             np.where(fwd_returns < -threshold, 0, np.nan))
    return labels
```

### Multi-Class Classification

Three classes for finer signal granularity:

| Class | Condition | Typical threshold |
|-------|-----------|-------------------|
| Strong Up | fwd_return > +2% | High confidence long |
| Mild Up | +0.5% to +2% | Moderate confidence |
| Down | fwd_return < -0.5% | Avoid / short |

Multi-class reduces per-class sample size. Use only with large datasets (1000+ samples per class).

### Probability Calibration

Raw model probabilities from XGBoost/LightGBM are not well-calibrated. A predicted 0.7 probability does not mean 70% chance of being correct. Use calibration to fix this:

```python
from sklearn.calibration import CalibratedClassifierCV

calibrated = CalibratedClassifierCV(base_model, cv=5, method="isotonic")
calibrated.fit(X_train, y_train)
probs = calibrated.predict_proba(X_test)[:, 1]
```

Isotonic calibration works better than Platt scaling for tree models.

## Walk-Forward Validation

**This is the single most important concept in trading ML.** Standard cross-validation randomly shuffles data, which creates lookahead bias. Walk-forward validation respects time ordering.

### How It Works

```
Window 1: [===TRAIN===][GAP][=TEST=]
Window 2:    [===TRAIN===][GAP][=TEST=]
Window 3:       [===TRAIN===][GAP][=TEST=]
Window 4:          [===TRAIN===][GAP][=TEST=]
```

Each window:
1. Train on past N bars
2. Skip a gap (embargo) equal to the forward return horizon
3. Predict on next M bars
4. Record out-of-sample predictions
5. Slide forward and repeat

### Typical Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Train window | 30 days (720 hourly bars) | Enough data to learn, recent enough to be relevant |
| Test window | 7 days (168 hourly bars) | Enough predictions for statistical significance |
| Step size | 1 day (24 bars) | Overlap test windows for more data points |
| Gap (embargo) | Same as forward horizon | Prevents label leakage |

### Walk-Forward Implementation

```python
from typing import Iterator

def walk_forward_splits(
    n_samples: int,
    train_size: int = 720,
    test_size: int = 168,
    step_size: int = 24,
    gap: int = 24,
) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """Generate walk-forward train/test index splits.

    Args:
        n_samples: Total number of samples.
        train_size: Number of training samples per window.
        test_size: Number of test samples per window.
        step_size: Step between successive windows.
        gap: Gap between train end and test start.

    Yields:
        Tuples of (train_indices, test_indices).
    """
    start = 0
    while start + train_size + gap + test_size <= n_samples:
        train_idx = np.arange(start, start + train_size)
        test_start = start + train_size + gap
        test_idx = np.arange(test_start, test_start + test_size)
        yield train_idx, test_idx
        start += step_size
```

See `references/validation_methods.md` for purged CV, CPCV, and evaluation metrics.

## Model Training Pipeline

### Full Pipeline Overview

1. **Feature engineering** — compute technical indicators, on-chain metrics, volume features (see `feature-engineering` skill)
2. **Label creation** — forward returns with threshold, drop neutral zone
3. **Walk-forward split** — time-ordered train/test windows with gap
4. **Train model** — XGBoost or LightGBM on each training window
5. **Predict on test** — generate out-of-sample probability predictions
6. **Aggregate predictions** — concatenate all out-of-sample results
7. **Evaluate** — accuracy, precision, recall, F1, AUC, profit factor

### Quick Training Example

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    use_label_encoder=False,
    random_state=42,
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False,
)

probabilities = model.predict_proba(X_test)[:, 1]
```

See `references/model_guide.md` for parameter recommendations and tuning.

## SHAP Feature Importance

SHAP (SHapley Additive exPlanations) provides the gold standard for understanding model predictions.

### Global Feature Importance

Which features matter most across all predictions:

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot (top 15 features)
shap.summary_plot(shap_values, X_test, max_display=15)
```

### Local Explanations

Why a specific prediction was made:

```python
# Explain a single prediction
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

### Temporal Feature Importance

Track how feature importance drifts over walk-forward windows. If a feature's importance drops significantly, the market regime may have shifted.

## Threshold Optimization

The default 0.5 probability threshold is almost never optimal for trading.

### Why Not 0.5?

- Class imbalance: if 60% of labels are "up", a 0.5 threshold is too aggressive
- Trading costs: marginal signals (0.51 probability) rarely cover transaction costs
- Asymmetric payoffs: precision matters more than recall for trading

### Optimize for Profit Factor

```python
def optimize_threshold(
    probabilities: np.ndarray,
    returns: np.ndarray,
    thresholds: np.ndarray | None = None,
) -> tuple[float, float]:
    """Find threshold that maximizes profit factor.

    Args:
        probabilities: Model predicted probabilities.
        returns: Actual forward returns.
        thresholds: Thresholds to search over.

    Returns:
        Tuple of (best_threshold, best_profit_factor).
    """
    if thresholds is None:
        thresholds = np.arange(0.50, 0.85, 0.01)
    best_threshold, best_pf = 0.5, 0.0
    for t in thresholds:
        signals = probabilities >= t
        if signals.sum() < 10:
            continue
        signal_returns = returns[signals]
        wins = signal_returns[signal_returns > 0].sum()
        losses = abs(signal_returns[signal_returns < 0].sum())
        pf = wins / losses if losses > 0 else 0.0
        if pf > best_pf:
            best_pf = pf
            best_threshold = t
    return best_threshold, best_pf
```

Typical finding: optimal threshold is 0.60-0.75 for crypto trading signals.

## Crypto-Specific Considerations

### Short Training Windows

Crypto market regimes change fast. A model trained on 6 months of data may perform worse than one trained on 30 days. Use shorter training windows and retrain frequently.

### Class Imbalance

Most time periods are "flat" (returns within the neutral zone). Strategies to handle this:

- **Drop neutral zone**: only train on clear up/down labels
- **Undersample majority class**: `scale_pos_weight` in XGBoost
- **SMOTE**: synthetic minority oversampling (use cautiously — can introduce lookahead)
- **Adjust threshold**: raise the probability threshold to compensate

### Transaction Costs

A model with 55% accuracy sounds good, but after 0.5% round-trip costs (slippage + fees), many signals become unprofitable. Always evaluate signals net of costs:

```python
net_return = gross_return - 0.005  # 50 bps round-trip
```

### Feature Decay

Features lose predictive power over time as more participants discover and trade on them. Monitor rolling performance and retrain when metrics degrade.

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `feature-engineering` | Compute input features for the classifier |
| `vectorbt` | Backtest trading strategies from ML signals |
| `regime-detection` | Train separate models per regime, or use regime as a feature |
| `position-sizing` | Size positions based on classifier confidence |
| `risk-management` | Apply portfolio-level risk limits to ML-generated signals |

## Files

### References
- `references/model_guide.md` — XGBoost and LightGBM parameter guide, tuning, and ensembling
- `references/validation_methods.md` — Walk-forward, purged CV, CPCV, and evaluation metrics

### Scripts
- `scripts/train_classifier.py` — Train a signal classifier with walk-forward validation and feature importance
- `scripts/walk_forward_backtest.py` — Backtest ML signals vs buy-and-hold with walk-forward validation

## Dependencies

```bash
# Core (required)
uv pip install pandas numpy scikit-learn

# Optional (recommended)
uv pip install xgboost lightgbm shap
```

## Key Takeaways

1. **Walk-forward validation is non-negotiable** — random CV will give you wildly inflated results
2. **Optimize threshold for profit factor**, not accuracy — a high-precision, low-recall model beats a high-accuracy one
3. **Short training windows** for crypto — 30 days beats 6 months in most regimes
4. **Monitor feature decay** — retrain when rolling metrics drop below baseline
5. **Always evaluate net of costs** — a 55% accurate model may be unprofitable after fees
6. **SHAP over raw feature importance** — SHAP gives consistent, theoretically grounded explanations

### Referencia: references/model_guide.md

# Signal Classification — Model Guide

## XGBoost for Trading

### Installation

```bash
uv pip install xgboost
```

### Key Parameters

| Parameter | Default | Recommended | Purpose |
|-----------|---------|-------------|---------|
| `n_estimators` | 100 | 200 | Number of boosting rounds |
| `max_depth` | 6 | 4 | Maximum tree depth (lower = less overfit) |
| `learning_rate` | 0.3 | 0.05 | Step size shrinkage (lower = needs more rounds) |
| `subsample` | 1.0 | 0.8 | Fraction of samples per tree |
| `colsample_bytree` | 1.0 | 0.8 | Fraction of features per tree |
| `min_child_weight` | 1 | 5 | Minimum sum of instance weight in a child |
| `gamma` | 0 | 0.1 | Minimum loss reduction for a split |
| `reg_alpha` | 0 | 0.01 | L1 regularization |
| `reg_lambda` | 1 | 1.0 | L2 regularization |
| `scale_pos_weight` | 1 | ratio neg/pos | Handles class imbalance |

### Recommended Starting Configuration

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=5,
    gamma=0.1,
    reg_alpha=0.01,
    reg_lambda=1.0,
    eval_metric="logloss",
    use_label_encoder=False,
    random_state=42,
    n_jobs=-1,
)
```

### Overfitting Control

- **Early stopping**: stop training when validation metric stops improving

```python
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False,
)
```

- **max_depth=3-5**: deeper trees memorize noise
- **min_child_weight=5-10**: prevents splits on tiny groups
- **subsample + colsample_bytree < 1.0**: adds randomness, reduces variance

### Feature Importance

```python
# Gain-based importance (preferred)
importance = model.get_booster().get_score(importance_type="gain")

# Or via sklearn interface
importance = dict(zip(feature_names, model.feature_importances_))
```

## LightGBM for Trading

### Installation

```bash
uv pip install lightgbm
```

### Key Parameters

| Parameter | Default | Recommended | Purpose |
|-----------|---------|-------------|---------|
| `num_leaves` | 31 | 31 | Maximum leaves per tree (primary complexity control) |
| `n_estimators` | 100 | 200 | Number of boosting rounds |
| `learning_rate` | 0.1 | 0.05 | Step size shrinkage |
| `feature_fraction` | 1.0 | 0.8 | Fraction of features per tree (= colsample_bytree) |
| `bagging_fraction` | 1.0 | 0.8 | Fraction of data per tree (= subsample) |
| `bagging_freq` | 0 | 5 | Perform bagging every N iterations |
| `min_child_samples` | 20 | 20 | Minimum samples in a leaf |
| `reg_alpha` | 0 | 0.01 | L1 regularization |
| `reg_lambda` | 0 | 1.0 | L2 regularization |
| `max_depth` | -1 | 6 | Max tree depth (-1 = unlimited) |

### Recommended Starting Configuration

```python
import lightgbm as lgb

model = lgb.LGBMClassifier(
    num_leaves=31,
    n_estimators=200,
    learning_rate=0.05,
    feature_fraction=0.8,
    bagging_fraction=0.8,
    bagging_freq=5,
    min_child_samples=20,
    reg_alpha=0.01,
    reg_lambda=1.0,
    max_depth=6,
    random_state=42,
    n_jobs=-1,
    verbose=-1,
)
```

### LightGBM vs XGBoost Key Differences

- LightGBM uses leaf-wise growth (deeper, narrower trees); XGBoost uses level-wise
- `num_leaves` controls complexity in LightGBM; `max_depth` controls it in XGBoost
- LightGBM is typically 2-5x faster on datasets > 10k samples
- Rule of thumb: `num_leaves` should be < `2^max_depth` to avoid overfitting

## Comparison: XGBoost vs LightGBM

| Aspect | XGBoost | LightGBM |
|--------|---------|----------|
| Training speed | Moderate | Fast (2-5x faster) |
| Memory usage | Higher | Lower |
| Accuracy | Very good | Very good (comparable) |
| Small datasets (<5k) | Slightly better | Good |
| Large datasets (>50k) | Good | Better |
| Missing values | Native support | Native support |
| Categorical features | Requires encoding | Native support |
| Community | Very large | Large |
| Interpretability | Good | Good |

**Recommendation**: Use XGBoost for small trading datasets (<10k samples). Use LightGBM for larger datasets or when training speed matters (e.g., hyperparameter search).

## Hyperparameter Tuning with Optuna

Use walk-forward validation as the objective to avoid overfitting the hyperparameters:

```python
import optuna

def objective(trial: optuna.Trial) -> float:
    """Optuna objective using walk-forward profit factor."""
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 6),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1, log=True),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
    }
    # Run walk-forward with these params, return avg profit factor
    avg_pf = run_walk_forward(X, y, returns, params)
    return avg_pf

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
best_params = study.best_params
```

**Critical**: the walk-forward validation inside the objective must use the same windows you will use in production. Do not optimize on random CV metrics.

## Ensemble Methods

### Simple Average

Average predictions from XGBoost and LightGBM for more robust signals:

```python
def ensemble_predict(
    xgb_model: "XGBClassifier",
    lgb_model: "LGBMClassifier",
    X: "pd.DataFrame",
    weights: tuple[float, float] = (0.5, 0.5),
) -> "np.ndarray":
    """Weighted average of XGBoost and LightGBM predictions.

    Args:
        xgb_model: Trained XGBoost classifier.
        lgb_model: Trained LightGBM classifier.
        X: Feature matrix.
        weights: Weights for each model (must sum to 1).

    Returns:
        Blended probability predictions.
    """
    xgb_prob = xgb_model.predict_proba(X)[:, 1]
    lgb_prob = lgb_model.predict_proba(X)[:, 1]
    return weights[0] * xgb_prob + weights[1] * lgb_prob
```

### Stacking

Use out-of-sample predictions from walk-forward as features for a meta-model:

1. Run walk-forward with XGBoost — collect OOS predictions
2. Run walk-forward with LightGBM — collect OOS predictions
3. Train a logistic regression on (xgb_pred, lgb_pred) -> label
4. Use the meta-model for final predictions

Stacking adds complexity. Start with simple averaging and only stack if it demonstrably improves out-of-sample metrics.

## Common Mistakes

1. **Using random CV instead of walk-forward**: inflates metrics by 10-30%
2. **Too many estimators without early stopping**: memorizes training data
3. **Ignoring class imbalance**: model predicts majority class for everything
4. **Optimizing hyperparameters on test data**: double-dipping produces overfit params
5. **max_depth > 6**: almost always overfits on trading data
6. **Not setting random_state**: results are not reproducible
7. **Forgetting to set verbose=False/n_jobs**: noisy output and single-threaded training

### Referencia: references/validation_methods.md

# Signal Classification — Validation Methods

## Walk-Forward Validation

### Why Time-Series CV, Not Random CV

Random k-fold cross-validation shuffles data, allowing the model to train on future data and predict the past. This creates **lookahead bias** — the most common and devastating mistake in trading ML.

Walk-forward validation enforces temporal ordering: the model only ever predicts data it has never seen, in chronological order.

**Impact**: Random CV typically inflates accuracy by 10-30% compared to walk-forward. A model showing 65% accuracy with random CV may only achieve 52% walk-forward.

### Implementation

```python
import numpy as np
from typing import Iterator

def walk_forward_splits(
    n_samples: int,
    train_size: int = 720,
    test_size: int = 168,
    step_size: int = 24,
    gap: int = 24,
) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """Generate walk-forward train/test splits respecting time order.

    Args:
        n_samples: Total number of time-ordered samples.
        train_size: Training window length in bars.
        test_size: Test window length in bars.
        step_size: How far to advance between windows.
        gap: Embargo period between train end and test start.

    Yields:
        Tuples of (train_indices, test_indices).
    """
    start = 0
    while start + train_size + gap + test_size <= n_samples:
        train_end = start + train_size
        test_start = train_end + gap
        test_end = test_start + test_size
        train_idx = np.arange(start, train_end)
        test_idx = np.arange(test_start, test_end)
        yield train_idx, test_idx
        start += step_size
```

### Metrics Aggregation

Aggregate out-of-sample predictions across all walk-forward windows:

1. **Concatenation**: combine all OOS predictions, compute metrics once on the full set
2. **Per-window averaging**: compute metrics per window, report mean and std
3. **Weighted averaging**: weight each window by number of test samples

Method 1 (concatenation) is preferred — it gives a single set of realistic metrics.

### Minimum Requirements

For statistically meaningful results:

- **30+ test periods** across all windows combined
- **100+ trades** (signals that exceed threshold) total
- **5+ walk-forward windows** to assess stability
- **Test window > 2x forward return horizon** to avoid single-event dominance

## Purged Cross-Validation

### The Problem

If the forward return horizon is 24 bars, then bars at the boundary between train and test overlap: the label for bar T-24 depends on the price at bar T, which is in the test set. This creates subtle leakage.

### The Solution: Embargo Period

Insert a gap between train end and test start equal to the forward return horizon:

```
[====TRAIN====][--GAP--][===TEST===]
                ^^^^^^^
           embargo period
```

**Typical gap size**: same as the forward return horizon. If predicting 24-hour returns, use a 24-bar gap.

### Implementation

The `gap` parameter in the walk-forward function above handles this. Always set `gap >= forward_return_horizon`.

## Combinatorial Purged Cross-Validation (CPCV)

### Concept

Standard walk-forward gives one path through the data. CPCV generates multiple train/test paths using combinatorial selection of blocks:

1. Divide data into N contiguous blocks (e.g., N=10)
2. Select k blocks for testing (e.g., k=2)
3. Use remaining blocks for training
4. Apply purging at boundaries
5. Repeat for all C(N, k) combinations

This gives C(10, 2) = 45 different train/test configurations, producing more robust estimates.

### When to Use CPCV

- Sufficient data: need at least 1000+ samples
- High-stakes model selection: choosing between model architectures
- Research: validating that a signal is real, not noise
- Computationally feasible: C(N, k) models to train

### When Walk-Forward Is Sufficient

- Moderate data: 500-2000 samples
- Rapid iteration: testing many feature combinations
- Production: regular retraining on latest data

## Evaluating Trading Classifiers

### Why Accuracy Is Misleading

If 60% of your labels are "up" (bull market bias), a model that always predicts "up" achieves 60% accuracy. Accuracy tells you nothing about trading profitability.

### Precision

**Of all signals the model gives, what fraction are correct?**

```
Precision = True Positives / (True Positives + False Positives)
```

High precision = fewer but more reliable signals. For trading, precision > 0.55 is a reasonable target for crypto.

### Recall

**Of all actual profitable opportunities, what fraction did the model catch?**

```
Recall = True Positives / (True Positives + False Negatives)
```

High recall = catching most moves, but with more false signals. Less important for trading — missing trades is okay, losing money is not.

### F1 Score

Harmonic mean of precision and recall. A balanced metric, but still not trading-specific.

### AUC-ROC

Area under the receiver operating characteristic curve. Measures the model's ability to rank positive samples higher than negative ones. AUC > 0.55 is meaningful for trading; AUC > 0.60 is strong.

### Trading-Specific Metrics

These matter more than generic ML metrics:

**Profit Factor from Signals**

```python
def signal_profit_factor(
    predictions: np.ndarray,
    returns: np.ndarray,
    threshold: float = 0.5,
) -> float:
    """Compute profit factor from ML signals.

    Args:
        predictions: Model predicted probabilities.
        returns: Actual forward returns.
        threshold: Signal threshold.

    Returns:
        Profit factor (gross_profit / gross_loss).
    """
    signals = predictions >= threshold
    if signals.sum() == 0:
        return 0.0
    signal_returns = returns[signals]
    gross_profit = signal_returns[signal_returns > 0].sum()
    gross_loss = abs(signal_returns[signal_returns < 0].sum())
    return gross_profit / gross_loss if gross_loss > 0 else float("inf")
```

Target: profit factor > 1.3 after costs.

**Expected Return per Signal**

```python
def expected_return_per_signal(
    predictions: np.ndarray,
    returns: np.ndarray,
    threshold: float = 0.5,
    cost: float = 0.005,
) -> float:
    """Average return per signal, net of transaction costs.

    Args:
        predictions: Model predicted probabilities.
        returns: Actual forward returns.
        threshold: Signal threshold.
        cost: Round-trip transaction cost (default 50bps).

    Returns:
        Mean return per signal after costs.
    """
    signals = predictions >= threshold
    if signals.sum() == 0:
        return 0.0
    return float(np.mean(returns[signals]) - cost)
```

Target: positive expected return net of 50bps round-trip costs.

## Overfitting Detection

### Train vs Test Metric Gap

Compare metrics on training data vs out-of-sample test data:

| Gap (train - test) | Interpretation |
|---------------------|----------------|
| < 5% | Healthy — model generalizes well |
| 5-15% | Mild overfit — consider more regularization |
| 15-30% | Significant overfit — reduce complexity |
| > 30% | Severe overfit — model is memorizing noise |

### Metric Degradation Over Time

Plot out-of-sample metrics for each walk-forward window chronologically. If metrics decline steadily, the model's features are losing predictive power (feature decay).

### Random Signal Baseline

Compare your model against a random signal generator:

```python
random_accuracy = np.mean(np.random.randint(0, 2, size=len(y_test)) == y_test)
random_pf = signal_profit_factor(np.random.rand(len(y_test)), returns_test)
```

Your model should significantly exceed random baseline across all windows, not just on average.

### Practical Thresholds

A signal classification model is worth deploying if:

- Walk-forward AUC > 0.55 consistently across windows
- Profit factor > 1.3 at optimal threshold, net of costs
- Expected return per signal > 0 net of costs
- Train-test metric gap < 15%
- Performance is stable (not declining) across walk-forward windows
- Model generates at least 2-3 signals per day for sufficient volume


---

## SKILL: signal-postmortem

- Fuente: `tradermonty/claude-trading-skills` → `skills/signal-postmortem` (MIT)
- Cuándo usarla: Record and analyze post-trade outcomes for signals generated by edge pipeline and other skills. Track false positives, missed opportunities, and regime mismatches. Feed results back to edge-signal-aggregator weights and skill improvement backlog.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/signal-postmortem/` (requirements.txt, postmortem_analyzer.py, postmortem_recorder.py)

# Signal Postmortem

## Overview

Signal Postmortem records and analyzes the outcomes of trading signals generated by the edge pipeline, screeners, and other skills. It compares predicted edge direction against 5-day and 20-day realized returns, categorizes outcomes (true positive, false positive, missed opportunity, regime mismatch), and generates feedback for edge-signal-aggregator weight adjustments and skill improvement backlog entries.

## When to Use

- After a trade has been closed and you want to record the outcome
- When reviewing a batch of signals that have reached their holding period (5 or 20 days)
- To identify systematic false positive patterns from specific skills
- To generate feedback for edge-signal-aggregator weight calibration
- When building a skill improvement backlog from decision quality metrics
- For periodic (weekly/monthly) signal quality audits

## Prerequisites

- Python 3.9+
- FMP API key (optional, for fetching realized returns if not provided manually)
- Standard library + `requests` for API calls
- Input: signal records in JSON format (from edge-signal-aggregator or screener outputs)

### API Key Setup (Optional)

If you want to automatically fetch price data for return calculations, set up the FMP API key:

```bash
export FMP_API_KEY=your_api_key_here
```

Alternatively, pass the key via command line with `--api-key YOUR_KEY`. Without an API key, you can still record outcomes manually by providing `--exit-price` and `--exit-date`.

## Workflow

### Step 1: Prepare Signal Records

Gather closed or matured signal records. Each record should include:
- `signal_id`: Unique identifier
- `ticker`: Stock symbol
- `signal_date`: Date signal was generated
- `predicted_direction`: LONG or SHORT
- `source_skill`: Which skill generated the signal
- `entry_price`: Price at signal generation (optional, for manual override)

```bash
# Example: List signals ready for postmortem (5+ days old)
python3 skills/signal-postmortem/scripts/postmortem_recorder.py \
  --list-ready \
  --signals-dir state/signals/ \
  --min-days 5
```

### Step 2: Record Outcomes

Run the postmortem recorder to fetch realized returns and classify outcomes.

```bash
python3 skills/signal-postmortem/scripts/postmortem_recorder.py \
  --signals-file state/signals/aggregated_signals_2026-03-10.json \
  --holding-periods 5,20 \
  --output-dir reports/
```

For manual outcome recording (when price data is already available):

```bash
python3 skills/signal-postmortem/scripts/postmortem_recorder.py \
  --signal-id sig_aapl_20260310_abc \
  --exit-price 178.50 \
  --exit-date 2026-03-15 \
  --outcome-notes "Closed at target, +3.2% in 5 days" \
  --output-dir reports/
```

### Step 3: Classify Outcomes

The recorder automatically classifies each signal into one of four categories:

| Category | Definition |
|----------|------------|
| TRUE_POSITIVE | Predicted direction matched realized return sign |
| FALSE_POSITIVE | Predicted direction opposite to realized return |
| MISSED_OPPORTUNITY | Signal not taken but would have been profitable |
| REGIME_MISMATCH | Signal failed due to market regime change |

Classification rules are documented in `references/outcome-classification.md`.

### Step 4: Generate Feedback Files

Generate feedback for downstream consumers:

```bash
# Generate weight adjustment suggestions for edge-signal-aggregator
python3 skills/signal-postmortem/scripts/postmortem_analyzer.py \
  --postmortems-dir reports/postmortems/ \
  --generate-weight-feedback \
  --output-dir reports/

# Generate skill improvement backlog entries
python3 skills/signal-postmortem/scripts/postmortem_analyzer.py \
  --postmortems-dir reports/postmortems/ \
  --generate-improvement-backlog \
  --output-dir reports/
```

### Step 5: Review Summary Statistics

Generate aggregate statistics by skill, by ticker, and by time period:

```bash
python3 skills/signal-postmortem/scripts/postmortem_analyzer.py \
  --postmortems-dir reports/postmortems/ \
  --summary \
  --group-by skill,month \
  --output-dir reports/
```

## Output Format

### Postmortem Record (JSON)

```json
{
  "schema_version": "1.0",
  "postmortem_id": "pm_sig_aapl_20260310_abc",
  "signal_id": "sig_aapl_20260310_abc",
  "ticker": "AAPL",
  "signal_date": "2026-03-10",
  "source_skill": "edge-signal-aggregator",
  "predicted_direction": "LONG",
  "entry_price": 172.50,
  "realized_returns": {
    "5d": 0.032,
    "20d": 0.058
  },
  "exit_price": 178.50,
  "exit_date": "2026-03-15",
  "holding_days": 5,
  "outcome_category": "TRUE_POSITIVE",
  "regime_at_signal": "RISK_ON",
  "regime_at_exit": "RISK_ON",
  "outcome_notes": "Clean breakout, held through minor pullback",
  "recorded_at": "2026-03-17T10:30:00Z"
}
```

### Weight Feedback (JSON)

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-03-17T10:35:00Z",
  "analysis_period": {
    "from": "2026-02-01",
    "to": "2026-03-15"
  },
  "skill_adjustments": [
    {
      "skill": "vcp-screener",
      "current_weight": 1.0,
      "suggested_weight": 0.85,
      "reason": "15% false positive rate in RISK_OFF regime",
      "sample_size": 42
    }
  ],
  "confidence": "MEDIUM",
  "min_sample_threshold": 20
}
```

### Skill Improvement Backlog Entry (YAML)

```yaml
- skill: vcp-screener
  issue_type: false_positive_cluster
  severity: medium
  evidence:
    false_positive_rate: 0.15
    sample_size: 42
    regime_correlation: RISK_OFF
  suggested_action: "Add regime filter or reduce signal confidence in RISK_OFF"
  generated_by: signal-postmortem
  generated_at: "2026-03-17T10:35:00Z"
```

### Summary Report (Markdown)

Reports are saved to `reports/` with filenames `postmortem_summary_YYYY-MM-DD.md`.

## Resources

- `scripts/postmortem_recorder.py` -- Records individual signal outcomes
- `scripts/postmortem_analyzer.py` -- Generates feedback and summary statistics
- `references/outcome-classification.md` -- Classification rules and edge cases
- `references/feedback-integration.md` -- How to integrate feedback with downstream skills

## Key Principles

1. **Honest Attribution** -- Every outcome is attributed to its source skill for accountability
2. **Regime Awareness** -- Regime context is recorded to distinguish skill failure from market regime shifts
3. **Minimum Sample Size** -- Weight adjustments require 20+ signals for statistical validity
4. **Feedback Loop Closure** -- Results flow back to improve both signal aggregation and skill quality

### Referencia: references/feedback-integration.md

# Feedback Integration Guide

## Overview

This document explains how signal postmortem results integrate with downstream systems: edge-signal-aggregator weight calibration and the skill improvement backlog.

## Feedback Targets

### 1. Edge-Signal-Aggregator Weight Calibration

**Purpose**: Adjust the weight of each contributing skill based on historical accuracy.

**Integration Point**: `reports/weight_feedback_YYYY-MM-DD.json`

**Consumption**:
1. edge-signal-aggregator reads feedback file on startup
2. Applies weight adjustments to skill contribution scores
3. Logs adjustment application for audit trail

**Weight Adjustment Formula**:

```
new_weight = current_weight * (1 + adjustment_factor)

adjustment_factor = (accuracy - baseline) * sensitivity

where:
- accuracy = true_positives / (true_positives + false_positives)
- baseline = 0.55 (expected random accuracy)
- sensitivity = 0.5 (dampening factor to avoid overreaction)
```

**Constraints**:
- Minimum weight: 0.3 (never fully disable a skill)
- Maximum weight: 2.0 (never over-amplify)
- Minimum sample size: 20 signals for adjustment
- Rolling window: 90 days of postmortem data

### 2. Skill Improvement Backlog

**Purpose**: Generate actionable improvement tasks for the skill improvement loop.

**Integration Point**: `reports/skill_improvement_backlog.yaml`

**Consumption**:
1. Skill improvement loop reads backlog entries
2. Prioritizes by severity and sample size
3. Creates improvement branches for high-severity issues

**Issue Types**:

| Issue Type | Trigger | Severity |
|------------|---------|----------|
| `false_positive_cluster` | >15% FP rate with 20+ samples | MEDIUM-HIGH |
| `regime_sensitivity` | >25% regime mismatch rate | MEDIUM |
| `sector_blind_spot` | >20% FP rate in specific sector | MEDIUM |
| `timing_drift` | Accuracy degraded >10% over 30 days | LOW-MEDIUM |
| `overconfidence` | High-confidence signals underperforming | HIGH |

**Backlog Entry Format**:

```yaml
- skill: vcp-screener
  issue_type: false_positive_cluster
  severity: medium
  evidence:
    false_positive_rate: 0.18
    sample_size: 45
    regime_correlation: RISK_OFF
    sector_correlation: Technology
  suggested_action: "Add RISK_OFF regime filter or reduce confidence"
  priority_score: 72  # Calculated from severity * sample_size * impact
  generated_by: signal-postmortem
  generated_at: "2026-03-17T10:35:00Z"
  status: pending
```

## Feedback Frequency

### Real-Time (Per Signal)

- Postmortem record created immediately after trade closure
- Stored in `reports/postmortems/`

### Daily Batch

- Weight feedback regenerated daily at 06:00
- Improvement backlog updated with new entries
- Old entries marked as `addressed` when improvements deployed

### Weekly Review

- Summary statistics by skill, sector, regime
- Trend analysis (rolling 4-week accuracy)
- Human review flagged for significant changes

## Data Flow Diagram

```
Signal Generated
       |
       v
Trade Executed (or skipped)
       |
       v
Holding Period Completes
       |
       v
postmortem_recorder.py
       |
       +---> postmortem record (JSON)
       |
       v
postmortem_analyzer.py
       |
       +---> weight_feedback.json --> edge-signal-aggregator
       |
       +---> skill_improvement_backlog.yaml --> skill improvement loop
       |
       +---> summary report (Markdown)
```

## Idempotency and Deduplication

### Postmortem Records

- `postmortem_id` = `pm_` + `signal_id`
- If postmortem already exists, update instead of duplicate
- Version field tracks updates

### Weight Feedback

- Regenerated fresh each run (not cumulative)
- Based on rolling 90-day window
- Old feedback files archived to `reports/archive/`

### Backlog Entries

- Keyed by `skill` + `issue_type` + `month`
- New evidence updates existing entry instead of creating duplicate
- Entry moved to `addressed` when skill version changes

## Minimum Thresholds

To avoid noisy feedback from small samples:

| Metric | Minimum |
|--------|---------|
| Weight adjustment | 20 signals |
| Backlog entry | 15 signals |
| Summary statistics | 10 signals |
| Regime correlation | 10 signals per regime |

## Manual Override Integration

When human review identifies an issue not caught by automated analysis:

```yaml
# Manual backlog entry
- skill: earnings-trade-analyzer
  issue_type: manual_review
  severity: high
  evidence:
    description: "Systematic gap fade failure in biotech earnings"
    reviewer: "tradermonty"
  suggested_action: "Exclude biotech from gap fade signals"
  generated_by: human_review
  generated_at: "2026-03-17T14:00:00Z"
```

Manual entries have `generated_by: human_review` and are prioritized higher.

## Conflict Resolution

When automated and manual feedback conflict:

1. Manual feedback takes precedence for immediate action
2. Automated feedback triggers investigation
3. Resolution documented in backlog entry

## Audit Trail

All feedback actions are logged:

```json
{
  "action": "weight_adjustment_applied",
  "skill": "vcp-screener",
  "old_weight": 1.0,
  "new_weight": 0.85,
  "reason": "15% FP rate in RISK_OFF",
  "applied_at": "2026-03-17T06:00:00Z",
  "applied_by": "edge-signal-aggregator"
}
```

Logs stored in `logs/feedback_audit.log` with 90-day retention.

### Referencia: references/outcome-classification.md

# Outcome Classification Guide

## Overview

This document defines how signal outcomes are classified in the postmortem process. Accurate classification is essential for meaningful feedback to edge-signal-aggregator and skill improvement.

## Classification Categories

### 1. TRUE_POSITIVE

**Definition**: The predicted direction matched the realized return sign.

**Criteria**:
- LONG signal with positive realized return at holding period
- SHORT signal with negative realized return at holding period
- Minimum threshold: |return| >= 0.5% to avoid noise classification

**Examples**:
- Signal: LONG AAPL at $170, predicted 5-day upside
- Outcome: AAPL at $175 after 5 days (+2.9%)
- Classification: TRUE_POSITIVE

### 2. FALSE_POSITIVE

**Definition**: The predicted direction was opposite to the realized return.

**Criteria**:
- LONG signal with negative realized return at holding period
- SHORT signal with positive realized return at holding period
- Minimum threshold: |return| >= 0.5% to avoid noise classification

**Sub-categories**:
- `FALSE_POSITIVE_MILD`: -0.5% to -2% for LONG (or +0.5% to +2% for SHORT)
- `FALSE_POSITIVE_SEVERE`: worse than -2% for LONG (or +2% for SHORT)

**Examples**:
- Signal: LONG NVDA at $900, predicted breakout
- Outcome: NVDA at $870 after 5 days (-3.3%)
- Classification: FALSE_POSITIVE_SEVERE

### 3. MISSED_OPPORTUNITY

**Definition**: A signal that was generated but not acted upon, and would have been profitable.

**Use Cases**:
- Signals filtered out by aggregator confidence threshold
- Signals skipped due to position sizing constraints
- Signals in watchlist but not traded

**Criteria**:
- Signal was generated but `trade_taken = false`
- Realized return in predicted direction >= 2%

**Note**: This category helps identify overly conservative filtering.

### 4. REGIME_MISMATCH

**Definition**: Signal failed primarily due to a market regime change rather than skill error.

**Criteria**:
- `regime_at_signal` differs from `regime_at_exit`
- AND return in opposite direction of prediction
- Regime change must be documented (e.g., VIX spike, Fed announcement)

**Examples**:
- Signal: LONG growth stock on 2026-03-05 (RISK_ON regime)
- Outcome: Tariff announcement on 2026-03-07 triggered RISK_OFF
- Result: Stock down 8% due to sector rotation
- Classification: REGIME_MISMATCH (not FALSE_POSITIVE)

**Regime Detection**:
- RISK_ON: VIX < 20, breadth > 60%, leading stocks advancing
- RISK_OFF: VIX > 25, breadth < 40%, defensive rotation
- TRANSITION: Mixed signals, high uncertainty

## Edge Cases

### Flat Outcome (|return| < 0.5%)

- Classification: `NEUTRAL`
- Does not count as TRUE_POSITIVE or FALSE_POSITIVE
- May indicate weak signal strength

### Early Exit

When a trade is closed before the target holding period:

```
holding_period_actual < holding_period_target
```

- Use actual holding period for return calculation
- Note `early_exit = true` in postmortem record
- Include `early_exit_reason`: stop_loss, target_reached, discretionary

### Gap Events

If the stock gapped significantly at open due to overnight news:

- Record `gap_event = true`
- Include `gap_pct` in postmortem
- Consider separate analysis for gap-driven outcomes

### Multiple Holding Periods

The skill tracks both 5-day and 20-day returns:

| Metric | 5-Day | 20-Day |
|--------|-------|--------|
| Purpose | Short-term edge validation | Medium-term edge validation |
| Threshold | 0.5% | 1.0% |
| Weight for feedback | 60% | 40% |

A signal can be TRUE_POSITIVE at 5 days but FALSE_POSITIVE at 20 days (or vice versa). Both are recorded.

## Classification Decision Tree

```
1. Was the trade taken?
   NO  -> If would have been profitable: MISSED_OPPORTUNITY
         Otherwise: SKIPPED (no postmortem needed)
   YES -> Continue

2. Did regime change during holding period?
   YES -> Is return in wrong direction AND > 2% loss?
          YES -> REGIME_MISMATCH
          NO  -> Continue
   NO  -> Continue

3. Is |return| < 0.5%?
   YES -> NEUTRAL
   NO  -> Continue

4. Does return sign match predicted direction?
   YES -> TRUE_POSITIVE
   NO  -> FALSE_POSITIVE (check severity)
```

## Attribution Rules

### Single-Source Signals

When a signal comes from one skill (e.g., vcp-screener alone):
- Full attribution to that skill

### Aggregated Signals

When a signal comes from edge-signal-aggregator combining multiple skills:
- Attribution proportional to each skill's contribution weight
- Example: VCP (0.4) + CANSLIM (0.3) + Breadth (0.3)
- If FALSE_POSITIVE: each skill receives proportional negative feedback

### Override Signals

When a human overrides a skill recommendation:
- Record `human_override = true`
- Separate analysis track for human decision quality

## Confidence Adjustment Factors

Classification confidence is adjusted based on:

| Factor | Adjustment |
|--------|------------|
| High volume day | +10% confidence |
| Low volume day | -10% confidence |
| Earnings during holding period | -20% confidence |
| VIX spike > 5 points | -15% confidence |
| Large gap (> 3%) | -15% confidence |

Final confidence is capped at [0.5, 1.0] range.


---

## SKILL: stock-correlation

- Fuente: `himself65/finance-skills` → `plugins/market-analysis/skills/stock-correlation` (MIT)
- Cuándo usarla: >

# Stock Correlation Analysis Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Finds and analyzes correlated stocks using historical price data from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance). Routes to specialized sub-skills based on user intent.

**Important**: This is for research and educational purposes only. Not financial advice. yfinance is not affiliated with Yahoo, Inc.

---

## Step 1: Ensure Dependencies Are Available

**Current environment status:**

```
!`python3 -c "exec('try:\n import yfinance, pandas, numpy\n print(f\'yfinance={yfinance.__version__} pandas={pandas.__version__} numpy={numpy.__version__}\')\nexcept Exception:\n print(\'DEPS_MISSING\')')"`
```

If `DEPS_MISSING`, install required packages before running any code:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "numpy"])
```

If all dependencies are already installed, skip the install step and proceed directly.

---

## Step 2: Route to the Correct Sub-Skill

Classify the user's request and jump to the matching sub-skill section below.

| User Request | Route To | Examples |
|---|---|---|
| Single ticker, wants to find related stocks | **Sub-Skill A: Co-movement Discovery** | "what correlates with NVDA", "find stocks related to AMD", "sympathy plays for TSLA" |
| Two or more specific tickers, wants relationship details | **Sub-Skill B: Return Correlation** | "correlation between AMD and NVDA", "how do LITE and COHR move together", "compare AAPL vs MSFT" |
| Group of tickers, wants structure/grouping | **Sub-Skill C: Sector Clustering** | "correlation matrix for FAANG", "cluster these semiconductor stocks", "sector peers for AMD" |
| Wants time-varying or conditional correlation | **Sub-Skill D: Realized Correlation** | "rolling correlation AMD NVDA", "when NVDA drops what else drops", "how has correlation changed" |

If ambiguous, default to **Sub-Skill A** (Co-movement Discovery) for single tickers, or **Sub-Skill B** (Return Correlation) for two tickers.

### Defaults for all sub-skills

| Parameter | Default |
|---|---|
| Lookback period | `1y` (1 year) |
| Data interval | `1d` (daily) |
| Correlation method | Pearson |
| Minimum correlation threshold | 0.60 |
| Number of results | Top 10 |
| Return type | Daily log returns |
| Rolling window | 60 trading days |

---

## Sub-Skill A: Co-movement Discovery

**Goal**: Given a single ticker, find stocks that move with it.

### A1: Build the peer universe

You need 15-30 candidates. **Do not use hardcoded ticker lists** — build the universe dynamically at runtime. See `references/sector_universes.md` for the full implementation. The approach:

1. **Screen same-industry stocks** using `yf.screen()` + `yf.EquityQuery` to find stocks in the same industry as the target
2. **Broaden to sector** if the industry screen returns fewer than 10 peers
3. **Add thematic/adjacent industries** — read the target's `longBusinessSummary` and screen 1-2 related industries (e.g., a semiconductor company → also screen semiconductor equipment)
4. **Combine, deduplicate, remove target ticker**

### A2: Compute correlations

```python
import yfinance as yf
import pandas as pd
import numpy as np

def discover_comovement(target_ticker, peer_tickers, period="1y"):
    all_tickers = [target_ticker] + [t for t in peer_tickers if t != target_ticker]
    data = yf.download(all_tickers, period=period, auto_adjust=True, progress=False)

    # Extract close prices — yf.download returns MultiIndex (Price, Ticker) columns
    closes = data["Close"].dropna(axis=1, thresh=max(60, len(data) // 2))

    # Log returns
    returns = np.log(closes / closes.shift(1)).dropna()
    corr_series = returns.corr()[target_ticker].drop(target_ticker, errors="ignore")

    # Rank by absolute correlation
    ranked = corr_series.abs().sort_values(ascending=False)

    result = pd.DataFrame({
        "Ticker": ranked.index,
        "Correlation": [round(corr_series[t], 4) for t in ranked.index],
    })
    return result, returns
```

### A3: Present results

Show a ranked table with company names and sectors (fetch via `yf.Ticker(t).info.get("shortName")`). Values below are illustrative:

| Rank | Ticker | Company | Correlation | Why linked |
|---|---|---|---|---|
| 1 | AMD | Advanced Micro Devices | 0.82 | Same industry — GPU/CPU |
| 2 | AVGO | Broadcom | 0.78 | AI infrastructure peer |

Include:
- Top 10 positively correlated stocks
- Any notable negatively correlated stocks (potential hedges)
- Brief explanation of **why** each might be linked (sector, supply chain, customer overlap)

---

## Sub-Skill B: Return Correlation

**Goal**: Deep-dive into the relationship between two (or a few) specific tickers.

### B1: Download and compute

```python
import yfinance as yf
import pandas as pd
import numpy as np

def return_correlation(ticker_a, ticker_b, period="1y"):
    data = yf.download([ticker_a, ticker_b], period=period, auto_adjust=True, progress=False)
    closes = data["Close"][[ticker_a, ticker_b]].dropna()

    returns = np.log(closes / closes.shift(1)).dropna()
    corr = returns[ticker_a].corr(returns[ticker_b])

    # Beta: how much does B move per unit move of A
    cov_matrix = returns.cov()
    beta = cov_matrix.loc[ticker_b, ticker_a] / cov_matrix.loc[ticker_a, ticker_a]

    # R-squared
    r_squared = corr ** 2

    # Rolling 60-day correlation for stability
    rolling_corr = returns[ticker_a].rolling(60).corr(returns[ticker_b])

    # Spread (log price ratio) for mean-reversion
    spread = np.log(closes[ticker_a] / closes[ticker_b])
    spread_z = (spread - spread.mean()) / spread.std()

    return {
        "correlation": round(corr, 4),
        "beta": round(beta, 4),
        "r_squared": round(r_squared, 4),
        "rolling_corr_mean": round(rolling_corr.mean(), 4),
        "rolling_corr_std": round(rolling_corr.std(), 4),
        "rolling_corr_min": round(rolling_corr.min(), 4),
        "rolling_corr_max": round(rolling_corr.max(), 4),
        "spread_z_current": round(spread_z.iloc[-1], 4),
        "observations": len(returns),
    }
```

### B2: Present results

Show a summary card (illustrative values):

| Metric | Value |
|---|---|
| Pearson Correlation | 0.82 |
| Beta (B vs A) | 1.15 |
| R-squared | 0.67 |
| Rolling Corr (60d avg) | 0.80 |
| Rolling Corr Range | [0.55, 0.94] |
| Rolling Corr Std Dev | 0.08 |
| Spread Z-Score (current) | +1.2 |
| Observations | 250 |

Interpretation guide:
- **Correlation > 0.80**: Strong co-movement — these stocks are tightly linked
- **Correlation 0.50–0.80**: Moderate — shared sector drivers but independent factors too
- **Correlation < 0.50**: Weak — limited co-movement despite possible sector overlap
- **High rolling std**: Unstable relationship — correlation varies significantly over time
- **Spread Z > |2|**: Unusual divergence from historical relationship

---

## Sub-Skill C: Sector Clustering

**Goal**: Given a group of tickers, show the full correlation structure and identify clusters.

### C1: Build the correlation matrix

```python
import yfinance as yf
import pandas as pd
import numpy as np

def sector_clustering(tickers, period="1y"):
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)

    # yf.download returns MultiIndex (Price, Ticker) columns
    closes = data["Close"].dropna(axis=1, thresh=max(60, len(data) // 2))
    returns = np.log(closes / closes.shift(1)).dropna()
    corr_matrix = returns.corr()

    # Hierarchical clustering order
    from scipy.cluster.hierarchy import linkage, leaves_list
    from scipy.spatial.distance import squareform

    dist_matrix = 1 - corr_matrix.abs()
    np.fill_diagonal(dist_matrix.values, 0)
    condensed = squareform(dist_matrix)
    linkage_matrix = linkage(condensed, method="ward")
    order = leaves_list(linkage_matrix)
    ordered_tickers = [corr_matrix.columns[i] for i in order]

    # Reorder matrix
    clustered = corr_matrix.loc[ordered_tickers, ordered_tickers]

    return clustered, returns
```

Note: if `scipy` is not available, fall back to sorting by average correlation instead of hierarchical clustering.

### C2: Present results

1. **Full correlation matrix** — formatted as a table. For more than 8 tickers, show as a heatmap description or highlight only the strongest/weakest pairs.

2. **Identified clusters** — group tickers that have high intra-group correlation:
   - Cluster 1: [NVDA, AMD, AVGO] — avg intra-correlation 0.82
   - Cluster 2: [AAPL, MSFT] — avg intra-correlation 0.75

3. **Outliers** — tickers with low average correlation to the group (potential diversifiers).

4. **Strongest pairs** — top 5 highest-correlation pairs in the matrix.

5. **Weakest pairs** — top 5 lowest/negative-correlation pairs (hedging candidates).

---

## Sub-Skill D: Realized Correlation

**Goal**: Show how correlation changes over time and under different market conditions.

### D1: Rolling correlation

```python
import yfinance as yf
import pandas as pd
import numpy as np

def realized_correlation(ticker_a, ticker_b, period="2y", windows=[20, 60, 120]):
    data = yf.download([ticker_a, ticker_b], period=period, auto_adjust=True, progress=False)
    closes = data["Close"][[ticker_a, ticker_b]].dropna()

    returns = np.log(closes / closes.shift(1)).dropna()

    rolling = {}
    for w in windows:
        rolling[f"{w}d"] = returns[ticker_a].rolling(w).corr(returns[ticker_b])

    return rolling, returns
```

### D2: Regime-conditional correlation

```python
def regime_correlation(returns, ticker_a, ticker_b, condition_ticker=None):
    """Compare correlation across up/down/volatile regimes."""
    if condition_ticker is None:
        condition_ticker = ticker_a

    ret = returns[condition_ticker]

    regimes = {
        "All Days": pd.Series(True, index=returns.index),
        "Up Days (target > 0)": ret > 0,
        "Down Days (target < 0)": ret < 0,
        "High Vol (top 25%)": ret.abs() > ret.abs().quantile(0.75),
        "Low Vol (bottom 25%)": ret.abs() < ret.abs().quantile(0.25),
        "Large Drawdown (< -2%)": ret < -0.02,
    }

    results = {}
    for name, mask in regimes.items():
        subset = returns[mask]
        if len(subset) >= 20:
            results[name] = {
                "correlation": round(subset[ticker_a].corr(subset[ticker_b]), 4),
                "days": int(mask.sum()),
            }

    return results
```

### D3: Present results

1. **Rolling correlation summary table** (illustrative values here and in the regime table):

| Window | Current | Mean | Min | Max | Std |
|---|---|---|---|---|---|
| 20-day | 0.88 | 0.76 | 0.32 | 0.95 | 0.12 |
| 60-day | 0.82 | 0.78 | 0.55 | 0.92 | 0.08 |
| 120-day | 0.80 | 0.79 | 0.68 | 0.88 | 0.05 |

2. **Regime correlation table**:

| Regime | Correlation | Days |
|---|---|---|
| All Days | 0.82 | 250 |
| Up Days | 0.75 | 132 |
| Down Days | 0.87 | 118 |
| High Vol (top 25%) | 0.90 | 63 |
| Large Drawdown (< -2%) | 0.93 | 28 |

3. **Key insight**: Highlight whether correlation **increases during sell-offs** (very common — "correlations go to 1 in a crisis"). This is critical for risk management.

4. **Trend**: Is correlation trending higher or lower recently vs. its historical average?

---

## Step 3: Respond to the User

After running the appropriate sub-skill, present results clearly:

### Always include

- The **lookback period** and **data interval** used
- The **number of observations** (trading days)
- Any tickers **dropped due to insufficient data**

### Always caveat

- **Correlation is not causation** — co-movement does not imply a causal link
- **Past correlation does not guarantee future correlation** — regimes shift
- **Short lookback windows** produce noisy estimates; longer windows smooth but may miss regime changes

### Practical applications (mention when relevant)

- **Sympathy plays**: Stocks likely to follow a peer's earnings/news move
- **Pair trading**: High-correlation pairs where the spread has diverged from its mean
- **Portfolio diversification**: Finding low-correlation assets to reduce risk
- **Hedging**: Identifying inversely correlated instruments
- **Sector rotation**: Understanding which sectors move together
- **Risk management**: Correlation spikes during stress — diversification may fail when needed most

Present the data and let the user draw conclusions; don't recommend specific trades.

---

## Reference Files

- `references/sector_universes.md` — Dynamic peer universe construction using yfinance Screener API

Read the reference file when you need to build a peer universe for a given ticker.

### Referencia: README.md

# stock-correlation

Analyze stock correlations to find related companies, sector peers, and pair-trading candidates using historical price data.

## What it does

Routes to four specialized sub-skills based on user intent:

- **Co-movement Discovery** — given a single ticker, find the most correlated stocks from curated sector and thematic peer universes (e.g., "what correlates with NVDA?")
- **Return Correlation** — deep-dive pairwise analysis between two tickers: Pearson correlation, beta, R-squared, spread Z-score, and rolling stability (e.g., "correlation between AMD and NVDA")
- **Sector Clustering** — full NxN correlation matrix with hierarchical clustering to identify groups and outliers (e.g., "correlation matrix for FAANG")
- **Realized Correlation** — time-varying and regime-conditional correlation: rolling windows (20/60/120-day), up vs down days, high-vol vs low-vol, drawdown regimes (e.g., "when NVDA drops what else drops?")

## Triggers

- "what correlates with NVDA", "find stocks related to AMD"
- "correlation between AAPL and MSFT", "how do LITE and COHR move together"
- "what moves with", "stocks that move together", "sympathy plays"
- "sector peers", "pair trading", "hedging pair"
- "when NVDA drops what else drops", "rolling correlation"
- "correlation matrix for FAANG", "cluster these stocks"
- Well-known pairs: AMD/NVDA, GOOGL/AVGO, LITE/COHR

## Prerequisites

- Python 3.8+
- The skill auto-installs `yfinance`, `pandas`, and `numpy` via pip if not already present
- `scipy` is optional (used for hierarchical clustering in Sector Clustering sub-skill; falls back to sorting if unavailable)

## Platform

Works on **all platforms** (Claude Code, Claude.ai with code execution, etc.).

## Setup

```bash
# Choose finance-market-analysis when prompted.
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill stock-correlation
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/sector_universes.md` — Dynamic peer universe construction using yfinance Screener API, with fallback strategies

### Referencia: references/sector_universes.md

# Dynamic Peer Universe Construction

How to build a peer universe at runtime for correlation analysis. **Do not hardcode ticker lists** — fetch them dynamically so results stay current.

---

## Method 1: Same-Sector Screen (Primary)

Use yfinance's `yf.screen()` + `EquityQuery` to find stocks in the same sector as the target. Note: the screener supports filtering by `sector` but not directly by `industry` — use sector-level screening and let the correlation math surface the closest peers.

```python
import yfinance as yf
from yfinance import EquityQuery

def get_sector_peers(ticker_symbol, min_market_cap=1_000_000_000, max_results=30):
    """Find peers in the same sector above a market cap threshold."""
    target = yf.Ticker(ticker_symbol)
    info = target.info
    sector = info.get("sector", "")

    if not sector:
        return []

    # Screen for same-sector stocks on major US exchanges
    query = EquityQuery("and", [
        EquityQuery("eq", ["sector", sector]),
        EquityQuery("gt", ["intradaymarketcap", min_market_cap]),
        EquityQuery("is-in", ["exchange", "NMS", "NYQ"]),
    ])

    result = yf.screen(query, size=max_results, sortField="intradaymarketcap", sortAsc=False)

    peers = []
    for quote in result.get("quotes", []):
        symbol = quote.get("symbol", "")
        if symbol and symbol != ticker_symbol:
            peers.append(symbol)

    return peers
```

## Method 2: Thematic Expansion

For cross-sector correlations (e.g., AI supply chain spans semis + cloud + software), read the target's business description and screen adjacent sectors:

```python
def get_thematic_context(ticker_symbol):
    """Get company context to inform adjacent-sector screening."""
    target = yf.Ticker(ticker_symbol)
    info = target.info
    return {
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "description": info.get("longBusinessSummary", ""),
    }
```

After reading the company description, screen 1-2 adjacent sectors. For example:
- A semiconductor company (Technology sector) → also consider screening for related names in "Industrials" (equipment suppliers)
- A cloud platform → also screen for networking/data-center REITs
- An EV maker (Consumer Cyclical) → also screen "Basic Materials" (battery materials), "Industrials" (auto parts)

## Combining Methods

Build the full universe by combining sector screen + thematic expansion:

```python
def build_peer_universe(ticker_symbol):
    """Build a comprehensive peer universe for correlation analysis."""
    peers = set()

    # 1. Same sector
    sector_peers = get_sector_peers(ticker_symbol, min_market_cap=1_000_000_000, max_results=25)
    peers.update(sector_peers)

    # 2. If too few, lower the market cap threshold
    if len(peers) < 10:
        more_peers = get_sector_peers(ticker_symbol, min_market_cap=500_000_000, max_results=30)
        peers.update(more_peers)

    # 3. Add thematic/adjacent sectors based on business description
    # (model should reason about which adjacent sectors to screen)

    peers.discard(ticker_symbol)
    return list(peers)
```

**Target**: 15-30 peers for a meaningful correlation scan. Too few gives sparse results; too many slows the yfinance download.

---

## Fallback: Well-Known Groupings

If the screener is unavailable or rate-limited, use well-known benchmarks:

- **Mag 7**: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
- **Major indices**: SPY (S&P 500), QQQ (Nasdaq 100), DIA (Dow 30), IWM (Russell 2000)
- **Sector ETFs**: XLK, XLF, XLE, XLV, XLI, XLP, XLU, XLY, XLC, XLRE, XLB

These ETFs are useful as correlation benchmarks — comparing a stock's correlation to sector ETFs quickly reveals its primary driver.


---

## SKILL: stock-liquidity

- Fuente: `himself65/finance-skills` → `plugins/market-analysis/skills/stock-liquidity` (MIT)
- Cuándo usarla: >

# Stock Liquidity Analysis Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Analyzes stock liquidity across multiple dimensions — bid-ask spreads, volume patterns, order book depth, estimated market impact, and turnover ratios — using data from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance).

Liquidity matters because it determines the real cost of trading. The quoted price is not what you actually pay — spreads, slippage, and market impact all eat into returns, especially for larger positions or less liquid names.

**Important**: This is for research and educational purposes only. Not financial advice. yfinance is not affiliated with Yahoo, Inc.

---

## Step 1: Ensure Dependencies Are Available

**Current environment status:**

```
!`python3 -c "exec('try:\n import yfinance, pandas, numpy\n print(f\'yfinance={yfinance.__version__} pandas={pandas.__version__} numpy={numpy.__version__}\')\nexcept Exception:\n print(\'DEPS_MISSING\')')"`
```

If `DEPS_MISSING`, install required packages:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "pandas", "numpy"])
```

If already installed, skip and proceed.

---

## Step 2: Route to the Correct Sub-Skill

Classify the user's request and jump to the matching section. If the user asks for a general liquidity assessment without specifying a particular metric, run **Sub-Skill A** (Liquidity Dashboard) which computes all key metrics together.

| User Request | Route To | Examples |
|---|---|---|
| General liquidity check, "how liquid is X" | **Sub-Skill A: Liquidity Dashboard** | "how liquid is AAPL", "liquidity analysis for TSLA", "is this stock liquid enough" |
| Bid-ask spread, trading costs, effective spread | **Sub-Skill B: Spread Analysis** | "bid-ask spread for AMD", "what's the spread on NVDA options", "trading cost estimate" |
| Volume, ADTV, dollar volume, volume profile | **Sub-Skill C: Volume Analysis** | "volume analysis MSFT", "average daily volume", "volume profile for SPY" |
| Order book depth, market depth, level 2 | **Sub-Skill D: Order Book Depth** | "order book depth for AAPL", "market depth", "show me the book" |
| Market impact, slippage, execution cost for large orders | **Sub-Skill E: Market Impact** | "how much would 50k shares move the price", "slippage estimate", "market impact of $1M order" |
| Turnover ratio, trading activity relative to float | **Sub-Skill F: Turnover Ratio** | "turnover ratio for GME", "float turnover", "how actively traded is this" |
| Compare liquidity across multiple stocks | **Sub-Skill A** (multi-ticker mode) | "compare liquidity AAPL vs TSLA", "which is more liquid AMD or INTC" |

### Defaults

| Parameter | Default |
|---|---|
| Lookback period | `3mo` (3 months) |
| Data interval | `1d` (daily) |
| Market impact model | Square-root model |
| Intraday interval (when needed) | `5m` |

---

## Sub-Skill A: Liquidity Dashboard

**Goal**: Produce a comprehensive liquidity snapshot combining all key metrics for one or more tickers.

### A1: Fetch data and compute all metrics

```python
import yfinance as yf
import pandas as pd
import numpy as np

def liquidity_dashboard(ticker_symbol, period="3mo"):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    hist = ticker.history(period=period)

    if hist.empty:
        return None

    # --- Spread metrics (from current quote) ---
    bid = info.get("bid", None)
    ask = info.get("ask", None)
    current_price = info.get("currentPrice") or info.get("regularMarketPrice") or hist["Close"].iloc[-1]

    spread = None
    spread_pct = None
    if bid and ask and bid > 0 and ask > 0:
        spread = round(ask - bid, 4)
        midpoint = (ask + bid) / 2
        spread_pct = round((spread / midpoint) * 100, 4)

    # --- Volume metrics ---
    avg_volume = hist["Volume"].mean()
    median_volume = hist["Volume"].median()
    avg_dollar_volume = (hist["Close"] * hist["Volume"]).mean()
    volume_std = hist["Volume"].std()
    volume_cv = volume_std / avg_volume if avg_volume > 0 else None  # coefficient of variation

    # --- Turnover ratio ---
    shares_outstanding = info.get("sharesOutstanding", None)
    float_shares = info.get("floatShares", None)
    base_shares = float_shares or shares_outstanding
    turnover_ratio = round(avg_volume / base_shares, 6) if base_shares else None

    # --- Amihud illiquidity ratio ---
    # Average of |daily return| / daily dollar volume
    returns = hist["Close"].pct_change().dropna()
    dollar_volume = (hist["Close"] * hist["Volume"]).iloc[1:]  # align with returns
    amihud_values = returns.abs() / dollar_volume
    amihud = amihud_values[amihud_values.replace([np.inf, -np.inf], np.nan).notna()].mean()

    # --- Market impact estimate (square-root model) ---
    # For a hypothetical order of 1% of ADV
    adv = avg_volume
    order_size = adv * 0.01
    daily_volatility = returns.std()
    sigma = daily_volatility
    participation_rate = order_size / adv if adv > 0 else 0
    impact_bps = sigma * np.sqrt(participation_rate) * 10000  # in basis points

    return {
        "ticker": ticker_symbol,
        "current_price": round(current_price, 2),
        "bid": bid,
        "ask": ask,
        "spread": spread,
        "spread_pct": spread_pct,
        "avg_daily_volume": int(avg_volume),
        "median_daily_volume": int(median_volume),
        "avg_dollar_volume": round(avg_dollar_volume, 0),
        "volume_cv": round(volume_cv, 3) if volume_cv else None,
        "shares_outstanding": shares_outstanding,
        "float_shares": float_shares,
        "turnover_ratio": turnover_ratio,
        "amihud_illiquidity": round(amihud * 1e9, 4) if not np.isnan(amihud) else None,
        "daily_volatility": round(daily_volatility * 100, 2),
        "impact_1pct_adv_bps": round(impact_bps, 2),
        "observations": len(hist),
    }
```

### A2: Interpret and present

Present as a summary card. For the Amihud illiquidity ratio, multiply by 1e9 for readability (standard convention).

**Liquidity grade** (use these rough thresholds for US equities):

| Grade | Avg Dollar Volume | Spread (%) | Amihud (×10⁹) |
|---|---|---|---|
| Very High | > $500M/day | < 0.03% | < 0.01 |
| High | $50M–$500M/day | 0.03–0.10% | 0.01–0.1 |
| Moderate | $5M–$50M/day | 0.10–0.50% | 0.1–1.0 |
| Low | $500K–$5M/day | 0.50–2.00% | 1.0–10 |
| Very Low | < $500K/day | > 2.00% | > 10 |

When comparing multiple tickers, show a side-by-side table and highlight which is more liquid and why.

---

## Sub-Skill B: Spread Analysis

**Goal**: Detailed bid-ask spread analysis including current spread, historical context from options data, and effective spread estimates.

### B1: Current spread from quote

```python
import yfinance as yf

def spread_analysis(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    bid = info.get("bid", 0)
    ask = info.get("ask", 0)
    bid_size = info.get("bidSize", None)
    ask_size = info.get("askSize", None)
    current_price = info.get("currentPrice") or info.get("regularMarketPrice", 0)

    result = {"bid": bid, "ask": ask, "bid_size": bid_size, "ask_size": ask_size}

    if bid > 0 and ask > 0:
        midpoint = (bid + ask) / 2
        result["absolute_spread"] = round(ask - bid, 4)
        result["relative_spread_pct"] = round((ask - bid) / midpoint * 100, 4)
        result["relative_spread_bps"] = round((ask - bid) / midpoint * 10000, 2)
    return result
```

### B2: Options spread context

Options data from yfinance includes bid/ask for each strike, which gives a sense of derivatives liquidity. Use the nearest expiration, extract near-the-money calls and puts, and compute spread and spread percentage for each.

See `references/liquidity_reference.md` § "Options Spread Analysis" for the full code template.

### B3: Present results

Show:
- Current quoted spread (absolute, relative %, basis points)
- Bid/ask sizes if available
- Near-the-money options spreads for context
- How the spread compares to typical ranges for this market cap tier

---

## Sub-Skill C: Volume Analysis

**Goal**: Analyze trading volume patterns — averages, trends, relative volume, and dollar volume.

### C1: Compute volume metrics

```python
import yfinance as yf
import pandas as pd
import numpy as np

def volume_analysis(ticker_symbol, period="3mo"):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)

    if hist.empty:
        return None

    vol = hist["Volume"]
    close = hist["Close"]
    dollar_vol = vol * close

    # Relative volume (today vs average)
    rvol = vol.iloc[-1] / vol.mean() if vol.mean() > 0 else None

    # Volume trend (linear regression slope over the period)
    x = np.arange(len(vol))
    slope, _ = np.polyfit(x, vol.values, 1) if len(vol) > 1 else (0, 0)
    trend_pct = (slope * len(vol)) / vol.mean() * 100  # % change over period

    # Volume profile by day of week
    hist_copy = hist.copy()
    hist_copy["DayOfWeek"] = hist_copy.index.dayofweek
    day_names = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri"}
    vol_by_day = hist_copy.groupby("DayOfWeek")["Volume"].mean()
    vol_by_day.index = vol_by_day.index.map(day_names)

    # High/low volume days
    high_vol_days = hist.nlargest(5, "Volume")[["Close", "Volume"]]
    low_vol_days = hist.nsmallest(5, "Volume")[["Close", "Volume"]]

    return {
        "avg_volume": int(vol.mean()),
        "median_volume": int(vol.median()),
        "avg_dollar_volume": round(dollar_vol.mean(), 0),
        "current_volume": int(vol.iloc[-1]),
        "relative_volume": round(rvol, 2) if rvol else None,
        "volume_trend_pct": round(trend_pct, 1),
        "volume_by_day": vol_by_day.to_dict(),
        "high_vol_days": high_vol_days,
        "low_vol_days": low_vol_days,
        "max_volume": int(vol.max()),
        "min_volume": int(vol.min()),
    }
```

### C2: Present results

Show:
- Average daily volume (shares and dollar) with median for comparison
- Relative volume (RVOL) — today's volume vs. the average. RVOL > 1.5 is elevated; RVOL < 0.5 is unusually quiet
- Volume trend — is trading activity increasing or declining?
- Day-of-week pattern (if meaningful variation exists)
- Top 5 highest-volume days with context (earnings? news?)

---

## Sub-Skill D: Order Book Depth

**Goal**: Estimate order book depth using available bid/ask data from the equity quote and options chain.

Yahoo Finance does not provide full Level 2 / order book data. Be upfront about this limitation. What we can do:

1. **Equity quote**: bid, ask, bid size, ask size (top of book only)
2. **Options chain**: bid/ask and open interest across strikes give a proxy for derivatives depth
3. **Intraday volume distribution**: how volume is distributed within the day suggests how deep the continuous market is

### D1: Gather available depth data

Collect three data points:

1. **Top of book** — bid, ask, bidSize, askSize from `ticker.info`
2. **Intraday volume distribution** — 5-min bars over the last 5 days, grouped by time-of-day and normalized to percentage of daily volume
3. **Options open interest** — total call/put OI and volume from the nearest expiration as a derivatives depth proxy

See `references/liquidity_reference.md` § "Order Book Depth Proxy" for the full code template.

### D2: Present results

Show:
- **Top of book**: current bid/ask with sizes
- **Intraday volume shape**: where volume concentrates (open/close vs. midday)
- **Options depth**: total open interest and volume as a proxy for derivatives liquidity
- **Honest limitation**: "Yahoo Finance provides top-of-book only. For full Level 2 depth, a direct market data feed (e.g., NYSE OpenBook, NASDAQ TotalView) is needed."

---

## Sub-Skill E: Market Impact

**Goal**: Estimate how much a given order size would move the price, using the square-root market impact model.

The standard model in practice is: **Impact (%) = σ × √(Q / V)** where σ is daily volatility, Q is order size in shares, and V is average daily volume. This is a simplified version of the Almgren-Chriss framework used by institutional traders.

### E1: Compute market impact estimate

```python
import yfinance as yf
import numpy as np

def market_impact(ticker_symbol, order_shares=None, order_dollars=None, period="3mo"):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    info = ticker.info

    if hist.empty:
        return None

    current_price = info.get("currentPrice") or hist["Close"].iloc[-1]
    avg_volume = hist["Volume"].mean()
    daily_volatility = hist["Close"].pct_change().dropna().std()

    # Determine order size in shares
    if order_dollars and not order_shares:
        order_shares = order_dollars / current_price
    elif not order_shares:
        # Default: estimate for various sizes
        order_shares = avg_volume * 0.01  # 1% of ADV

    participation_rate = order_shares / avg_volume if avg_volume > 0 else 0
    pct_adv = (order_shares / avg_volume * 100) if avg_volume > 0 else 0

    # Square-root impact model
    impact_pct = daily_volatility * np.sqrt(participation_rate) * 100
    impact_bps = impact_pct * 100
    impact_dollars = impact_pct / 100 * current_price * order_shares

    # Generate impact curve for multiple order sizes
    sizes = [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.50]  # as fraction of ADV
    curve = []
    for s in sizes:
        q = avg_volume * s
        imp = daily_volatility * np.sqrt(s) * 100
        curve.append({
            "pct_adv": round(s * 100, 1),
            "shares": int(q),
            "dollars": round(q * current_price, 0),
            "impact_bps": round(imp * 100, 1),
            "impact_dollars_per_share": round(imp / 100 * current_price, 4),
        })

    return {
        "ticker": ticker_symbol,
        "current_price": round(current_price, 2),
        "avg_daily_volume": int(avg_volume),
        "daily_volatility_pct": round(daily_volatility * 100, 2),
        "order_shares": int(order_shares),
        "order_dollars": round(order_shares * current_price, 0),
        "pct_of_adv": round(pct_adv, 2),
        "estimated_impact_bps": round(impact_bps, 1),
        "estimated_impact_pct": round(impact_pct, 4),
        "estimated_impact_total_dollars": round(impact_dollars, 2),
        "impact_curve": curve,
    }
```

### E2: Present results

Show:
- The estimated impact for the user's specific order size
- An impact curve table showing how cost scales with order size
- Context: "This uses the square-root market impact model, a standard institutional estimate. Actual impact depends on execution strategy (VWAP, TWAP, etc.), time of day, and current market conditions."
- Above ~25 bps, note that the order is large for the stock's liquidity; above ~50 bps, flag it clearly and suggest the user consider algorithmic execution or splitting the order across days

---

## Sub-Skill F: Turnover Ratio

**Goal**: Measure how actively a stock trades relative to its shares outstanding and free float.

### F1: Compute turnover metrics

```python
import yfinance as yf
import pandas as pd
import numpy as np

def turnover_analysis(ticker_symbol, period="3mo"):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    info = ticker.info

    if hist.empty:
        return None

    avg_volume = hist["Volume"].mean()
    shares_outstanding = info.get("sharesOutstanding")
    float_shares = info.get("floatShares")

    result = {
        "avg_daily_volume": int(avg_volume),
        "shares_outstanding": shares_outstanding,
        "float_shares": float_shares,
    }

    if shares_outstanding:
        daily_turnover = avg_volume / shares_outstanding
        result["daily_turnover_ratio"] = round(daily_turnover, 6)
        result["annualized_turnover"] = round(daily_turnover * 252, 2)
        result["days_to_trade_float"] = round(
            (float_shares or shares_outstanding) / avg_volume, 1
        ) if avg_volume > 0 else None

    if float_shares:
        float_turnover = avg_volume / float_shares
        result["float_turnover_daily"] = round(float_turnover, 6)
        result["float_turnover_annualized"] = round(float_turnover * 252, 2)

    # Turnover trend
    vol = hist["Volume"]
    base = float_shares or shares_outstanding
    if base:
        hist_copy = hist.copy()
        hist_copy["turnover"] = hist_copy["Volume"] / base
        recent_turnover = hist_copy["turnover"].tail(20).mean()
        older_turnover = hist_copy["turnover"].head(20).mean()
        if older_turnover > 0:
            result["turnover_trend_pct"] = round(
                (recent_turnover - older_turnover) / older_turnover * 100, 1
            )

    return result
```

### F2: Present results

Show:
- Daily and annualized turnover ratios (vs. outstanding and float)
- "Days to trade the float" — how many days at average volume to turn over the entire free float
- Turnover trend — is the stock becoming more or less actively traded?
- Context:

| Turnover (Annualized) | Interpretation |
|---|---|
| > 500% | Extremely active — likely speculative or momentum-driven |
| 100–500% | Actively traded |
| 30–100% | Moderate activity |
| < 30% | Thinly traded — likely institutional buy-and-hold or neglected |

---

## Step 3: Respond to the User

After running the appropriate sub-skill:

### Always include

- The **lookback period** used for historical metrics
- The **data timestamp** — spreads and quotes are snapshots, not real-time
- Any tickers that returned **empty data** (invalid symbol, delisted, etc.)

### Always caveat

- Yahoo Finance quote data has a **15-minute delay** for most exchanges — spreads shown may not reflect the current live market
- Full order book (Level 2) data is **not available** through Yahoo Finance
- Market impact estimates are **models, not guarantees** — actual execution costs depend on strategy, timing, and market conditions
- Liquidity can **change rapidly** — a stock that's liquid today may not be tomorrow (especially around events, halts, or during extended hours)

### Practical guidance (mention when relevant)

- **Position sizing**: If estimated impact exceeds ~25 bps, the position may be too large for the stock's liquidity (see the thresholds in Sub-Skill E)
- **Small/micro-cap warning**: Stocks with < $1M daily dollar volume require careful execution
- **Spread costs compound**: A 0.10% spread on a round-trip (buy + sell) costs 0.20% — this adds up for active strategies
- **Illiquidity premium**: Less liquid stocks historically earn higher returns as compensation — but the transaction costs can eat this premium

Present liquidity data and let the user make their own decisions; don't recommend specific trades.

---

## Reference Files

- `references/liquidity_reference.md` — Detailed formulas, extended code templates, metric interpretation guides, and academic references for all liquidity measures

Read the reference file when you need exact formulas, edge case handling, or deeper background on liquidity metrics.

### Referencia: README.md

# Stock Liquidity Analysis

Analyze stock liquidity across multiple dimensions using Yahoo Finance data — bid-ask spreads, volume profiles, order book depth estimates, market impact modeling, and turnover ratios.

## Triggers

- "how liquid is AAPL"
- "bid-ask spread for TSLA"
- "volume analysis for MSFT"
- "order book depth"
- "how much would 50k shares move the price"
- "market impact of a $1M order"
- "turnover ratio for GME"
- "slippage estimate"
- "compare liquidity between stocks"
- "is this stock liquid enough to trade"
- "Amihud illiquidity ratio"
- "average daily dollar volume"

## Platform

All platforms (CLI + Claude.ai with code execution enabled)

## Prerequisites

- Python 3.8+
- `yfinance`, `pandas`, `numpy` (auto-installed if missing)

## Sub-Skills

| Sub-Skill | Description |
|---|---|
| **Liquidity Dashboard** | Comprehensive snapshot combining all key metrics |
| **Spread Analysis** | Bid-ask spread breakdown with options context |
| **Volume Analysis** | ADV, dollar volume, RVOL, volume trends and patterns |
| **Order Book Depth** | Top-of-book data with intraday volume distribution proxy |
| **Market Impact** | Square-root model for estimating execution cost of large orders |
| **Turnover Ratio** | Trading activity relative to shares outstanding and free float |

## Reference Files

- `references/liquidity_reference.md` — Detailed formulas, code templates, metric interpretation guides, edge cases, and yfinance field reference

### Referencia: references/liquidity_reference.md

# Liquidity Metrics Reference

Complete reference for all liquidity metrics, formulas, code templates, and interpretation guidelines.

---

## Table of Contents

1. [Bid-Ask Spread Metrics](#bid-ask-spread-metrics)
2. [Volume Metrics](#volume-metrics)
3. [Amihud Illiquidity Ratio](#amihud-illiquidity-ratio)
4. [Square-Root Market Impact Model](#square-root-market-impact-model)
5. [Turnover Ratio](#turnover-ratio)
6. [Composite Liquidity Score](#composite-liquidity-score)
7. [yfinance Fields Reference](#yfinance-fields-reference)
8. [Edge Cases and Gotchas](#edge-cases-and-gotchas)

---

## Bid-Ask Spread Metrics

### Quoted Spread

The difference between the best ask and best bid price.

```
Absolute Spread = Ask - Bid
Relative Spread (%) = (Ask - Bid) / Midpoint × 100
Spread (bps) = (Ask - Bid) / Midpoint × 10,000
Midpoint = (Ask + Bid) / 2
```

### Effective Spread (estimated)

The effective spread captures the actual transaction cost, accounting for trades that execute inside the quoted spread. Without tick-level data, estimate as:

```
Effective Spread ≈ 2 × |Trade Price - Midpoint|
```

Since yfinance doesn't provide tick data, use the quoted spread as an upper bound. The effective spread is typically 60–80% of the quoted spread for liquid stocks.

### Spread as a Function of Price Level

Low-priced stocks often have wider percentage spreads due to the minimum tick size ($0.01). A $5 stock with a $0.01 spread has a 0.20% spread, while a $500 stock with a $0.01 spread has a 0.002% spread. Always report relative spread, not just absolute.

---

## Volume Metrics

### Average Daily Volume (ADV)

```python
adv = hist["Volume"].mean()
```

Use median for a more robust measure when volume has large spikes (earnings, index rebalancing).

### Average Daily Dollar Volume (ADDV)

```python
addv = (hist["Close"] * hist["Volume"]).mean()
```

Dollar volume is more meaningful than share volume for cross-stock comparisons because it normalizes for price differences.

### Relative Volume (RVOL)

```python
rvol = current_volume / avg_volume
```

| RVOL | Interpretation |
|---|---|
| > 3.0 | Extreme — likely news, earnings, or event |
| 1.5–3.0 | Elevated — increased interest |
| 0.8–1.2 | Normal |
| 0.5–0.8 | Below average — quiet day |
| < 0.5 | Very low — possible holiday, pre-event calm |

### Volume Coefficient of Variation

```python
volume_cv = hist["Volume"].std() / hist["Volume"].mean()
```

High CV (> 1.0) means volume is "spiky" — the stock alternates between very quiet and very active days. This matters for execution: you can't rely on the average volume being available every day.

### Intraday Volume Distribution

Volume follows a U-shape pattern in US equities — highest at open and close, lowest midday. Use 5-minute bars to visualize:

```python
intraday = ticker.history(period="5d", interval="5m")
intraday["time"] = intraday.index.time
vol_by_time = intraday.groupby("time")["Volume"].mean()
```

Typical distribution for US equities:
- **First 30 min (9:30–10:00)**: ~15–20% of daily volume
- **Midday (11:00–14:00)**: ~25–30% of daily volume
- **Last 30 min (15:30–16:00)**: ~15–20% of daily volume

---

## Amihud Illiquidity Ratio

### Formula

Amihud (2002) illiquidity ratio measures the daily price response per dollar of trading volume:

```
ILLIQ = (1/D) × Σ |rₜ| / DVOLₜ
```

Where:
- `D` = number of trading days in the period
- `rₜ` = daily return on day t
- `DVOLₜ` = daily dollar volume on day t (price × volume)

### Code

```python
returns = hist["Close"].pct_change().dropna()
dollar_volume = (hist["Close"] * hist["Volume"]).iloc[1:]  # align with returns

amihud_daily = returns.abs() / dollar_volume
# Remove inf values (zero-volume days)
amihud_daily = amihud_daily.replace([np.inf, -np.inf], np.nan).dropna()
amihud = amihud_daily.mean()

# Convention: multiply by 10^9 for readability
amihud_scaled = amihud * 1e9
```

### Interpretation

Higher values = less liquid. The ratio captures how much "price bang" you get per dollar of volume.

| Amihud (×10⁹) | Liquidity Level |
|---|---|
| < 0.01 | Mega-cap, extremely liquid (AAPL, MSFT) |
| 0.01–0.1 | Large-cap, highly liquid |
| 0.1–1.0 | Mid-cap, moderately liquid |
| 1.0–10 | Small-cap, less liquid |
| > 10 | Micro-cap, illiquid |

### Rolling Amihud

Track how liquidity changes over time:

```python
window = 20  # trading days
rolling_amihud = amihud_daily.rolling(window).mean() * 1e9
```

---

## Square-Root Market Impact Model

### Theory

The square-root law of market impact is one of the most robust empirical findings in market microstructure. Price impact scales with the square root of order size:

```
Impact (%) = σ × √(Q / V)
```

Where:
- `σ` = daily return volatility (standard deviation)
- `Q` = order size in shares
- `V` = average daily volume in shares

This means doubling the order size only increases impact by ~41% (√2 ≈ 1.41), not 100%. This concavity arises because large orders are typically split across time.

### Extended Model with Participation Rate

For orders executed over multiple periods:

```
Impact (%) = σ × √(Q / (V × T))
```

Where `T` is the number of days over which the order is executed.

### Total Execution Cost

```
Total Cost = Spread Cost + Market Impact
Spread Cost = 0.5 × Bid-Ask Spread (one way)
Total Round-Trip = 2 × (Spread Cost + Impact)
```

### Code for Impact Curve

```python
def impact_curve(ticker_symbol, period="3mo"):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period=period)
    info = ticker.info
    
    price = info.get("currentPrice") or hist["Close"].iloc[-1]
    adv = hist["Volume"].mean()
    sigma = hist["Close"].pct_change().dropna().std()
    
    sizes_pct_adv = [0.1, 0.5, 1, 2, 5, 10, 20, 50]
    
    results = []
    for pct in sizes_pct_adv:
        frac = pct / 100
        shares = int(adv * frac)
        impact_pct = sigma * np.sqrt(frac) * 100
        impact_per_share = impact_pct / 100 * price
        total_cost = impact_per_share * shares
        
        results.append({
            "pct_adv": pct,
            "shares": shares,
            "notional": round(shares * price),
            "impact_bps": round(impact_pct * 100, 1),
            "cost_per_share": round(impact_per_share, 4),
            "total_cost": round(total_cost, 2),
        })
    
    return results
```

---

## Turnover Ratio

### Formulas

```
Daily Turnover = Daily Volume / Shares Outstanding
Float Turnover = Daily Volume / Free Float Shares
Annualized Turnover = Daily Turnover × 252
Days to Trade Float = Float Shares / Average Daily Volume
```

### yfinance Fields

```python
info = ticker.info
shares_outstanding = info.get("sharesOutstanding")
float_shares = info.get("floatShares")
```

Float shares excludes restricted stock, insider holdings, and other locked-up shares. Float turnover is generally more informative than total turnover because it measures trading relative to the actually tradable supply.

### Interpretation

| Annualized Float Turnover | Interpretation |
|---|---|
| > 1000% | Hyper-active — meme stock, short squeeze, or speculative frenzy |
| 500–1000% | Very active — high retail or momentum interest |
| 100–500% | Actively traded — typical for popular large/mid-caps |
| 30–100% | Moderate — normal institutional holding pattern |
| 10–30% | Low — buy-and-hold investor base, limited trading |
| < 10% | Very low — thinly traded, possibly neglected or closely held |

---

## Composite Liquidity Score

For a quick single-number summary, combine normalized metrics:

```python
def liquidity_score(spread_pct, avg_dollar_volume, amihud_scaled, turnover_annual):
    """Returns 0-100 score. Higher = more liquid."""
    import numpy as np
    
    # Spread score (lower spread = higher score)
    spread_score = max(0, min(100, 100 - spread_pct * 200))
    
    # Dollar volume score (log scale)
    dv_log = np.log10(max(avg_dollar_volume, 1))
    dv_score = max(0, min(100, (dv_log - 4) / 6 * 100))  # $10K=0, $10B=100
    
    # Amihud score (lower = better)
    ami_score = max(0, min(100, 100 - np.log10(max(amihud_scaled, 0.001)) * 25))
    
    # Turnover score
    turn_score = max(0, min(100, turnover_annual / 5))  # 500% annual = 100
    
    # Weighted composite
    composite = (
        spread_score * 0.30 +
        dv_score * 0.35 +
        ami_score * 0.20 +
        turn_score * 0.15
    )
    return round(composite, 1)
```

This is a heuristic, not a formal measure. It's useful for quick comparisons but should not replace examining individual metrics.

---

## yfinance Fields Reference

### From `ticker.info`

| Field | Description | Used For |
|---|---|---|
| `bid` | Current best bid price | Spread |
| `ask` | Current best ask price | Spread |
| `bidSize` | Size at best bid (lots) | Book depth |
| `askSize` | Size at best ask (lots) | Book depth |
| `currentPrice` | Last trade price | Impact calc |
| `regularMarketPrice` | Regular session last price | Fallback price |
| `averageVolume` | 3-month avg daily volume | Volume metrics |
| `averageVolume10days` | 10-day avg daily volume | Recent volume |
| `averageDailyVolume10Day` | Same as above (alias) | Recent volume |
| `volume` | Today's volume so far | RVOL |
| `sharesOutstanding` | Total shares outstanding | Turnover |
| `floatShares` | Free float shares | Float turnover |
| `marketCap` | Market capitalization | Context |

### From `ticker.history()`

| Column | Description |
|---|---|
| `Open` | Opening price |
| `High` | Day's high |
| `Low` | Day's low |
| `Close` | Closing price |
| `Volume` | Shares traded |

### From `ticker.option_chain(expiration)`

| Column | Description | Used For |
|---|---|---|
| `bid` | Option bid price | Options spread |
| `ask` | Option ask price | Options spread |
| `volume` | Option contracts traded | Options liquidity |
| `openInterest` | Open contracts | Depth proxy |

---

## Options Spread Analysis

Analyze near-the-money options spreads from the nearest expiration to gauge derivatives liquidity:

```python
def options_spread_analysis(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    expirations = ticker.options
    if not expirations:
        return None

    # Use nearest expiration
    chain = ticker.option_chain(expirations[0])
    for label, df in [("Calls", chain.calls), ("Puts", chain.puts)]:
        atm = pd.concat([df[df["inTheMoney"]].tail(3), df[~df["inTheMoney"]].head(3)])
        atm["spread"] = atm["ask"] - atm["bid"]
        atm["spread_pct"] = (atm["spread"] / ((atm["ask"] + atm["bid"]) / 2) * 100).round(2)
    return chain
```

---

## Order Book Depth Proxy

Yahoo Finance does not provide full Level 2 data. Use this function to gather available depth signals:

```python
def order_book_proxy(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    # Top of book
    top_of_book = {
        "bid": info.get("bid"),
        "ask": info.get("ask"),
        "bid_size": info.get("bidSize"),
        "ask_size": info.get("askSize"),
    }

    # Intraday volume distribution (5-min bars, last 5 days)
    intraday = ticker.history(period="5d", interval="5m")
    if not intraday.empty:
        intraday_copy = intraday.copy()
        intraday_copy["time"] = intraday_copy.index.time
        vol_by_time = intraday_copy.groupby("time")["Volume"].mean()
        # Normalize to percentage of daily volume
        total = vol_by_time.sum()
        vol_pct = (vol_by_time / total * 100).round(2) if total > 0 else vol_by_time

    # Options open interest as depth proxy
    expirations = ticker.options
    if expirations:
        chain = ticker.option_chain(expirations[0])
        total_call_oi = chain.calls["openInterest"].sum()
        total_put_oi = chain.puts["openInterest"].sum()
        total_call_volume = chain.calls["volume"].sum()
        total_put_volume = chain.puts["volume"].sum()

    return top_of_book, vol_pct if not intraday.empty else None
```

---

## Edge Cases and Gotchas

### Zero-Volume Days

Some thinly traded stocks have days with zero volume. Filter these before computing Amihud (division by zero) and volume averages:

```python
# Remove zero-volume days for Amihud
mask = hist["Volume"] > 0
hist_filtered = hist[mask]
```

### Pre/Post Market Data

yfinance `prepost=True` includes extended hours data, which has wider spreads and lower volume. For liquidity analysis, use regular hours only (the default).

### Quote Staleness

Yahoo Finance quotes can be delayed 15+ minutes. During market hours, bid/ask may not reflect the current state. Note this in output.

### ADRs and Foreign Stocks

American Depositary Receipts (ADRs) may show different liquidity than the underlying foreign-listed stock. The ADR spread can be wider than the home-market spread. When analyzing ADR liquidity, note this distinction.

### ETFs vs. Stocks

ETF liquidity is more complex — the ETF may appear illiquid (low volume, wide spread) but the underlying basket is very liquid, meaning authorized participants can create/redeem shares efficiently. The "true" liquidity of an ETF is the liquidity of its underlying holdings. Note this when the user asks about ETF liquidity.

### Penny Stocks (< $1)

Minimum tick size ($0.01) creates a floor on absolute spreads. A $0.50 stock can't have less than a 2% spread (at minimum tick). Relative spread metrics are especially important for low-priced securities.

### Weekend/Holiday Gaps

Volume averages should use trading days only (yfinance handles this by default). But be careful when computing "days to trade float" — these are trading days, not calendar days.


---

## SKILL: strategy-framework

- Fuente: `agiprolabs/claude-trading-skills` → `skills/strategy-framework` (MIT)
- Cuándo usarla: Standardized template for defining trading strategies with entry rules, exit rules, position sizing, risk parameters, and performance criteria
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/strategy-framework/` (define_strategy.py, strategy_scorecard.py)

# Strategy Framework

A standardized system for defining, documenting, testing, and managing trading strategies. This skill provides templates and tools that enforce discipline, enable reproducibility, and make strategies testable.

## Why a Strategy Framework Matters

Trading without a written strategy framework leads to:
- **Inconsistency**: ad-hoc decisions driven by emotion rather than rules
- **Untestability**: vague ideas that cannot be backtested or evaluated
- **Scope creep**: strategies that drift without version-controlled definitions
- **Unmanaged risk**: missing stop losses, position limits, or drawdown halts

A strategy framework forces you to:
1. State a falsifiable hypothesis about a market inefficiency
2. Define precise, machine-testable entry and exit rules
3. Specify position sizing and risk parameters before trading
4. Set minimum performance criteria for continuation or retirement
5. Track changes through versioned strategy documents

## Strategy Definition Template

Every strategy must be documented using the standard template. The full copy-paste template is in `references/strategy_template.md`.

### Core Sections

**Identity**
```
Name: SOL-EMA-Cross v1.0
Asset class: Solana tokens (top 50 by 24h volume)
Timeframe: Primary 1H, confirmation 4H
Style: Trend following
```

**Edge Hypothesis**: State what market inefficiency you are exploiting and why it exists.

```
Hypothesis: Solana mid-cap tokens exhibit momentum persistence
on the 1H timeframe due to retail herding behavior and low
institutional participation. EMA crossovers capture the
initiation of these trends.
```

**Entry Rules**: Specific, testable conditions combined with AND/OR logic.

```python
def entry_signal(data: pd.DataFrame) -> bool:
    """All conditions must be True (AND logic)."""
    ema_cross = data["ema_12"] > data["ema_26"]  # EMA 12 crossed above 26
    ema_rising = data["ema_26"].diff(3) > 0       # 26 EMA trending up
    volume_ok = data["volume"] > data["vol_sma_20"] * 1.5  # Volume confirmation
    regime_ok = data["adx"] > 20                  # Trending regime
    return ema_cross & ema_rising & volume_ok & regime_ok
```

**Exit Rules**: Every strategy needs multiple exit mechanisms.

| Exit Type | Method | Parameters |
|-----------|--------|------------|
| Stop Loss | ATR-based | 2.0 × ATR(14) below entry |
| Take Profit | Risk multiple | 3.0 × risk (3:1 R:R) |
| Trailing Stop | Chandelier | 3.0 × ATR(14) from highest high |
| Time Stop | Bar count | Close if flat after 20 bars |
| Signal Exit | EMA reversal | EMA 12 crosses below EMA 26 |

**Position Sizing**: Method and parameters. See the `position-sizing` skill for details.

```python
risk_per_trade = 0.02        # 2% of portfolio
stop_distance_pct = 0.05     # 5% from entry (ATR-derived)
position_size = (portfolio * risk_per_trade) / stop_distance_pct
```

**Risk Parameters**: Portfolio-level guardrails. See the `risk-management` skill.

```
Max concurrent positions: 5
Risk per trade: 2% of portfolio
Daily loss limit: 5% of portfolio
Max drawdown halt: 15% — stop trading, review strategy
Correlated exposure limit: 10% (e.g., meme tokens combined)
```

**Filters**: Conditions that prevent entry even if signals fire.

```python
def filters_pass(token: dict, market: dict) -> bool:
    """All filters must pass before entry is allowed."""
    volume_ok = token["volume_24h"] > 500_000      # Min $500K volume
    liquidity_ok = token["liquidity"] > 100_000    # Min $100K liquidity
    age_ok = token["age_days"] > 7                 # Not brand new
    holders_ok = token["holder_count"] > 500       # Sufficient distribution
    regime_ok = market["regime"] != "crisis"       # No crisis regime
    return all([volume_ok, liquidity_ok, age_ok, holders_ok, regime_ok])
```

**Performance Criteria**: When to continue, review, or retire.

```
Continue: Sharpe > 1.0, PF > 1.5, Win Rate > 40%, MDD < 20%
Review:   Any metric degrades 25% from baseline
Retire:   Rolling 30-day Sharpe < 0, or 3 consecutive losing months
```

## Strategy Lifecycle

### 1. Hypothesis

Identify a market inefficiency and explain why it exists and why it might persist.

**Good hypothesis**: "New PumpFun tokens that reach 80+ SOL in bonding curve within 10 minutes have a 65% probability of graduating to Raydium, creating a predictable price spike at graduation."

**Bad hypothesis**: "SOL will go up." (Not specific, not testable, no edge identified.)

### 2. Definition

Write the full strategy document using the template in `references/strategy_template.md`. Every field must be filled. If you cannot fill a field, the strategy is not ready.

### 3. Backtest

Test on historical data using `vectorbt` or equivalent. Requirements:
- Minimum 100 trades in the test period
- Use walk-forward validation (train on 70%, test on 30%)
- Account for slippage and fees (see `slippage-modeling` skill)
- Report both in-sample and out-of-sample metrics

### 4. Paper Trade

Run the strategy in simulation for at least 2 weeks (or 30 trades, whichever is longer).
- Compare paper results to backtest expectations
- If results differ by more than 25%, investigate before proceeding

### 5. Small Live

Trade with minimum viable size (enough to cover fees, small enough to be inconsequential).
- Run for at least 30 trades
- Compare to paper trade results

### 6. Scale

If small-live metrics match expectations (within 25% of backtest):
- Increase position size gradually (25% increments per week)
- Monitor metrics continuously

### 7. Monitor

Ongoing performance tracking:
- Daily: P&L, trade count, win rate
- Weekly: Sharpe ratio, profit factor, drawdown
- Monthly: Full strategy review against performance criteria

### 8. Retire

Stop using a strategy when:
- Rolling 30-day Sharpe drops below 0
- Three consecutive losing months
- Market regime permanently shifts (e.g., regulatory change)
- A better strategy replaces it for the same edge

## Strategy Evaluation Criteria

Minimum thresholds before a strategy should be traded live:

| Metric | Trend Following | Mean Reversion | Scalping |
|--------|----------------|----------------|----------|
| Min Trades | 100 | 100 | 500 |
| Sharpe (OOS) | > 1.0 | > 1.0 | > 1.5 |
| Profit Factor | > 1.5 | > 1.5 | > 1.3 |
| Max Drawdown | < 20% | < 15% | < 10% |
| Win Rate | > 35% | > 55% | > 55% |
| Avg Win/Avg Loss | > 2.0 | > 1.0 | > 1.0 |

## Strategy Types for Crypto

Detailed descriptions of each strategy type are in `references/strategy_types.md`.

### Momentum / Trend Following
- **Edge**: Price trends persist due to behavioral biases and information asymmetry
- **Indicators**: EMA crossovers, SuperTrend, ADX, MACD
- **Win rate**: 35-45%, relies on large winners
- **Best regime**: Trending markets with moderate volatility

### Mean Reversion
- **Edge**: Price oscillates around equilibrium due to overreaction
- **Indicators**: RSI, Bollinger Bands, z-score, VWAP deviation
- **Win rate**: 55-65%, relies on high win rate with smaller gains
- **Best regime**: Ranging markets with low-moderate volatility

### Breakout
- **Edge**: Compressed volatility leads to directional expansion
- **Indicators**: Bollinger Band squeeze, Donchian channels, volume breakout
- **Win rate**: 30-40%, relies on catching large moves
- **Best regime**: Transitioning from low to high volatility

### Copy Trading / Wallet Following
- **Edge**: Skilled wallets have informational or analytical advantages
- **Indicators**: Wallet PnL history, trade frequency, token selection
- **Win rate**: Depends on followed wallet quality
- **Best regime**: Any (depends on followed wallet's strategy)

### PumpFun Sniping
- **Edge**: Predictable price dynamics around token creation and graduation
- **Strategies**: Creation snipe, volume confirmation, graduation play
- **Win rate**: Highly variable (20-60% depending on approach)
- **Best regime**: High retail activity periods

### Arbitrage
- **Edge**: Price discrepancies across DEXs or between spot and perpetuals
- **Indicators**: Price feeds from multiple venues, funding rates
- **Win rate**: > 80% when executed correctly
- **Best regime**: High volatility, fragmented liquidity

### Market Making
- **Edge**: Capturing bid-ask spread while managing inventory risk
- **Indicators**: Order book depth, volatility, inventory position
- **Win rate**: > 60%, relies on volume and spread capture
- **Best regime**: Stable markets with consistent volume

## Common Strategy Mistakes

1. **No written rules**: Trading on intuition, unable to backtest or reproduce
2. **Curve fitting**: Optimizing parameters until backtest looks perfect, fails live
3. **Missing stops**: "I'll exit when it feels right" leads to catastrophic losses
4. **Ignoring regime**: Using a trend strategy in a ranging market (or vice versa)
5. **Survivorship bias**: Only backtesting tokens that still exist
6. **Lookahead bias**: Using future information in backtest signals
7. **Ignoring costs**: Not accounting for slippage, fees, and market impact
8. **Over-trading**: Entering on marginal signals to "stay active"
9. **Strategy hopping**: Abandoning strategies after normal losing streaks
10. **No retirement plan**: Continuing to trade a broken strategy out of attachment

## Integration with Other Skills

| Skill | Integration |
|-------|------------|
| `vectorbt` | Backtest strategy definitions programmatically |
| `pandas-ta` | Compute technical indicators for entry/exit signals |
| `regime-detection` | Market regime filters for strategy activation |
| `exit-strategies` | Detailed exit rule implementation |
| `position-sizing` | Position size calculation methods |
| `risk-management` | Portfolio-level risk parameter enforcement |
| `slippage-modeling` | Realistic execution cost estimation |
| `feature-engineering` | ML feature computation from strategy signals |

## Files

### References
- `references/strategy_template.md` — Complete copy-paste strategy definition template
- `references/strategy_types.md` — Detailed guide to each strategy type with parameters and examples

### Scripts
- `scripts/define_strategy.py` — Interactive strategy definition tool with `--demo` mode
- `scripts/strategy_scorecard.py` — Strategy evaluation scorecard with GO/REVIEW/NO-GO recommendations

### Referencia: references/strategy_template.md

# Strategy Definition Template

Copy this template and fill in every section. If you cannot fill a section, the strategy is not ready for testing.

## Template

```markdown
# Strategy: [Name] v[X.Y]

## Overview
- **Asset class**: [e.g., Solana tokens, top 50 by 24h volume]
- **Timeframe**: Primary [1H], Confirmation [4H]
- **Style**: [Trend following / Mean reversion / Breakout / Scalping / Other]
- **Edge hypothesis**: [One paragraph: what inefficiency exists and why it persists]

## Entry Rules

All conditions use AND logic unless noted otherwise.

- Condition 1: [specific, testable — e.g., EMA(12) > EMA(26)]
- Condition 2: [specific, testable — e.g., ADX > 20]
- Condition 3: [specific, testable — e.g., Volume > 1.5x 20-period SMA]
- Condition 4 (optional): [additional confirmation]

**Entry logic**: ALL of conditions 1-3 must be True (AND)

**Entry execution**:
- Order type: [Market / Limit at bid+X bps]
- Slippage tolerance: [X bps]
- Max entry time: [fill within N seconds or cancel]

## Exit Rules

### Stop Loss
- **Method**: [Fixed % / ATR-based / Support level / Volatility-adjusted]
- **Parameters**: [e.g., 2.0 × ATR(14) below entry]
- **Hard stop**: [absolute max loss per trade, e.g., 3% of portfolio]

### Take Profit
- **Method**: [Fixed R:R / Resistance level / Indicator target]
- **Parameters**: [e.g., 3.0 × risk distance above entry]
- **Partial exits**: [e.g., 50% at 2R, 50% at 3R]

### Trailing Stop
- **Method**: [Chandelier / Percentage / Parabolic SAR / ATR trail]
- **Parameters**: [e.g., 3.0 × ATR(14) from highest high since entry]
- **Activation**: [e.g., activate after 1.5R profit reached]

### Time Stop
- **Trigger**: [e.g., close position if flat (< 0.5R move) after 20 bars]
- **Rationale**: [capital is better deployed elsewhere if no movement]

### Signal Exit
- **Condition**: [e.g., EMA(12) crosses below EMA(26)]
- **Overrides**: [does this override trailing stop? take profit?]

### Exit Priority
1. Hard stop loss (always honored)
2. Signal exit
3. Trailing stop
4. Take profit
5. Time stop

## Position Sizing

- **Method**: [Fixed fractional / Volatility-adjusted / Kelly criterion]
- **Risk per trade**: [X% of portfolio]
- **Calculation**:
  ```
  position_size = (portfolio_value × risk_per_trade) / stop_distance
  ```
- **Max position**: [Y% of portfolio in any single trade]
- **Min position**: [Z SOL or $W — must cover fees]

## Risk Parameters

- **Max concurrent positions**: [N]
- **Max correlated positions**: [M positions in same sector/narrative]
- **Daily loss limit**: [X% — stop trading for the day if hit]
- **Weekly loss limit**: [Y% — reduce size by 50% if hit]
- **Max drawdown halt**: [Z% — stop trading entirely, review strategy]
- **Correlated exposure limit**: [W% of portfolio in correlated assets]

## Filters

Conditions that prevent entry even when signals fire.

### Market Filters
- **Regime filter**: [e.g., only trade when ADX > 20 (trending)]
- **Volatility filter**: [e.g., skip if ATR/price > 15% (too volatile)]
- **Correlation filter**: [e.g., skip if BTC correlation > 0.9 during BTC downtrend]

### Token Filters
- **Volume filter**: [minimum 24h volume, e.g., > $500K]
- **Liquidity filter**: [minimum pool liquidity, e.g., > $100K]
- **Age filter**: [minimum token age, e.g., > 7 days]
- **Holder filter**: [minimum holder count, e.g., > 500]
- **Concentration filter**: [top 10 holders < 50% of supply]

### Time Filters
- **Active hours**: [e.g., 08:00-22:00 UTC only]
- **Day filter**: [e.g., avoid weekends for low-liquidity tokens]
- **Event filter**: [e.g., avoid 1H before/after major announcements]

## Performance Criteria

### Continue Trading
- Rolling 30d Sharpe > [1.0]
- Rolling 30d Profit Factor > [1.5]
- Rolling 30d Win Rate > [40%]
- Max drawdown from peak < [20%]

### Review Required
- Any metric degrades [25%] from baseline
- Three consecutive losing weeks
- Significant market regime change detected

### Retire Strategy
- Rolling 30d Sharpe < [0] for [2 consecutive weeks]
- Three consecutive losing months
- Max drawdown halt triggered [twice in 30 days]
- Fundamental edge no longer exists (e.g., protocol change)

## Backtest Results

### In-Sample (Training Period)
- **Period**: [YYYY-MM-DD to YYYY-MM-DD]
- **Total return**: [X%]
- **Sharpe ratio**: [X.XX]
- **Max drawdown**: [X%]
- **Win rate**: [X%]
- **Profit factor**: [X.XX]
- **Trade count**: [N]
- **Avg trade duration**: [N bars]

### Out-of-Sample (Test Period)
- **Period**: [YYYY-MM-DD to YYYY-MM-DD]
- **Total return**: [X%]
- **Sharpe ratio**: [X.XX]
- **Max drawdown**: [X%]
- **Win rate**: [X%]
- **Profit factor**: [X.XX]
- **Trade count**: [N]
- **Degradation from IS**: [X% Sharpe drop, X% PF drop]

### Paper Trade Results
- **Period**: [YYYY-MM-DD to YYYY-MM-DD]
- **Total return**: [X%]
- **Comparison to OOS**: [within X% — acceptable / needs investigation]

## Dependencies
- Data source: [e.g., Birdeye API, DexScreener]
- Indicators: [e.g., pandas-ta EMA, ADX, ATR]
- Execution: [e.g., Jupiter API via jupiter-swap skill]
- Risk: [e.g., position-sizing skill, risk-management skill]

## Notes
- [Any additional context, known limitations, or observations]

## Change Log
- **v1.0** [YYYY-MM-DD]: Initial strategy definition
- **v1.1** [YYYY-MM-DD]: [Description of changes and reason]
```

## Usage Notes

1. **Fill every field**: Empty fields indicate an incomplete strategy. Do not trade an incomplete strategy.
2. **Be specific**: "Buy when RSI is low" is not testable. "Buy when RSI(14) < 30 AND price > EMA(200)" is testable.
3. **Version your changes**: Every parameter change gets a new version number and changelog entry.
4. **Keep it updated**: After backtesting and paper trading, fill in the results sections.
5. **One strategy per document**: Do not combine multiple strategies in one template.

### Referencia: references/strategy_types.md

# Strategy Types for Crypto Trading

Detailed guide to each strategy archetype with entry/exit logic, expected metrics, and parameter suggestions.

## Momentum / Trend Following

**Edge**: Price trends persist due to behavioral biases (herding, anchoring) and information diffusion lag. In crypto, low institutional participation amplifies trend persistence.

**Entry signals**:
- EMA(12) crosses above EMA(26) with ADX > 20
- SuperTrend flips bullish on primary timeframe
- Price breaks above N-period high with volume confirmation (> 1.5x average)
- MACD histogram turns positive after bearish-to-bullish crossover

**Exit signals**:
- Trailing stop: Chandelier exit at 3.0 × ATR(14) from highest high
- Signal reversal: EMA(12) crosses below EMA(26)
- Trend exhaustion: ADX peaks and turns down from above 40

**Expected metrics**:
- Win rate: 35-45%
- Avg win / avg loss: 2.0-4.0x
- Profit factor: 1.5-2.5
- Best Sharpe: 1.0-2.0 in trending regimes

**Parameter suggestions by timeframe**:

| Timeframe | Fast EMA | Slow EMA | ATR Period | ATR Multiplier |
|-----------|----------|----------|------------|----------------|
| 5m | 8 | 21 | 10 | 1.5 |
| 15m | 9 | 21 | 14 | 2.0 |
| 1H | 12 | 26 | 14 | 2.5 |
| 4H | 12 | 26 | 14 | 3.0 |
| 1D | 20 | 50 | 14 | 3.0 |

**Risk notes**: Trend following suffers in ranging markets. Use ADX > 20 or regime detection as a filter. Expect 5-8 consecutive losers during chop — size accordingly.

## Mean Reversion

**Edge**: Price oscillates around a fair value equilibrium. Overreactions (panic selling, FOMO buying) create temporary dislocations that correct. Works best for established tokens with consistent liquidity.

**Entry signals**:
- RSI(14) < 30 AND price above EMA(200) (oversold in uptrend)
- Price below lower Bollinger Band(20, 2.0) with band width > 0.05
- Z-score of price relative to 20-period mean < -2.0
- Price deviates > 2% below VWAP with increasing volume

**Exit signals**:
- Return to mean: price crosses back above EMA(20) or VWAP
- RSI(14) > 50 (neutral zone)
- Bollinger Band midline touch
- Time stop: 10-20 bars if no mean reversion occurs

**Expected metrics**:
- Win rate: 55-65%
- Avg win / avg loss: 0.8-1.5x
- Profit factor: 1.3-2.0
- Best Sharpe: 1.0-1.5 in ranging regimes

**Parameter suggestions by timeframe**:

| Timeframe | RSI Period | BB Period | BB Std | Z-Score Lookback |
|-----------|-----------|-----------|--------|-----------------|
| 5m | 10 | 15 | 2.0 | 20 |
| 15m | 14 | 20 | 2.0 | 30 |
| 1H | 14 | 20 | 2.0 | 30 |
| 4H | 14 | 20 | 2.5 | 40 |
| 1D | 14 | 20 | 2.5 | 50 |

**Risk notes**: Mean reversion fails catastrophically in trending markets. A "cheap" token can get much cheaper. Always use a hard stop loss. Never mean-revert tokens with broken fundamentals.

## Breakout

**Edge**: Periods of low volatility (consolidation) build potential energy that resolves in directional moves. Volume confirmation distinguishes real breakouts from fakeouts.

**Entry signals**:
- Bollinger Band width contracts to lowest 20% of 100-period range, then expands
- Price breaks above/below Donchian channel (20-period high/low)
- Volume spike > 2.5x 20-period average on breakout bar
- Range contraction (inside bars or narrowing ATR) followed by expansion

**Exit signals**:
- ATR trailing stop: 2.5 × ATR(14) from entry direction
- Time stop: close if no follow-through within 5-10 bars
- Failed breakout: price returns inside prior range within 3 bars

**Expected metrics**:
- Win rate: 30-40%
- Avg win / avg loss: 3.0-5.0x
- Profit factor: 1.5-2.5
- Many false breakouts — accept low win rate for large winners

**Risk notes**: False breakouts are common (50-60% of breakout signals fail). Volume confirmation is critical. Avoid breakout strategies on low-liquidity tokens where a single large order can fake a breakout.

## Copy Trading / Wallet Following

**Edge**: Skilled wallets (early token discoverers, profitable traders) have informational or analytical advantages. Following their trades captures some of their edge.

**Entry signals**:
- Tracked wallet buys token matching your criteria
- Wallet has historical PnL > 50% over 30 days
- Wallet has > 60% win rate on similar tokens
- Multiple tracked wallets buy same token within short window (consensus signal)

**Exit signals**:
- Tracked wallet sells (follow their exit)
- Independent stop loss (do not rely solely on wallet exit)
- Time stop: wallet has not exited after N hours
- Your own technical stop loss triggers

**Implementation considerations**:
- Monitor wallets via Helius webhooks or polling (see `helius-api` skill)
- Latency matters: detect and execute within seconds of wallet transaction
- Wallet quality degrades over time — continuously re-evaluate tracked wallets
- Filter by wallet style: sniper, swing trader, accumulator

**Risk notes**: Wallet following has significant latency risk — by the time you buy, the price may have moved. Smart wallets may front-run followers. Diversify across multiple wallets. Re-evaluate wallet quality monthly.

## PumpFun Strategies

**Edge**: PumpFun token lifecycle creates predictable price dynamics at known milestones.

### Sniper Strategy
- **Entry**: Buy within first 10 transactions of token creation
- **Exit**: Sell within 1-5 minutes (quick flip)
- **Win rate**: 20-30% (most new tokens fail immediately)
- **Risk**: Extremely high. Most tokens go to zero. Size very small.
- **Key metric**: The 20-30% of winners must return 5-10x to compensate

### Volume Confirmation Strategy
- **Entry**: Buy after token shows sustained buying volume for 5+ minutes
- **Exit**: Sell on first volume decline or reversal signal
- **Win rate**: 35-45%
- **Risk**: Lower than sniping but still high. Volume can evaporate instantly.

### Graduation Play
- **Entry**: Buy when bonding curve approaches 85 SOL (near graduation threshold)
- **Exit**: Sell during post-graduation pump on Raydium
- **Win rate**: 50-65% (tokens that reach 85 SOL often graduate)
- **Risk**: If graduation fails or dumps immediately post-graduation

**Risk notes**: PumpFun strategies involve extremely high-risk tokens. Never allocate more than 1-2% of portfolio to any single PumpFun trade. Most tokens go to zero.

## Arbitrage

**Edge**: Price discrepancies across DEXs or between spot and perpetual markets.

**Types**:
- **DEX-to-DEX**: Same token priced differently on Raydium vs Orca
- **CEX-DEX**: Price difference between centralized and decentralized exchanges
- **Funding rate**: Long spot, short perp when funding is positive (or vice versa)
- **Triangle**: A→B→C→A across three token pairs

**Entry**: Price discrepancy exceeds transaction costs + slippage + margin of safety

**Exit**: Both legs of the trade execute or unwind immediately

**Expected metrics**:
- Win rate: > 80% (if costs are modeled correctly)
- Avg profit per trade: 0.1-1.0% (thin margins, high frequency)
- Profit factor: > 3.0
- Risk: execution risk (one leg fills, other does not)

**Risk notes**: Arbitrage requires speed (sub-second execution), accurate cost modeling, and capital efficiency. MEV bots compete for the same opportunities. See `mev-analysis` skill.

## Market Making

**Edge**: Capturing bid-ask spread while managing inventory risk. Profitable when spread exceeds adverse selection cost.

**Entry**: Place limit orders on both sides of the market (bid and ask)

**Exit**: Opposing order fills, or inventory limit reached

**Parameters**:
- Spread width: function of volatility and inventory
- Order size: small relative to book depth
- Inventory limits: maximum long/short exposure
- Rebalancing: frequency of quote updates

**Expected metrics**:
- Win rate: > 60%
- Profit per trade: very small (captured spread)
- Volume: high (many trades per day)
- Risk: inventory risk during sharp moves

**Risk notes**: Market making on Solana DEXs is complex due to AMM mechanics. Traditional limit-order market making is mainly on CLOBs (e.g., Phoenix, OpenBook). LP provision on AMMs is a form of passive market making. See `lp-math` and `impermanent-loss` skills.

## Choosing the Right Strategy Type

| Factor | Best Strategy Type |
|--------|--------------------|
| Trending market | Momentum / Trend Following |
| Ranging market | Mean Reversion |
| Low volatility transitioning to high | Breakout |
| Access to skilled wallet data | Copy Trading |
| High retail activity on PumpFun | PumpFun Strategies |
| Multi-venue infrastructure | Arbitrage |
| High capital, low-vol stable pairs | Market Making |
