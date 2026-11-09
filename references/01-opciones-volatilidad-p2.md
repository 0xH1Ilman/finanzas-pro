# 01-opciones-volatilidad — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: options-pricing

- Fuente: `agiprolabs/claude-trading-skills` → `skills/options-pricing` (MIT)
- Cuándo usarla: [STUB] Options pricing models including Black-Scholes, binomial trees, Monte Carlo, implied volatility surfaces, and Greeks for crypto options
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/options-pricing/` (black_scholes.py)

# Options Pricing

> **Status: STUB** — This skill provides a basic Black-Scholes implementation and an overview of planned capabilities. Full implementation is awaiting community contribution.

Options pricing is the quantitative foundation of derivatives trading. For crypto markets, options on BTC and ETH trade actively on Deribit, Lyra, and Aevo, while Solana options are emerging on platforms like Zeta Markets and PsyOptions. Understanding pricing models, implied volatility surfaces, and Greeks is essential for hedging, volatility trading, and constructing structured products.

This skill is informational and analytical only. It does not provide financial advice or trading recommendations.

---

## Current Capabilities

This stub includes a working Black-Scholes calculator with Greeks computation and a basic implied volatility solver. See `scripts/black_scholes.py` for the implementation.

```python
import math
from scipy.stats import norm

def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Price a European call option using Black-Scholes.

    Args:
        S: Current underlying price.
        K: Strike price.
        T: Time to expiration in years.
        r: Risk-free rate (annualized).
        sigma: Volatility (annualized).

    Returns:
        Theoretical call option price.
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
```

Run the demo:

```bash
python scripts/black_scholes.py --demo
```

---

## Planned Capabilities

When fully implemented, this skill will cover:

### Pricing Models

| Model | Option Style | Use Case |
|-------|-------------|----------|
| Black-Scholes | European | Vanilla calls/puts, quick Greeks |
| Binomial Tree | American | Early exercise, dividend-paying assets |
| Monte Carlo | Exotic | Path-dependent, barrier, Asian options |
| Black-76 | Futures | Futures options on crypto perpetuals |

### Greeks

| Greek | Measures | Formula Basis |
|-------|----------|---------------|
| Delta | Price sensitivity to underlying | dC/dS |
| Gamma | Delta sensitivity to underlying | d²C/dS² |
| Theta | Time decay per day | dC/dT |
| Vega | Sensitivity to volatility | dC/dσ |
| Rho | Sensitivity to interest rates | dC/dr |

### Implied Volatility

- Newton-Raphson and bisection IV solvers
- Volatility smile and skew analysis
- IV surface construction (strike x expiry)
- IV term structure analysis
- Vol-of-vol estimation

### Crypto Options Platforms

| Platform | Chain | Assets | Style |
|----------|-------|--------|-------|
| Deribit | Off-chain | BTC, ETH | European |
| Lyra | Optimism/Arbitrum | ETH, BTC | European |
| Aevo | Ethereum L2 | BTC, ETH, alts | European |
| Zeta Markets | Solana | SOL, BTC | European |
| PsyOptions | Solana | SOL, various | American |

### Structured Products

- Covered calls and protective puts
- Straddles and strangles for volatility trading
- Vertical spreads for directional exposure
- Iron condors for range-bound markets
- Calendar spreads for term structure trades

---

## Prerequisites

```bash
# Core (for full implementation)
uv pip install numpy scipy

# Optional (for visualization)
uv pip install matplotlib
```

The included `scripts/black_scholes.py` uses only the Python standard library (`math` module) and runs without any dependencies.

---

## Use Cases

### Hedging
Compute delta-neutral hedge ratios for crypto spot positions using options. Calculate the number of put contracts needed to protect a portfolio against downside moves.

### Volatility Trading
Compare implied volatility to realized volatility to identify over/underpriced options. When IV significantly exceeds realized vol, selling premium may be favorable (and vice versa).

### Structured Products
Price structured products that combine options at different strikes and expirations. Analyze payoff profiles and breakeven points before execution.

### Risk Assessment
Use Greeks to understand portfolio-level exposure to price moves (delta), acceleration (gamma), time decay (theta), and volatility changes (vega).

---

## Quick Reference: Black-Scholes Formulas

**Call price:**
```
C = S * N(d1) - K * e^(-rT) * N(d2)
```

**Put price:**
```
P = K * e^(-rT) * N(-d2) - S * N(-d1)
```

**Where:**
```
d1 = [ln(S/K) + (r + σ²/2) * T] / (σ * √T)
d2 = d1 - σ * √T
```

**Put-call parity:**
```
C - P = S - K * e^(-rT)
```

---

## Files

| File | Description |
|------|-------------|
| `references/planned_features.md` | Planned features, formulas, data sources, and implementation priorities |
| `scripts/black_scholes.py` | Black-Scholes calculator with Greeks and implied vol solver |

---

## Contributing

This skill is a stub awaiting full implementation. To contribute:

1. Implement binomial tree pricing for American-style options
2. Add Monte Carlo simulation for exotic payoffs
3. Build IV surface construction from market quotes
4. Integrate Deribit API for live options chain data
5. Add portfolio Greeks aggregation

See `references/planned_features.md` for the full feature list and implementation priorities.

---

*This skill provides analytical tools and mathematical models for informational purposes only. It does not constitute financial advice. Options trading involves substantial risk of loss.*

### Referencia: references/planned_features.md

# Options Pricing — Planned Features

> **Status: STUB** — This document outlines the planned feature set for the options-pricing skill.

---

## 1. Pricing Models

### Black-Scholes-Merton (Implemented in stub)

The foundational closed-form solution for European option pricing.

**Call price:**
```
C = S * N(d1) - K * e^(-rT) * N(d2)
```

**Put price:**
```
P = K * e^(-rT) * N(-d2) - S * N(-d1)
```

**Where:**
```
d1 = [ln(S/K) + (r + σ²/2) * T] / (σ * √T)
d2 = d1 - σ * √T
N(x) = standard normal CDF
```

**Assumptions:** Constant volatility, no dividends, continuous trading, log-normal returns, no transaction costs.

### Binomial Tree (Planned)

Cox-Ross-Rubinstein model for American options with early exercise.

```
u = e^(σ√Δt)          # up factor
d = 1/u                # down factor
p = (e^(rΔt) - d) / (u - d)  # risk-neutral probability
```

Backward induction with early exercise check at each node. Priority: **High** — needed for American-style crypto options.

### Monte Carlo Simulation (Planned)

For path-dependent and exotic options.

```
S(t+dt) = S(t) * exp((r - σ²/2)*dt + σ*√dt*Z)
where Z ~ N(0,1)
```

Variance reduction techniques: antithetic variates, control variates. Priority: **Medium**.

### Black-76 (Planned)

For futures options (relevant to crypto perpetual futures options).

```
C = e^(-rT) * [F*N(d1) - K*N(d2)]
d1 = [ln(F/K) + (σ²/2)*T] / (σ√T)
```

Priority: **Medium** — useful for Deribit futures options.

---

## 2. Greeks Formulas

All Greeks are implemented in the stub `scripts/black_scholes.py`.

| Greek | Call Formula | Put Formula |
|-------|------------|------------|
| Delta | N(d1) | N(d1) - 1 |
| Gamma | n(d1) / (S * σ * √T) | Same as call |
| Theta | -(S*n(d1)*σ)/(2√T) - r*K*e^(-rT)*N(d2) | -(S*n(d1)*σ)/(2√T) + r*K*e^(-rT)*N(-d2) |
| Vega | S * n(d1) * √T | Same as call |
| Rho | K*T*e^(-rT)*N(d2) | -K*T*e^(-rT)*N(-d2) |

Where n(x) is the standard normal PDF.

---

## 3. Implied Volatility

### Solvers (Stub includes bisection method)

| Method | Convergence | Robustness |
|--------|------------|------------|
| Bisection | Slow (linear) | Very robust |
| Newton-Raphson | Fast (quadratic) | Needs good initial guess |
| Brent's method | Fast | Robust, recommended |
| Jaeckel (2015) | Very fast | Industry standard |

### IV Surface Construction (Planned)

- Collect IV across strikes and expirations
- Interpolate using SVI (Stochastic Volatility Inspired) parameterization
- Detect skew, smile, and term structure patterns
- Arbitrage-free surface validation

Priority: **High** — critical for volatility trading.

---

## 4. Crypto Options Data Sources

### Deribit API

- **Base URL:** `https://www.deribit.com/api/v2/`
- **Auth:** API key + secret (public endpoints available without auth)
- **Key endpoints:**
  - `public/get_instruments` — list available options
  - `public/get_order_book` — bid/ask for an option
  - `public/ticker` — mark price, IV, Greeks
  - `public/get_book_summary_by_currency` — all options for BTC/ETH
- **Rate limits:** 20 requests/second (non-matching), 5/second (matching)
- **Assets:** BTC, ETH options (European, cash-settled)

### Lyra API

- On-chain options protocol on Optimism/Arbitrum
- Subgraph queries for historical data
- SDK for pricing and Greeks

### Zeta Markets (Solana)

- Solana-native options and futures
- Program ID-based on-chain data
- Limited API, primarily on-chain interaction

---

## 5. Implementation Priorities

| Priority | Feature | Complexity | Dependencies |
|----------|---------|-----------|-------------|
| 1 (Done) | Black-Scholes pricing | Low | math stdlib |
| 2 (Done) | Greeks computation | Low | math stdlib |
| 3 (Done) | Bisection IV solver | Low | math stdlib |
| 4 | Newton-Raphson IV solver | Low | scipy |
| 5 | Binomial tree pricing | Medium | numpy |
| 6 | Deribit API integration | Medium | httpx |
| 7 | IV surface construction | High | numpy, scipy |
| 8 | Monte Carlo simulation | Medium | numpy |
| 9 | Portfolio Greeks aggregation | Medium | numpy |
| 10 | Strategy payoff diagrams | Low | matplotlib |

---

## 6. Crypto-Specific Considerations

- **24/7 markets:** No market close — theta decay is continuous, adjust T calculation accordingly
- **High volatility:** Crypto vol ranges 50-150% annualized vs 15-30% for equities
- **Funding rates:** Perpetual futures funding affects put-call parity
- **No dividends:** Simplifies Black-Scholes (no dividend adjustment needed for most tokens)
- **Liquidity:** Options liquidity is concentrated in BTC/ETH; Solana options markets are thin
- **Settlement:** Most crypto options are cash-settled in the underlying or USD

---

*This document is for informational and planning purposes only. It does not constitute financial advice.*


---

## SKILL: options-strategy-advisor

- Fuente: `tradermonty/claude-trading-skills` → `skills/options-strategy-advisor` (MIT)
- Cuándo usarla: Options trading strategy analysis and simulation tool. Provides theoretical pricing using Black-Scholes model, Greeks calculation, strategy P/L simulation, and risk management guidance. Use when user requests options strategy analysis, covered calls, protective puts, spreads, iron condors, earnings plays, or options risk management. Includes volatility analysis, position sizing, and earnings-based strategy recommendations. Educational focus with practical trade simulation.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/options-strategy-advisor/` (requirements.txt, black_scholes.py)

# Options Strategy Advisor

## Overview

This skill provides comprehensive options strategy analysis and education using theoretical pricing models. It helps traders understand, analyze, and simulate options strategies without requiring real-time market data subscriptions.

**Core Capabilities:**
- **Black-Scholes Pricing**: Theoretical option prices and Greeks calculation
- **Strategy Simulation**: P/L analysis for major options strategies
- **Earnings Strategies**: Pre-earnings volatility plays integrated with Earnings Calendar
- **Risk Management**: Position sizing, Greeks exposure, max loss/profit analysis
- **Educational Focus**: Detailed explanations of strategies and risk metrics

**Data Sources:**
- FMP API: Stock prices, historical volatility, dividends, earnings dates
- User Input: Implied volatility (IV), risk-free rate
- Theoretical Models: Black-Scholes for pricing and Greeks

## Prerequisites

**Required:**
- Python 3.9+ with `numpy`, `scipy`, `requests`

**Optional:**
- FMP API key (for real-time stock prices and historical volatility)
  - Set via `FMP_API_KEY` environment variable or `--api-key` argument
  - Without API key: Use manual inputs for stock price and volatility

**Installation:**
```bash
pip install numpy scipy requests
```

**Quick Start Examples:**
```bash
# Basic call option pricing (no API key needed)
python3 scripts/black_scholes.py

# With FMP API key for real-time data
python3 scripts/black_scholes.py --ticker AAPL --api-key $FMP_API_KEY

# Custom option parameters
python3 scripts/black_scholes.py --stock-price 180 --strike 185 --days 30 --volatility 0.25

# Put option analysis
python3 scripts/black_scholes.py --stock-price 180 --strike 175 --days 30 --option-type put
```

## When to Use This Skill

Use this skill when:
- User asks about options strategies ("What's a covered call?", "How does an iron condor work?")
- User wants to simulate strategy P/L ("What's my max profit on a bull call spread?")
- User needs Greeks analysis ("What's my delta exposure?")
- User asks about earnings strategies ("Should I buy a straddle before earnings?")
- User wants to compare strategies ("Covered call vs protective put?")
- User needs position sizing guidance ("How many contracts should I trade?")
- User asks about volatility ("Is IV high right now?")

Example requests:
- "Analyze a covered call on AAPL"
- "What's the P/L on a $100/$105 bull call spread on MSFT?"
- "Should I trade a straddle before NVDA earnings?"
- "Calculate Greeks for my iron condor position"
- "Compare protective put vs covered call for downside protection"

## Supported Strategies

### Income Strategies
1. **Covered Call** - Own stock, sell call (generate income, cap upside)
2. **Cash-Secured Put** - Sell put with cash backing (collect premium, willing to buy stock)
3. **Poor Man's Covered Call** - LEAPS call + short near-term call (capital efficient)

### Protection Strategies
4. **Protective Put** - Own stock, buy put (insurance, limited downside)
5. **Collar** - Own stock, sell call + buy put (limited upside/downside)

### Directional Strategies
6. **Bull Call Spread** - Buy lower strike call, sell higher strike call (limited risk/reward bullish)
7. **Bull Put Spread** - Sell higher strike put, buy lower strike put (credit spread, bullish)
8. **Bear Call Spread** - Sell lower strike call, buy higher strike call (credit spread, bearish)
9. **Bear Put Spread** - Buy higher strike put, sell lower strike put (limited risk/reward bearish)

### Volatility Strategies
10. **Long Straddle** - Buy ATM call + ATM put (profit from big move either direction)
11. **Long Strangle** - Buy OTM call + OTM put (cheaper than straddle, bigger move needed)
12. **Short Straddle** - Sell ATM call + ATM put (profit from no movement, unlimited risk)
13. **Short Strangle** - Sell OTM call + OTM put (profit from no movement, wider range)

### Range-Bound Strategies
14. **Iron Condor** - Bull put spread + bear call spread (profit from range-bound movement)
15. **Iron Butterfly** - Sell ATM straddle, buy OTM strangle (profit from tight range)

### Advanced Strategies
16. **Calendar Spread** - Sell near-term option, buy longer-term option (profit from time decay)
17. **Diagonal Spread** - Calendar spread with different strikes (directional + time decay)
18. **Ratio Spread** - Unbalanced spread (more contracts on one leg)

## Analysis Workflow

### Step 1: Gather Input Data

**Required from User:**
- Ticker symbol
- Strategy type
- Strike prices
- Expiration date(s)
- Position size (number of contracts)

**Optional from User:**
- Implied Volatility (IV) - if not provided, use Historical Volatility (HV)
- Risk-free rate - default to current 3-month T-bill rate (~5.3% as of 2025)

**Fetched from FMP API:**
- Current stock price
- Historical prices (for HV calculation)
- Dividend yield
- Upcoming earnings date (for earnings strategies)

**Example User Input:**
```
Ticker: AAPL
Strategy: Bull Call Spread
Long Strike: $180
Short Strike: $185
Expiration: 30 days
Contracts: 10
IV: 25% (or use HV if not provided)
```

### Step 2: Calculate Historical Volatility (if IV not provided)

**Objective:** Estimate volatility from historical price movements.

**Method:**
```python
# Fetch 90 days of price data
prices = get_historical_prices("AAPL", days=90)

# Calculate daily returns
returns = np.log(prices / prices.shift(1))

# Annualized volatility
HV = returns.std() * np.sqrt(252)  # 252 trading days
```

**Output:**
- Historical Volatility (annualized percentage)
- Note to user: "HV = 24.5%, consider using current market IV for more accuracy"

**User Can Override:**
- Provide IV from broker platform (ThinkorSwim, TastyTrade, etc.)
- Script accepts `--iv 28.0` parameter

### Step 3: Price Options Using Black-Scholes

**Black-Scholes Model:**

For European-style options:
```
Call Price = S * N(d1) - K * e^(-r*T) * N(d2)
Put Price = K * e^(-r*T) * N(-d2) - S * N(-d1)

Where:
d1 = [ln(S/K) + (r + σ²/2) * T] / (σ * √T)
d2 = d1 - σ * √T

S = Current stock price
K = Strike price
r = Risk-free rate
T = Time to expiration (years)
σ = Volatility (IV or HV)
N() = Cumulative standard normal distribution
```

**Adjustments:**
- Subtract present value of dividends from S for calls
- American options: Use approximation or note "European pricing, may undervalue American options"

**Python Implementation:**
```python
from scipy.stats import norm
import numpy as np

def black_scholes_call(S, K, T, r, sigma, q=0):
    """
    S: Stock price
    K: Strike price
    T: Time to expiration (years)
    r: Risk-free rate
    sigma: Volatility
    q: Dividend yield
    """
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    call_price = S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    put_price = K*np.exp(-r*T)*norm.cdf(-d2) - S*np.exp(-q*T)*norm.cdf(-d1)
    return put_price
```

**Output for Each Option Leg:**
- Theoretical price
- Note: "Market price may differ due to bid-ask spread and American vs European pricing"

### Step 4: Calculate Greeks

**The Greeks** measure option price sensitivity to various factors:

**Delta (Δ):** Change in option price per $1 change in stock price
```python
def delta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.cdf(d1)

def delta_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * (norm.cdf(d1) - 1)
```

**Gamma (Γ):** Change in delta per $1 change in stock price
```python
def gamma(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-q*T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
```

**Theta (Θ):** Change in option price per day (time decay)
```python
def theta_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    theta = (-S*norm.pdf(d1)*sigma*np.exp(-q*T)/(2*np.sqrt(T))
             - r*K*np.exp(-r*T)*norm.cdf(d2)
             + q*S*norm.cdf(d1)*np.exp(-q*T))

    return theta / 365  # Per day
```

**Vega (ν):** Change in option price per 1% change in volatility
```python
def vega(S, K, T, r, sigma, q=0):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return S * np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T) / 100  # Per 1%
```

**Rho (ρ):** Change in option price per 1% change in interest rate
```python
def rho_call(S, K, T, r, sigma, q=0):
    d2 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T)) - sigma*np.sqrt(T)
    return K * T * np.exp(-r*T) * norm.cdf(d2) / 100  # Per 1%
```

**Position Greeks:**

For a strategy with multiple legs, sum Greeks across all legs:
```python
# Example: Bull Call Spread
# Long 1x $180 call
# Short 1x $185 call

delta_position = (1 * delta_long) + (-1 * delta_short)
gamma_position = (1 * gamma_long) + (-1 * gamma_short)
theta_position = (1 * theta_long) + (-1 * theta_short)
vega_position = (1 * vega_long) + (-1 * vega_short)
```

**Greeks Interpretation:**

| Greek | Meaning | Example |
|-------|---------|---------|
| **Delta** | Directional exposure | Δ = 0.50 → $50 profit if stock +$1 |
| **Gamma** | Delta acceleration | Γ = 0.05 → Delta increases by 0.05 if stock +$1 |
| **Theta** | Daily time decay | Θ = -$5 → Lose $5/day from time passing |
| **Vega** | Volatility sensitivity | ν = $10 → Gain $10 if IV increases 1% |
| **Rho** | Interest rate sensitivity | ρ = $2 → Gain $2 if rates increase 1% |

### Step 5: Simulate Strategy P/L

**Objective:** Calculate profit/loss at various stock prices at expiration.

**Method:**

Generate stock price range (e.g., ±30% from current price):
```python
current_price = 180
price_range = np.linspace(current_price * 0.7, current_price * 1.3, 100)
```

For each price point, calculate P/L:
```python
def calculate_pnl(strategy, stock_price_at_expiration):
    pnl = 0

    for leg in strategy.legs:
        if leg.type == 'call':
            intrinsic_value = max(0, stock_price_at_expiration - leg.strike)
        else:  # put
            intrinsic_value = max(0, leg.strike - stock_price_at_expiration)

        if leg.position == 'long':
            pnl += (intrinsic_value - leg.premium_paid) * 100  # Per contract
        else:  # short
            pnl += (leg.premium_received - intrinsic_value) * 100

    return pnl * num_contracts
```

**Key Metrics:**
- **Max Profit**: Highest possible P/L
- **Max Loss**: Worst possible P/L
- **Breakeven Point(s)**: Stock price(s) where P/L = 0
- **Profit Probability**: Percentage of price range that's profitable (simplified)

**Example Output:**
```
Bull Call Spread: $180/$185 on AAPL (30 DTE, 10 contracts)

Current Price: $180.00
Net Debit: $2.50 per spread ($2,500 total)

Max Profit: $2,500 (at $185+)
Max Loss: -$2,500 (at $180-)
Breakeven: $182.50
Risk/Reward: 1:1

Probability Profit: ~55% (if stock stays above $182.50)
```

### Step 6: Generate P/L Diagram (ASCII Art)

**Visual representation of P/L across stock prices:**

```python
def generate_pnl_diagram(price_range, pnl_values, current_price, width=60, height=15):
    """Generate ASCII P/L diagram"""

    # Normalize to chart dimensions
    max_pnl = max(pnl_values)
    min_pnl = min(pnl_values)

    lines = []
    lines.append(f"\nP/L Diagram: {strategy_name}")
    lines.append("-" * width)

    # Y-axis levels
    levels = np.linspace(max_pnl, min_pnl, height)

    for level in levels:
        if abs(level) < (max_pnl - min_pnl) * 0.05:
            label = f"    0 |"  # Zero line
        else:
            label = f"{level:6.0f} |"

        row = label
        for i in range(width - len(label)):
            idx = int(i / (width - len(label)) * len(price_range))
            pnl = pnl_values[idx]
            price = price_range[idx]

            # Determine character
            if abs(pnl - level) < (max_pnl - min_pnl) / height:
                if pnl > 0:
                    char = '█'  # Profit
                elif pnl < 0:
                    char = '░'  # Loss
                else:
                    char = '─'  # Breakeven
            elif abs(level) < (max_pnl - min_pnl) * 0.05:
                char = '─'  # Zero line
            elif abs(price - current_price) < (price_range[-1] - price_range[0]) * 0.02:
                char = '│'  # Current price line
            else:
                char = ' '

            row += char

        lines.append(row)

    lines.append(" " * 6 + "|" + "-" * (width - 6))
    lines.append(" " * 6 + f"${price_range[0]:.0f}" + " " * (width - 20) + f"${price_range[-1]:.0f}")
    lines.append(" " * (width // 2 - 5) + "Stock Price")

    return "\n".join(lines)
```

**Example Output:**
```
P/L Diagram: Bull Call Spread $180/$185
------------------------------------------------------------
 +2500 |                               ████████████████████
       |                         ██████
       |                   ██████
       |             ██████
     0 |       ──────
       | ░░░░░░
       |░░░░░░
 -2500 |░░░░░
      |____________________________________________________________
       $126                  $180                   $234
                          Stock Price

Legend: █ Profit  ░ Loss  ── Breakeven  │ Current Price
```

### Step 7: Strategy-Specific Analysis

Provide tailored guidance based on strategy type:

**Covered Call:**
```
Income Strategy: Generate premium while capping upside

Setup:
- Own 100 shares of AAPL @ $180
- Sell 1x $185 call (30 DTE) for $3.50

Max Profit: $850 (Stock at $185+ = $5 stock gain + $3.50 premium)
Max Loss: Unlimited downside (stock ownership)
Breakeven: $176.50 (Cost basis - premium received)

Greeks:
- Delta: -0.30 (reduces stock delta from 1.00 to 0.70)
- Theta: +$8/day (time decay benefit)

Assignment Risk: If AAPL > $185 at expiration, shares called away

When to Use:
- Neutral to slightly bullish
- Want income in sideways market
- Willing to sell stock at $185

Exit Plan:
- Buy back call if stock rallies strongly (preserve upside)
- Let expire if stock stays below $185
- Roll to next month if want to keep shares
```

**Protective Put:**
```
Insurance Strategy: Limit downside while keeping upside

Setup:
- Own 100 shares of AAPL @ $180
- Buy 1x $175 put (30 DTE) for $2.00

Max Profit: Unlimited (stock can rise infinitely)
Max Loss: -$7 per share = ($5 stock loss + $2 premium)
Breakeven: $182 (Cost basis + premium paid)

Greeks:
- Delta: +0.80 (stock delta 1.00 - put delta 0.20)
- Theta: -$6/day (time decay cost)

Protection: Guaranteed to sell at $175, no matter how far stock falls

When to Use:
- Own stock, worried about short-term drop
- Earnings coming up, want protection
- Alternative to stop-loss (can't be stopped out)

Cost: "Insurance premium" - typically 1-3% of stock value

Exit Plan:
- Let expire worthless if stock rises (cost of insurance)
- Exercise put if stock falls below $175
- Sell put if stock drops but want to keep shares
```

**Iron Condor:**
```
Range-Bound Strategy: Profit from low volatility

Setup (example on AAPL @ $180):
- Sell $175 put for $1.50
- Buy $170 put for $0.50
- Sell $185 call for $1.50
- Buy $190 call for $0.50

Net Credit: $2.00 ($200 per iron condor)

Max Profit: $200 (if stock stays between $175-$185)
Max Loss: $300 (if stock moves outside $170-$190)
Breakevens: $173 and $187
Profit Range: $175 to $185 (58% probability)

Greeks:
- Delta: ~0 (market neutral)
- Theta: +$15/day (time decay benefit)
- Vega: -$25 (short volatility)

When to Use:
- Expect low volatility, range-bound movement
- After big move, think consolidation
- High IV environment (sell expensive options)

Risk: Unlimited if one side tested
- Use stop loss at 2x credit received (exit at -$400)

Adjustments:
- If tested on one side, roll that side out in time
- Close early at 50% max profit to reduce tail risk
```

### Step 8: Earnings Strategy Analysis

**Integration with Earnings Calendar:**

When user asks about earnings strategies, fetch earnings date:
```python
from earnings_calendar import get_next_earnings_date

earnings_date = get_next_earnings_date("AAPL")
days_to_earnings = (earnings_date - today).days
```

**Pre-Earnings Strategies:**

**Long Straddle/Strangle:**
```
Setup (AAPL @ $180, earnings in 7 days):
- Buy $180 call for $5.00
- Buy $180 put for $4.50
- Total Cost: $9.50

Thesis: Expect big move (>5%) but unsure of direction

Breakevens: $170.50 and $189.50
Profit if: Stock moves >$9.50 in either direction

Greeks:
- Delta: ~0 (neutral)
- Vega: +$50 (long volatility)
- Theta: -$25/day (time decay hurts)

IV Crush Risk: ⚠️ CRITICAL
- Pre-earnings IV: 40% (elevated)
- Post-earnings IV: 25% (typical)
- IV drop: -15 points = -$750 loss even if stock doesn't move!

Analysis:
- Implied Move: √(DTE/365) × IV × Stock Price
  = √(7/365) × 0.40 × 180 = ±$10.50
- Breakeven Move Needed: ±$9.50
- Probability Profit: ~30-40% (implied move > breakeven move)

Recommendation:
✅ Consider if you expect >10% move (larger than implied)
❌ Avoid if expect normal ~5% earnings move (IV crush will hurt)

Alternative: Buy further OTM strikes to reduce cost
- $175/$185 strangle cost $4.00 (need >$8 move, but cheaper)
```

**Short Iron Condor:**
```
Setup (AAPL @ $180, earnings in 7 days):
- Sell $170/$175 put spread for $2.00
- Sell $185/$190 call spread for $2.00
- Net Credit: $4.00

Thesis: Expect stock to stay range-bound ($175-$185)

Profit Zone: $175 to $185
Max Profit: $400
Max Loss: $100

IV Crush Benefit: ✅
- Short high IV before earnings
- IV drops after earnings → profit on vega
- Even if stock moves slightly, IV drop helps

Greeks:
- Delta: ~0 (market neutral)
- Vega: -$40 (short volatility - good here!)
- Theta: +$20/day

Recommendation:
✅ Good if expect normal earnings reaction (<8% move)
✅ Benefit from IV crush regardless of direction
⚠️ Risk if stock gaps outside range (>10% move)

Exit Plan:
- Close next day if IV crushed (capture profit early)
- Use stop loss if one side tested (-2x credit)
```

### Step 9: Risk Management Guidance

**Position Sizing:**

```
Account Size: $50,000
Risk Tolerance: 2% per trade = $1,000 max risk

Iron Condor Example:
- Max loss per spread: $300
- Max contracts: $1,000 / $300 = 3 contracts
- Actual position: 3 iron condors

Bull Call Spread Example:
- Debit paid: $2.50 per spread
- Max contracts: $1,000 / $250 = 4 contracts
- Actual position: 4 spreads
```

**Portfolio Greeks Management:**

```
Portfolio Guidelines:
- Delta: -10 to +10 (mostly neutral)
- Theta: Positive preferred (seller advantage)
- Vega: Monitor if >$500 (IV risk)

Current Portfolio:
- Delta: +5 (slightly bullish)
- Theta: +$150/day (collecting $150 daily)
- Vega: -$300 (short volatility)

Interpretation:
✅ Neutral delta (safe)
✅ Positive theta (time working for you)
⚠️ Short vega: If IV spikes, lose $300 per 1% IV increase
→ Reduce short premium positions if VIX rising
```

**Adjustments and Exits:**

```
Exit Rules by Strategy:

Covered Call:
- Profit: 50-75% of max profit
- Loss: Stock drops >5%, buy back call to preserve upside
- Time: 7-10 DTE, roll to avoid assignment

Spreads:
- Profit: 50% of max profit (close early, reduce tail risk)
- Loss: 2x debit paid (cut losses early)
- Time: 21 DTE, close or roll (avoid gamma risk)

Iron Condor:
- Profit: 50% of credit (close early common)
- Loss: One side tested, 2x credit lost
- Adjustment: Roll tested side out in time

Straddle/Strangle:
- Profit: Stock moved >breakeven, close immediately
- Loss: Theta eating position, stock not moving
- Time: Day after earnings (if earnings play)
```

## Output Format

**Strategy Analysis Report Template:**

```markdown
# Options Strategy Analysis: [Strategy Name]

**Symbol:** [TICKER]
**Strategy:** [Strategy Type]
**Expiration:** [Date] ([DTE] days)
**Contracts:** [Number]

---

## Strategy Setup

### Leg Details
| Leg | Type | Strike | Price | Position | Quantity |
|-----|------|--------|-------|----------|----------|
| 1 | Call | $180 | $5.00 | Long | 1 |
| 2 | Call | $185 | $2.50 | Short | 1 |

**Net Debit/Credit:** $2.50 debit ($250 total for 1 spread)

---

## Profit/Loss Analysis

**Max Profit:** $250 (at $185+)
**Max Loss:** -$250 (at $180-)
**Breakeven:** $182.50
**Risk/Reward Ratio:** 1:1

**Probability Analysis:**
- Probability of Profit: ~55% (stock above $182.50)
- Expected Value: $25 (simplified)

---

## P/L Diagram

[ASCII art diagram here]

---

## Greeks Analysis

### Position Greeks (1 spread)
- **Delta:** +0.20 (gains $20 if stock +$1)
- **Gamma:** +0.03 (delta increases by 0.03 if stock +$1)
- **Theta:** -$5/day (loses $5 per day from time decay)
- **Vega:** +$8 (gains $8 if IV increases 1%)

### Interpretation
- **Directional Bias:** Slightly bullish (positive delta)
- **Time Decay:** Working against you (negative theta)
- **Volatility:** Benefits from IV increase (positive vega)

---

## Risk Assessment

### Maximum Risk
**Scenario:** Stock falls below $180
**Max Loss:** -$250 (100% of premium paid)
**% of Account:** 0.5% (if $50k account)

### Assignment Risk
**Early Assignment:** Low (calls have time value)
**At Expiration:** Manage positions if in-the-money

---

## Trade Management

### Entry
✅ Enter if: [Conditions]
- Stock price $178-$182
- IV below 30%
- >21 DTE

### Profit Taking
- **Target 1:** 50% profit ($125) - Close half
- **Target 2:** 75% profit ($187.50) - Close all

### Stop Loss
- **Trigger:** Stock falls below $177 (-$150 loss)
- **Action:** Close position immediately

### Adjustments
- If stock rallies to $184, consider rolling short call higher
- If stock drops to $179, add second spread at $175/$180

---

## Suitability

### When to Use This Strategy
✅ Moderately bullish on AAPL
✅ Expect upside to $185-$190
✅ Want defined risk
✅ 21-45 DTE timeframe

### When to Avoid
❌ Very bullish (buy stock or long call instead)
❌ High IV environment (wait for IV to drop)
❌ Earnings in <7 days (IV crush risk)

---

## Alternatives Comparison

| Strategy | Max Profit | Max Loss | Complexity | When Better |
|----------|-----------|----------|------------|-------------|
| Bull Call Spread | $250 | -$250 | Medium | Moderately bullish |
| Long Call | Unlimited | -$500 | Low | Very bullish |
| Covered Call | $850 | Unlimited | Medium | Own stock already |
| Bull Put Spread | $300 | -$200 | Medium | Want credit spread |

**Recommendation:** Bull call spread is good balance of risk/reward for moderate bullish thesis.

---

*Disclaimer: This is theoretical analysis using Black-Scholes pricing. Actual market prices may differ. Trade at your own risk. Options are complex instruments with significant loss potential.*
```

**File Naming Convention:**
```
options_analysis_[TICKER]_[STRATEGY]_[DATE].md
```

Example: `options_analysis_AAPL_BullCallSpread_2025-11-08.md`

## Key Principles

### Theoretical Pricing Limitations

**What Users Should Know:**
1. **Black-Scholes Assumptions:**
   - European-style options (can't exercise early)
   - Constant volatility (IV changes in reality)
   - No transaction costs
   - Continuous trading

2. **Real vs Theoretical:**
   - Bid-ask spread: Actual cost higher than theoretical
   - American options: Can be exercised early (especially ITM puts)
   - Liquidity: Wide markets on illiquid options
   - Dividends: Ex-dividend dates affect pricing

3. **Best Practices:**
   - Use as educational tool and comparative analysis
   - Get real quotes from broker before trading
   - Understand theoretical price ≈ mid-market price
   - Account for commissions and slippage

### Volatility Guidance

**Historical vs Implied Volatility:**

```
Historical Volatility (HV): What happened
- Calculated from past price movements
- Objective, based on data
- Available for free (FMP API)

Implied Volatility (IV): What market expects
- Derived from option prices
- Subjective, based on supply/demand
- Requires live options data (user provides)

Comparison:
- IV > HV: Options expensive (consider selling)
- IV < HV: Options cheap (consider buying)
- IV = HV: Fairly priced
```

**IV Percentile:**

User provides current IV, we calculate percentile:
```python
# Fetch 1-year HV data
historical_hvs = calculate_hv_series(prices_1yr, window=30)

# Calculate IV percentile
iv_percentile = percentileofscore(historical_hvs, current_iv)

if iv_percentile > 75:
    guidance = "High IV - consider selling premium (credit spreads, iron condors)"
elif iv_percentile < 25:
    guidance = "Low IV - consider buying options (long calls/puts, debit spreads)"
else:
    guidance = "Normal IV - any strategy appropriate"
```

## Integration with Other Skills

**Earnings Calendar:**
- Fetch earnings dates automatically
- Suggest earnings-specific strategies
- Calculate days to earnings (DTE critical for IV)
- Warn about IV crush risk

**Technical Analyst:**
- Use support/resistance for strike selection
- Trend analysis for directional strategies
- Breakout potential for straddle/strangle timing

**US Stock Analysis:**
- Fundamental analysis for longer-term strategies (LEAPS)
- Dividend yield for covered call/put analysis
- Earnings quality for earnings plays

**Bubble Detector:**
- High bubble risk → focus on protective puts
- Low risk → bullish strategies
- Critical risk → avoid long premium (theta hurts)

**Portfolio Manager:**
- Track options positions alongside stock positions
- Aggregate Greeks across portfolio
- Options as hedging tool for stock positions

## Important Notes

- **All analysis in English**
- **Educational focus**: Strategies explained clearly
- **Theoretical pricing**: Black-Scholes approximation
- **User IV input**: Optional, defaults to HV
- **No real-time data required**: FMP Free tier sufficient
- **Dependencies**: Python 3.9+, numpy, scipy, requests

## Common Use Cases

**Use Case 1: Learn Strategy**
```
User: "Explain a covered call"

Workflow:
1. Read the strategy descriptions in this document and the pricing methodology
   in references/black_scholes_methodology.md
2. Explain concept, risk/reward, when to use
3. Simulate example on AAPL
4. Show P/L diagram
5. Compare to alternatives
```

**Use Case 2: Analyze Specific Trade**
```
User: "Analyze $180/$185 bull call spread on AAPL, 30 days"

Workflow:
1. Fetch AAPL price from FMP
2. Calculate HV or ask user for IV
3. Price both options (Black-Scholes)
4. Calculate Greeks
5. Simulate P/L
6. Generate analysis report
```

**Use Case 3: Earnings Strategy**
```
User: "Should I trade options before NVDA earnings?"

Workflow:
1. Fetch NVDA earnings date (Earnings Calendar)
2. Calculate days to earnings
3. Estimate IV percentile (if user provides IV)
4. Suggest straddle/strangle vs iron condor
5. Warn about IV crush
6. Simulate both strategies
```

**Use Case 4: Portfolio Greeks Check**
```
User: "What are my total portfolio Greeks?"

Workflow:
1. User provides current positions
2. Calculate Greeks for each position
3. Sum Greeks across portfolio
4. Assess overall exposure
5. Suggest adjustments if needed
```

## Troubleshooting

**Problem: IV not available**
- Solution: Use HV as proxy, note to user
- Ask user to provide IV from broker platform

**Problem: Negative option price**
- Solution: Check inputs (strike vs stock price)
- Deep ITM options may have numerical issues

**Problem: Greeks seem wrong**
- Solution: Verify inputs (T, sigma, r)
- Check if using annual vs daily values

**Problem: Strategy too complex**
- Solution: Break into legs, analyze separately
- Refer to references for strategy details

## Resources

**References:**
- `references/black_scholes_methodology.md` - Black-Scholes formulas, Greeks, and interpretation

**Scripts:**
- `scripts/black_scholes.py` - Pricing engine and Greeks

**External Resources:**
- Options Playbook: https://www.optionsplaybook.com/
- CBOE Education: https://www.cboe.com/education/
- Black-Scholes Calculator: Various online tools for verification

---

**Version**: 1.0
**Last Updated**: 2025-11-08
**Dependencies**: Python 3.9+, numpy, scipy, requests
**API**: FMP API (Free tier sufficient)

### Referencia: README.md

# Options Strategy Advisor

Educational options trading tool providing theoretical pricing, strategy analysis, and risk management guidance using Black-Scholes model.

## Overview

Options Strategy Advisor helps traders understand and analyze options strategies without requiring expensive real-time options data. It uses theoretical pricing models (Black-Scholes) combined with free stock market data (FMP API) to simulate strategies and calculate Greeks.

**Key Features:**
- ✅ Black-Scholes pricing engine
- ✅ All Greeks calculation (Delta, Gamma, Theta, Vega, Rho)
- ✅ 17+ options strategies supported
- ✅ P/L simulation and visualization
- ✅ Earnings strategy integration
- ✅ Historical volatility calculation
- ✅ Risk management guidance

## Why This Approach?

**No expensive data subscriptions needed:**
- Real-time options data: $99-$500/month (Polygon.io, Intrinio)
- FMP API Free tier: $0/month (250 requests/day)

**Educational focus:**
- Learn how strategies work
- Understand Greeks and risk metrics
- Compare strategies side-by-side

**Practical application:**
- Theoretical prices ≈ market mid-prices
- User can input actual IV from broker
- Good for strategy planning and education

## Supported Strategies

### Income Strategies
1. **Covered Call** - Generate income from stock holdings
2. **Cash-Secured Put** - Get paid to buy stock
3. **Poor Man's Covered Call** - Capital-efficient covered call

### Protection Strategies
4. **Protective Put** - Insurance for stock positions
5. **Collar** - Limited risk/reward protection

### Directional Strategies
6. **Bull Call Spread** - Limited risk bullish play
7. **Bull Put Spread** - Credit spread for bullish view
8. **Bear Call Spread** - Credit spread for bearish view
9. **Bear Put Spread** - Limited risk bearish play

### Volatility Strategies
10. **Long Straddle** - Profit from big moves
11. **Long Strangle** - Cheaper straddle, bigger move needed
12. **Short Straddle** - Profit from no movement (high risk)
13. **Short Strangle** - Wider range straddle

### Range-Bound Strategies
14. **Iron Condor** - Profit from range-bound trading
15. **Iron Butterfly** - Tight range profit

### Advanced Strategies
16. **Calendar Spread** - Time decay play
17. **Diagonal Spread** - Directional + time decay

## Installation

### Prerequisites
- Python 3.8+
- FMP API key (free tier sufficient)

### Install Dependencies
```bash
pip install numpy scipy requests pandas
```

### Get FMP API Key
1. Visit https://financialmodelingprep.com/developer/docs
2. Sign up for free account
3. Copy API key
4. Set environment variable:
```bash
export FMP_API_KEY="your_key_here"
```

## Quick Start

### Test Black-Scholes Pricer

```bash
python scripts/black_scholes.py
```

**Example Output:**
```
BLACK-SCHOLES OPTIONS PRICER - EXAMPLE
======================================================================

Input Parameters:
  Stock Price: $180.00
  Strike Price: $185.00
  Days to Expiration: 30
  Volatility: 25.0%
  Risk-Free Rate: 5.30%
  Dividend Yield: 1.0%

======================================================================
CALL OPTION
======================================================================
Price: $2.45
Intrinsic Value: $0.00
Time Value: $2.45

Greeks:
  Delta: 0.3654 ($36.54 per $1 move)
  Gamma: 0.0234 (delta changes by 0.0234)
  Theta: -$0.18/day (loses $0.18 per day)
  Vega: $0.25 per 1% IV (gains $0.25 if IV +1%)
  Rho: $0.12 per 1% rate (gains $0.12 if rate +1%)
```

### Use in Your Code

```python
from scripts.black_scholes import OptionPricer

# Initialize pricer
pricer = OptionPricer(
    S=180,          # Stock price
    K=185,          # Strike price
    T=30/365,       # Time to expiration (years)
    r=0.053,        # Risk-free rate (5.3%)
    sigma=0.25,     # Volatility (25%)
    q=0.01          # Dividend yield (1%)
)

# Get call option price
call_price = pricer.call_price()
print(f"Call Price: ${call_price:.2f}")

# Get all Greeks for call
call_greeks = pricer.get_all_greeks('call')
print(f"Delta: {call_greeks['delta']:.4f}")
print(f"Gamma: {call_greeks['gamma']:.4f}")
print(f"Theta: ${call_greeks['theta']:.2f}/day")
print(f"Vega: ${call_greeks['vega']:.2f} per 1%")
```

### Calculate Historical Volatility

```python
from scripts.black_scholes import (
    calculate_historical_volatility,
    fetch_historical_prices_for_hv
)

# Fetch prices from FMP
api_key = "your_key"
prices = fetch_historical_prices_for_hv("AAPL", api_key, days=90)

# Calculate 30-day HV
hv = calculate_historical_volatility(prices, window=30)
print(f"30-Day HV: {hv*100:.2f}%")
```

## Understanding the Metrics

### Option Price Components

**Intrinsic Value:**
- Call: max(0, Stock Price - Strike Price)
- Put: max(0, Strike Price - Stock Price)

**Time Value:**
- Option Price - Intrinsic Value
- Decays to $0 at expiration

### The Greeks

**Delta (Δ)** - Directional Exposure
```
Range: 0 to 1 (calls), -1 to 0 (puts)
Meaning: Change in option price per $1 stock move

Example: Δ = 0.50
→ If stock +$1, option +$0.50
→ If stock -$1, option -$0.50
```

**Gamma (Γ)** - Delta Acceleration
```
Meaning: Change in delta per $1 stock move
Peak: ATM options
Low: Deep ITM or OTM

Example: Γ = 0.05, Δ currently = 0.50
→ If stock +$1, delta becomes 0.55
```

**Theta (Θ)** - Time Decay
```
Meaning: Change in option price per day
Sign: Usually negative (options lose value over time)
Peak: Last 30 days before expiration

Example: Θ = -$0.15/day
→ Tomorrow, option loses $0.15 if nothing else changes
```

**Vega (ν)** - Volatility Sensitivity
```
Meaning: Change in option price per 1% IV change
Sign: Always positive (options gain value when vol increases)

Example: ν = $0.25 per 1%
→ If IV increases from 25% to 26%, option +$0.25
```

**Rho (ρ)** - Interest Rate Sensitivity
```
Meaning: Change in option price per 1% rate change
Sign: Positive for calls, negative for puts
Impact: Usually small unless long-dated options

Example: ρ = $0.10 per 1%
→ If interest rate increases 1%, option +$0.10
```

### Volatility: HV vs IV

**Historical Volatility (HV):**
- Calculated from past price movements
- Objective, based on actual data
- Available free (from price data)

**Implied Volatility (IV):**
- Derived from option market prices
- Subjective, based on supply/demand
- Requires real-time options data (or user input)

**Comparison:**
```
IV > HV: Options expensive → Consider selling premium
IV < HV: Options cheap → Consider buying options
IV = HV: Fairly priced → Any strategy works
```

## Common Workflows

### 1. Analyze a Strategy

```python
from scripts.black_scholes import OptionPricer

# Stock: AAPL @ $180
# Strategy: Bull Call Spread $180/$185 (30 DTE)

# Price long call ($180 strike)
long_call = OptionPricer(S=180, K=180, T=30/365, r=0.053, sigma=0.25)
long_price = long_call.call_price()
long_delta = long_call.call_delta()

# Price short call ($185 strike)
short_call = OptionPricer(S=180, K=185, T=30/365, r=0.053, sigma=0.25)
short_price = short_call.call_price()
short_delta = short_call.call_delta()

# Strategy metrics
net_debit = long_price - short_price
max_profit = (185 - 180) - net_debit
max_loss = -net_debit
position_delta = long_delta - short_delta

print(f"Bull Call Spread $180/$185")
print(f"Net Debit: ${net_debit:.2f}")
print(f"Max Profit: ${max_profit:.2f} (at $185+)")
print(f"Max Loss: ${max_loss:.2f} (at $180-)")
print(f"Position Delta: {position_delta:.4f}")
```

### 2. Compare IV to HV

```python
# Get HV
prices = fetch_historical_prices_for_hv("AAPL", api_key, days=90)
hv = calculate_historical_volatility(prices, window=30)

# User provides IV (from broker platform)
iv = 0.28  # 28% from ThinkorSwim

print(f"Historical Volatility: {hv*100:.2f}%")
print(f"Implied Volatility: {iv*100:.1f}%")

if iv > hv * 1.1:
    print("→ Options expensive (IV > HV) - Consider selling premium")
elif iv < hv * 0.9:
    print("→ Options cheap (IV < HV) - Consider buying options")
else:
    print("→ Fairly priced")
```

### 3. Earnings Strategy

Check if earnings coming up (use Earnings Calendar skill):
```python
# If earnings in 7 days:
# - IV typically elevated (30-50% higher)
# - Consider straddle/strangle (profit from big move)
# - Or sell iron condor (profit from IV crush)

# Example: Long Straddle
straddle_cost = call_price + put_price
breakeven_up = stock_price + straddle_cost
breakeven_down = stock_price - straddle_cost

print(f"Straddle Cost: ${straddle_cost:.2f}")
print(f"Breakevens: ${breakeven_down:.2f} / ${breakeven_up:.2f}")
print(f"Need {abs(breakeven_up - stock_price)/stock_price*100:.1f}% move to profit")
```

## Limitations & Best Practices

### Theoretical vs Market Prices

**Black-Scholes Assumptions:**
- European options (can't exercise early)
- Constant volatility (changes in reality)
- No transaction costs
- Continuous trading

**Real World Differences:**
- American options (most stocks) can exercise early
- Bid-ask spread: Actual cost higher than theoretical mid
- Commissions and slippage
- Liquidity: Wide markets on illiquid options

### Best Practices

**1. Use for Education & Planning:**
- Learn how strategies work
- Compare different approaches
- Understand risk/reward before trading

**2. Verify Before Trading:**
- Get real quotes from your broker
- Check bid-ask spread
- Confirm option liquidity (open interest, volume)

**3. Input Actual IV:**
- Theoretical price assumes constant volatility
- Use current market IV for accuracy
- Check IV percentile (high/low relative to history)

**4. Account for Dividends:**
- Ex-dividend dates affect option prices
- Calls lose value, puts gain value on ex-div date
- Script supports dividend yield input

**5. Monitor Greeks:**
- Delta: Overall directional exposure
- Theta: Daily time decay (seller advantage)
- Vega: Volatility risk (watch during earnings)
- Gamma: Risk of delta changing (avoid near expiration)

## Integration with Other Skills

**Earnings Calendar:**
- Fetch earnings dates
- Identify IV crush opportunities
- Time earnings strategies

**Technical Analyst:**
- Use support/resistance for strike selection
- Trend analysis for directional strategies
- Breakout potential for straddle timing

**US Stock Analysis:**
- Fundamental analysis for LEAPS
- Dividend yield for covered call/put
- Earnings quality for earnings plays

**Bubble Detector:**
- High risk → protective puts
- Low risk → bullish strategies
- Critical risk → avoid long premium

**Portfolio Manager:**
- Track options with stock positions
- Aggregate Greeks across portfolio
- Options as hedging tool

## API Usage & Costs

**Free Tier Sufficient:**
- Stock prices: 1 request per symbol
- Historical prices (HV): 1 request per symbol
- Dividend data: 1 request per symbol

**Example Analysis Cost:**
```
Covered Call on AAPL:
- Current price: 1 request
- HV calculation: 1 request (90 days data)
- Dividend yield: 1 request
Total: 3 requests

Daily budget: 250 requests / day
→ Can analyze ~80 strategies per day
```

## Troubleshooting

### Negative Option Price
**Cause:** Invalid inputs (strike vs stock price)
**Solution:** Check that inputs make sense

### Greeks Seem Wrong
**Cause:** Using wrong units (annual vs daily)
**Solution:** Verify T is in years, theta is per day

### HV Very Different from IV
**Normal:** IV reflects future expectations, HV is past
**Action:** Use IV from broker for more accuracy

### Option Price Too High/Low
**Cause:** Volatility input incorrect
**Solution:** Verify sigma is annual (e.g., 0.25 for 25%)

## Resources

### Documentation
- `SKILL.md` - Complete workflow and strategies
- `references/strategies_guide.md` - All strategies explained (TBD)
- `references/greeks_explained.md` - Greeks deep dive (TBD)

### External Resources
- Options Playbook: https://www.optionsplaybook.com/
- CBOE Education: https://www.cboe.com/education/
- Black-Scholes Calculator: https://www.option-price.com/

### Get Real IV
- ThinkorSwim (TD Ameritrade): Free
- TastyTrade: Free
- Barchart: https://www.barchart.com/options
- CBOE: http://www.cboe.com/delayedquote/

## Future Enhancements

**Planned:**
- Strategy simulation script (complete P/L analysis)
- P/L diagram generator (ASCII art)
- Earnings strategy advisor (integrated with Earnings Calendar)
- Complete strategy reference guides

**Contributions Welcome:**
- Additional strategies
- Improved volatility models
- Better visualization tools

## License

Educational use. Trade at your own risk. Options involve significant risk and are not suitable for all investors.

---

**Version:** 1.0
**Last Updated:** 2025-11-08
**Dependencies:** Python 3.8+, numpy, scipy, requests
**API:** FMP API (Free tier sufficient)
**Model:** Black-Scholes (European options pricing)

### Referencia: references/black_scholes_methodology.md

# Black-Scholes Methodology Reference

## Overview

The Black-Scholes model is the foundation for theoretical options pricing in this skill. This document provides the mathematical framework and interpretation guidance.

## Black-Scholes Formula

### Call Option Price
```
C = S × e^(-qT) × N(d₁) - K × e^(-rT) × N(d₂)
```

### Put Option Price
```
P = K × e^(-rT) × N(-d₂) - S × e^(-qT) × N(-d₁)
```

### Parameters
| Symbol | Description | Typical Range |
|--------|-------------|---------------|
| S | Current stock price | Market price |
| K | Strike price | User selected |
| T | Time to expiration (years) | 0.01 - 2.0 |
| r | Risk-free rate | 0.03 - 0.06 |
| σ | Volatility | 0.10 - 1.00 |
| q | Dividend yield | 0.00 - 0.05 |

### d₁ and d₂ Calculations
```
d₁ = [ln(S/K) + (r - q + σ²/2) × T] / (σ × √T)
d₂ = d₁ - σ × √T
```

## The Greeks

### Delta (Δ)
- **Definition**: Price change per $1 move in underlying
- **Call**: 0 to +1 (positive, bullish)
- **Put**: -1 to 0 (negative, bearish)
- **ATM options**: ~0.50 (call) or ~-0.50 (put)

### Gamma (Γ)
- **Definition**: Rate of change of delta
- **Always positive** for long options
- **Highest at ATM**, decreases as option moves ITM/OTM
- **Increases** as expiration approaches

### Theta (Θ)
- **Definition**: Daily time decay ($/day)
- **Negative** for long options (lose value daily)
- **Positive** for short options (collect decay)
- **Accelerates** in final 30 days

### Vega (ν)
- **Definition**: Price change per 1% IV move
- **Always positive** for long options
- **Highest at ATM**
- **Critical** for earnings plays

### Rho (ρ)
- **Definition**: Price change per 1% rate change
- **Positive** for calls, **negative** for puts
- **Small impact** in short-dated options

## Historical vs Implied Volatility

| Metric | Description | Source |
|--------|-------------|--------|
| HV (Historical) | Past price movement | Calculated from prices |
| IV (Implied) | Market expectation | Derived from option prices |

### IV-HV Relationship
- **IV > HV**: Options expensive → consider selling premium
- **IV < HV**: Options cheap → consider buying
- **IV ≈ HV**: Fairly priced

### IV Percentile Interpretation
| Percentile | Interpretation | Strategy Bias |
|------------|----------------|---------------|
| >80% | Very high IV | Sell premium |
| 50-80% | Elevated IV | Neutral/sell |
| 20-50% | Normal IV | Direction-based |
| <20% | Low IV | Buy premium |

## Model Limitations

### Assumptions (Not Always True)
1. **Constant volatility** - IV changes constantly
2. **European exercise** - American options can exercise early
3. **No transaction costs** - Commissions and slippage exist
4. **Continuous trading** - Gaps and halts occur
5. **Log-normal distribution** - Fat tails exist in practice

### When Model Underperforms
- Deep ITM American puts (early exercise value)
- Near expiration with high gamma
- Earnings/events (IV regime change)
- Low liquidity options (wide bid-ask)

## Practical Adjustments

### American Options
- Calls: Black-Scholes accurate if no dividends
- Puts: May undervalue ITM puts near expiration
- Solution: Note "European pricing approximation"

### Dividend Handling
- Include dividend yield (q) in calculations
- For discrete dividends: subtract PV from stock price
- Ex-dividend dates affect early exercise decisions

## Strategy Selection Framework

### By Market Outlook
| Outlook | Delta Target | Strategies |
|---------|--------------|------------|
| Bullish | +0.3 to +0.7 | Long call, bull spread, covered call |
| Bearish | -0.3 to -0.7 | Long put, bear spread, protective put |
| Neutral | -0.1 to +0.1 | Iron condor, straddle, butterfly |

### By Volatility View
| IV View | Vega Target | Strategies |
|---------|-------------|------------|
| IV rising | Positive | Long straddle, long strangle |
| IV falling | Negative | Iron condor, short straddle |
| IV neutral | Near zero | Spreads, collars |

## Position Sizing Guidelines

### Risk-Based Sizing
```
Max Contracts = (Account Risk $) / (Max Loss per Contract)
```

### Portfolio Greeks Limits
| Greek | Conservative | Moderate | Aggressive |
|-------|--------------|----------|------------|
| Delta | ±10 | ±25 | ±50 |
| Theta | +$50/day | +$150/day | +$300/day |
| Vega | ±$200 | ±$500 | ±$1000 |

## References

- Black, F. & Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities"
- Hull, J.C. "Options, Futures, and Other Derivatives"
- CBOE Education: https://www.cboe.com/education/


---

## SKILL: pandas-ta

- Fuente: `agiprolabs/claude-trading-skills` → `skills/pandas-ta` (MIT)
- Cuándo usarla: Technical analysis with 130+ indicators using pandas-ta for crypto market data
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/pandas-ta/` (compute_indicators.py, multi_indicator_scan.py)

# pandas-ta — Technical Analysis for Crypto Markets

pandas-ta is a Python library that extends pandas DataFrames with 130+ technical analysis indicators accessible via `df.ta`. It covers trend, momentum, volatility, volume, and overlap indicator categories — all callable with a single method on any OHLCV DataFrame.

## Installation

```bash
uv pip install pandas-ta pandas httpx
```

## Quick Start

```python
import pandas as pd
import pandas_ta as ta

# Assume df is a DataFrame with columns: open, high, low, close, volume
# All lowercase column names required

# Single indicator
df["rsi"] = df.ta.rsi(length=14)
df["atr"] = df.ta.atr(length=14)

# Multiple indicators via strategy
df.ta.strategy(ta.Strategy(
    name="Quick Check",
    ta=[
        {"kind": "rsi", "length": 14},
        {"kind": "macd", "fast": 12, "slow": 26, "signal": 9},
        {"kind": "bbands", "length": 20, "std": 2.0},
    ]
))
```

## OHLCV DataFrame Format

pandas-ta expects a DataFrame with lowercase column names:

```python
import pandas as pd

df = pd.DataFrame({
    "open": [...],
    "high": [...],
    "low": [...],
    "close": [...],
    "volume": [...]
}, index=pd.DatetimeIndex([...]))
```

**Important**: Set the index to a `DatetimeIndex` for time-aware indicators like VWAP. Column names must be lowercase (`close`, not `Close`).

### Handling Missing Data

```python
# Drop rows with NaN in OHLCV columns
df = df.dropna(subset=["open", "high", "low", "close", "volume"])

# Forward-fill small gaps (1-2 bars max)
df = df.ffill(limit=2)

# Verify no zero-volume bars for volume indicators
df = df[df["volume"] > 0]
```

## Core Indicator Categories

### Trend Indicators

Identify market direction and trend strength.

| Indicator | Call | Key Signal |
|-----------|------|------------|
| SMA | `df.ta.sma(length=20)` | Price above = bullish |
| EMA | `df.ta.ema(length=20)` | Faster than SMA, less lag |
| SuperTrend | `df.ta.supertrend(length=10, multiplier=3)` | Direction column: 1=bull, -1=bear |
| Ichimoku | `df.ta.ichimoku()` | Returns tuple of (span, lines) DataFrames |
| VWMA | `df.ta.vwma(length=20)` | Volume-weighted price trend |
| HMA | `df.ta.hma(length=20)` | Minimal lag, smooth trend |
| ADX | `df.ta.adx(length=14)` | >25 = trending, <20 = ranging |

### Momentum Indicators

Measure speed and magnitude of price changes.

| Indicator | Call | Key Signal |
|-----------|------|------------|
| RSI | `df.ta.rsi(length=14)` | >70 overbought, <30 oversold |
| MACD | `df.ta.macd(fast=12, slow=26, signal=9)` | Histogram crossover = entry |
| Stochastic | `df.ta.stoch(k=14, d=3, smooth_k=3)` | >80 overbought, <20 oversold |
| CCI | `df.ta.cci(length=20)` | >100 overbought, <-100 oversold |
| Williams %R | `df.ta.willr(length=14)` | >-20 overbought, <-80 oversold |
| ROC | `df.ta.roc(length=10)` | Positive = upward momentum |
| MFI | `df.ta.mfi(length=14)` | Money flow version of RSI |

### Volatility Indicators

Measure price dispersion and expected range.

| Indicator | Call | Key Signal |
|-----------|------|------------|
| Bollinger Bands | `df.ta.bbands(length=20, std=2)` | Squeeze = breakout pending |
| ATR | `df.ta.atr(length=14)` | Position sizing, stop placement |
| Keltner Channels | `df.ta.kc(length=20, scalar=1.5)` | BB inside KC = squeeze |
| Donchian Channels | `df.ta.donchian(lower_length=20, upper_length=20)` | Breakout detection |

### Volume Indicators

Confirm price moves with volume analysis.

| Indicator | Call | Key Signal |
|-----------|------|------------|
| OBV | `df.ta.obv()` | Divergence from price = reversal |
| VWAP | `df.ta.vwap()` | Intraday fair value (needs DatetimeIndex) |
| CMF | `df.ta.cmf(length=20)` | >0 accumulation, <0 distribution |
| AD | `df.ta.ad()` | Accumulation/Distribution line |

## Strategy Class

Run multiple indicators in a single call using `ta.Strategy`:

```python
import pandas_ta as ta

# Built-in "All" strategy runs every indicator
df.ta.strategy(ta.AllStrategy)

# Custom strategy
my_strategy = ta.Strategy(
    name="Crypto Scalp",
    description="Fast indicators for crypto scalping",
    ta=[
        {"kind": "ema", "length": 9},
        {"kind": "ema", "length": 21},
        {"kind": "rsi", "length": 7},
        {"kind": "stoch", "k": 5, "d": 3, "smooth_k": 3},
        {"kind": "atr", "length": 7},
        {"kind": "bbands", "length": 10, "std": 2.0},
        {"kind": "obv"},
    ]
)
df.ta.strategy(my_strategy)
```

### Named Strategy Patterns

```python
# Trend following
trend_strategy = ta.Strategy(
    name="Trend",
    ta=[
        {"kind": "ema", "length": 20},
        {"kind": "ema", "length": 50},
        {"kind": "adx", "length": 14},
        {"kind": "supertrend", "length": 10, "multiplier": 3},
        {"kind": "atr", "length": 14},
    ]
)

# Mean reversion
reversion_strategy = ta.Strategy(
    name="Mean Reversion",
    ta=[
        {"kind": "rsi", "length": 14},
        {"kind": "bbands", "length": 20, "std": 2.0},
        {"kind": "stoch", "k": 14, "d": 3, "smooth_k": 3},
        {"kind": "cci", "length": 20},
    ]
)

# Momentum
momentum_strategy = ta.Strategy(
    name="Momentum",
    ta=[
        {"kind": "macd", "fast": 12, "slow": 26, "signal": 9},
        {"kind": "rsi", "length": 14},
        {"kind": "obv"},
        {"kind": "roc", "length": 10},
        {"kind": "mfi", "length": 14},
    ]
)
```

## Crypto-Specific Considerations

### 24/7 Markets
- No session gaps — indicators that rely on open/close of sessions behave differently
- VWAP resets at midnight UTC by default; consider anchored VWAP for custom periods
- Weekend data is continuous — no Monday gap effects

### High Volatility Adjustments
- **Bollinger Bands**: Use 2.5-3x standard deviation instead of the default 2x
- **RSI periods**: Shorter periods (7-10) capture faster crypto cycles
- **ATR**: Use for dynamic stop-losses; crypto ATR is typically 2-5x equity ATR
- **SuperTrend multiplier**: 3-4x for crypto vs 2-3x for equities

### Low-Cap Token Considerations
- Volume indicators (OBV, CMF, MFI) are unreliable with thin order books
- Prefer price-based indicators (RSI, BBands, SuperTrend) for low-liquidity tokens
- ATR-based position sizing is critical — wide spreads amplify losses
- Wash trading inflates volume; cross-reference with on-chain data

### Timeframe Selection
| Timeframe | Use Case | Recommended Indicators |
|-----------|----------|----------------------|
| 1m-5m | Scalping, PumpFun | RSI(5-7), EMA(5,13), ATR(5) |
| 15m-1h | Day trading | MACD, RSI(14), BBands, EMA(20,50) |
| 4h-1d | Swing trading | SuperTrend, ADX, EMA(50,200) |
| 1w | Position trading | SMA(20,50), RSI(14), monthly VWAP |

## Common Indicator Combinations

### Trend Following
```python
# EMA crossover + ADX confirmation + SuperTrend direction
ema_fast = df.ta.ema(length=20)
ema_slow = df.ta.ema(length=50)
adx_df = df.ta.adx(length=14)
st_df = df.ta.supertrend(length=10, multiplier=3)

bullish = (
    (ema_fast > ema_slow) &
    (adx_df["ADX_14"] > 25) &
    (st_df["SUPERTd_10_3.0"] == 1)
)
```

### Mean Reversion
```python
# RSI oversold + price at lower BB + Stochastic oversold
rsi = df.ta.rsi(length=14)
bb = df.ta.bbands(length=20, std=2.5)
stoch = df.ta.stoch(k=14, d=3, smooth_k=3)

buy_signal = (
    (rsi < 30) &
    (df["close"] <= bb["BBL_20_2.5"]) &
    (stoch["STOCHk_14_3_3"] < 20)
)
```

### Momentum Confirmation
```python
# MACD histogram positive + RSI above 50 + OBV rising
macd = df.ta.macd(fast=12, slow=26, signal=9)
rsi = df.ta.rsi(length=14)
obv = df.ta.obv()

momentum_bull = (
    (macd["MACDh_12_26_9"] > 0) &
    (rsi > 50) &
    (obv > obv.shift(1))
)
```

### Volatility Breakout (BB Squeeze)
```python
# Bollinger Band width contracting + volume spike
bb = df.ta.bbands(length=20, std=2.0)
atr = df.ta.atr(length=14)
vol_sma = df["volume"].rolling(20).mean()

bb_width = (bb["BBU_20_2.0"] - bb["BBL_20_2.0"]) / bb["BBM_20_2.0"]
squeeze = bb_width < bb_width.rolling(120).quantile(0.1)
vol_spike = df["volume"] > (vol_sma * 2.0)

breakout_setup = squeeze & vol_spike
```

## Integration with Other Skills

- **birdeye-api**: Fetch OHLCV data → feed into pandas-ta for indicator computation
- **vectorbt**: Use pandas-ta indicators as signal inputs for backtesting
- **trading-visualization**: Plot indicator overlays on price charts
- **slippage-modeling**: Combine ATR with slippage estimates for realistic execution modeling
- **position-sizing**: Use ATR-based sizing from pandas-ta output

## Files

### References
- `references/indicator_guide.md` — Top 20 crypto indicators with syntax, parameters, and interpretation
- `references/strategy_patterns.md` — Pre-built strategy combinations for scalping, day trading, and swing trading
- `references/common_pitfalls.md` — Common mistakes with technical indicators in crypto markets

### Scripts
- `scripts/compute_indicators.py` — Fetch OHLCV data and compute standard indicator set with signal summary
- `scripts/multi_indicator_scan.py` — Run multiple strategy profiles and score current signal alignment

### Referencia: references/common_pitfalls.md

# pandas-ta — Common Pitfalls in Crypto Technical Analysis

Mistakes that cause false signals, incorrect backtests, and real losses when using technical indicators on crypto market data.

## 1. NaN Values at Start of Series

**Problem**: Every indicator produces NaN for its warmup period. RSI(14) has 14+ NaN bars. MACD(12,26,9) has 33+ NaN bars. Treating NaN as 0 or ignoring it generates false signals.

**Fix**:
```python
# Always check for sufficient data
min_bars = 200  # Enough warmup for most indicators
if len(df) < min_bars:
    raise ValueError(f"Need {min_bars} bars, got {len(df)}")

# Drop NaN rows before signal evaluation
signals = signals.dropna()

# Or check explicitly
rsi = df.ta.rsi(length=14)
valid_rsi = rsi.iloc[14:]  # Skip warmup period
```

**Rule of thumb**: Need at least 3x the longest indicator period in your dataset.

## 2. Lookahead Bias

**Problem**: Using future data to make current decisions. Common in backtesting when indicators or signals reference data not yet available at decision time.

**Examples**:
- Using `df["close"]` for the current bar before the bar closes
- Centering a moving average (pandas default for some rolling operations)
- Using `BBP` (Bollinger Band percent) calculated on the full dataset

**Fix**:
```python
# Shift signals by 1 bar — act on NEXT bar after signal
df["signal"] = (df["RSI_14"] < 30).astype(int)
df["entry"] = df["signal"].shift(1)  # Enter on next bar

# In backtesting, always use .shift(1) for signal-to-execution
# You see the signal at bar N close, you act at bar N+1 open
```

## 3. Overfitting with Too Many Indicators

**Problem**: Combining 10+ indicators to find "perfect" entry conditions produces a system that worked historically but fails live. More indicators = more curve fitting.

**Symptoms**:
- Backtest win rate > 80% but live trading loses money
- Strategy only works on one specific token in one specific time period
- Adding or removing one indicator drastically changes results

**Fix**:
- Use 3-5 indicators maximum per strategy
- Each indicator should measure something different (trend + momentum + volatility, not RSI + Stochastic + Williams %R which all measure momentum)
- Validate on out-of-sample data from a different time period
- Use walk-forward analysis, not single backtest optimization

## 4. Parameter Optimization Trap

**Problem**: Optimizing indicator parameters on historical data finds the best past parameters, not the best future parameters. RSI(13) beating RSI(14) on historical data is noise, not signal.

**Fix**:
```python
# Test a small range of standard parameters, not a wide sweep
# Standard RSI: 7, 9, 14, 21 — not RSI(1) through RSI(50)
standard_params = {
    "rsi": [7, 9, 14, 21],
    "ema_fast": [9, 12, 20],
    "ema_slow": [21, 26, 50],
    "bb_std": [2.0, 2.5, 3.0],
}

# If results are very sensitive to parameter choice, the edge is fragile
# Robust strategies work across a range of parameters
```

## 5. Volume Indicator Reliability on Low-Cap Tokens

**Problem**: OBV, CMF, MFI, and VWAP assume volume data is accurate. On Solana memecoins and low-cap tokens, volume is often unreliable due to:
- Wash trading (bots trading with themselves)
- Concentrated liquidity (one market maker = most volume)
- Cross-DEX arbitrage inflating volume
- Different DEX APIs reporting different volume

**Fix**:
- Use price-based indicators (RSI, BBands, SuperTrend, EMAs) as primary
- Use volume indicators only for confirmation, not as primary signals
- Cross-reference volume with on-chain transaction count
- For tokens with < $100K daily volume, ignore volume indicators entirely

## 6. Repainting Indicators

**Problem**: Some indicators change their historical values as new data arrives. The signal that appeared on bar N may look different when viewed from bar N+10.

**Common repainting indicators**:
- Zigzag (by definition)
- Pivot points (require future data to confirm)
- Some implementations of SuperTrend (confirm pandas-ta uses non-repainting version)

**Fix**:
- Test by comparing indicator values computed on data ending at bar N vs. data ending at bar N+100
- If historical values change, the indicator repaints
- pandas-ta's standard indicators (RSI, MACD, BBands, EMA) do NOT repaint

```python
# Verification: compute indicator twice, compare
rsi_full = df.ta.rsi(length=14)
rsi_partial = df.iloc[:100].ta.rsi(length=14)

# These should be identical for overlapping bars
assert rsi_full.iloc[:100].equals(rsi_partial), "Indicator repaints!"
```

## 7. Timeframe Mismatch

**Problem**: Indicator parameters calibrated for daily charts produce garbage on 1-minute charts. RSI(14) on 1d = 14 trading days. RSI(14) on 1m = 14 minutes. They measure completely different things.

**Fix**:
- Scale parameters to match the timeframe's noise level
- 1m charts: shorter periods (5-9), wider bands (3x std)
- 1d charts: standard periods (14-21), standard bands (2-2.5x std)
- See the parameter table in `indicator_guide.md` for recommended values

## 8. Missing Data and Gaps

**Problem**: Gaps in OHLCV data (missing bars) cause indicator distortion. A 1h chart missing 3 bars has a gap that makes EMAs jump.

**Common causes in crypto**:
- API rate limits causing missed fetches
- DEX downtime or low liquidity periods with no trades
- Data provider outages

**Fix**:
```python
# Detect gaps
expected_freq = pd.Timedelta("1h")  # Adjust for your timeframe
time_diffs = df.index.to_series().diff()
gaps = time_diffs[time_diffs > expected_freq * 1.5]
if len(gaps) > 0:
    print(f"Warning: {len(gaps)} gaps detected")
    print(gaps)

# Option 1: Forward-fill small gaps (1-2 bars)
df = df.asfreq(expected_freq, method="ffill")

# Option 2: Split into continuous segments
segments = []
gap_indices = gaps.index.tolist()
# Process each segment separately

# Option 3: Recompute indicators after gap
# Drop all indicator columns, recompute from scratch
```

## 9. VWAP Misuse in 24/7 Markets

**Problem**: VWAP is designed to reset at market open. Crypto has no market open. pandas-ta resets VWAP at midnight UTC, which is arbitrary for most traders.

**Fix**:
- Use VWAP for intraday reference only, not as a multi-day indicator
- Consider anchored VWAP from significant swing highs/lows instead
- VWMA (volume-weighted moving average) is often more useful than VWAP for crypto

```python
# VWAP requires DatetimeIndex
df.index = pd.DatetimeIndex(df.index)
vwap = df.ta.vwap()  # Resets daily at midnight UTC

# For multi-day analysis, use VWMA instead
vwma = df.ta.vwma(length=20)
```

## 10. Treating Indicators as Absolute Truth

**Problem**: RSI < 30 does not mean "buy". It means price has dropped significantly relative to recent history. In a crash, RSI can stay below 30 for weeks while price drops another 80%.

**Key principles**:
- Indicators are probability modifiers, not binary signals
- Combine indicator signals with market context (regime, trend, volume)
- No single indicator works in all market conditions
- Mean reversion indicators fail in trending markets; trend indicators fail in ranges
- Always have a stop-loss independent of indicator readings

## 11. Column Name Confusion

**Problem**: pandas-ta uses specific column naming conventions. Getting the name wrong returns KeyError or operates on the wrong column.

**Fix**:
```python
# After computing, inspect column names
df.ta.macd(append=True)
print([c for c in df.columns if "MACD" in c])
# Output: ['MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9']

# Common pattern: {INDICATOR}_{param1}_{param2}
# BBands: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0, BBB_20_2.0, BBP_20_2.0
# Stoch: STOCHk_14_3_3, STOCHd_14_3_3
# SuperTrend: SUPERT_10_3.0, SUPERTd_10_3.0, SUPERTl_10_3.0, SUPERTs_10_3.0
```

## 12. Ignoring Indicator Divergence

**Problem**: Price making new highs while RSI makes lower highs (bearish divergence) is one of the strongest signals in TA — but many traders ignore it because the trend "looks strong."

**Fix**:
```python
# Simple divergence detection
def detect_divergence(price: pd.Series, indicator: pd.Series, lookback: int = 20) -> str:
    """Detect bullish or bearish divergence."""
    price_higher = price.iloc[-1] > price.iloc[-lookback:].max() * 0.98
    ind_lower = indicator.iloc[-1] < indicator.iloc[-lookback:].max() * 0.95

    if price_higher and ind_lower:
        return "bearish_divergence"

    price_lower = price.iloc[-1] < price.iloc[-lookback:].min() * 1.02
    ind_higher = indicator.iloc[-1] > indicator.iloc[-lookback:].min() * 1.05

    if price_lower and ind_higher:
        return "bullish_divergence"

    return "none"
```

## Summary Checklist

Before using any indicator-based strategy:

- [ ] Dataset has 3x the longest indicator period in bars
- [ ] NaN values from warmup are excluded from signals
- [ ] Signals are shifted by 1 bar (no lookahead)
- [ ] Using 3-5 indicators max, each measuring different things
- [ ] Parameters are standard values, not over-optimized
- [ ] Volume indicators only used on tokens with reliable volume
- [ ] Tested on out-of-sample data from a different time period
- [ ] Gap detection and handling is implemented
- [ ] Stop-losses are defined independently of indicators
- [ ] Column names are verified after computation

### Referencia: references/indicator_guide.md

# pandas-ta — Top 20 Crypto Indicators Guide

The most useful pandas-ta indicators for crypto trading, organized by category with syntax, recommended parameters, and signal interpretation.

## Trend Indicators

### 1. EMA (Exponential Moving Average)
- **Call**: `df.ta.ema(length=20)`
- **Returns**: `pd.Series` named `EMA_20`
- **Default**: `length=10`
- **Crypto params**: 9/21 for scalping, 20/50 for day trading, 50/200 for swing
- **Signal**: Price above EMA = bullish; EMA crossovers (fast > slow) = buy signal
- **Note**: Responds faster than SMA to recent price changes

### 2. SMA (Simple Moving Average)
- **Call**: `df.ta.sma(length=50)`
- **Returns**: `pd.Series` named `SMA_50`
- **Default**: `length=10`
- **Crypto params**: 20/50/200 are standard levels
- **Signal**: Golden cross (50 > 200) = bullish; death cross (50 < 200) = bearish

### 3. SuperTrend
- **Call**: `df.ta.supertrend(length=10, multiplier=3.0)`
- **Returns**: DataFrame with columns `SUPERT_10_3.0`, `SUPERTd_10_3.0`, `SUPERTl_10_3.0`, `SUPERTs_10_3.0`
- **Default**: `length=7, multiplier=3.0`
- **Crypto params**: `length=10, multiplier=3.0-4.0` (wider for volatile tokens)
- **Signal**: `SUPERTd` = 1 (bullish) or -1 (bearish); direction flip = trend change
- **Note**: Excellent standalone trend filter for crypto

### 4. ADX (Average Directional Index)
- **Call**: `df.ta.adx(length=14)`
- **Returns**: DataFrame with `ADX_14`, `DMP_14`, `DMN_14`
- **Default**: `length=14`
- **Signal**: ADX > 25 = trending, ADX < 20 = ranging; DMP > DMN = uptrend

### 5. HMA (Hull Moving Average)
- **Call**: `df.ta.hma(length=20)`
- **Returns**: `pd.Series` named `HMA_20`
- **Default**: `length=10`
- **Signal**: Minimal lag; direction change = early trend signal
- **Note**: Best low-lag moving average for fast crypto markets

### 6. VWMA (Volume Weighted Moving Average)
- **Call**: `df.ta.vwma(length=20)`
- **Returns**: `pd.Series` named `VWMA_20`
- **Default**: `length=10`
- **Signal**: Price above VWMA = volume-confirmed bullish; divergence = weakening trend
- **Note**: Less reliable on low-cap tokens with thin volume

## Momentum Indicators

### 7. RSI (Relative Strength Index)
- **Call**: `df.ta.rsi(length=14)`
- **Returns**: `pd.Series` named `RSI_14`
- **Default**: `length=14`
- **Crypto params**: 7-10 for scalping, 14 for standard, 21 for swing
- **Signal**: > 70 overbought, < 30 oversold; divergence from price = reversal warning
- **Note**: In strong crypto trends, RSI can stay >70 for extended periods

### 8. MACD (Moving Average Convergence Divergence)
- **Call**: `df.ta.macd(fast=12, slow=26, signal=9)`
- **Returns**: DataFrame with `MACD_12_26_9`, `MACDh_12_26_9`, `MACDs_12_26_9`
- **Default**: `fast=12, slow=26, signal=9`
- **Signal**: Histogram > 0 = bullish momentum; zero-line crossover = trend change
- **Note**: Histogram is the most actionable component for timing

### 9. Stochastic Oscillator
- **Call**: `df.ta.stoch(k=14, d=3, smooth_k=3)`
- **Returns**: DataFrame with `STOCHk_14_3_3`, `STOCHd_14_3_3`
- **Default**: `k=14, d=3, smooth_k=3`
- **Crypto params**: `k=5, d=3, smooth_k=3` for scalping
- **Signal**: > 80 overbought, < 20 oversold; %K crossing above %D = buy

### 10. CCI (Commodity Channel Index)
- **Call**: `df.ta.cci(length=20)`
- **Returns**: `pd.Series` named `CCI_20_0.015`
- **Default**: `length=14`
- **Signal**: > 100 overbought, < -100 oversold; zero-line cross = trend direction

### 11. Williams %R
- **Call**: `df.ta.willr(length=14)`
- **Returns**: `pd.Series` named `WILLR_14`
- **Default**: `length=14`
- **Signal**: > -20 overbought, < -80 oversold; faster than RSI

### 12. ROC (Rate of Change)
- **Call**: `df.ta.roc(length=10)`
- **Returns**: `pd.Series` named `ROC_10`
- **Default**: `length=10`
- **Signal**: Positive = upward momentum; crossing zero = trend shift

### 13. MFI (Money Flow Index)
- **Call**: `df.ta.mfi(length=14)`
- **Returns**: `pd.Series` named `MFI_14`
- **Default**: `length=14`
- **Signal**: > 80 overbought, < 20 oversold; volume-weighted RSI equivalent
- **Note**: Requires reliable volume data; unreliable on low-cap tokens

## Volatility Indicators

### 14. Bollinger Bands
- **Call**: `df.ta.bbands(length=20, std=2.0)`
- **Returns**: DataFrame with `BBL_20_2.0`, `BBM_20_2.0`, `BBU_20_2.0`, `BBB_20_2.0`, `BBP_20_2.0`
- **Default**: `length=5, std=2.0`
- **Crypto params**: `length=20, std=2.5` (wider for crypto volatility)
- **Signal**: BBP (percent B) < 0 = below lower band; BBB (bandwidth) contracting = squeeze
- **Note**: Use BBB for squeeze detection; narrow BBB = imminent breakout

### 15. ATR (Average True Range)
- **Call**: `df.ta.atr(length=14)`
- **Returns**: `pd.Series` named `ATRr_14`
- **Default**: `length=14`
- **Crypto params**: 7 for scalping, 14 for standard
- **Signal**: Rising ATR = increasing volatility; use for stop-loss distance (1.5-2x ATR)
- **Note**: Essential for position sizing — normalize by price for cross-asset comparison

### 16. Keltner Channels
- **Call**: `df.ta.kc(length=20, scalar=1.5)`
- **Returns**: DataFrame with `KCLe_20_1.5`, `KCBe_20_1.5`, `KCUe_20_1.5`
- **Default**: `length=20, scalar=2`
- **Signal**: BBands inside KC = TTM Squeeze (low volatility, breakout pending)

### 17. Donchian Channels
- **Call**: `df.ta.donchian(lower_length=20, upper_length=20)`
- **Returns**: DataFrame with `DCL_20_20`, `DCM_20_20`, `DCU_20_20`
- **Default**: `lower_length=20, upper_length=20`
- **Signal**: Price at upper channel = breakout; price at lower = breakdown

## Volume Indicators

### 18. OBV (On-Balance Volume)
- **Call**: `df.ta.obv()`
- **Returns**: `pd.Series` named `OBV`
- **Signal**: OBV rising while price flat = accumulation; OBV falling while price rising = distribution
- **Note**: Trend of OBV matters more than absolute value

### 19. VWAP (Volume Weighted Average Price)
- **Call**: `df.ta.vwap()`
- **Returns**: `pd.Series` named `VWAP_D`
- **Signal**: Price above VWAP = bullish intraday bias; price below = bearish
- **Note**: Requires DatetimeIndex; resets daily at midnight UTC for crypto
- **Crypto consideration**: Anchored VWAP from key swing points is more useful than daily reset

### 20. CMF (Chaikin Money Flow)
- **Call**: `df.ta.cmf(length=20)`
- **Returns**: `pd.Series` named `CMF_20`
- **Default**: `length=20`
- **Signal**: > 0 = buying pressure (accumulation); < 0 = selling pressure (distribution)
- **Note**: Combines price and volume; confirm with OBV for stronger signals

## Parameter Adjustment by Timeframe

| Timeframe | RSI | EMA fast/slow | BB length/std | ATR | Stoch k |
|-----------|-----|--------------|---------------|-----|---------|
| 1m-5m | 5-7 | 5/13 | 10/2.0 | 5 | 5 |
| 15m | 9-14 | 9/21 | 15/2.0 | 10 | 9 |
| 1h | 14 | 20/50 | 20/2.0 | 14 | 14 |
| 4h | 14 | 20/50 | 20/2.5 | 14 | 14 |
| 1d | 14-21 | 50/200 | 20/2.5 | 14 | 14 |

**General rule**: Shorter timeframes need shorter indicator periods to remain responsive. Longer timeframes benefit from wider volatility bands (higher BB std, higher SuperTrend multiplier).

### Referencia: references/strategy_patterns.md

# pandas-ta — Strategy Patterns for Crypto Trading

Pre-built indicator combinations for common crypto trading styles, with ta.Strategy definitions and signal generation logic.

## Scalping Strategy (1m-5m Timeframes)

Fast indicators tuned for rapid entries and exits on volatile crypto pairs.

### Indicator Set
```python
import pandas_ta as ta

scalp_strategy = ta.Strategy(
    name="Crypto Scalp",
    ta=[
        {"kind": "ema", "length": 9},
        {"kind": "ema", "length": 21},
        {"kind": "rsi", "length": 7},
        {"kind": "stoch", "k": 5, "d": 3, "smooth_k": 3},
        {"kind": "atr", "length": 7},
        {"kind": "obv"},
    ]
)
df.ta.strategy(scalp_strategy)
```

### Signal Logic
```python
# Buy: EMA9 > EMA21, RSI recovering from <30, Stoch %K crossing above %D
buy = (
    (df["EMA_9"] > df["EMA_21"]) &
    (df["RSI_7"] > 30) & (df["RSI_7"].shift(1) <= 30) &
    (df["STOCHk_5_3_3"] > df["STOCHd_5_3_3"])
)

# Stop loss: 1.5x ATR below entry
stop_distance = df["ATRr_7"] * 1.5

# Exit: EMA9 crosses below EMA21 or RSI > 75
exit_signal = (df["EMA_9"] < df["EMA_21"]) | (df["RSI_7"] > 75)
```

### Notes
- Hold time: seconds to minutes
- Best for: high-volume pairs (SOL/USDC, major memecoins with volume)
- Risk: high false signal rate — combine with order flow or L2 data

## Day Trading Strategy (15m-1h Timeframes)

Balanced indicator set for intraday position management.

### Indicator Set
```python
day_strategy = ta.Strategy(
    name="Crypto Day Trade",
    ta=[
        {"kind": "ema", "length": 20},
        {"kind": "ema", "length": 50},
        {"kind": "macd", "fast": 12, "slow": 26, "signal": 9},
        {"kind": "rsi", "length": 14},
        {"kind": "bbands", "length": 20, "std": 2.0},
        {"kind": "atr", "length": 14},
        {"kind": "vwap"},
        {"kind": "obv"},
    ]
)
df.ta.strategy(day_strategy)
```

### Signal Logic
```python
# Buy: Price above VWAP, EMA20 > EMA50, MACD histogram positive, RSI 40-65
buy = (
    (df["close"] > df["VWAP_D"]) &
    (df["EMA_20"] > df["EMA_50"]) &
    (df["MACDh_12_26_9"] > 0) &
    (df["RSI_14"].between(40, 65))
)

# Take profit: Price touches upper Bollinger Band or RSI > 70
take_profit = (df["close"] >= df["BBU_20_2.0"]) | (df["RSI_14"] > 70)

# Stop loss: 2x ATR below entry or price below lower BB
stop_loss = (df["close"] < df["BBL_20_2.0"])
```

### Notes
- Hold time: minutes to hours
- Best for: established tokens with consistent volume
- Confirm direction with higher timeframe (4h trend)

## Swing Trading Strategy (4h-1d Timeframes)

Slower indicators for multi-day positions with trend confirmation.

### Indicator Set
```python
swing_strategy = ta.Strategy(
    name="Crypto Swing",
    ta=[
        {"kind": "ema", "length": 50},
        {"kind": "ema", "length": 200},
        {"kind": "supertrend", "length": 10, "multiplier": 3.0},
        {"kind": "rsi", "length": 14},
        {"kind": "adx", "length": 14},
        {"kind": "atr", "length": 14},
        {"kind": "bbands", "length": 20, "std": 2.5},
        {"kind": "macd", "fast": 12, "slow": 26, "signal": 9},
    ]
)
df.ta.strategy(swing_strategy)
```

### Signal Logic
```python
# Buy: EMA50 > EMA200, SuperTrend bullish, ADX > 25, RSI 40-60 (pullback entry)
buy = (
    (df["EMA_50"] > df["EMA_200"]) &
    (df["SUPERTd_10_3.0"] == 1) &
    (df["ADX_14"] > 25) &
    (df["RSI_14"].between(40, 60))
)

# Stop loss: SuperTrend flip or 2.5x ATR
stop_loss = df["SUPERTd_10_3.0"] == -1

# Take profit: RSI > 75 and MACD histogram declining
take_profit = (df["RSI_14"] > 75) & (df["MACDh_12_26_9"] < df["MACDh_12_26_9"].shift(1))
```

### Notes
- Hold time: days to weeks
- Best for: large-cap crypto (SOL, ETH, BTC)
- Use weekly chart for overall trend direction

## PumpFun / Memecoin Scalping (1m-5m)

Ultra-fast indicators for new token launches with extreme volatility.

### Indicator Set
```python
pump_strategy = ta.Strategy(
    name="PumpFun Scalp",
    ta=[
        {"kind": "ema", "length": 5},
        {"kind": "ema", "length": 13},
        {"kind": "rsi", "length": 5},
        {"kind": "atr", "length": 5},
        {"kind": "bbands", "length": 10, "std": 3.0},
    ]
)
df.ta.strategy(pump_strategy)
```

### Signal Logic
```python
# Volume ratio (not a pandas-ta indicator, compute manually)
vol_ratio = df["volume"] / df["volume"].rolling(20).mean()

# Buy: EMA5 > EMA13, RSI recovering (was <25, now >35), volume 3x+ average
buy = (
    (df["EMA_5"] > df["EMA_13"]) &
    (df["RSI_5"] > 35) & (df["RSI_5"].shift(2) < 25) &
    (vol_ratio > 3.0)
)

# Exit: EMA5 < EMA13 or RSI > 85 (take profit) or 2x ATR stop
exit_signal = (df["EMA_5"] < df["EMA_13"]) | (df["RSI_5"] > 85)
```

### Notes
- Hold time: seconds to minutes
- Extremely high risk — most PumpFun tokens go to zero
- Volume data is often unreliable — use as secondary confirmation only
- Always set hard stop-losses; never average down on memecoins

## Multi-Timeframe Analysis Pattern

Combine signals from multiple timeframes for higher confidence entries.

```python
import pandas as pd
import pandas_ta as ta

def analyze_multi_timeframe(
    df_5m: pd.DataFrame,
    df_1h: pd.DataFrame,
    df_4h: pd.DataFrame,
) -> dict:
    """Score alignment across timeframes.

    Args:
        df_5m: 5-minute OHLCV DataFrame
        df_1h: 1-hour OHLCV DataFrame
        df_4h: 4-hour OHLCV DataFrame

    Returns:
        Dictionary with alignment score and per-timeframe signals.
    """
    signals = {}

    # 4h: overall trend direction
    df_4h.ta.supertrend(length=10, multiplier=3.0, append=True)
    df_4h.ta.adx(length=14, append=True)
    trend_bull = (df_4h["SUPERTd_10_3.0"].iloc[-1] == 1)
    trending = (df_4h["ADX_14"].iloc[-1] > 25)
    signals["4h"] = "bullish" if trend_bull and trending else "bearish" if not trend_bull and trending else "neutral"

    # 1h: momentum confirmation
    df_1h.ta.macd(append=True)
    df_1h.ta.rsi(append=True)
    macd_bull = df_1h["MACDh_12_26_9"].iloc[-1] > 0
    rsi_ok = 40 < df_1h["RSI_14"].iloc[-1] < 70
    signals["1h"] = "bullish" if macd_bull and rsi_ok else "bearish" if not macd_bull else "neutral"

    # 5m: entry timing
    df_5m.ta.ema(length=9, append=True)
    df_5m.ta.ema(length=21, append=True)
    df_5m.ta.rsi(length=7, append=True)
    ema_cross = df_5m["EMA_9"].iloc[-1] > df_5m["EMA_21"].iloc[-1]
    rsi_entry = df_5m["RSI_7"].iloc[-1] < 60
    signals["5m"] = "bullish" if ema_cross and rsi_entry else "neutral"

    # Alignment score
    bull_count = sum(1 for v in signals.values() if v == "bullish")
    signals["alignment"] = bull_count / len(signals)
    signals["recommendation"] = "strong" if bull_count == 3 else "moderate" if bull_count == 2 else "weak"

    return signals
```

## Signal Scoring Framework

Convert raw indicator values into a normalized score for comparison.

```python
def score_indicators(df: pd.DataFrame) -> dict:
    """Score current indicator readings on a -100 to +100 scale.

    Positive = bullish bias, negative = bearish bias.
    """
    scores = {}
    last = df.iloc[-1]

    # RSI: 0-30 = bullish (oversold), 70-100 = bearish (overbought)
    if "RSI_14" in df.columns:
        rsi = last["RSI_14"]
        scores["rsi"] = (50 - rsi) * 2  # 30→+40, 50→0, 70→-40

    # MACD histogram: positive = bullish
    if "MACDh_12_26_9" in df.columns:
        macd_h = last["MACDh_12_26_9"]
        scores["macd"] = min(max(macd_h * 100, -100), 100)

    # BB position: below mid = bullish, above = bearish
    if "BBP_20_2.0" in df.columns:
        bbp = last["BBP_20_2.0"]
        scores["bbands"] = (0.5 - bbp) * 200  # 0→+100, 0.5→0, 1→-100

    # SuperTrend direction
    st_col = [c for c in df.columns if c.startswith("SUPERTd")]
    if st_col:
        scores["supertrend"] = last[st_col[0]] * 50  # +50 or -50

    # Composite
    if scores:
        scores["composite"] = sum(scores.values()) / len(scores)

    return scores
```

## Running Strategies with ta.Strategy

```python
# Run and inspect results
df.ta.strategy(my_strategy)

# All new columns added to df
new_cols = [c for c in df.columns if c not in ["open", "high", "low", "close", "volume"]]
print(f"Added {len(new_cols)} indicator columns: {new_cols}")

# Get the last row summary
summary = df[new_cols].iloc[-1].to_dict()
for name, value in summary.items():
    print(f"  {name}: {value:.4f}" if isinstance(value, float) else f"  {name}: {value}")
```


---

## SKILL: private-placements

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/private-placements` (MIT)
- Cuándo usarla: Analyze private placement and exempt offering compliance under Regulation D, the Investment Company Act fund exclusions, and FINRA private placement rules. Owns the accredited investor definition (Rule 501(a)), the '506(b) vs 506(c)' distinction, 'general solicitation' analysis, 'Form D' filing mechanics, the 'qualified purchaser' standard for 3(c)(7) funds, bad-actor disqualification, integration, and Rule 144 resale restrictions. Use when the user asks 'can my client invest in this private fund', whether an investor is an 'accredited investor' or qualified purchaser, how to verify accredited status in a 'Reg D offering', 506(c) verification steps, FINRA 5122/5123 filing obligations, or the Reg BI/fiduciary overlay when recommending private placements. Also trigger on 'exempt offering', 'private fund exemption', '3(c)(1) vs 3(c)(7)', or 'restricted securities holding period'.

# Private Placements and Exempt Offerings

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### The Registration Baseline and the Exemption Architecture
Securities Act §5 prohibits offering or selling a security without an effective registration statement. Every private placement rests on an exemption from that requirement. The statutory exemption is §4(a)(2) — "transactions by an issuer not involving any public offering" — a facts-and-circumstances standard shaped by *SEC v. Ralston Purina* (investors must be able to "fend for themselves"). Because §4(a)(2) alone is uncertain, most issuers rely on Regulation D (17 CFR 230.500-508), a non-exclusive safe harbor. Losing the safe harbor does not automatically mean a §5 violation, but the issuer must then defend the offering under raw §4(a)(2), a materially weaker position. State blue-sky registration is preempted for Rule 506 offerings because they are "covered securities" under Securities Act §18(b)(4)(F), though states retain notice-filing and antifraud authority.

### Rule 506(b) — The Traditional Private Placement (17 CFR 230.506(b))
- **No general solicitation or general advertising** (Rule 502(c)). The issuer (and anyone acting on its behalf, including a placement agent) must have a pre-existing, substantive relationship with offerees, or use another means that does not constitute general solicitation.
- **Unlimited accredited investors** plus up to **35 non-accredited purchasers** (per offering, counted under Rule 501(e)), each of whom must be "sophisticated" — alone or with a purchaser representative, capable of evaluating the merits and risks (Rule 506(b)(2)(ii)).
- **If any non-accredited investor purchases**, the issuer must furnish the disclosure specified in Rule 502(b) — financial statements and information comparable to a registered offering — which is why most 506(b) offerings in practice are accredited-only.
- **Self-certification is acceptable**: the issuer needs a reasonable belief that investors are accredited (Rule 501(a) preamble), typically documented through an investor questionnaire. No verification procedures are mandated.

### Rule 506(c) — General Solicitation with Verification (17 CFR 230.506(c))
Added by the JOBS Act (2012, effective September 2013):
- **General solicitation is permitted** — public websites, mass email, advertising, demo days.
- **All purchasers must be accredited**, and the issuer must take **reasonable steps to verify** accredited status. Self-certification alone is not sufficient. The verification requirement is a separate condition — an issuer can fail 506(c) even if every purchaser was in fact accredited.
- **Non-exclusive verification methods** (Rule 506(c)(2)(ii)): review of tax forms (W-2, 1099, K-1) for the two most recent years plus a written representation for the current year (income test); review of bank/brokerage statements and a credit report within the prior three months plus a liabilities representation (net worth test); written confirmation from a registered broker-dealer, SEC-registered investment adviser, licensed attorney, or CPA who has verified status within the prior three months.
- **Minimum-investment-based verification (SEC staff no-action guidance, March 2025)**: an issuer may reasonably rely on high minimum investment amounts (at least $200,000 for natural persons, $1,000,000 for entities) combined with written representations of accredited status and that the investment is not financed by third parties, absent contrary knowledge. Where those conditions are not met, apply the principles-based standard: the reasonableness of steps depends on the nature of the purchaser, the information the issuer has, and the terms of the offering (minimum investment, manner of solicitation).
- An offering that begins under 506(b) may convert to 506(c) prospectively (SEC C&DI 256.34), but not the reverse — once general solicitation has occurred, 506(b) is unavailable for that offering.

### Accredited Investor — Rule 501(a) (17 CFR 230.501(a))
Natural persons qualify by:
- **Income**: individual income over $200,000, or joint income with a spouse or spousal equivalent over $300,000, in each of the two most recent years with a reasonable expectation of the same in the current year (Rule 501(a)(6)).
- **Net worth**: over $1,000,000, individually or jointly, **excluding the primary residence** (and excluding mortgage debt up to the home's value; underwater mortgage excess counts as a liability) (Rule 501(a)(5), as amended by Dodd-Frank §413(a)).
- **Professional certifications** (2020 amendments, effective December 2020): holders in good standing of FINRA Series 7, Series 65, or Series 82 licenses (Rule 501(a)(10) and the SEC's designating order).
- **Knowledgeable employees** of a private fund, for investments in that fund (Rule 501(a)(11), cross-referencing Investment Company Act Rule 3c-5).

Entities qualify as, among others: entities with over $5 million in assets not formed for the specific purpose of the investment (Rule 501(a)(3)); SEC- and state-registered investment advisers and exempt reporting advisers (Rule 501(a)(1)); any entity owning over $5 million in "investments" as defined in ICA Rule 2a51-1 (Rule 501(a)(9), a 2020 catch-all covering Indian tribes, governmental bodies, and foreign entities); family offices with over $5 million under management and their family clients (Rule 501(a)(12)-(13)); and entities all of whose equity owners are accredited (Rule 501(a)(8), look-through).

**Time anchoring**: the $200,000/$300,000 income and $1,000,000 net worth thresholds are fixed in Rule 501(a) and are **not inflation-indexed** — they have been unchanged since 1982 (income) and since the 2010 Dodd-Frank primary-residence exclusion (net worth). Dodd-Frank §413(b) requires the SEC to review the accredited investor definition at least every four years; reviews have so far left the dollar tests unchanged, but pending rulemaking could change them — verify before advising.

### Qualified Purchaser and the Fund Exclusions — ICA §3(c)(1) vs §3(c)(7)
Private funds avoid Investment Company Act registration through one of two exclusions from the §3(a) "investment company" definition:
- **§3(c)(1)**: no more than **100 beneficial owners** of the fund's outstanding securities and no public offering. A **qualifying venture capital fund** — one with no more than $12 million in aggregate capital contributions and uncalled commitments (as adjusted; originally $10 million under the Economic Growth Act of 2018, raised by SEC inflation adjustment effective 2024) — may have up to **250 beneficial owners** (§3(c)(1)(C)).
- **§3(c)(7)**: no beneficial-owner limit (in practice capped at 1,999 holders of record to avoid Exchange Act §12(g) registration), but every owner must be a **qualified purchaser** at the time of acquisition.
- **Qualified purchaser** (ICA §2(a)(51)(A)): a natural person owning at least **$5,000,000 in "investments"** (as defined in Rule 2a51-1 — securities, real estate held for investment, commodity interests, cash held for investment; not the primary residence or a personally used asset); a family-owned company with $5 million in investments; a trust meeting specified conditions; or any person owning and investing at least $25 million in investments for its own account or others. The $5 million threshold is **not inflation-indexed** — anchored as of 2026, unchanged since the 1996 statute.
- A fund cannot mix regimes for one vehicle: a §3(c)(1) fund may admit accredited-but-not-qualified purchasers; a §3(c)(7) fund may not, ever. Look-through rules apply when an entity formed for the purpose of investing, or a §3(c)(1)/§3(c)(7) fund owning 10%+ of a §3(c)(1) fund's voting securities, invests (§3(c)(1)(A)).

### The Three-Tier Confusion: Accredited vs Qualified Client vs Qualified Purchaser
Advisers routinely conflate three distinct tests that serve three distinct statutes:
1. **Accredited investor** (Securities Act Rule 501(a)) — who may buy in a Reg D offering. $200K/$300K income or $1M net worth ex-residence; not indexed.
2. **Qualified client** (Advisers Act Rule 205-3) — to whom a registered adviser may charge performance fees under §205(a)(1). This threshold **is** inflation-adjusted by SEC order every five years; as of the 2026 anchor it sits above the accredited tests ($1.1M assets under management with the adviser or $2.2M net worth, per the 2021 order, with the next adjustment due 2026). See the **fee-billing** skill for the authoritative current figures and adjustment mechanics.
3. **Qualified purchaser** (ICA §2(a)(51)) — who may own a §3(c)(7) fund. $5M in investments; not indexed.

An investor can be accredited but neither a qualified client nor a qualified purchaser. A 3(c)(1) fund charging carried interest must confirm investors are qualified clients (if the manager is an SEC-registered adviser); a 3(c)(7) fund needs qualified purchasers, full stop.

### Form D, Bad Actors, Integration, and Resales
- **Form D** (Rule 503): the issuer must file a notice on Form D with the SEC via EDGAR no later than **15 calendar days after the first sale** of securities in the offering, and amend annually for continuous offerings and upon material changes (Rule 503(a)(3)). Filing is not a condition of the 506 exemption itself, but Rule 507 disqualifies future Reg D reliance for issuers enjoined for Rule 503 violations, and states expect parallel notice filings.
- **Bad-actor disqualification** (Rule 506(d)): the exemption is unavailable if the issuer or a "covered person" (directors, executive officers, 20% beneficial owners, promoters, placement agents and their covered personnel) has a disqualifying event — criminal convictions, SEC or state regulatory orders, FINRA suspension/bar — occurring after September 23, 2013. Pre-existing events must instead be disclosed under Rule 506(e). The issuer must exercise reasonable care (factual inquiry, questionnaires) to establish the absence of disqualifying events.
- **Integration** (Rule 152, restructured March 2021): two offerings are not integrated if, based on facts and circumstances, each independently complies with an exemption; four safe harbors apply, including offerings more than **30 days apart** (Rule 152(b)(1), subject to the general-solicitation carve-outs) and a completed 506(b) offering followed by a 506(c) offering. The old five-factor test and six-month rule are superseded.
- **Resale restrictions**: Reg D securities are "restricted securities" (Rule 144(a)(3)). Purchasers must buy for investment, not distribution; resales rely on Rule 144 — a **six-month holding period** for issuers subject to Exchange Act reporting, **one year** for non-reporting issuers (Rule 144(d)), with additional current-information, volume, and manner-of-sale conditions for affiliates — or on §4(a)(7)/the so-called "§4(a)(1-1/2)" doctrine for private resales to accredited investors.

### FINRA Filing Requirements and the Recommendation Overlay
- **FINRA Rule 5123**: a member selling a private placement to retail investors must file the offering documents (PPM, term sheet) with FINRA's Corporate Financing Department **within 15 calendar days of the first sale**, or indicate no offering documents were used. Exemptions cover sales solely to institutional accounts, qualified purchasers, and other listed categories (Rule 5123(b)).
- **FINRA Rule 5122**: member private offerings (a BD selling its own or a control entity's securities) require that at least 85% of proceeds be used for the disclosed business purposes and that the PPM be filed at or before first use.
- **Reg BI / fiduciary overlay**: recommending a private placement to a retail customer triggers the Reg BI Care Obligation (17 CFR 240.15l-1(a)(2)(ii)) for BDs and the Advisers Act §206 fiduciary duty for RIAs. Heightened factors: illiquidity against the client's liquidity needs and time horizon, concentration relative to net worth (many firms cap alternatives at 10-20% of liquid net worth), fee opacity (management fee plus carry plus fund expenses plus placement fees), stale or manager-marked valuations, limited transparency, and reasonable-basis diligence on the issuer (FINRA Regulatory Notice 10-22 requires independent investigation of the issuer and offering, not reliance on the PPM alone). Eligibility (accredited status) is the floor, not the analysis — an accredited investor can still receive an unsuitable or not-in-best-interest recommendation.
- **AML**: private funds and their placement agents face customer due diligence and beneficial-ownership expectations; FinCEN's investment adviser AML program rule (effective January 1, 2026, compliance date subject to FinCEN's 2025 postponement proposal — verify status) brings SEC-registered and exempt reporting advisers into the BSA regime. See the anti-money-laundering skill.

## Worked Examples

### Example 1: RIA Recommends a 506(b) Fund to a Non-Accredited Client
**Scenario:** An RIA recommends a $150,000 investment in a private real estate fund offered under Rule 506(b) to a client with $160,000 individual income (spouse not employed), a $700,000 net worth excluding her primary residence, and no purchaser representative. The client signs the fund's subscription agreement self-certifying accredited status; the adviser, who knows her full financial picture, does not correct it.

**Compliance Issues:**
- The client fails every Rule 501(a) natural-person test: income under $200,000 individual / $300,000 joint (Rule 501(a)(6)), net worth under $1,000,000 excluding the primary residence (Rule 501(a)(5)), and no Series 7/65/82 license (Rule 501(a)(10)).
- The issuer's "reasonable belief" of accredited status is undermined if the adviser channels contradicting information; while a 506(b) issuer may accept self-certification, a certification known to be false by the intermediary who procured it does not support reasonable belief.
- The client could still purchase as one of up to 35 non-accredited investors under Rule 506(b)(2)(ii), but only if sophisticated and only if the issuer furnishes Rule 502(b) disclosure — which this accredited-only offering does not provide.
- The adviser's fiduciary duty under Advisers Act §206(1)-(2) is independently violated: facilitating a false certification and recommending an investment the client is not eligible to make is a breach of the duty of care, and the concentration ($150,000 against $700,000 net worth, over 20% in one illiquid position) compounds it.

**Analysis:** The adviser must withdraw the recommendation and inform the issuer of the eligibility failure before closing. If the sale closed, the investor likely holds rescission rights, and the issuer's exemption for the entire offering is at risk if the non-accredited sale occurred without Rule 502(b) disclosure and a sophistication determination. For the adviser, this is a §206 exam finding and potentially a fraud referral — a fiduciary cannot cure ineligibility with a signature. The correct practice: the adviser screens Rule 501(a) status against known client financials before presenting any Reg D opportunity, documents the basis (accreditation category and figures), and treats eligibility as a gate before the separate best-interest analysis of concentration, liquidity, and fees.

### Example 2: General Solicitation Contamination in a 506(b) Offering
**Scenario:** A startup begins a 506(b) raise through a placement-agent BD. Midway, the founder gives a podcast interview describing the "open funding round" and posts terms on LinkedIn. Sixty investors sign up through the resulting inbound interest, all self-certifying as accredited. The BD proposes to "switch the paperwork to 506(c)" and close everyone.

**Compliance Issues:**
- The podcast and LinkedIn posts are general solicitation under Rule 502(c), destroying 506(b) for this offering. There is no pre-existing substantive relationship with the inbound investors.
- The offering may convert to 506(c) prospectively (SEC C&DI 256.34), but 506(c) requires **reasonable steps to verify** accreditation under Rule 506(c)(2) for all purchasers who buy after conversion — self-certification is insufficient. Investors sourced through the solicitation cannot close on questionnaires alone.
- Verification options: tax documents or account statements per the Rule 506(c)(2)(ii) non-exclusive methods, third-party verification letters from a BD/RIA/attorney/CPA, or — if minimums are at least $200,000 per natural person with the required representations and no financing red flags — reliance on the March 2025 SEC staff minimum-investment guidance.
- Sales completed before the solicitation under valid 506(b) conditions can stand; Rule 152's integration framework and the 506(b)-then-506(c) safe harbor support treating the phases separately, but the issuer must file/amend Form D (Rule 503) to reflect the 506(c) claim.
- The BD's obligations: FINRA Rule 5123 filing within 15 days of first retail sale, reasonable-basis diligence under Regulatory Notice 10-22, and Rule 506(d) bad-actor certification sweep covering itself as compensated solicitor.

**Analysis:** The cure is conversion, not relabeling. The issuer amends Form D to check 506(c), implements documented verification for every post-solicitation purchaser, and papers the file showing which sales predated contamination. If any post-solicitation investor turns out non-accredited, 506(c) fails for the offering (all purchasers must be accredited) and the fallback is naked §4(a)(2) — indefensible after a podcast. The BD should refuse to close unverified subscriptions; closing them exposes it to §5 aiding liability and FINRA sales-practice charges.

### Example 3: Qualified-Purchaser Gap in a 3(c)(7) Fund
**Scenario:** A hedge fund relying on ICA §3(c)(7) admits an investor introduced by an advisory firm. The investor is comfortably accredited — $2.5M net worth excluding residence, $400K income — and is a qualified client under Advisers Act Rule 205-3 (as adjusted, anchored 2026). The subscription documents' qualified-purchaser representation was checked by the investor without review. Her actual "investments" under ICA Rule 2a51-1 total $3.1M (the balance of her net worth is her vacation home used personally and a business she operates).

**Compliance Issues:**
- She is not a qualified purchaser: ICA §2(a)(51)(A)(i) requires $5,000,000 in "investments," and Rule 2a51-1 excludes personal-use real estate and an operating business she controls (unless held for investment). $3.1M fails the test. Accredited status and qualified-client status are irrelevant to §3(c)(7) — this is the three-tier confusion in action.
- Admitting a non-qualified purchaser means the fund has a beneficial owner outside §3(c)(7), jeopardizing the exclusion; without it the fund is an unregistered investment company, contaminating its performance-fee arrangements and contracts (ICA §47(b) makes contracts of an unregistered investment company potentially unenforceable/rescindable).
- The fund cannot patch this by pointing to §3(c)(1) — a single vehicle relies on one exclusion, and a §3(c)(7) fund's offering documents, ERISA representations, and other investors' expectations are built on the qualified-purchaser-only structure.
- The adviser who introduced her had the data showing $3.1M in investments and breached its Advisers Act §206 duty of care by letting a false representation through; the fund's manager had a reasonable-belief obligation at acquisition and relied on an unexamined checkbox.

**Analysis:** The fund should rescind the subscription promptly and refund capital, documenting that the investor was never accepted as within §3(c)(7) — prompt rescission upon discovery is the standard remediation and supports the position that the exclusion was not lost. Going forward: the subscription process must collect the components of the "investments" calculation (not a bare representation), the manager should apply Rule 2a51-1 categories explicitly, and introducing advisers must be instructed that the screen is $5M in *investments*, not net worth. If the manager wants to serve accredited-but-not-QP clients, the answer is a parallel §3(c)(1) vehicle (100 owners; 250 if a qualifying venture capital fund within the ~$12M cap as adjusted) with qualified-client confirmation before charging carry.

## Common Pitfalls
- Treating accredited investor, qualified client, and qualified purchaser as interchangeable — they gate different statutes (Reg D eligibility, performance fees, 3(c)(7) ownership) at very different dollar levels
- Assuming the accredited-investor dollar tests adjust for inflation — the $200K/$300K/$1M figures in Rule 501(a) are fixed (unchanged since 1982/2010); only the qualified-client thresholds under Rule 205-3 are inflation-adjusted (every five years)
- Counting the primary residence in net worth for Rule 501(a)(5), or counting personal-use assets as "investments" under ICA Rule 2a51-1
- Relying on self-certification in a 506(c) offering — reasonable-steps verification is a separate condition of the exemption, failable even when every purchaser is in fact accredited
- Any public statement about an active 506(b) raise — press, podcasts, social media, demo days without Rule 148 protections — is general solicitation that forfeits 506(b) for the offering
- Treating Form D as a condition of the exemption (it is not) or ignoring it (Rule 507 disqualification risk and state notice-filing exposure both attach)
- Skipping bad-actor diligence on placement agents and 20% owners — Rule 506(d) reaches covered persons beyond the issuer itself
- Applying the pre-2021 five-factor integration test or six-month rule instead of the current Rule 152 framework
- Forgetting resale restrictions — clients expecting liquidity face Rule 144's six-month/one-year holding periods and, for fund interests, transfer consent provisions
- BDs missing the FINRA Rule 5123 filing (15 days from first retail sale) or relying on the issuer's PPM instead of independent diligence (Regulatory Notice 10-22)
- Treating eligibility as the end of the analysis — an accredited client can still fail the Reg BI Care Obligation or fiduciary best-interest test on concentration, liquidity, fee, and valuation grounds
- Letting a 3(c)(7) fund accept an accredited-but-not-QP investor, or letting a 3(c)(1) fund drift past 100 beneficial owners without applying the look-through rules

## Cross-References
- **investment-suitability** (compliance plugin): heightened suitability and due-diligence expectations for private placements and alternatives under FINRA Rule 2111 and Notice 10-22
- **reg-bi** (compliance plugin): the Care Obligation analysis that applies when a BD recommends a private placement to a retail customer
- **advertising-compliance** (compliance plugin): what constitutes general solicitation and how 506(c) marketing materials must be treated
- **advice-standards** (compliance plugin): adviser registration and exempt reporting adviser status for private fund managers
- **client-disclosures** (compliance plugin): PPM delivery, Rule 502(b) disclosure to non-accredited investors, and conflict disclosures around placement compensation
- **alternatives** (wealth-management plugin): the investment-merits side of private funds — strategies, fees, liquidity terms, and portfolio fit
- **anti-money-laundering** (compliance plugin): AML program and beneficial-ownership considerations for private funds, placement agents, and advisers


---

## SKILL: rl-execution

- Fuente: `agiprolabs/claude-trading-skills` → `skills/rl-execution` (MIT)
- Cuándo usarla: Reinforcement learning for trade execution optimization including order splitting, adaptive timing, and impact minimization
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/rl-execution/` (almgren_chriss.py, execution_simulator.py)

# RL Execution Optimization

Reinforcement learning (RL) for trade execution teaches an agent to split and
time large orders so that total market impact is minimized. Instead of following
a fixed schedule (TWAP, VWAP), an RL agent observes real-time market state and
adapts its trading rate on the fly.

## Why Execution Optimization Matters

Every trade has a cost beyond the quoted spread:

| Cost Component | Cause | Typical Magnitude |
|---|---|---|
| Spread cost | Crossing the bid-ask | 5-50 bps on DEXs |
| Temporary impact | Consuming liquidity | Scales with trade rate |
| Permanent impact | Information leakage | Scales with total size |
| Timing risk | Price drifts while waiting | Scales with volatility and time |

A 100 SOL market buy on a thin pool can move the price 2-5%. Splitting it into
ten 10 SOL slices over a few minutes can cut that cost by 30-60%. The question
is **how** to split optimally — and that is where execution algorithms and RL
come in.

## The RL Framework for Execution

### State Space

The agent observes at each decision step:

```
state = [
    remaining_qty,    # How much is left to trade (0-1 normalized)
    time_remaining,   # Fraction of allowed horizon remaining
    current_price,    # Current mid-price (normalized to arrival price)
    spread,           # Current bid-ask spread
    volatility,       # Recent realized volatility
    volume,           # Recent trading volume (normalized)
]
```

### Action Space

Discrete actions controlling how much to trade this step:

```
actions = [0%, 10%, 25%, 50%, 100%]  # of remaining quantity
```

A small action space keeps the problem tractable. Each action represents the
fraction of the remaining order to execute in the current time step.

### Reward Function

The reward penalizes execution cost relative to a benchmark:

```
reward = -(execution_price - arrival_price) * quantity_traded
```

Summed over all steps, the total reward equals the negative implementation
shortfall. The agent learns to minimize total cost.

### Episode Structure

One episode = one order from placement to completion:

1. Agent receives order: buy/sell Q units within T time steps
2. At each step, agent picks an action (trade amount)
3. Market simulator applies price impact and updates state
4. Episode ends when quantity is fully executed or time expires
5. Any remaining quantity at expiry is executed at market (penalty)

## Standard Execution Algorithms

### TWAP (Time-Weighted Average Price)

The simplest baseline — split the order equally across all time steps:

```python
trade_per_step = total_quantity / num_steps
```

**Pros**: Simple, deterministic, easy to implement.
**Cons**: Ignores market conditions entirely.

### VWAP (Volume-Weighted Average Price)

Split proportional to expected volume in each period:

```python
trade_at_step_t = total_quantity * (expected_volume[t] / total_expected_volume)
```

**Pros**: Trades more when liquidity is available.
**Cons**: Requires accurate volume forecasts; still non-adaptive.

### Almgren-Chriss Optimal Execution

The foundational analytical model. Minimizes a combination of execution cost
and timing risk:

```
minimize: E[cost] + λ * Var[cost]
```

With linear impact assumptions, this yields a closed-form optimal trajectory.
See `references/execution_algorithms.md` for the full derivation.

### RL-Based Adaptive Execution

An RL agent (DQN, PPO, or similar) that learns the execution policy from
simulated experience:

```python
# Pseudocode training loop
for episode in range(num_episodes):
    state = env.reset(order_qty=Q, horizon=T)
    done = False
    while not done:
        action = agent.select_action(state)
        next_state, reward, done, info = env.step(action)
        agent.store_transition(state, action, reward, next_state, done)
        agent.update()
        state = next_state
```

**Pros**: Adapts to current market conditions, can learn non-linear patterns.
**Cons**: Requires realistic simulator, sim-to-real gap, training instability.

## Price Impact Model

The simulator uses a standard two-component impact model:

```
temporary_impact = η * (trade_rate / avg_volume)
permanent_impact = γ * (trade_rate / avg_volume)
```

- **Temporary impact** decays after the trade (liquidity replenishes)
- **Permanent impact** shifts the equilibrium price (information effect)

The execution price for a trade of size `q` at time `t`:

```
exec_price = mid_price + permanent_impact + temporary_impact
mid_price_next = mid_price + permanent_impact + noise
```

## When to Use This Skill

This skill is most valuable when:

- **Order size is large relative to available liquidity** (>1% of daily volume)
- **Market impact is significant** (thin DEX pools, low-cap tokens)
- **Execution window is flexible** (minutes to hours, not milliseconds)
- **Cost savings justify complexity** (institutional-scale orders)

For small retail orders (<$1,000 on liquid pairs), simple market orders or
basic slippage limits are sufficient. See the `slippage-modeling` skill instead.

## Practical Limitations

1. **Sim-to-real gap**: Simulated markets do not capture all real dynamics
   (queue position, adversarial flow, MEV).
2. **Non-stationarity**: Market microstructure changes over time; models
   trained on one regime may fail in another.
3. **DEX specifics**: On-chain execution has block-level granularity (~400ms
   on Solana), not continuous-time. Gas/priority fees add cost.
4. **Data requirements**: Training requires historical orderbook or trade data
   for realistic simulation.

## Integration with Other Skills

| Skill | Integration |
|---|---|
| `slippage-modeling` | Provides impact estimates to calibrate the simulator |
| `position-sizing` | Determines the total order size to execute |
| `liquidity-analysis` | Assesses available liquidity for realistic simulation |
| `volatility-modeling` | Supplies volatility estimates for the state vector |
| `jupiter-swap` | Actual on-chain execution of the computed trade schedule |

## Quick Start

### Compare Execution Strategies (No API Needed)

```bash
python scripts/execution_simulator.py
```

Runs TWAP, VWAP, and adaptive strategies in a simulated market and compares
execution costs across many trials.

### Almgren-Chriss Optimal Trajectory

```bash
python scripts/almgren_chriss.py
```

Computes the analytically optimal execution trajectory and compares it to
TWAP for a given set of market parameters.

## Files

### References
- `references/execution_algorithms.md` — TWAP, VWAP, Almgren-Chriss, IS, and
  RL execution algorithms with formulas and comparison
- `references/rl_framework.md` — MDP formulation, environment design, training
  methodology, and practical considerations for RL execution

### Scripts
- `scripts/execution_simulator.py` — Simulated order execution comparing TWAP,
  VWAP, and adaptive strategies with price impact
- `scripts/almgren_chriss.py` — Almgren-Chriss optimal execution model with
  trajectory computation and cost analysis

## Dependencies

```bash
uv pip install numpy
```

No API keys required — all scripts run in simulation/demo mode.

## Further Reading

- Almgren, R. & Chriss, N. (2001). "Optimal execution of portfolio transactions."
  *Journal of Risk*, 3(2), 5-39.
- Bertsimas, D. & Lo, A. (1998). "Optimal control of execution costs."
  *Journal of Financial Markets*, 1(1), 1-50.
- Ning, B., Lin, F. H. T., & Jaimungal, S. (2021). "Double deep Q-learning
  for optimal execution." *Applied Mathematical Finance*, 28(4), 361-380.

## Disclaimer

This skill provides educational analysis tools for studying execution
algorithms. It does not constitute financial advice. Simulated results do
not guarantee real-world performance. Always test execution strategies
with small sizes before scaling up.

### Referencia: references/execution_algorithms.md

# Execution Algorithms Reference

## Overview

Execution algorithms determine how to split a large order across time to
minimize total trading cost. This reference covers the major approaches from
simplest to most sophisticated.

## TWAP — Time-Weighted Average Price

**Idea**: Trade equal amounts at equal time intervals.

**Formula**:

```
q_t = Q / N    for all t = 1, ..., N
```

Where `Q` = total quantity, `N` = number of time steps.

**Properties**:
- Zero information requirement — no forecasts needed
- Deterministic schedule — fully predictable
- Baseline benchmark for all other algorithms
- Suboptimal when volume or volatility varies over time

**Best for**: Orders where simplicity and predictability outweigh optimization.

## VWAP — Volume-Weighted Average Price

**Idea**: Trade proportional to expected volume in each period.

**Formula**:

```
q_t = Q * (V_t / sum(V_1..V_N))
```

Where `V_t` = expected volume at step `t`.

**Volume profile estimation**:
- Historical average volume by time-of-day (most common)
- Exponential moving average of recent volume patterns
- Intraday volume U-shape: higher at open/close, lower midday

**Properties**:
- Trades more when liquidity is naturally higher
- Reduces temporary impact vs TWAP
- Requires volume forecasting (forecast error adds risk)
- Does not adapt to real-time conditions

**Best for**: Medium-sized orders where volume patterns are stable.

## Almgren-Chriss Optimal Execution

**Idea**: Minimize expected cost + risk penalty with linear impact assumptions.

### Model Setup

- Total quantity to sell: `Q` shares
- Time horizon: `T`, divided into `N` steps of length `τ = T/N`
- Trading trajectory: `x_0 = Q, x_1, ..., x_N = 0`
- Trade at step `k`: `n_k = x_{k-1} - x_k` (units sold)
- Trade rate: `v_k = n_k / τ`

### Impact Model

**Temporary impact** (per-trade cost, decays immediately):

```
h(v) = ε * sign(v) + η * v
```

- `ε` = fixed cost per trade (half-spread)
- `η` = temporary impact coefficient

**Permanent impact** (shifts equilibrium price):

```
g(v) = γ * v
```

- `γ` = permanent impact coefficient

### Objective Function

```
minimize: E[cost(x)] + λ * Var[cost(x)]
```

Where `λ` is the risk-aversion parameter:
- `λ = 0`: minimize expected cost only (patient trader)
- `λ → ∞`: execute immediately (urgent trader)

### Expected Cost

```
E[cost] = 0.5 * γ * Q² + ε * Σ|n_k| + η * Σ(n_k² / τ)
```

Components:
1. Permanent impact cost: `0.5 * γ * Q²` (unavoidable)
2. Fixed transaction cost: `ε * Σ|n_k|`
3. Temporary impact cost: `η * Σ(n_k² / τ)` (minimized by spreading trades)

### Variance of Cost

```
Var[cost] = σ² * τ * Σ x_k²
```

Where `σ` = price volatility. Holding inventory exposes us to price risk.

### Optimal Solution

For the linear impact model, the optimal trajectory is:

```
x_k = Q * sinh(κ * (N - k)) / sinh(κ * N)
```

Where:

```
κ = arccosh((τ² * λ * σ² / (2 * η)) + 1)
```

The parameter `κ` controls the aggressiveness:
- Small `κ` (low risk aversion): trade slowly, close to TWAP
- Large `κ` (high risk aversion): front-load trades, execute quickly

### Cost Components

| Component | Formula | Nature |
|---|---|---|
| Permanent impact | `0.5 * γ * Q²` | Fixed, unavoidable |
| Temporary impact | `η * Σ(n_k²/τ)` | Decreases with more spreading |
| Timing risk | `λ * σ² * τ * Σ x_k²` | Increases with more spreading |

The optimal solution balances temporary impact (favors slow execution) against
timing risk (favors fast execution).

## IS — Implementation Shortfall

**Idea**: Minimize slippage from the decision price (price when order is placed).

**Formula**:

```
IS = (execution_price - decision_price) * quantity
```

**Implementation**:
- Set a benchmark at order arrival
- Dynamically adjust trade rate based on how far price has moved
- Trade faster if price is moving against you (adverse selection)
- Trade slower if price is favorable

**Properties**:
- Directly targets the metric traders care about
- Naturally adapts to price movements
- More complex than TWAP/VWAP to implement
- Sensitive to the benchmark price choice

## RL-Based Execution

**Idea**: Learn the optimal execution policy from simulated experience using
reinforcement learning (DQN, PPO, or actor-critic methods).

### Architecture

```
State → Neural Network → Action (trade size)
         ↑ trained via
    Experience Replay
```

### DQN Approach

- Q-network maps state → Q-values for each discrete action
- Actions: {0%, 10%, 25%, 50%, 100%} of remaining quantity
- Train with experience replay and target network
- Epsilon-greedy exploration during training

### PPO Approach

- Policy network outputs action probabilities
- Value network estimates expected return
- Train with clipped surrogate objective
- More stable than DQN for continuous-like problems

### Advantages Over Classical Methods

- Can learn non-linear impact relationships
- Adapts to current market conditions in real time
- Can incorporate rich state features (orderbook shape, etc.)
- No need for closed-form solutions

### Disadvantages

- Requires realistic market simulator for training
- Sim-to-real gap is a major challenge
- Training can be unstable and sample-inefficient
- Harder to explain/audit than analytical solutions

## Algorithm Comparison

| Algorithm | Adaptivity | Complexity | Data Needs | Best For |
|---|---|---|---|---|
| TWAP | None | Trivial | None | Benchmarking, small orders |
| VWAP | Volume | Low | Volume history | Medium orders, stable markets |
| Almgren-Chriss | None (offline) | Medium | σ, η, γ estimates | Large orders, known parameters |
| IS | Price-reactive | Medium | Real-time price | Urgent orders, adverse selection |
| RL | Full (learned) | High | Simulator + training | Research, institutional scale |

## Choosing an Algorithm

1. **Order < 0.1% daily volume**: Use market order or basic limit order
2. **Order 0.1-1% daily volume**: TWAP or VWAP is sufficient
3. **Order 1-5% daily volume**: Almgren-Chriss or IS recommended
4. **Order > 5% daily volume**: RL or sophisticated adaptive strategies
5. **DEX with thin liquidity**: Even small orders may need execution algorithms

## Parameter Calibration

### Estimating Temporary Impact (η)

```
η ≈ spread / (2 * avg_trade_size)
```

Or fit from historical data: regress realized impact on trade size.

### Estimating Permanent Impact (γ)

```
γ ≈ daily_volatility * sqrt(1 / daily_volume)
```

Typically `γ << η` for liquid assets; `γ ≈ η` for illiquid ones.

### Risk Aversion (λ)

- Conservative (institutional): `λ = 1e-6` to `1e-5`
- Moderate: `λ = 1e-5` to `1e-4`
- Aggressive (retail): `λ = 1e-4` to `1e-3`

Higher `λ` means faster execution and higher impact cost but lower timing risk.

### Referencia: references/rl_framework.md

# RL Framework for Execution Optimization

## MDP Formulation

Execution optimization is modeled as a finite-horizon Markov Decision Process
(MDP) where the agent must fully execute an order within a fixed time window.

### State Space

```python
state = {
    "remaining_qty": float,   # Normalized: 1.0 at start, 0.0 when done
    "time_remaining": float,  # Normalized: 1.0 at start, 0.0 at deadline
    "price_relative": float,  # Current price / arrival price
    "spread": float,          # Current bid-ask spread (normalized)
    "volatility": float,      # Recent realized volatility (rolling window)
    "volume": float,          # Recent volume / average volume
}
```

**Normalization**: All state features are scaled to roughly [0, 1] or [-1, 1]
for stable neural network training.

**Optional extensions**:
- Orderbook imbalance (bid_volume - ask_volume) / total
- Momentum indicator (short-term price change)
- Time-of-day encoding (captures intraday patterns)

### Action Space

Discrete actions keep the problem tractable:

| Action | Meaning | When Useful |
|---|---|---|
| 0 | Trade 0% of remaining | Wait for better conditions |
| 1 | Trade 10% of remaining | Conservative participation |
| 2 | Trade 25% of remaining | Moderate participation |
| 3 | Trade 50% of remaining | Aggressive participation |
| 4 | Trade 100% of remaining | Immediate completion |

**Continuous alternative**: Output a single float in [0, 1] representing
fraction of remaining to trade. Requires actor-critic methods (PPO, SAC).

### Reward Function

**Per-step reward** (implementation shortfall):

```python
reward_t = -(exec_price_t - arrival_price) * qty_traded_t
```

**Terminal penalty** (if order not completed by deadline):

```python
if remaining_qty > 0 at deadline:
    penalty = -remaining_qty * slippage_estimate * penalty_multiplier
```

**Alternative rewards**:
- TWAP-relative: `-(exec_price_t - twap_price_t) * qty_traded_t`
- Risk-adjusted: add variance penalty term
- Shaped: small bonus for maintaining smooth trade rate

### Episode Structure

```
t=0: Order arrives. State = (1.0, 1.0, 1.0, spread, vol, volume)
t=1..N-1: Agent selects actions, environment simulates trades
t=N: Deadline. Force-execute any remaining quantity.
Total reward = sum of per-step rewards + terminal penalty
```

Typical episode: 20-50 time steps representing a 10-minute to 1-hour window.

## Environment Design

### Price Dynamics

Geometric Brownian Motion with impact:

```python
# Per time step
dW = np.random.normal(0, 1)
price_change = mu * dt + sigma * sqrt(dt) * dW
permanent_shift = gamma * trade_rate
temporary_cost = eta * trade_rate

# Update mid-price (permanent impact persists)
mid_price *= (1 + price_change + permanent_shift)

# Execution price (temporary impact is per-trade only)
exec_price = mid_price * (1 + temporary_cost)
```

### Impact Model Parameters

```python
# Calibration from market data
eta = 0.001      # Temporary impact coefficient
gamma = 0.0005   # Permanent impact coefficient
sigma = 0.02     # Volatility (per step)
mu = 0.0         # Drift (typically zero for short horizons)
```

**Square-root impact** (more realistic for large orders):

```python
temporary_impact = eta * sign(v) * sqrt(abs(v) / avg_volume)
permanent_impact = gamma * sign(v) * sqrt(abs(v) / avg_volume)
```

### Volume Dynamics

Simulate realistic intraday volume patterns:

```python
def volume_profile(t: float) -> float:
    """U-shaped intraday volume (higher at open/close)."""
    return 1.0 + 0.5 * (4 * (t - 0.5)**2)
```

### Spread Dynamics

Spread widens with volatility and narrows with volume:

```python
spread = base_spread * (1 + vol_sensitivity * volatility) / (1 + vol_factor * volume)
```

## Training Methodology

### DQN Training

```python
# Hyperparameters
learning_rate = 1e-4
batch_size = 64
replay_buffer_size = 100_000
target_update_freq = 1000
gamma_discount = 0.99
epsilon_start = 1.0
epsilon_end = 0.01
epsilon_decay = 0.995

# Training loop
for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    while not done:
        action = epsilon_greedy(q_network, state, epsilon)
        next_state, reward, done, info = env.step(action)
        replay_buffer.add(state, action, reward, next_state, done)
        if len(replay_buffer) >= batch_size:
            batch = replay_buffer.sample(batch_size)
            loss = update_q_network(batch)
        state = next_state
        total_reward += reward
    epsilon *= epsilon_decay
```

### PPO Training

```python
# Hyperparameters
learning_rate = 3e-4
clip_ratio = 0.2
epochs_per_update = 10
batch_size = 2048
gamma_discount = 0.99
gae_lambda = 0.95

# Collect trajectories, then update
trajectories = collect_rollouts(policy, env, num_steps=batch_size)
advantages = compute_gae(trajectories, value_network, gamma, gae_lambda)
for epoch in range(epochs_per_update):
    update_policy(policy, trajectories, advantages, clip_ratio)
    update_value(value_network, trajectories)
```

### Training Tips

1. **Curriculum learning**: Start with easy orders (small size, long horizon)
   and gradually increase difficulty.
2. **Domain randomization**: Vary impact parameters, volatility, and volume
   across episodes to improve generalization.
3. **Reward normalization**: Normalize rewards by order size for stable training.
4. **Multiple seeds**: Train 3-5 agents with different seeds; ensemble or pick
   the best on a validation set.

## Evaluation

### Metrics

| Metric | Formula | Target |
|---|---|---|
| Implementation Shortfall | `(VWAP_exec - arrival_price) * Q` | Minimize |
| TWAP Improvement | `(cost_TWAP - cost_RL) / cost_TWAP` | Positive |
| Cost Std Dev | `std(cost across episodes)` | Low |
| Completion Rate | `% of episodes fully executed on time` | >99% |

### Benchmark Comparison Protocol

1. Fix a set of 1,000+ test scenarios (same random seeds)
2. Run TWAP, VWAP, Almgren-Chriss, and RL agent on each
3. Compare mean cost, std, 95th percentile, worst case
4. Statistical significance: paired t-test or Wilcoxon signed-rank

### Walk-Forward Validation

- Train on simulated data from period 1
- Validate on simulated data from period 2 (different parameters)
- Test on held-out scenarios with unseen parameter combinations
- Monitor for overfitting to specific simulator dynamics

## Practical Considerations

### Sim-to-Real Gap

The biggest challenge in RL execution. Mitigations:

1. **Realistic simulation**: Calibrate impact model from real trade data
2. **Domain randomization**: Vary parameters widely during training
3. **Conservative deployment**: Start with small orders, blend RL with TWAP
4. **Online adaptation**: Fine-tune the agent on live execution data
5. **Safety constraints**: Hard limits on maximum trade rate per step

### DEX-Specific Considerations

- **Block-level granularity**: Solana blocks are ~400ms; cannot trade faster
- **AMM mechanics**: Impact follows the bonding curve, not a linear model
- **MEV risk**: Sandwich attacks can increase execution cost
- **Gas/priority fees**: Each transaction has a base cost
- **Slippage tolerance**: Must set per-transaction slippage limits

### When RL Execution Is Not Worth It

- Order size < 0.1% of available liquidity
- Execution window is very short (< 1 minute)
- Market is highly liquid with tight spreads
- Regulatory constraints require specific execution algorithms
- Team lacks ML infrastructure for training and monitoring

### Deployment Architecture

```
Market Data Feed → State Encoder → RL Agent → Trade Scheduler → DEX Router
                                      ↑                            ↓
                                  Model Store              Execution Monitor
                                      ↑                            ↓
                                Training Pipeline ← Performance Tracker
```

The agent runs inference at each decision point (every block or every N
seconds), outputting the next trade size. A trade scheduler converts this
to actual transactions via a DEX aggregator.


---

## SKILL: scanner-pmcc

- Fuente: `staskh/trading_skills` → `.claude/skills/scanner-pmcc` (MIT)
- Cuándo usarla: Scan stocks for Poor Man's Covered Call (PMCC) suitability. Analyzes LEAPS and short call options for delta, liquidity, spread, IV, yield, trend direction, and earnings proximity. Use when user asks about PMCC candidates, diagonal spreads, or LEAPS strategies.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/scanner-pmcc/` (scan.py)

# PMCC Scanner

Finds optimal Poor Man's Covered Call setups by scoring symbols on option chain quality.

## What is PMCC?

Buy deep ITM LEAPS call (delta ~0.80) + Sell short-term OTM call (delta ~0.20) against it. Cheaper alternative to covered calls.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/scan.py SYMBOLS [options]
```

## Arguments

- `SYMBOLS` - Comma-separated tickers or path to JSON file from bullish scanner
- `--min-leaps-days` - Minimum LEAPS expiration in days (default: 270 = 9 months)
- `--leaps-delta` - Target LEAPS delta (default: 0.80)
- `--short-delta` - Target short call delta (default: 0.20)
- `--output` - Save results to JSON file (use this; Claude generates the report from the JSON)
- `--report` - Save auto-generated markdown to file (programmatic fallback only — prefer Claude-generated reports)

## Scoring System (max possible: 14, range: -8 to 14)

| Category | Condition | Points |
|----------|-----------|--------|
| **Delta Accuracy** | LEAPS within ±0.05 | +2 |
| | LEAPS within ±0.10 | +1 |
| | Short within ±0.05 | +1 |
| | Short within ±0.10 | +0.5 |
| **Liquidity** | LEAPS vol+OI > 100 | +1 |
| | LEAPS vol+OI > 20 | +0.5 |
| | Short vol+OI > 500 | +1 |
| | Short vol+OI > 100 | +0.5 |
| **Spread** | LEAPS spread < 5% | +1 |
| | LEAPS spread < 10% | +0.5 |
| | Short spread < 10% | +1 |
| | Short spread < 20% | +0.5 |
| **IV Level** | 25-50% (ideal) | +2 |
| | 20-60% | +1 |
| **Yield** | Annual > 50% | +2 |
| | Annual > 30% | +1 |
| | Annual > 15% | +0.5 |
| **Trend** | Price > SMA50 | +1 / -1 |
| | RSI > 50 | +0.5 / -0.5 |
| | MACD > signal | +0.5 / -0.5 |
| **Earnings** | Next earnings > 45 days | +1.0 |
| | Earnings within 45 days | -1.0 |
| | Earnings within short expiry | -2.0 |
| **Weekly Options** | No weekly options listed | -1 |
| **Strike Density** | < 3 strikes spot→short | -2 |
| | < 5 strikes spot→short | -1 |
| **Short Premium** | Short mid < $0.10 | -1 |
| | Short mid < $0.50 | -0.5 |

Weekly-options, strike-density, and short-premium are penalty-only (0 at best), so
`max_possible_score` stays **14** while the theoretical minimum is **-8** (base 0,
trend -2, earnings -2, weekly -1, strike -2, short premium -1).

## Output

Returns JSON with:
- `criteria` - Scan parameters used
- `results` - Array sorted by score:
  - `symbol`, `price`, `iv_pct`, `pmcc_score`, `max_possible_score` (always 14)
  - `industry` - GICS industry (falls back to sector), or null
  - `description` - one-sentence company description, or null
  - `has_weeklies` - whether the symbol lists weekly options (bool)
  - `short_window` - short-expiry window actually used: `"7-21"` or `"5-30 (fallback)"`
  - `dividend_yield` - continuous dividend yield (fraction) used in the BS/IV math
  - `leaps` - expiry, strike, delta, **iv** (calculated from bid/ask), **last_price**, bid/ask, spread%, volume, OI
  - `short` - expiry, strike, delta, **iv** (calculated from bid/ask), **last_price**, bid/ask, spread%, volume, OI
  - `earnings_date` - next earnings date (YYYY-MM-DD) or null
  - `metrics` - net_debit, short_yield% (period yield over the short window), annual_yield%, capital_required
  - `score_breakdown` - every scoring component as a `<name>_delta` (float) + `<name>` (explanation string) pair:
    - Base: `leaps_delta`, `short_delta`, `leaps_liquidity`, `short_liquidity`, `leaps_spread`, `short_spread`, `iv`, `yield`
    - Trend: `trend_delta`, `trend` (per-indicator dict)
    - Earnings: `earnings_delta`, `earnings`
    - Weekly options: `weekly_options_delta`, `weekly_options`
    - Strike density: `strike_density_delta`, `strike_density`
    - Short premium: `short_premium_delta`, `short_premium`
    - All `_delta` values sum to `pmcc_score`
- `errors` - Symbols that failed (no options, insufficient data)

## Report Generation

When the user asks for a report, a written analysis, or a saved document:

1. Run the scanner with `--output` to capture JSON data:
   ```bash
   uv run python scripts/scan.py SYMBOLS --output sandbox/PMCC_Scan_YYYY-MM-DD_HHmm.json
   ```

2. Read the JSON output.

3. Generate the markdown report yourself using the template defined in `templates/markdown-template.md`. Do **not** use the `--report` flag — that produces mechanical string output. Claude-generated reports include real analysis, contextual warnings, and trader-relevant narrative.

4. Save the generated markdown to `sandbox/PMCC_Scan_YYYY-MM-DD_HHmm.md` (match the JSON timestamp).

5. Display the full report to the user.

## Examples

```bash
# Scan specific symbols
uv run python scripts/scan.py AAPL,MSFT,GOOGL,NVDA

# Scan and save JSON for report generation
uv run python scripts/scan.py AAPL,MSFT,GOOGL --output sandbox/PMCC_Scan_2026-01-15_1430.json

# Use output from bullish scanner
uv run python scripts/scan.py bullish_results.json

# Custom delta targets
uv run python scripts/scan.py AAPL,MSFT --leaps-delta 0.70 --short-delta 0.15

# Longer LEAPS (1 year minimum)
uv run python scripts/scan.py AAPL,MSFT --min-leaps-days 365
```

## IV Calculation

IV is always computed from market price data via Black-Scholes, never taken from Yahoo Finance's `impliedVolatility` column:

- **During trading hours**: IV derived from bid/ask mid price
- **Off-hours (bid=ask=0)**: IV derived from last price, using the option's last trade timestamp as the pricing moment (not current wall-clock time)

This applies to both `compute_atm_iv` (used for scanner baseline IV) and per-option delta calculations.

**Dividends**: the Black-Scholes inversion uses the underlying's continuous dividend
yield (Merton model). Ignoring it biases recovered IV downward for calls on dividend
payers — badly for high yielders (e.g. a 7%-yield name would read ~12% IV instead of
~24%). The yield is normalized from yfinance's inconsistent fields (`dividendRate/price`,
then `trailingAnnualDividendYield`, then `dividendYield`) and reported as `dividend_yield`
(a fraction) in each result. The same yield feeds the strike-selection deltas and the
max-profit repricing.

## Key Constraints

- Short strike **must be above** LEAPS strike
- Options with bid = 0 and no last price are skipped
- Moderate IV (25-50%) scores highest

## Interpretation

- Score > 12: Excellent candidate (strong structure + bullish trend + clear earnings runway)
- Score 10-12: Good candidate
- Score 6-10: Acceptable with caveats
- Score < 6: Poor structure, bearish trend, or earnings risk
- `max_possible_score` is always 14 — use `pmcc_score / max_possible_score` to gauge how close a candidate is to perfect
- **Off-hours scores are not comparable to market-hours scores.** When bid/ask aren't both > 0 (outside trading hours), `spread_pct` is forced to 100%, which zeroes out both spread scores (−2 vs a live scan). A candidate can look up to 2 points worse simply because it was scanned off-hours. Compare candidates only within the same scan.

## Dependencies

- `numpy`
- `pandas`
- `scipy`
- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.

### Referencia: templates/markdown-template.md

# PMCC Scan Report — Claude Generation Template

This file defines the structure and requirements for Claude-generated PMCC reports.
When the user requests a report, run the scanner to get JSON data, then generate
the markdown report below using your analysis — not mechanical string formatting.

---

## Report Structure

### Header

```
# PMCC Scan Report
**Generated:** {generated_at}
**Symbols:** {comma-separated list}
**Criteria:** LEAPS ≥ {min_leaps_days}d · LEAPS δ {leaps_target_delta} · Short δ {short_target_delta}
```

---

### Section 1 — Scan Summary Table

One row per symbol, sorted by `pmcc_score` descending. Use these exact columns:

| Symbol | Industry | Price | IV% | Capital | Ann. Yield | Trend | Earnings | Weeklies | PMCC Score |
|--------|----------|------:|----:|--------:|-----------:|-------|----------|:--------:|:----------:|

Column definitions:
- **Symbol** — ticker
- **Industry** — `industry` (falls back to sector); "N/A" if unknown
- **Price** — current stock price (`price`)
- **IV%** — ATM implied volatility (`iv_pct`)
- **Capital** — LEAPS cost basis (`leaps.mid × 100`, formatted as `$X,XXX`)
- **Ann. Yield** — annualized short-call yield estimate (`metrics.annual_yield_est_pct`)
- **Trend** — derive from `score_breakdown.trend_delta`: ≥1.5 → Bullish, ≤-1.5 → Bearish, >0 → Leaning Bull, <0 → Leaning Bear, 0 → Neutral
- **Earnings** — days to next earnings from `earnings_date`; flag with ⚠ if < 30 days; "passed" if in the past; "N/A" if unknown
- **Weeklies** — `has_weeklies`: "Yes" / "No" (No costs −1 in the score)
- **PMCC Score** — `pmcc_score/max_possible_score`

---

### Section 2 — Per-Symbol Detail Sections

One section per symbol, in the same order as the summary table. Each section contains:

#### 2a. Section Header
```
### {SYMBOL} — Score {pmcc_score}/{max_possible_score}
```

Follow the header with a one-line italicized company description from `description`
(omit if null).

#### 2b. Indicators

Report every trend indicator the scorer actually consumed, from
`score_breakdown.trend` (keys such as `sma50`, `rsi`, `macd`). One bullet per
indicator, e.g. `- SMA50: price above (+1.0)`. Keep this list in sync with whatever
indicators appear in `score_breakdown.trend` — do not hardcode the set.

#### 2c. LEAPS Table

| Expiry | Strike | Delta | IV% | Last | Bid | Ask | Mid | Capital |
|--------|-------:|------:|----:|-----:|----:|----:|----:|--------:|

Populate from `leaps.*`. IV% = `leaps.iv × 100`. Flag off-hours data: if `leaps.bid == 0 and leaps.ask == 0`, add note: `⚠ No live bid/ask — using last price`.

#### 2d. Short Call Table

| Expiry | Strike | Delta | IV% | Last | Bid | Ask | Mid | Premium | Yield% |
|--------|-------:|------:|----:|-----:|----:|----:|----:|--------:|-------:|

Populate from `short.*`. Premium = `short.mid × 100`. Yield% = `metrics.short_yield_pct`.
Flag wide spreads: if `short.spread_pct > 20`, add note: `⚠ Wide spread — use limit order at mid`.

#### 2e. Suggested PMCC Setup

Short bullet list:
- **Buy**: `{leaps.expiry}` `${leaps.strike}C` @ `${leaps.mid}` (δ `{leaps.delta}`)
- **Sell**: `{short.expiry}` `${short.strike}C` @ `${short.mid}` (δ `{short.delta}`)
- **Net Debit**: `${metrics.net_debit}` | **Max Risk**: `${metrics.capital_required}`
- **Max Profit**: `${metrics.max_profit}` | **Ann. Yield Est.**: `{metrics.annual_yield_est_pct}%`

#### 2f. Strengths

Bullet list of positive scoring factors from `score_breakdown`. Include:
- Delta accuracy (LEAPS and short)
- Liquidity (if scoring > 0)
- Spread quality (if scoring > 0)
- IV level and why it matters for this setup
- Yield quality
- Trend indicators that are positive
- Earnings clearance

Write each as a human-readable sentence, not a raw score string. Example:
- ✓ LEAPS delta 0.787 is on target (±0.05 of 0.80)
- ✓ Strong bullish trend: price above SMA50, RSI 76.8, MACD positive

#### 2g. Weaknesses

Bullet list of zero or negative scoring factors. Same style as Strengths.
If there are no weaknesses, write: `No material weaknesses identified.`

Highlight these risk factors explicitly when present:
- **LEAPS liquidity**: if vol+OI < 20, warn that fills may be difficult
- **LEAPS no bid/ask**: warn to confirm live market before entering
- **Wide short spread** (>20%): warn about slippage
- **Earnings within short expiry**: warn IV crush / gap risk
- **High IV** (>70%): warn expensive entry, IV crush exposure
- **Bearish trend**: note momentum is against the position
- **No weekly options** (`weekly_options_delta` = −1): warn that roll/adjustment cadence is limited to monthly expiries
- **Thin strike density** (`strike_density_delta` < 0): warn that few strikes between spot and short limit strike selection and rolls
- **Thin short premium** (`short_premium_delta` < 0): warn the credit collected is too small to justify the assignment/transaction risk

#### 2h. Verdict

One paragraph (3–5 sentences) synthesizing the setup. Cover:
1. Go / No-go recommendation with confidence level
2. The single most important supporting reason
3. The single biggest risk or watch item
4. Specific action advice (e.g., "use limit at mid", "wait for post-earnings reset", "confirm live bid before entry")

Lead with a bold label:
- **Go** — score ≥ 12
- **Go with notes** — score 10–11
- **Proceed with caution** — score 6–9
- **No-go** — score < 6

Separator: `---` between each symbol section.

---

## Tone and Style Requirements

- Write like an experienced options trader reviewing setups for a colleague
- Be direct and specific — reference actual numbers (deltas, spreads, IV%, etc.)
- Flag risks clearly, don't soften important warnings
- Keep each verdict paragraph tight: 3–5 sentences max
- No generic filler ("this is a solid stock" without data to back it) 
- Earnings proximity warnings must be explicit and actionable

---

## File Naming Convention

When saving to disk:
```
sandbox/PMCC_Scan_YYYY-MM-DD_HHmm.md
```
Use the `generated_at` timestamp from the JSON output.

---

## What NOT to include

- Do not reproduce the raw JSON or score breakdown strings verbatim
- Do not include implementation details (Black-Scholes, scoring algorithm internals)
- Do not speculate about future price direction beyond what the technicals indicate
- Do not recommend position sizing — that's the trader's job


---

## SKILL: spread-analysis

- Fuente: `staskh/trading_skills` → `.claude/skills/spread-analysis` (MIT)
- Cuándo usarla: Analyze option spread strategies like vertical spreads, iron condors, straddles, strangles. Use when user asks about spreads, multi-leg strategies, vertical spread, iron condor, straddle, strangle, or strategy analysis.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/spread-analysis/` (spreads.py)

# Spread Analysis

Analyze multi-leg option strategies.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/spreads.py SYMBOL --strategy STRATEGY --expiry YYYY-MM-DD [options]
```

## Strategies and Options

**Vertical Spread** (bull/bear call/put spread):
```bash
uv run python scripts/spreads.py AAPL --strategy vertical --expiry 2026-01-16 --type call --long-strike 180 --short-strike 185
```

**Straddle** (long call + long put at same strike):
```bash
uv run python scripts/spreads.py AAPL --strategy straddle --expiry 2026-01-16 --strike 180
```

**Strangle** (long call + long put at different strikes):
```bash
uv run python scripts/spreads.py AAPL --strategy strangle --expiry 2026-01-16 --put-strike 175 --call-strike 185
```

**Iron Condor** (sell strangle + buy wider strangle):
```bash
uv run python scripts/spreads.py AAPL --strategy iron-condor --expiry 2026-01-16 --put-short 175 --put-long 170 --call-short 185 --call-long 190
```

## Output

Returns JSON with:
- `strategy` - Strategy name and legs
- `cost` - Net debit or credit
- `max_profit` - Maximum potential profit
- `max_loss` - Maximum potential loss
- `breakeven` - Breakeven price(s)
- `probability` - Estimated probability of profit (based on IV)

Explain the risk/reward and when this strategy is appropriate.

## Dependencies

- `pandas`
- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: sybil-detection

- Fuente: `agiprolabs/claude-trading-skills` → `skills/sybil-detection` (MIT)
- Cuándo usarla: Coordinated wallet cluster detection, wash trading identification, and fake activity analysis for Solana tokens
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/sybil-detection/` (detect_sybils.py, funding_tracer.py)

# Sybil Detection — Coordinated Wallet & Fake Activity Analysis

Sybil attacks in Solana token markets involve a single entity operating many wallets to create the illusion of organic activity. This skill covers detecting coordinated wallet clusters, wash trading, bundled transactions, and fake holder inflation — critical for evaluating whether a token's metrics reflect real demand or manufactured signals.

## Why Sybil Detection Matters

Token markets on Solana are rife with manufactured signals:

- **Inflated holder counts**: 500 "holders" that are really 10 entities with 50 wallets each
- **Fake volume**: Wash trading between self-controlled wallets to simulate demand
- **Artificial social proof**: Many wallets holding small amounts to appear broadly distributed
- **Rug preparation**: Creator distributes supply across many wallets, then sells coordinated
- **Bundled launches**: PumpFun tokens where creator buys via Jito bundle in first slot

A token showing 1,000 holders with 80% funded from 3 wallets is fundamentally different from one with 1,000 independently-funded holders. Sybil detection separates real demand from theater.

## Detection Categories

### 1. Funding Source Analysis

Trace each holder wallet back 1-2 hops to find who sent them SOL:

```python
import httpx

def trace_funding_source(wallet: str, api_key: str, max_hops: int = 2) -> list[str]:
    """Trace SOL funding sources for a wallet via Helius parsed transactions."""
    url = f"https://api.helius.xyz/v0/addresses/{wallet}/transactions"
    resp = httpx.get(url, params={"api-key": api_key, "type": "TRANSFER", "limit": 50})
    transfers = resp.json()

    funders = []
    for tx in transfers:
        for transfer in tx.get("nativeTransfers", []):
            if transfer["toUserAccount"] == wallet and transfer["amount"] > 0.001 * 1e9:
                funders.append(transfer["fromUserAccount"])
    return funders
```

**Key signals:**
- 3+ holder wallets funded from the same source = cluster
- Funding within 24h of token creation = high suspicion
- Funding amounts are identical (e.g., 0.05 SOL to each) = automated distribution

### 2. Co-Trading Patterns

Wallets that buy the same token at nearly the same time are likely coordinated:

```python
def detect_co_trades(buy_events: list[dict], slot_window: int = 3) -> list[list[str]]:
    """Group wallets that bought within the same slot window."""
    buy_events.sort(key=lambda x: x["slot"])
    clusters = []
    current_cluster = [buy_events[0]]

    for i in range(1, len(buy_events)):
        if buy_events[i]["slot"] - current_cluster[0]["slot"] <= slot_window:
            current_cluster.append(buy_events[i])
        else:
            if len(current_cluster) >= 3:
                clusters.append([b["wallet"] for b in current_cluster])
            current_cluster = [buy_events[i]]

    if len(current_cluster) >= 3:
        clusters.append([b["wallet"] for b in current_cluster])
    return clusters
```

**Interpretation:**
- Same slot, different transactions = coordinated (bot-driven)
- Same transaction = bundled (definite sybil)
- First 3 slots after token creation = launch sniping cluster

### 3. Bundled Transactions

Multiple buys packed into a single Solana transaction or Jito bundle:

```python
def check_bundle_ratio(early_buys: list[dict], bundle_window_slots: int = 5) -> dict:
    """Calculate the ratio of bundled vs independent early buys."""
    bundled = [b for b in early_buys if b.get("is_bundled", False)]
    first_slot = min(b["slot"] for b in early_buys) if early_buys else 0
    early = [b for b in early_buys if b["slot"] - first_slot <= bundle_window_slots]

    return {
        "total_early_buys": len(early),
        "bundled_buys": len(bundled),
        "bundle_ratio": len(bundled) / max(len(early), 1),
        "bundled_supply_pct": sum(b["amount"] for b in bundled) / max(sum(b["amount"] for b in early), 1),
    }
```

See `references/bundler_detection.md` for PumpFun-specific patterns and Jito bundle mechanics.

### 4. Wash Trading Detection

Same entity buying and selling through multiple wallets to inflate volume:

**Signals:**
- Wallet A buys token, transfers to Wallet B, Wallet B sells — circular flow
- Multiple wallets trading back and forth with no net position change
- Volume concentrated in wallet pairs with funding links

```python
def detect_wash_cycles(transfers: list[dict], holder_set: set[str]) -> list[tuple]:
    """Find circular transfer patterns among known holders."""
    # Build directed graph of transfers between holders
    edges: dict[tuple, float] = {}
    for t in transfers:
        if t["from"] in holder_set and t["to"] in holder_set:
            key = (t["from"], t["to"])
            edges[key] = edges.get(key, 0) + t["amount"]

    # Find reciprocal pairs (A->B and B->A both exist)
    wash_pairs = []
    for (a, b), vol_ab in edges.items():
        vol_ba = edges.get((b, a), 0)
        if vol_ba > 0:
            wash_pairs.append((a, b, vol_ab, vol_ba))
    return wash_pairs
```

### 5. Creator Network Analysis

Identify wallets controlled by the token creator:

- Creator wallet's funding history reveals other wallets it funded
- Those wallets holding token supply = insider distribution
- Creator selling from "different" wallets = disguised dump

## Key Metrics

| Metric | Formula | Healthy | Suspicious | Critical |
|--------|---------|---------|------------|----------|
| Unique funder ratio | unique_funders / total_holders | > 0.8 | 0.4-0.8 | < 0.4 |
| Funding cluster size | max(cluster_sizes) | < 5 | 5-20 | > 20 |
| Co-trade score | wallets_in_first_3_slots / total_holders | < 0.1 | 0.1-0.3 | > 0.3 |
| Bundle ratio | bundled_buys / total_early_buys | < 0.1 | 0.1-0.4 | > 0.4 |
| Bundled supply % | bundled_token_amount / total_supply_sold | < 5% | 5-20% | > 20% |
| Transfer density | internal_transfers / total_transfers | < 0.1 | 0.1-0.3 | > 0.3 |
| Wash trade pairs | reciprocal_pairs / total_holder_pairs | 0 | 1-3 pairs | > 3 pairs |

## Composite Risk Score

Combine individual signals into a single sybil risk score (0-100):

```python
def compute_sybil_score(metrics: dict) -> dict:
    """Compute composite sybil risk score from individual metrics."""
    weights = {
        "funding_cluster": 25,    # Wallets from same funder
        "co_trade": 20,           # Coordinated buy timing
        "bundle_ratio": 20,       # Bundled early transactions
        "unique_funder": 15,      # Diversity of funding sources
        "transfer_density": 10,   # Internal transfers between holders
        "wash_trade": 10,         # Circular trading patterns
    }

    scores = {}
    # Each sub-score normalized to 0-1, then weighted
    scores["funding_cluster"] = min(metrics.get("max_cluster_size", 0) / 20, 1.0)
    scores["co_trade"] = min(metrics.get("co_trade_pct", 0) / 0.3, 1.0)
    scores["bundle_ratio"] = min(metrics.get("bundle_ratio", 0) / 0.5, 1.0)
    scores["unique_funder"] = 1.0 - min(metrics.get("unique_funder_ratio", 1.0), 1.0)
    scores["transfer_density"] = min(metrics.get("transfer_density", 0) / 0.3, 1.0)
    scores["wash_trade"] = min(metrics.get("wash_pairs", 0) / 5, 1.0)

    composite = sum(scores[k] * weights[k] for k in weights)
    risk_level = "LOW" if composite < 30 else "MEDIUM" if composite < 60 else "HIGH"

    return {"score": round(composite, 1), "risk_level": risk_level, "components": scores}
```

## Data Sources

| Source | What It Provides | Auth Required |
|--------|-----------------|---------------|
| Helius parsed transactions | Funding history, transfer details, parsed instruction data | API key (free tier: 30 req/s) |
| SolanaTracker API | Bundler detection, holder lists, token metadata | API key |
| Solana RPC (getSignaturesForAddress) | Raw transaction signatures for any wallet | RPC URL |
| Solana RPC (getTokenLargestAccounts) | Top holders by balance | RPC URL |
| DexScreener | Basic token/pair data for cross-referencing | None |

## Workflow: Evaluate a Token

```python
# 1. Get top holders
holders = get_top_holders(token_mint, rpc_url)

# 2. Trace funding sources for each holder
funding_map = {}
for wallet in holders[:30]:  # Top 30 is usually sufficient
    funding_map[wallet] = trace_funding_source(wallet, helius_key)

# 3. Cluster by common funder
clusters = cluster_by_funder(funding_map)

# 4. Check co-trade timing
early_buys = get_early_buy_events(token_mint, helius_key)
co_trade_groups = detect_co_trades(early_buys)

# 5. Check for bundles
bundle_stats = check_bundle_ratio(early_buys)

# 6. Check wash trading
transfers = get_token_transfers(token_mint, helius_key)
wash_pairs = detect_wash_cycles(transfers, set(holders))

# 7. Compute composite score
metrics = {
    "max_cluster_size": max(len(c) for c in clusters) if clusters else 0,
    "co_trade_pct": sum(len(g) for g in co_trade_groups) / len(holders),
    "bundle_ratio": bundle_stats["bundle_ratio"],
    "unique_funder_ratio": len(set(f for fs in funding_map.values() for f in fs)) / len(holders),
    "transfer_density": len(wash_pairs) / max(len(holders), 1),
    "wash_pairs": len(wash_pairs),
}
result = compute_sybil_score(metrics)
print(f"Sybil Risk: {result['risk_level']} ({result['score']}/100)")
```

## Integration with Other Skills

- **token-holder-analysis**: Use holder list as input; sybil detection adds cluster context
- **helius-api**: Primary data source for parsed transaction history
- **jito-bundles**: Detailed bundle detection and MEV context
- **liquidity-analysis**: Combine with sybil score — low liquidity + high sybil = extreme risk
- **whale-tracking**: Distinguish real whales from sybil cluster aggregates

## Files

| File | Description |
|------|-------------|
| `references/clustering_methods.md` | Funding source clustering, co-trade timing analysis, graph-based detection methods |
| `references/bundler_detection.md` | Bundled transaction detection, PumpFun patterns, Jito bundle mechanics |
| `scripts/detect_sybils.py` | Full sybil detection pipeline: holders -> funding -> clusters -> risk score |
| `scripts/funding_tracer.py` | Trace funding sources for a set of wallets, group by common ancestor |

### Referencia: references/bundler_detection.md

# Sybil Detection — Bundler Detection

How to detect bundled transactions on Solana, with focus on PumpFun token launches and Jito bundle mechanics.

## What Are Bundled Transactions?

On Solana, bundled transactions take two forms:

### 1. Single-Transaction Bundles

Multiple swap instructions packed into one Solana transaction. One signer executes buys for multiple destination wallets in a single atomic operation.

**Detection signals:**
- Transaction has multiple token transfer instructions to different wallets
- Single fee payer for all instructions
- All transfers are for the same token mint

### 2. Jito Bundles

Multiple separate transactions submitted together to a Jito validator. They execute sequentially in the same slot with guaranteed ordering.

**Detection signals:**
- Multiple transactions in the same slot buying the same token
- Transactions appear sequential (consecutive within the slot)
- Often include a Jito tip transaction to the tip program

## Detecting Bundled Buys from Transaction Data

### Via Helius Parsed Transactions

```python
import httpx

def detect_single_tx_bundles(
    token_mint: str, helius_key: str, limit: int = 100
) -> list[dict]:
    """Find transactions that contain multiple buys of the same token.

    These are single transactions where one signer buys tokens
    and distributes to multiple wallets.
    """
    url = f"https://api.helius.xyz/v0/addresses/{token_mint}/transactions"
    resp = httpx.get(url, params={"api-key": helius_key, "limit": limit}, timeout=15)
    if resp.status_code != 200:
        return []

    bundled_txs = []
    for tx in resp.json():
        token_transfers = [
            t for t in tx.get("tokenTransfers", [])
            if t.get("mint") == token_mint
        ]
        unique_recipients = set(t["toUserAccount"] for t in token_transfers)

        if len(unique_recipients) >= 2:
            bundled_txs.append({
                "signature": tx.get("signature", ""),
                "slot": tx.get("slot", 0),
                "recipient_count": len(unique_recipients),
                "recipients": list(unique_recipients),
                "total_amount": sum(t.get("tokenAmount", 0) for t in token_transfers),
                "fee_payer": tx.get("feePayer", ""),
            })

    return bundled_txs
```

### Via Slot-Based Jito Bundle Detection

```python
from collections import defaultdict

def detect_jito_bundles(
    buy_events: list[dict], max_slot_gap: int = 0
) -> list[dict]:
    """Detect likely Jito bundles by grouping buys in the same slot.

    Jito bundles execute multiple transactions in the same slot with
    guaranteed sequential ordering.

    Args:
        buy_events: List of {"wallet": str, "slot": int, "tx_sig": str, "amount": float}.
        max_slot_gap: Maximum slot gap to consider as same bundle (0 = same slot only).

    Returns:
        List of detected bundle groups.
    """
    slot_groups: dict[int, list[dict]] = defaultdict(list)
    for event in buy_events:
        slot_groups[event["slot"]].append(event)

    bundles = []
    for slot, events in sorted(slot_groups.items()):
        if len(events) >= 2:
            unique_wallets = set(e["wallet"] for e in events)
            unique_sigs = set(e["tx_sig"] for e in events)
            bundles.append({
                "slot": slot,
                "tx_count": len(unique_sigs),
                "wallet_count": len(unique_wallets),
                "wallets": list(unique_wallets),
                "total_amount": sum(e["amount"] for e in events),
                "is_single_tx": len(unique_sigs) == 1,
                "is_jito_bundle": len(unique_sigs) > 1,
            })

    return bundles
```

### Via SolanaTracker Bundler API

SolanaTracker provides a dedicated bundler detection endpoint:

```python
def check_bundler_solanatracker(
    token_mint: str, api_key: str
) -> dict:
    """Check for bundled transactions via SolanaTracker API."""
    url = f"https://data.solanatracker.io/tokens/{token_mint}/bundled"
    resp = httpx.get(url, headers={"x-api-key": api_key}, timeout=15)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}"}
    return resp.json()
```

## PumpFun-Specific Patterns

PumpFun tokens are the most common target for sybil attacks. Common patterns:

### Creator Self-Buy Bundle

1. Creator calls PumpFun `create` instruction
2. In the same transaction (or same slot via Jito), creator buys tokens through multiple wallets
3. These wallets now appear as "early holders"

**Detection:**
- Check if any early buyer wallets were funded by the token creator
- Check if buys in slots 0-2 (relative to creation) came from related wallets
- First-slot buys from multiple wallets = almost always bundled

### Supply Concentration from Bundles

```python
def pumpfun_bundle_analysis(
    early_buys: list[dict], creation_slot: int
) -> dict:
    """Analyze bundling patterns for a PumpFun token.

    Args:
        early_buys: Buy events with slot, wallet, amount, is_bundled fields.
        creation_slot: The slot where the token was created.

    Returns:
        Analysis dict with bundle metrics.
    """
    first_3_slots = [b for b in early_buys if b["slot"] - creation_slot <= 3]
    bundled_early = [b for b in first_3_slots if b.get("is_bundled", False)]

    total_early_supply = sum(b["amount"] for b in first_3_slots)
    bundled_supply = sum(b["amount"] for b in bundled_early)

    unique_early_wallets = set(b["wallet"] for b in first_3_slots)
    bundled_wallets = set(b["wallet"] for b in bundled_early)

    return {
        "creation_slot": creation_slot,
        "first_3_slot_buys": len(first_3_slots),
        "bundled_buys": len(bundled_early),
        "unique_early_wallets": len(unique_early_wallets),
        "bundled_wallets": len(bundled_wallets),
        "total_early_supply": total_early_supply,
        "bundled_supply": bundled_supply,
        "bundled_supply_pct": bundled_supply / max(total_early_supply, 1) * 100,
    }
```

## Metrics and Risk Interpretation

### Bundle Ratio

`bundle_ratio = bundled_buys / total_early_buys`

| Bundle Ratio | Risk Level | Interpretation |
|-------------|------------|----------------|
| 0.0 | None | No bundled activity detected |
| 0.01 - 0.10 | Low | Minor bundling, possibly MEV bots |
| 0.10 - 0.25 | Moderate | Significant bundling, review clusters |
| 0.25 - 0.50 | High | Heavy bundling, likely coordinated launch |
| > 0.50 | Critical | Majority of early buys bundled, probable sybil |

### Bundled Supply Percentage

`bundled_supply_pct = bundled_token_amount / total_circulating_supply * 100`

| Bundled Supply % | Risk Level | Interpretation |
|-----------------|------------|----------------|
| < 2% | Low | Negligible bundled holdings |
| 2-10% | Moderate | Notable bundled position |
| 10-30% | High | Large coordinated position |
| > 30% | Critical | Dominant supply held by bundlers |

### Bundler Wallet Count

| Bundler Wallets | Interpretation |
|----------------|----------------|
| 1-2 | Single actor with modest distribution |
| 3-10 | Organized sybil operation |
| 10-30 | Large-scale fake holder inflation |
| > 30 | Industrial sybil farming |

## Combining Bundle Detection with Funding Analysis

Bundle detection alone identifies the mechanism. Combining with funding source analysis identifies the actor:

```python
def correlate_bundles_with_funding(
    bundle_wallets: list[str],
    funding_clusters: dict[str, list[str]],
) -> list[dict]:
    """Find overlap between bundled wallets and funding clusters.

    When bundled wallets also share a funding source, confidence
    in sybil detection is very high.
    """
    results = []
    bundle_set = set(bundle_wallets)

    for funder, funded_wallets in funding_clusters.items():
        overlap = bundle_set.intersection(set(funded_wallets))
        if overlap:
            results.append({
                "funder": funder,
                "bundled_and_funded": list(overlap),
                "overlap_count": len(overlap),
                "total_funded": len(funded_wallets),
                "confidence": "HIGH" if len(overlap) >= 3 else "MODERATE",
            })

    return results
```

## Edge Cases

- **MEV bots**: Legitimate MEV searchers also use bundles — not all bundles are sybil
- **Aggregator routers**: Jupiter and other aggregators may route through multiple accounts
- **Partial detection**: Some bundles only detectable via Jito-specific APIs, not standard RPC
- **Historical data**: Jito bundle metadata may not be available for older transactions
- **False negatives**: Sophisticated operators use separate wallets with no on-chain link

### Referencia: references/clustering_methods.md

# Sybil Detection — Clustering Methods

Methods for grouping wallets into coordinated clusters based on funding sources, trading timing, and transfer graph structure.

## Funding Source Clustering

The most reliable sybil signal: multiple holder wallets funded from the same SOL source.

### Algorithm

1. For each holder wallet, fetch recent SOL transfers **in** (received)
2. Extract the `fromUserAccount` for each incoming SOL transfer
3. Group holder wallets by their funder address
4. Clusters of 3+ wallets from the same funder = suspicious

### Implementation

```python
from collections import defaultdict
import httpx

def cluster_by_funding(
    holder_wallets: list[str],
    helius_key: str,
    min_cluster_size: int = 3,
    min_sol_amount: float = 0.001,
) -> dict[str, list[str]]:
    """Group holder wallets by their SOL funding source.

    Args:
        holder_wallets: List of token holder wallet addresses.
        helius_key: Helius API key for transaction lookups.
        min_cluster_size: Minimum wallets from same funder to flag.
        min_sol_amount: Minimum SOL transfer to consider as funding (in SOL).

    Returns:
        Dict mapping funder address -> list of funded holder wallets.
    """
    funder_to_holders: dict[str, list[str]] = defaultdict(list)

    for wallet in holder_wallets:
        url = f"https://api.helius.xyz/v0/addresses/{wallet}/transactions"
        resp = httpx.get(url, params={
            "api-key": helius_key,
            "type": "TRANSFER",
            "limit": 50,
        }, timeout=15)
        if resp.status_code != 200:
            continue

        for tx in resp.json():
            for transfer in tx.get("nativeTransfers", []):
                if (
                    transfer["toUserAccount"] == wallet
                    and transfer["amount"] > min_sol_amount * 1e9
                ):
                    funder_to_holders[transfer["fromUserAccount"]].append(wallet)

    # Filter to clusters meeting minimum size
    return {
        funder: wallets
        for funder, wallets in funder_to_holders.items()
        if len(wallets) >= min_cluster_size
    }
```

### Multi-Hop Tracing

Sophisticated sybils use intermediary wallets. Trace 2 hops:

```
Real Funder -> Intermediary A -> Holder Wallet 1
Real Funder -> Intermediary B -> Holder Wallet 2
Real Funder -> Intermediary C -> Holder Wallet 3
```

At hop 1, each holder has a different funder. At hop 2, all trace to the same source.

```python
def trace_funding_chain(
    wallet: str, helius_key: str, max_hops: int = 2
) -> list[list[str]]:
    """Trace funding chain back N hops. Returns list of chains.

    Each chain is [wallet, funder_hop1, funder_hop2, ...].
    """
    chains: list[list[str]] = [[wallet]]

    for hop in range(max_hops):
        new_chains = []
        for chain in chains:
            tip = chain[-1]
            funders = _get_sol_funders(tip, helius_key)
            if funders:
                for funder in funders[:3]:  # Limit branching
                    new_chains.append(chain + [funder])
            else:
                new_chains.append(chain)
        chains = new_chains

    return chains
```

### Time Window Analysis

Funding timing adds confidence to cluster detection:

| Timing | Interpretation |
|--------|---------------|
| Funded < 1h before token creation | Very likely sybil preparation |
| Funded < 24h before token creation | Suspicious, especially if clustered |
| Funded > 7 days before token creation | Lower suspicion (pre-existing wallet) |
| Funded identical amounts | Automated distribution (high confidence sybil) |

## Co-Trade Timing Analysis

Wallets buying the same token within a narrow time window indicates coordination.

### Slot-Based Grouping

Solana slots are ~400ms. Buys in the same slot from different wallets are almost certainly coordinated.

```python
from collections import defaultdict

def group_buys_by_slot(
    buy_events: list[dict], window: int = 3
) -> list[dict]:
    """Group buy events into slot-based clusters.

    Args:
        buy_events: List of {"wallet": str, "slot": int, "amount": float, "tx_sig": str}.
        window: Number of slots to consider as "same time".

    Returns:
        List of cluster dicts with wallets, slot range, and total amount.
    """
    if not buy_events:
        return []

    buy_events.sort(key=lambda x: x["slot"])
    clusters = []
    current = [buy_events[0]]

    for event in buy_events[1:]:
        if event["slot"] - current[0]["slot"] <= window:
            current.append(event)
        else:
            if len(current) >= 2:
                clusters.append({
                    "wallets": [e["wallet"] for e in current],
                    "slot_start": current[0]["slot"],
                    "slot_end": current[-1]["slot"],
                    "total_amount": sum(e["amount"] for e in current),
                    "buy_count": len(current),
                })
            current = [event]

    if len(current) >= 2:
        clusters.append({
            "wallets": [e["wallet"] for e in current],
            "slot_start": current[0]["slot"],
            "slot_end": current[-1]["slot"],
            "total_amount": sum(e["amount"] for e in current),
            "buy_count": len(current),
        })

    return clusters
```

### Statistical Baseline

To distinguish coordination from coincidence, compare observed co-occurrence against a random baseline:

- **Null hypothesis**: Buys are uniformly distributed across slots
- **Test**: Given N buys over S slots, expected buys per slot = N/S
- **Flag**: If any slot has > 3x expected density, likely coordinated

```python
def co_trade_significance(
    buy_slots: list[int], total_slot_range: int
) -> dict:
    """Test if buy timing is more clustered than random."""
    from collections import Counter
    slot_counts = Counter(buy_slots)
    n_buys = len(buy_slots)
    expected_per_slot = n_buys / max(total_slot_range, 1)

    max_in_slot = max(slot_counts.values()) if slot_counts else 0
    concentration_ratio = max_in_slot / max(expected_per_slot, 0.001)

    return {
        "max_buys_in_single_slot": max_in_slot,
        "expected_per_slot": round(expected_per_slot, 4),
        "concentration_ratio": round(concentration_ratio, 2),
        "is_suspicious": concentration_ratio > 3.0,
    }
```

## Graph-Based Methods

Build a transfer graph between token holders to find densely connected subgroups.

### Transfer Graph Construction

```python
def build_transfer_graph(
    transfers: list[dict], holder_set: set[str]
) -> dict[str, dict[str, float]]:
    """Build directed weighted graph of transfers between holders.

    Args:
        transfers: List of {"from": str, "to": str, "amount": float}.
        holder_set: Set of known holder wallet addresses.

    Returns:
        Adjacency dict: {from_wallet: {to_wallet: total_volume}}.
    """
    graph: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    for t in transfers:
        if t["from"] in holder_set and t["to"] in holder_set:
            graph[t["from"]][t["to"]] += t["amount"]

    return dict(graph)
```

### Connected Components

Find groups of wallets that have transferred tokens among themselves:

```python
def find_connected_components(
    graph: dict[str, dict[str, float]]
) -> list[set[str]]:
    """Find connected components in transfer graph (undirected)."""
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors.keys())

    visited: set[str] = set()
    components: list[set[str]] = []

    for node in all_nodes:
        if node in visited:
            continue
        component: set[str] = set()
        stack = [node]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            component.add(current)
            # Add neighbors (both directions)
            for neighbor in graph.get(current, {}):
                stack.append(neighbor)
            for src, neighbors in graph.items():
                if current in neighbors:
                    stack.append(src)
        if len(component) >= 2:
            components.append(component)

    return components
```

### Graph Density Metric

Dense subgraphs (many edges relative to nodes) indicate tightly coordinated groups:

| Density | Interpretation |
|---------|---------------|
| < 0.1 | Normal — sparse transfers between holders |
| 0.1-0.3 | Moderate — some internal circulation |
| > 0.3 | High — likely coordinated wallet cluster |

```python
def subgraph_density(component: set[str], graph: dict[str, dict[str, float]]) -> float:
    """Calculate density of a subgraph (edges / possible edges)."""
    n = len(component)
    if n < 2:
        return 0.0
    possible_edges = n * (n - 1)  # Directed graph
    actual_edges = sum(
        1 for src in component for dst in graph.get(src, {}) if dst in component
    )
    return actual_edges / possible_edges
```

## Limitations

- **Chain-hopping**: Sybils can fund wallets from CEX withdrawals (different addresses each time)
- **Mixing services**: SOL mixers break the funding chain
- **Time delays**: Patient attackers fund wallets days/weeks in advance
- **Intermediary depth**: Tracing beyond 2 hops is computationally expensive and noisy
- **False positives**: Airdrop campaigns legitimately fund many wallets from one source
- **RPC rate limits**: Tracing 100+ wallets requires significant API quota

Combine multiple signals — the intersection of funding clusters + co-trade timing + bundle detection catches most coordinated activity even when individual methods miss sophisticated sybils.


---

## SKILL: ta-lib

- Fuente: `agiprolabs/claude-trading-skills` → `skills/ta-lib` (MIT)
- Cuándo usarla: C-optimized technical analysis with 150+ functions and 61 candlestick pattern recognition functions via TA-Lib
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/ta-lib/` (compute_indicators.py, pattern_scanner.py)

# ta-lib — C-Optimized Technical Analysis

TA-Lib (Technical Analysis Library) is a C library with a Python wrapper providing 150+ technical analysis functions and 61 candlestick pattern recognition functions. It is the industry standard for performance-critical indicator computation, used in production trading systems where pandas-ta or pure-Python alternatives are too slow.

## What TA-Lib Is

TA-Lib was originally written in C for financial market data analysis. The Python wrapper (`TA-Lib` on PyPI, imported as `talib`) provides:

- **150+ indicator functions** across overlap, momentum, volume, volatility, cycle, and math categories
- **61 candlestick pattern recognition functions** — the most comprehensive pattern library available
- **C-speed computation** — 10-100x faster than pure-Python equivalents on large datasets
- **Two APIs**: a function API (pass arrays directly) and an abstract API (pass dict of arrays)
- **NumPy native** — all inputs and outputs are NumPy arrays

## Installation

TA-Lib requires the underlying C library to be installed first:

```bash
# macOS
brew install ta-lib
uv pip install TA-Lib numpy pandas

# Ubuntu/Debian
sudo apt-get install -y ta-lib
uv pip install TA-Lib numpy pandas

# From source (any platform)
wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz
tar -xzf ta-lib-0.6.4-src.tar.gz
cd ta-lib-0.6.4
./configure --prefix=/usr/local
make && sudo make install
uv pip install TA-Lib numpy pandas
```

If the C library is not installed, `import talib` will fail with an `ImportError`. The scripts in this skill include fallback logic for environments without TA-Lib installed.

## When to Use TA-Lib vs pandas-ta

| Criterion | TA-Lib | pandas-ta |
|---|---|---|
| Speed | C-optimized, 10-100x faster | Pure Python, slower on large data |
| Candlestick patterns | 61 built-in patterns | Limited pattern support |
| Installation | Requires C library | `pip install` only |
| API style | NumPy arrays | DataFrame `.ta` accessor |
| Indicator count | 150+ | 130+ |
| Streaming | Single-value update possible | Recompute entire series |
| Dependencies | C lib + numpy | pandas only |

**Use TA-Lib when:**
- Processing millions of bars or running backtests at scale
- You need candlestick pattern recognition (TA-Lib is unmatched here)
- You are building a production pipeline where latency matters
- You need cycle indicators (Hilbert Transform family)

**Use pandas-ta when:**
- You want DataFrame-native convenience
- Installation simplicity matters (no C dependency)
- You need indicators not in TA-Lib (pandas-ta has some extras)

## Quick Start

```python
import numpy as np
import talib

# Create sample data
close = np.random.randn(100).cumsum() + 50
high = close + np.abs(np.random.randn(100))
low = close - np.abs(np.random.randn(100))
open_ = close + np.random.randn(100) * 0.5
volume = np.random.randint(1000, 10000, 100).astype(float)

# Function API — pass arrays directly
rsi = talib.RSI(close, timeperiod=14)
macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
atr = talib.ATR(high, low, close, timeperiod=14)

# Candlestick patterns — return +100 (bullish), -100 (bearish), or 0
doji = talib.CDLDOJI(open_, high, low, close)
hammer = talib.CDLHAMMER(open_, high, low, close)
engulfing = talib.CDLENGULFING(open_, high, low, close)
```

## Function API vs Abstract API

### Function API (Recommended)

Call functions directly with NumPy arrays:

```python
import talib

rsi = talib.RSI(close, timeperiod=14)
sma = talib.SMA(close, timeperiod=20)
upper, mid, lower = talib.BBANDS(close)
```

### Abstract API

Pass a dictionary of arrays and get results by name:

```python
from talib import abstract

inputs = {"open": open_, "high": high, "low": low, "close": close, "volume": volume}

# Call by function name
rsi = abstract.RSI(inputs, timeperiod=14)
macd = abstract.MACD(inputs)  # returns (macd, signal, hist)
```

The abstract API is useful for dynamic indicator selection (e.g., looping over a list of indicator names).

## Function Groups

TA-Lib organizes functions into these groups:

### Overlap Studies
Moving averages and envelope indicators that overlay price charts.

```python
sma = talib.SMA(close, timeperiod=20)
ema = talib.EMA(close, timeperiod=12)
upper, mid, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
mama, fama = talib.MAMA(close, fastlimit=0.5, slowlimit=0.05)
```

### Momentum Indicators
Oscillators and trend-strength measures.

```python
rsi = talib.RSI(close, timeperiod=14)
macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
slowk, slowd = talib.STOCH(high, low, close)
cci = talib.CCI(high, low, close, timeperiod=14)
willr = talib.WILLR(high, low, close, timeperiod=14)
adx = talib.ADX(high, low, close, timeperiod=14)
mfi = talib.MFI(high, low, close, volume, timeperiod=14)
```

### Volume Indicators
Volume-based analysis functions.

```python
obv = talib.OBV(close, volume)
ad = talib.AD(high, low, close, volume)
adosc = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
```

### Volatility Indicators
Measures of price variability.

```python
atr = talib.ATR(high, low, close, timeperiod=14)
natr = talib.NATR(high, low, close, timeperiod=14)
trange = talib.TRANGE(high, low, close)
```

### Pattern Recognition (Candlestick)
61 functions that detect candlestick patterns. All return integer arrays:
- `+100` = bullish pattern detected
- `-100` = bearish pattern detected
- `0` = no pattern

```python
# Single patterns
doji = talib.CDLDOJI(open_, high, low, close)
hammer = talib.CDLHAMMER(open_, high, low, close)
engulfing = talib.CDLENGULFING(open_, high, low, close)

# Scan all 61 patterns at once
candle_names = talib.get_function_groups()["Pattern Recognition"]
for name in candle_names:
    func = getattr(talib, name)
    result = func(open_, high, low, close)
    hits = np.nonzero(result)[0]
    if len(hits) > 0:
        print(f"{name}: {len(hits)} detections")
```

See `references/candlestick_patterns.md` for the full list of 61 patterns with reliability ratings and crypto relevance.

### Math Transform & Math Operators
Mathematical functions (sin, cos, ln, etc.) and operators (add, sub, mult, div) on arrays. Rarely used directly but available.

## Crypto Considerations

### 24/7 Markets
- Candlestick patterns designed for traditional markets with opening/closing gaps may behave differently on crypto's continuous markets
- Gap-based patterns (morning star, evening star) are less reliable without session gaps
- Body-ratio patterns (doji, hammer, engulfing) still work well on any timeframe

### Timeframe Selection
- **1m-5m**: Patterns are noisy; combine with volume confirmation
- **15m-1h**: Good for intraday signals on high-cap tokens
- **4h-1d**: Most reliable for pattern recognition
- **Tip**: Higher timeframes produce fewer but more reliable pattern signals

### NaN Handling
TA-Lib returns `NaN` for the initial lookback period of each indicator. Always account for this:

```python
rsi = talib.RSI(close, timeperiod=14)
# First 14 values will be NaN
valid_rsi = rsi[~np.isnan(rsi)]
```

### Solana Token Data
When using TA-Lib with Solana token OHLCV data:
- Ensure arrays are `float64` dtype — TA-Lib requires this
- Sort by timestamp ascending before passing to TA-Lib
- Handle gaps in low-liquidity token data before computing indicators

```python
# Convert to float64 for TA-Lib compatibility
close = df["close"].values.astype(np.float64)
high = df["high"].values.astype(np.float64)
low = df["low"].values.astype(np.float64)
```

## Integration with Other Skills

### With pandas-ta
pandas-ta can use TA-Lib as a backend when installed, getting C-speed through the pandas-ta API:

```python
import pandas_ta as ta
# pandas-ta auto-detects TA-Lib and uses it for supported indicators
# Set explicitly:
ta.Imports["talib"] = True  # Force TA-Lib backend
df.ta.rsi(length=14)  # Uses TA-Lib under the hood if available
```

### With vectorbt
vectorbt integrates with TA-Lib for fast backtesting:

```python
import vectorbt as vbt

# Use TA-Lib indicators in vectorbt
rsi = vbt.talib("RSI").run(close, timeperiod=14)
entries = rsi.real_crossed_below(30)
exits = rsi.real_crossed_above(70)
```

### With Birdeye/DexScreener Data
Fetch OHLCV data from API skills, then process with TA-Lib:

```python
# After fetching OHLCV from birdeye-api or dexscreener-api
close = np.array(ohlcv_data["close"], dtype=np.float64)
rsi = talib.RSI(close, timeperiod=14)
```

## Listing Available Functions

```python
import talib

# All function groups
groups = talib.get_function_groups()
for group, funcs in groups.items():
    print(f"{group}: {len(funcs)} functions")

# All function names
all_funcs = talib.get_functions()
print(f"Total: {len(all_funcs)} functions")

# Info about a specific function
info = talib.abstract.Function("RSI").info
print(info["display_name"], info["group"])
```

## Files

| File | Description |
|---|---|
| `references/function_reference.md` | Most useful functions by category with syntax and parameters |
| `references/candlestick_patterns.md` | All 61 candlestick patterns grouped by type with reliability ratings |
| `scripts/compute_indicators.py` | Computes common indicators with TA-Lib/fallback comparison |
| `scripts/pattern_scanner.py` | Scans OHLCV data for all 61 candlestick patterns |

### Referencia: references/candlestick_patterns.md

# TA-Lib Candlestick Patterns — Complete Reference

All 61 candlestick pattern recognition functions. Every function takes `(open, high, low, close)` as float64 NumPy arrays and returns an integer array: `+100` = bullish, `-100` = bearish, `0` = no pattern detected. Some patterns return `+200`/`-200` for strong confirmation.

## Return Value Convention

```python
result = talib.CDLHAMMER(open_, high, low, close)
# result[i] == 100   → bullish hammer on bar i
# result[i] == -100  → bearish variant (if applicable)
# result[i] == 0     → no pattern on bar i
```

## Reversal Bullish (12 patterns)

Patterns that signal a potential bottom/reversal from bearish to bullish trend.

| # | Function | Name | Bars | Reliability | Crypto Notes |
|---|---|---|---|---|---|
| 1 | `CDLHAMMER` | Hammer | 1 | High | Works well on all timeframes |
| 2 | `CDLINVERTEDHAMMER` | Inverted Hammer | 1 | Medium | Needs volume confirmation |
| 3 | `CDLENGULFING` | Bullish Engulfing | 2 | High | Strong on 4h+ timeframes |
| 4 | `CDLPIERCING` | Piercing Line | 2 | High | Less reliable without gaps |
| 5 | `CDLMORNINGSTAR` | Morning Star | 3 | High | Rare on crypto (needs gaps) |
| 6 | `CDLMORNINGDOJISTAR` | Morning Doji Star | 3 | High | Rare on crypto |
| 7 | `CDLHARAMI` | Bullish Harami | 2 | Medium | Common but weak alone |
| 8 | `CDLHARAMICROSS` | Bullish Harami Cross | 2 | Medium | Harami with doji inside |
| 9 | `CDLDRAGONFLYDOJI` | Dragonfly Doji | 1 | Medium | Good at support levels |
| 10 | `CDLABANDONEDBABY` | Abandoned Baby (Bull) | 3 | High | Very rare on crypto |
| 11 | `CDLTHREEWHITESOLDIERS` | Three White Soldiers | 3 | High | Strong trend reversal |
| 12 | `CDLKICKING` | Kicking (Bull) | 2 | High | Needs gaps, rare on crypto |

## Reversal Bearish (12 patterns)

Patterns that signal a potential top/reversal from bullish to bearish trend.

| # | Function | Name | Bars | Reliability | Crypto Notes |
|---|---|---|---|---|---|
| 13 | `CDLSHOOTINGSTAR` | Shooting Star | 1 | High | Works well, confirm with volume |
| 14 | `CDLHANGINGMAN` | Hanging Man | 1 | Medium | Hammer at top, needs confirmation |
| 15 | `CDLENGULFING` | Bearish Engulfing | 2 | High | Returns -100 for bearish |
| 16 | `CDLDARKCLOUDCOVER` | Dark Cloud Cover | 2 | High | Less reliable without gaps |
| 17 | `CDLEVENINGSTAR` | Evening Star | 3 | High | Rare on crypto (needs gaps) |
| 18 | `CDLEVENINGDOJISTAR` | Evening Doji Star | 3 | High | Rare on crypto |
| 19 | `CDLHARAMI` | Bearish Harami | 2 | Medium | Returns -100 for bearish |
| 20 | `CDLHARAMICROSS` | Bearish Harami Cross | 2 | Medium | Harami with doji inside |
| 21 | `CDLGRAVESTONEDOJI` | Gravestone Doji | 1 | Medium | Good at resistance levels |
| 22 | `CDLABANDONEDBABY` | Abandoned Baby (Bear) | 3 | High | Very rare on crypto |
| 23 | `CDLTHREEBLACKCROWS` | Three Black Crows | 3 | High | Strong downtrend signal |
| 24 | `CDLKICKING` | Kicking (Bear) | 2 | High | Needs gaps, rare on crypto |

## Continuation Patterns (8 patterns)

Patterns that suggest the existing trend will continue.

| # | Function | Name | Bars | Reliability | Crypto Notes |
|---|---|---|---|---|---|
| 25 | `CDLRISEFALL3METHODS` | Rising/Falling Three | 5 | High | Needs clear prior trend |
| 26 | `CDLTASUKIGAP` | Tasuki Gap | 3 | Medium | Gap-dependent, rare crypto |
| 27 | `CDLGAPSIDESIDEWHITE` | Side-by-Side White | 3 | Low | Gap-dependent |
| 28 | `CDLSEPARATINGLINES` | Separating Lines | 2 | Medium | Gap-dependent |
| 29 | `CDLMATHOLD` | Mat Hold | 5 | High | Rare but reliable |
| 30 | `CDLINNECK` | In-Neck | 2 | Low | Bearish continuation |
| 31 | `CDLONNECK` | On-Neck | 2 | Low | Bearish continuation |
| 32 | `CDLTHRUSTING` | Thrusting | 2 | Low | Bearish continuation |

## Indecision Patterns (5 patterns)

Patterns indicating market indecision — potential inflection points.

| # | Function | Name | Bars | Reliability | Crypto Notes |
|---|---|---|---|---|---|
| 33 | `CDLDOJI` | Doji | 1 | Medium | Very common on low TFs |
| 34 | `CDLDRAGONFLYDOJI` | Dragonfly Doji | 1 | Medium | Bullish bias at support |
| 35 | `CDLGRAVESTONEDOJI` | Gravestone Doji | 1 | Medium | Bearish bias at resistance |
| 36 | `CDLLONGLEGGEDDOJI` | Long-Legged Doji | 1 | Medium | High volatility indecision |
| 37 | `CDLSPINNINGTOP` | Spinning Top | 1 | Low | Very common, weak signal |

## Complex Multi-Bar Patterns (14 patterns)

| # | Function | Name | Bars | Reliability |
|---|---|---|---|---|
| 38 | `CDLADVANCEBLOCK` | Advance Block | 3 | Medium |
| 39 | `CDLBELTHOLD` | Belt Hold | 1 | Low |
| 40 | `CDLBREAKAWAY` | Breakaway | 5 | Medium |
| 41 | `CDLCLOSINGMARUBOZU` | Closing Marubozu | 1 | Medium |
| 42 | `CDLCONCEALBABYSWALL` | Concealing Baby Swallow | 4 | High |
| 43 | `CDLCOUNTERATTACK` | Counterattack | 2 | Medium |
| 44 | `CDLDOJISTAR` | Doji Star | 2 | Medium |
| 45 | `CDLHIGHWAVE` | High Wave | 1 | Low |
| 46 | `CDLHIKKAKE` | Hikkake | 3 | Medium |
| 47 | `CDLHIKKAKEMOD` | Modified Hikkake | 3 | Medium |
| 48 | `CDLHOMINGPIGEON` | Homing Pigeon | 2 | Low |
| 49 | `CDLIDENTICAL3CROWS` | Identical Three Crows | 3 | High |
| 50 | `CDLLADDERBOTTOM` | Ladder Bottom | 5 | Medium |
| 51 | `CDLLONGLINE` | Long Line | 1 | Low |

## Remaining Patterns (10 patterns)

| # | Function | Name | Bars | Reliability |
|---|---|---|---|---|
| 52 | `CDLMARUBOZU` | Marubozu | 1 | High |
| 53 | `CDLMATCHINGLOW` | Matching Low | 2 | Medium |
| 54 | `CDLRICKSHAWMAN` | Rickshaw Man | 1 | Low |
| 55 | `CDLSHORTLINE` | Short Line | 1 | Low |
| 56 | `CDLSTALLEDPATTERN` | Stalled Pattern | 3 | Medium |
| 57 | `CDLSTICKSANDWICH` | Stick Sandwich | 3 | Medium |
| 58 | `CDLTAKURI` | Takuri | 1 | Medium |
| 59 | `CDLTRISTAR` | Tri-Star | 3 | Medium |
| 60 | `CDLUNIQUE3RIVER` | Unique Three River | 3 | Medium |
| 61 | `CDLXSIDEGAP3METHODS` | Side Gap Three Methods | 3 | Medium |

## Reliability Tiers for Crypto

### Tier 1 — Most Reliable on 24/7 Markets
These patterns depend on body ratios, not gaps, so they work well on continuous crypto markets:
- `CDLHAMMER`, `CDLSHOOTINGSTAR` — Single-bar reversal, body/wick ratio based
- `CDLENGULFING` — Two-bar reversal, strong on 4h+ timeframes
- `CDLDOJI` variants — Indecision at key levels
- `CDLMARUBOZU` — Strong momentum candle
- `CDLTHREEWHITESOLDIERS`, `CDLTHREEBLACKCROWS` — Three-bar trend

### Tier 2 — Moderately Reliable
Work on crypto but less frequently than traditional markets:
- `CDLHARAMI`, `CDLHARAMICROSS` — Inside bar patterns
- `CDLPIERCING`, `CDLDARKCLOUDCOVER` — Two-bar patterns
- `CDLRISEFALL3METHODS` — Continuation patterns

### Tier 3 — Less Reliable on Crypto
Gap-dependent patterns that rarely form on 24/7 markets:
- `CDLMORNINGSTAR`, `CDLEVENINGSTAR` — Need session gaps
- `CDLABANDONEDBABY` — Requires true gaps
- `CDLKICKING` — Marubozu with gap
- `CDLTASUKIGAP`, `CDLGAPSIDESIDEWHITE` — Gap-dependent

## Scanning All Patterns

```python
import talib
import numpy as np

def scan_all_patterns(open_: np.ndarray, high: np.ndarray,
                      low: np.ndarray, close: np.ndarray) -> dict:
    """Scan OHLC data for all 61 candlestick patterns."""
    candle_funcs = talib.get_function_groups()["Pattern Recognition"]
    results = {}
    for name in candle_funcs:
        func = getattr(talib, name)
        result = func(open_, high, low, close)
        hits = np.nonzero(result)[0]
        if len(hits) > 0:
            results[name] = {
                "count": len(hits),
                "bars": hits.tolist(),
                "values": result[hits].tolist()
            }
    return results
```

## Combining Patterns with Indicators

Candlestick patterns alone generate many false signals. Combine with trend/momentum:

```python
rsi = talib.RSI(close, timeperiod=14)
hammer = talib.CDLHAMMER(open_, high, low, close)

# Only take bullish hammer when RSI is oversold
confirmed = np.where((hammer > 0) & (rsi < 30), hammer, 0)
```

### Referencia: references/function_reference.md

# TA-Lib Function Reference

Most useful functions by category with syntax, parameters, defaults, and return values.

## Overlap Studies

### SMA — Simple Moving Average
```python
sma = talib.SMA(close, timeperiod=30)
```
- **Parameters**: `timeperiod` (default 30)
- **Returns**: Single array. NaN for first `timeperiod - 1` bars.
- **Use**: Trend direction, dynamic support/resistance.

### EMA — Exponential Moving Average
```python
ema = talib.EMA(close, timeperiod=30)
```
- **Parameters**: `timeperiod` (default 30)
- **Returns**: Single array. NaN for first `timeperiod - 1` bars.
- **Use**: Faster-reacting trend filter than SMA. EMA 12/26 used in MACD.

### BBANDS — Bollinger Bands
```python
upper, middle, lower = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
```
- **Parameters**: `timeperiod` (default 5), `nbdevup` (default 2), `nbdevdn` (default 2), `matype` (0=SMA, 1=EMA, etc.)
- **Returns**: Three arrays (upper, middle, lower). Middle is the moving average.
- **Use**: Volatility bands, mean reversion entries at band touches.

### SAR — Parabolic SAR
```python
sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
```
- **Parameters**: `acceleration` (default 0.02), `maximum` (default 0.2)
- **Returns**: Single array of SAR values.
- **Use**: Trailing stop placement, trend direction (price above SAR = bullish).

### MAMA — MESA Adaptive Moving Average
```python
mama, fama = talib.MAMA(close, fastlimit=0.5, slowlimit=0.05)
```
- **Parameters**: `fastlimit` (default 0.5), `slowlimit` (default 0.05)
- **Returns**: Two arrays (MAMA, FAMA). MAMA crosses above FAMA = bullish.
- **Use**: Adaptive trend following with reduced lag.

### DEMA / TEMA — Double/Triple EMA
```python
dema = talib.DEMA(close, timeperiod=30)
tema = talib.TEMA(close, timeperiod=30)
```
- **Use**: Reduced-lag moving averages for faster signal generation.

### WMA — Weighted Moving Average
```python
wma = talib.WMA(close, timeperiod=30)
```

### KAMA — Kaufman Adaptive Moving Average
```python
kama = talib.KAMA(close, timeperiod=30)
```
- **Use**: Adapts speed based on market noise. Slower in choppy markets, faster in trends.

## Momentum Indicators

### RSI — Relative Strength Index
```python
rsi = talib.RSI(close, timeperiod=14)
```
- **Parameters**: `timeperiod` (default 14)
- **Returns**: Single array, values 0-100. NaN for first `timeperiod` bars.
- **Interpretation**: < 30 oversold, > 70 overbought. Crypto often uses 20/80 thresholds.

### MACD — Moving Average Convergence Divergence
```python
macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
```
- **Parameters**: `fastperiod` (12), `slowperiod` (26), `signalperiod` (9)
- **Returns**: Three arrays (MACD line, signal line, histogram).
- **Interpretation**: MACD crosses above signal = bullish. Histogram shows momentum.

### STOCH — Stochastic Oscillator
```python
slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
```
- **Returns**: Two arrays (SlowK, SlowD), values 0-100.
- **Interpretation**: < 20 oversold, > 80 overbought. K crossing D = signal.

### STOCHRSI — Stochastic RSI
```python
fastk, fastd = talib.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
```
- **Returns**: Two arrays (FastK, FastD), values 0-100.
- **Use**: More sensitive than RSI alone. Popular in crypto analysis.

### CCI — Commodity Channel Index
```python
cci = talib.CCI(high, low, close, timeperiod=14)
```
- **Returns**: Single array, unbounded. Typically oscillates -200 to +200.
- **Interpretation**: > +100 overbought, < -100 oversold.

### WILLR — Williams %R
```python
willr = talib.WILLR(high, low, close, timeperiod=14)
```
- **Returns**: Single array, values -100 to 0.
- **Interpretation**: < -80 oversold, > -20 overbought.

### ADX — Average Directional Index
```python
adx = talib.ADX(high, low, close, timeperiod=14)
```
- **Returns**: Single array, values 0-100.
- **Interpretation**: > 25 trending, < 20 ranging. Does not indicate direction.

### PLUS_DI / MINUS_DI — Directional Indicators
```python
plus_di = talib.PLUS_DI(high, low, close, timeperiod=14)
minus_di = talib.MINUS_DI(high, low, close, timeperiod=14)
```
- **Use**: Combined with ADX. +DI > -DI = bullish trend, -DI > +DI = bearish.

### MFI — Money Flow Index
```python
mfi = talib.MFI(high, low, close, volume, timeperiod=14)
```
- **Returns**: Single array, values 0-100.
- **Interpretation**: Volume-weighted RSI. < 20 oversold, > 80 overbought.

### ROC — Rate of Change
```python
roc = talib.ROC(close, timeperiod=10)
```
- **Returns**: Percentage change over `timeperiod` bars.

### MOM — Momentum
```python
mom = talib.MOM(close, timeperiod=10)
```
- **Returns**: Price difference over `timeperiod` bars (close - close[n]).

## Volume Indicators

### OBV — On Balance Volume
```python
obv = talib.OBV(close, volume)
```
- **Returns**: Cumulative volume series. Rising OBV = buying pressure.

### AD — Chaikin A/D Line
```python
ad = talib.AD(high, low, close, volume)
```
- **Returns**: Accumulation/Distribution line. Divergence from price signals reversals.

### ADOSC — Chaikin A/D Oscillator
```python
adosc = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
```
- **Returns**: Difference between fast and slow A/D EMAs.

## Volatility Indicators

### ATR — Average True Range
```python
atr = talib.ATR(high, low, close, timeperiod=14)
```
- **Returns**: Single array in price units. Higher = more volatile.
- **Use**: Stop-loss placement, position sizing. Common: 2x ATR stop.

### NATR — Normalized ATR
```python
natr = talib.NATR(high, low, close, timeperiod=14)
```
- **Returns**: ATR as percentage of close. Comparable across different price levels.

### TRANGE — True Range
```python
trange = talib.TRANGE(high, low, close)
```
- **Returns**: Single-bar true range (max of high-low, |high-prevclose|, |low-prevclose|).

## Pattern Recognition (Top 20)

All candlestick functions take `(open, high, low, close)` and return integer arrays:
`+100` = bullish, `-100` = bearish, `0` = no pattern. Some return `+200`/`-200` for strong signals.

| Function | Pattern | Bars | Reliability |
|---|---|---|---|
| `CDLDOJI` | Doji | 1 | Medium |
| `CDLHAMMER` | Hammer | 1 | High |
| `CDLINVERTEDHAMMER` | Inverted Hammer | 1 | Medium |
| `CDLSHOOTINGSTAR` | Shooting Star | 1 | High |
| `CDLHANGINGMAN` | Hanging Man | 1 | Medium |
| `CDLENGULFING` | Engulfing | 2 | High |
| `CDLHARAMI` | Harami | 2 | Medium |
| `CDLPIERCING` | Piercing Line | 2 | High |
| `CDLDARKCLOUDCOVER` | Dark Cloud Cover | 2 | High |
| `CDLMORNINGSTAR` | Morning Star | 3 | High |
| `CDLEVENINGSTAR` | Evening Star | 3 | High |
| `CDLMORNINGDOJISTAR` | Morning Doji Star | 3 | High |
| `CDLEVENINGDOJISTAR` | Evening Doji Star | 3 | High |
| `CDLTHREEWHITESOLDIERS` | Three White Soldiers | 3 | High |
| `CDLTHREEBLACKCROWS` | Three Black Crows | 3 | High |
| `CDLMARUBOZU` | Marubozu | 1 | High |
| `CDLSPINNINGTOP` | Spinning Top | 1 | Low |
| `CDLDRAGONFLYDOJI` | Dragonfly Doji | 1 | Medium |
| `CDLGRAVESTONEDOJI` | Gravestone Doji | 1 | Medium |
| `CDLABANDONEDBABY` | Abandoned Baby | 3 | High |

See `candlestick_patterns.md` for the complete list of all 61 patterns.

## Discovering Functions

```python
# List all groups and their functions
groups = talib.get_function_groups()
for group, funcs in groups.items():
    print(f"\n{group} ({len(funcs)}):")
    for f in funcs:
        print(f"  {f}")

# Get info about any function
info = talib.abstract.Function("RSI").info
print(info["display_name"])       # "Relative Strength Index"
print(info["group"])              # "Momentum Indicators"
print(info["parameters"])         # {"timeperiod": 14}
print(info["output_names"])       # ["real"]
```


---

## SKILL: trading-visualization

- Fuente: `agiprolabs/claude-trading-skills` → `skills/trading-visualization` (MIT)
- Cuándo usarla: Professional trading charts including candlesticks, equity curves, drawdowns, correlation heatmaps, and return distributions
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/trading-visualization/` (chart_generator.py, performance_report.py)

# Trading Visualization

Visualization is the primary interface between a trader and their data. Charts reveal patterns that tables and numbers cannot: breakdowns in strategy, regime transitions, clustering of losses, and the shape of risk. A well-designed chart communicates more in a glance than a page of statistics.

**Three uses of trading charts:**

1. **Pattern recognition** — Spot structural changes in price, volume, and momentum that quantitative filters miss.
2. **Strategy evaluation** — Equity curves, drawdown plots, and return distributions expose whether a strategy is robust or curve-fit.
3. **Reporting** — Communicate performance to stakeholders, journals, or your future self with publication-quality visuals.

---

## Chart Types Covered

| Chart Type | Purpose | Library |
|------------|---------|---------|
| Candlestick | OHLCV price action with overlays | mplfinance |
| Equity curve | Portfolio value over time | matplotlib |
| Drawdown | Underwater equity plot | matplotlib |
| Return distribution | Histogram + normal fit | matplotlib |
| Correlation heatmap | Cross-asset correlation matrix | matplotlib / seaborn |
| Trade markers | Entry/exit points on price chart | mplfinance / matplotlib |
| Indicator panels | RSI, MACD below price chart | mplfinance |
| Position timeline | When positions were held | matplotlib |

---

## Libraries

### mplfinance

Best for candlestick charts. Built on matplotlib with finance-specific defaults.

```bash
uv pip install mplfinance
```

```python
import mplfinance as mpf

# Basic candlestick from a DataFrame with DatetimeIndex
# Columns: Open, High, Low, Close, Volume
mpf.plot(df, type="candle", volume=True, style="charles")
```

Key features:
- Native OHLCV support — pass a DataFrame directly
- Built-in volume bars
- `addplot` for overlays (moving averages, Bollinger Bands)
- Custom styles via `mpf.make_mpf_style()`

### matplotlib

General purpose, most flexible. Use when you need full control over layout.

```bash
uv pip install matplotlib
```

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1],
                         sharex=True)
axes[0].plot(dates, equity, color="#00ff88")
axes[1].fill_between(dates, drawdown, 0, color="#ff4444", alpha=0.5)
```

### plotly

Interactive charts rendered as HTML. Best for exploration and dashboards.

```bash
uv pip install plotly
```

```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Candlestick(
    x=df.index, open=df["Open"], high=df["High"],
    low=df["Low"], close=df["Close"]
)])
fig.update_layout(template="plotly_dark")
fig.write_html("chart.html")
```

---

## Styling: Dark Theme Default

Trading terminals use dark backgrounds by default. All charts in this skill follow that convention.

### Quick dark theme setup

```python
import matplotlib.pyplot as plt

plt.style.use("dark_background")
plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#1a1a2e",
    "axes.edgecolor": "#333333",
    "grid.color": "#333333",
    "grid.alpha": 0.4,
    "text.color": "#e0e0e0",
    "xtick.color": "#aaaaaa",
    "ytick.color": "#aaaaaa",
})
```

### Trading color scheme

| Element | Color | Hex |
|---------|-------|-----|
| Bullish / profit | Green | `#00ff88` |
| Bearish / loss | Red | `#ff4444` |
| Neutral / info | Blue | `#4488ff` |
| Warning | Amber | `#ffaa00` |
| MA short | Orange | `#ff6600` |
| MA long | Blue | `#3399ff` |
| MA signal | Yellow | `#ffcc00` |

See `references/styling_guide.md` for complete typography, layout ratios, and export settings.

---

## Chart Composition: Multi-Panel Layout

Most trading charts need multiple synchronized panels — price on top, volume in the middle, indicators at the bottom.

### Stacked panels with shared x-axis

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.05)

ax_price = fig.add_subplot(gs[0])
ax_volume = fig.add_subplot(gs[1], sharex=ax_price)
ax_rsi = fig.add_subplot(gs[2], sharex=ax_price)

# Hide x-tick labels on upper panels
ax_price.tick_params(labelbottom=False)
ax_volume.tick_params(labelbottom=False)
```

### Panel height ratios

| Layout | Ratios | Use Case |
|--------|--------|----------|
| Price + Volume | `[3, 1]` | Simple OHLCV chart |
| Price + Volume + Indicator | `[3, 1, 1]` | Standard analysis view |
| Equity + Drawdown | `[2, 1]` | Performance review |
| Price + RSI + MACD | `[3, 1, 1]` | Full indicator stack |

---

## Candlestick Charts with Overlays

```python
import mplfinance as mpf
import pandas as pd

# df: DataFrame with DatetimeIndex, columns Open/High/Low/Close/Volume
ema20 = df["Close"].ewm(span=20).mean()
ema50 = df["Close"].ewm(span=50).mean()

ap = [
    mpf.make_addplot(ema20, color="#ff6600", width=1.2),
    mpf.make_addplot(ema50, color="#3399ff", width=1.2),
]

style = mpf.make_mpf_style(
    base_mpf_style="nightclouds",
    marketcolors=mpf.make_marketcolors(
        up="#00ff88", down="#ff4444",
        wick={"up": "#00ff88", "down": "#ff4444"},
        edge={"up": "#00ff88", "down": "#ff4444"},
        volume={"up": "#00ff88", "down": "#ff4444"},
    ),
    facecolor="#1a1a2e", figcolor="#1a1a2e",
    gridcolor="#333333", gridstyle="--",
)

mpf.plot(df, type="candle", style=style, addplot=ap,
         volume=True, figsize=(14, 8),
         title="Token / SOL — 15m", savefig="candles.png")
```

---

## Equity Curve with Drawdown Panel

```python
import numpy as np
import matplotlib.pyplot as plt

def plot_equity_drawdown(equity: pd.Series, title: str = "Portfolio") -> plt.Figure:
    """Plot equity curve with drawdown panel below."""
    peak = equity.cummax()
    drawdown = (equity - peak) / peak

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8),
                                    height_ratios=[2, 1], sharex=True)
    ax1.plot(equity.index, equity, color="#00ff88", linewidth=1.5)
    ax1.plot(equity.index, peak, color="#555555", linewidth=0.8,
             linestyle="--", label="Peak")
    ax1.set_title(title, fontsize=14, fontweight="bold", color="white")
    ax1.set_ylabel("Portfolio Value", fontsize=11)
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)

    ax2.fill_between(equity.index, drawdown, 0, color="#ff4444", alpha=0.5)
    ax2.set_ylabel("Drawdown", fontsize=11)
    ax2.set_xlabel("Date", fontsize=11)
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig
```

---

## Return Distribution

```python
from scipy import stats

def plot_return_distribution(returns: pd.Series) -> plt.Figure:
    """Histogram of returns with normal fit and risk metrics."""
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(returns, bins=50, density=True, alpha=0.7,
            color="#4488ff", edgecolor="#333333")

    # Normal fit overlay
    mu, sigma = returns.mean(), returns.std()
    x = np.linspace(returns.min(), returns.max(), 200)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color="#ffaa00",
            linewidth=2, label=f"Normal(μ={mu:.4f}, σ={sigma:.4f})")

    # VaR line
    var_95 = returns.quantile(0.05)
    ax.axvline(var_95, color="#ff4444", linestyle="--",
               label=f"VaR 95%: {var_95:.4f}")

    ax.set_title("Return Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Return", fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig
```

---

## Correlation Heatmap

```python
def plot_correlation_heatmap(returns_df: pd.DataFrame) -> plt.Figure:
    """Correlation matrix heatmap with annotations."""
    corr = returns_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)

    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                    ha="center", va="center", fontsize=9,
                    color="black" if abs(corr.iloc[i, j]) < 0.5 else "white")

    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Correlation Matrix", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig
```

---

## Trade Markers on Price Chart

```python
def plot_trades_on_price(
    price: pd.Series,
    entries: pd.DataFrame,  # columns: date, price, side
    exits: pd.DataFrame,    # columns: date, price, pnl
) -> plt.Figure:
    """Price chart with entry/exit markers."""
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(price.index, price, color="#aaaaaa", linewidth=1)

    # Entry markers
    buy_mask = entries["side"] == "long"
    ax.scatter(entries.loc[buy_mask, "date"], entries.loc[buy_mask, "price"],
               marker="^", color="#00ff88", s=100, zorder=5, label="Buy")
    ax.scatter(entries.loc[~buy_mask, "date"], entries.loc[~buy_mask, "price"],
               marker="v", color="#ff4444", s=100, zorder=5, label="Short")

    # Exit markers
    win_mask = exits["pnl"] > 0
    ax.scatter(exits.loc[win_mask, "date"], exits.loc[win_mask, "price"],
               marker="x", color="#00ff88", s=80, zorder=5)
    ax.scatter(exits.loc[~win_mask, "date"], exits.loc[~win_mask, "price"],
               marker="x", color="#ff4444", s=80, zorder=5)

    ax.set_title("Trades on Price", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig
```

---

## Output Formats

| Format | Method | Use Case |
|--------|--------|----------|
| PNG | `fig.savefig("chart.png", dpi=150)` | Sharing, embedding |
| SVG | `fig.savefig("chart.svg")` | Editing, scaling |
| HTML | `fig.write_html("chart.html")` (plotly) | Interactive exploration |
| Inline | `plt.show()` | Jupyter notebooks |

### Saving with dark background

```python
fig.savefig("chart.png", dpi=150, facecolor=fig.get_facecolor(),
            edgecolor="none", bbox_inches="tight")
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `pandas-ta` | Compute indicators, pass to addplot overlays |
| `vectorbt` | Extract equity curve and trade list for visualization |
| `portfolio-analytics` | Plot Sharpe, drawdown, and return metrics |
| `risk-management` | Visualize position limits and exposure over time |
| `position-sizing` | Chart position size vs account equity over time |
| `regime-detection` | Color background by detected market regime |
| `correlation-analysis` | Generate correlation heatmaps from return data |

---

## Files

### References
- `references/chart_recipes.md` — Complete code recipes for six common chart types
- `references/styling_guide.md` — Dark theme setup, colors, typography, layout, and export settings

### Scripts
- `scripts/chart_generator.py` — Generate four chart types from synthetic data (candlestick, equity, returns, trades)
- `scripts/performance_report.py` — Multi-chart performance report with summary statistics

### Referencia: references/chart_recipes.md

# Chart Recipes

Copy-paste-ready recipes for six common trading chart types with dark theme styling.

## Recipe 1: Candlestick with Moving Averages

```python
import pandas as pd
import mplfinance as mpf

def candlestick_with_ma(df: pd.DataFrame, short: int = 20, long: int = 50,
                        save_path: str = "candles.png") -> None:
    """Candlestick chart with EMA overlays and volume bars."""
    ema_short = df["Close"].ewm(span=short).mean()
    ema_long = df["Close"].ewm(span=long).mean()

    ap = [
        mpf.make_addplot(ema_short, color="#ff6600", width=1.2,
                         label=f"EMA {short}"),
        mpf.make_addplot(ema_long, color="#3399ff", width=1.2,
                         label=f"EMA {long}"),
    ]

    mc = mpf.make_marketcolors(
        up="#00ff88", down="#ff4444",
        wick={"up": "#00ff88", "down": "#ff4444"},
        edge={"up": "#00ff88", "down": "#ff4444"},
        volume={"up": "#00ff88", "down": "#ff4444"},
    )
    style = mpf.make_mpf_style(
        base_mpf_style="nightclouds", marketcolors=mc,
        facecolor="#1a1a2e", figcolor="#1a1a2e",
        gridcolor="#333333", gridstyle="--",
    )

    mpf.plot(df, type="candle", style=style, addplot=ap,
             volume=True, figsize=(14, 8),
             title="\nCandlestick with EMAs",
             savefig=dict(fname=save_path, dpi=150, facecolor="#1a1a2e"))
```

---

## Recipe 2: Equity Curve with Drawdown

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def equity_with_drawdown(equity: pd.Series,
                         save_path: str = "equity.png") -> plt.Figure:
    """Two-panel chart: equity on top, drawdown filled area below."""
    plt.style.use("dark_background")
    peak = equity.cummax()
    dd = (equity - peak) / peak

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8),
                                    height_ratios=[2, 1], sharex=True)
    fig.patch.set_facecolor("#1a1a2e")
    for ax in (ax1, ax2):
        ax.set_facecolor("#1a1a2e")

    ax1.plot(equity.index, equity, color="#00ff88", linewidth=1.5,
             label="Equity")
    ax1.plot(equity.index, peak, color="#555555", linewidth=0.8,
             linestyle="--", label="Peak")
    ax1.set_ylabel("Portfolio Value", fontsize=11)
    ax1.set_title("Equity Curve", fontsize=14, fontweight="bold")
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3, color="#333333")

    ax2.fill_between(equity.index, dd, 0, color="#ff4444", alpha=0.5)
    ax2.plot(equity.index, dd, color="#ff4444", linewidth=0.8)
    ax2.set_ylabel("Drawdown", fontsize=11)
    ax2.set_xlabel("Date", fontsize=11)
    ax2.grid(True, alpha=0.3, color="#333333")

    fig.tight_layout()
    fig.savefig(save_path, dpi=150, facecolor="#1a1a2e",
                edgecolor="none", bbox_inches="tight")
    return fig
```

---

## Recipe 3: Multi-Indicator Panel (Price + RSI + MACD)

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def multi_indicator_panel(df: pd.DataFrame,
                          save_path: str = "indicators.png") -> plt.Figure:
    """Three-panel chart: price with MAs, RSI, and MACD."""
    plt.style.use("dark_background")
    close = df["Close"]

    # Compute indicators
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9).mean()
    macd_hist = macd_line - signal_line

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))

    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor("#1a1a2e")
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.05)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    for ax in (ax1, ax2, ax3):
        ax.set_facecolor("#1a1a2e")
        ax.grid(True, alpha=0.3, color="#333333")

    # Price panel
    ax1.plot(close.index, close, color="#e0e0e0", linewidth=1.2)
    ax1.plot(close.index, close.rolling(20).mean(), color="#ff6600",
             linewidth=1, label="SMA 20")
    ax1.set_ylabel("Price", fontsize=11)
    ax1.legend(loc="upper left", fontsize=9)
    ax1.tick_params(labelbottom=False)

    # RSI panel
    ax2.plot(rsi.index, rsi, color="#4488ff", linewidth=1)
    ax2.axhline(70, color="#ff4444", linewidth=0.7, linestyle="--")
    ax2.axhline(30, color="#00ff88", linewidth=0.7, linestyle="--")
    ax2.set_ylabel("RSI", fontsize=11)
    ax2.set_ylim(0, 100)
    ax2.tick_params(labelbottom=False)

    # MACD panel
    colors = ["#00ff88" if v >= 0 else "#ff4444" for v in macd_hist]
    ax3.bar(close.index, macd_hist, color=colors, alpha=0.6, width=0.8)
    ax3.plot(close.index, macd_line, color="#4488ff", linewidth=1)
    ax3.plot(close.index, signal_line, color="#ffaa00", linewidth=1)
    ax3.set_ylabel("MACD", fontsize=11)
    ax3.set_xlabel("Date", fontsize=11)

    fig.savefig(save_path, dpi=150, facecolor="#1a1a2e",
                edgecolor="none", bbox_inches="tight")
    return fig
```

---

## Recipe 4: Correlation Heatmap

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def correlation_heatmap(returns_df: pd.DataFrame,
                        save_path: str = "corr.png") -> plt.Figure:
    """Annotated heatmap with diverging red-white-green scale."""
    plt.style.use("dark_background")
    corr = returns_df.corr()
    n = len(corr)

    fig, ax = plt.subplots(figsize=(max(8, n * 1.2), max(6, n)))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    im = ax.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1,
                   aspect="auto")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=10)
    ax.set_yticklabels(corr.columns, fontsize=10)

    for i in range(n):
        for j in range(n):
            val = corr.iloc[i, j]
            color = "black" if abs(val) < 0.5 else "white"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=9, color=color)

    fig.colorbar(im, ax=ax, shrink=0.8, label="Correlation")
    ax.set_title("Asset Correlation Matrix", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, facecolor="#1a1a2e",
                edgecolor="none", bbox_inches="tight")
    return fig
```

---

## Recipe 5: Return Distribution with VaR/CVaR

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def return_distribution(returns: pd.Series,
                        save_path: str = "returns_dist.png") -> plt.Figure:
    """Histogram with normal fit, VaR, and CVaR lines."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    ax.hist(returns, bins=50, density=True, alpha=0.7,
            color="#4488ff", edgecolor="#222222")

    mu, sigma = returns.mean(), returns.std()
    x = np.linspace(returns.min(), returns.max(), 200)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color="#ffaa00",
            linewidth=2, label=f"Normal (μ={mu:.4f}, σ={sigma:.4f})")

    var_95 = float(returns.quantile(0.05))
    cvar_95 = float(returns[returns <= var_95].mean())
    ax.axvline(var_95, color="#ff4444", linestyle="--", linewidth=1.5,
               label=f"VaR 95%: {var_95:.4f}")
    ax.axvline(cvar_95, color="#ff6600", linestyle=":", linewidth=1.5,
               label=f"CVaR 95%: {cvar_95:.4f}")

    ax.set_title("Return Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Return", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, color="#333333")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, facecolor="#1a1a2e",
                edgecolor="none", bbox_inches="tight")
    return fig
```

---

## Recipe 6: Trade Performance Scatter

```python
import pandas as pd
import matplotlib.pyplot as plt

def trade_scatter(trades: pd.DataFrame,
                  save_path: str = "trade_scatter.png") -> plt.Figure:
    """Scatter plot: return vs holding period, colored by win/loss."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    wins = trades[trades["return_pct"] >= 0]
    losses = trades[trades["return_pct"] < 0]

    ax.scatter(wins["hold_hours"], wins["return_pct"],
               s=wins["size_usd"] / 10, color="#00ff88", alpha=0.6,
               label=f"Wins ({len(wins)})")
    ax.scatter(losses["hold_hours"], losses["return_pct"],
               s=losses["size_usd"].abs() / 10, color="#ff4444", alpha=0.6,
               label=f"Losses ({len(losses)})")

    ax.axhline(0, color="#555555", linewidth=0.8)
    ax.set_xlabel("Holding Period (hours)", fontsize=11)
    ax.set_ylabel("Return %", fontsize=11)
    ax.set_title("Trade Performance", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, color="#333333")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, facecolor="#1a1a2e",
                edgecolor="none", bbox_inches="tight")
    return fig
```

### Referencia: references/styling_guide.md

# Styling Guide

Complete reference for dark theme trading chart aesthetics: colors, typography, layout ratios, and export settings.

---

## Dark Theme Setup

### Method 1: Style sheet + rcParams override

```python
import matplotlib.pyplot as plt

plt.style.use("dark_background")
plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#1a1a2e",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#e0e0e0",
    "axes.titleweight": "bold",
    "grid.color": "#333333",
    "grid.alpha": 0.4,
    "grid.linestyle": "--",
    "text.color": "#e0e0e0",
    "xtick.color": "#aaaaaa",
    "ytick.color": "#aaaaaa",
    "legend.facecolor": "#1a1a2e",
    "legend.edgecolor": "#333333",
    "figure.figsize": [14, 8],
    "savefig.facecolor": "#1a1a2e",
    "savefig.edgecolor": "none",
    "savefig.dpi": 150,
})
```

### Method 2: Per-figure styling (no global mutation)

```python
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#1a1a2e")
ax.spines["bottom"].set_color("#333333")
ax.spines["left"].set_color("#333333")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(colors="#aaaaaa")
ax.grid(True, alpha=0.3, color="#333333", linestyle="--")
```

### Method 3: mplfinance custom style

```python
import mplfinance as mpf

mc = mpf.make_marketcolors(
    up="#00ff88", down="#ff4444",
    wick={"up": "#00ff88", "down": "#ff4444"},
    edge={"up": "#00ff88", "down": "#ff4444"},
    volume={"up": "#00ff88", "down": "#ff4444"},
)
dark_style = mpf.make_mpf_style(
    base_mpf_style="nightclouds",
    marketcolors=mc,
    facecolor="#1a1a2e",
    figcolor="#1a1a2e",
    gridcolor="#333333",
    gridstyle="--",
    y_on_right=True,
)
```

---

## Color Palette

### Primary trading colors

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Bullish / Profit | Green | `#00ff88` | (0, 255, 136) |
| Bearish / Loss | Red | `#ff4444` | (255, 68, 68) |
| Neutral / Info | Blue | `#4488ff` | (68, 136, 255) |
| Warning / Caution | Amber | `#ffaa00` | (255, 170, 0) |
| Background | Dark navy | `#1a1a2e` | (26, 26, 46) |
| Grid / Border | Dark gray | `#333333` | (51, 51, 51) |
| Text primary | Light gray | `#e0e0e0` | (224, 224, 224) |
| Text secondary | Mid gray | `#aaaaaa` | (170, 170, 170) |
| Muted element | Dim gray | `#555555` | (85, 85, 85) |

### Moving average colors

| Line | Color | Hex |
|------|-------|-----|
| MA short (10-20) | Orange | `#ff6600` |
| MA medium (50) | Blue | `#3399ff` |
| MA long (100-200) | Yellow | `#ffcc00` |

### Multi-series palette (for 5+ overlapping lines)

```python
SERIES_COLORS = [
    "#00ff88",  # green
    "#4488ff",  # blue
    "#ff6600",  # orange
    "#ffcc00",  # yellow
    "#cc44ff",  # purple
    "#ff4488",  # pink
    "#00cccc",  # teal
    "#ff8844",  # coral
]
```

### Alternative background: GitHub dark

Use `#0d1117` for a slightly cooler tone matching GitHub's dark mode.

---

## Typography

### Font sizes

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Chart title | 14pt | Bold | `#e0e0e0` |
| Axis label | 11pt | Normal | `#e0e0e0` |
| Tick label | 9pt | Normal | `#aaaaaa` |
| Legend text | 9-10pt | Normal | `#e0e0e0` |
| Annotation | 10pt | Normal | `#e0e0e0` |
| Stat box text | 10pt | Monospace | `#e0e0e0` |

### Applying fonts

```python
ax.set_title("Price Chart", fontsize=14, fontweight="bold", color="#e0e0e0")
ax.set_xlabel("Date", fontsize=11, color="#e0e0e0")
ax.set_ylabel("Price (SOL)", fontsize=11, color="#e0e0e0")
ax.tick_params(axis="both", labelsize=9, colors="#aaaaaa")
ax.legend(fontsize=9, facecolor="#1a1a2e", edgecolor="#333333")
```

### Stat box (performance summary on chart)

```python
stats_text = (
    f"Return: {total_return:.1%}\n"
    f"Sharpe: {sharpe:.2f}\n"
    f"Max DD: {max_dd:.1%}"
)
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
        fontsize=10, fontfamily="monospace", color="#e0e0e0",
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#222233",
                  edgecolor="#333333", alpha=0.9))
```

---

## Layout Principles

### Figure sizes

| Chart Type | Size (inches) | Aspect |
|------------|---------------|--------|
| Full analysis (multi-panel) | `(14, 10)` | Wide |
| Standard chart | `(14, 8)` | Wide |
| Simple plot | `(10, 6)` | Standard |
| Heatmap (square) | `(10, 8)` | Near-square |
| Dashboard tile | `(7, 5)` | Compact |

### Multi-panel height ratios

| Layout | Ratios | Use |
|--------|--------|-----|
| Price + Volume | `[3, 1]` | Basic OHLCV |
| Equity + Drawdown | `[2, 1]` | Performance |
| Price + Vol + Indicator | `[3, 1, 1]` | Full analysis |
| Price + RSI + MACD | `[3, 1, 1]` | Indicator stack |
| 4-panel | `[3, 1, 1, 1]` | Deep analysis |

### Spacing

```python
# Option 1: tight_layout (simple)
fig.tight_layout()

# Option 2: constrained_layout (better for complex)
fig, axes = plt.subplots(3, 1, figsize=(14, 10),
                          constrained_layout=True)

# Option 3: GridSpec with hspace
gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.05)
```

Use `hspace=0.05` for shared-axis panels (price + volume) to make them look connected. Use `hspace=0.15` or `tight_layout()` when panels are independent.

---

## Saving Charts

### Standard save

```python
fig.savefig("chart.png", dpi=150,
            facecolor=fig.get_facecolor(),
            edgecolor="none",
            bbox_inches="tight")
```

### DPI guidelines

| Use | DPI |
|-----|-----|
| Screen / sharing | 150 |
| Presentation | 200 |
| Publication / print | 300 |

### Format comparison

| Format | Size | Quality | Editable | Use |
|--------|------|---------|----------|-----|
| PNG | Medium | Raster | No | Default for sharing |
| SVG | Small | Vector | Yes | Editing, scaling |
| PDF | Medium | Vector | Partial | Reports, papers |
| HTML | Large | Interactive | N/A | Plotly dashboards |

### Transparent background (for embedding)

```python
fig.savefig("chart.png", dpi=150, transparent=True,
            bbox_inches="tight")
```

### Plotly dark template

```python
import plotly.io as pio

pio.templates["trading_dark"] = go.layout.Template(
    layout=dict(
        paper_bgcolor="#1a1a2e",
        plot_bgcolor="#1a1a2e",
        font=dict(color="#e0e0e0"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333"),
    )
)
pio.templates.default = "trading_dark"
```


---

## SKILL: volatility-modeling

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/volatility-modeling` (MIT)
- Cuándo usarla: Model, forecast, and interpret volatility using time-series models and options-implied measures. Use when the user asks about EWMA, GARCH models, implied volatility, volatility surfaces, volatility term structure, or the VIX. Also trigger when users mention 'volatility smile', 'volatility skew', 'realized vs implied vol', 'volatility risk premium', 'vol clustering', 'mean-reverting volatility', 'options pricing inputs', 'RiskMetrics', 'decay factor', or ask how to forecast future volatility for risk management.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/volatility-modeling/` (volatility_modeling.py)

# Volatility Modeling

## Core Concepts

### EWMA (Exponentially Weighted Moving Average)
A simple volatility model that gives more weight to recent observations. RiskMetrics popularized this approach with a standard decay factor.

```
sigma^2_t = lambda * sigma^2_{t-1} + (1 - lambda) * r^2_{t-1}
```

where:
- lambda = decay factor (RiskMetrics standard: 0.94 for daily, 0.97 for monthly)
- r_{t-1} = return in period t-1 (typically demeaned, but for daily returns the mean is often assumed to be zero)
- sigma^2_{t-1} = previous period's variance estimate

**Properties:**
- Assigns exponentially decaying weights to past squared returns.
- Effective window is approximately 1/(1 - lambda) observations. For lambda = 0.94, effective window is approximately 17 days.
- No mean reversion: the model is equivalent to IGARCH (integrated GARCH) where alpha + beta = 1. Volatility shocks persist indefinitely.
- Simple to implement and requires only one parameter.

### GARCH(1,1)
The Generalized Autoregressive Conditional Heteroskedasticity model adds a constant term that induces mean reversion in volatility.

```
sigma^2_t = omega + alpha * r^2_{t-1} + beta * sigma^2_{t-1}
```

where:
- omega > 0: constant term (determines long-run variance level)
- alpha >= 0: reaction coefficient (sensitivity to recent shocks)
- beta >= 0: persistence coefficient (memory of past variance)

**Stationarity condition:** alpha + beta < 1. This ensures the process is covariance-stationary and mean-reverting.

**Long-run (unconditional) variance:**

```
V_L = omega / (1 - alpha - beta)
```

Long-run annualized volatility: sigma_L = sqrt(V_L * 252).

**Persistence:** The quantity alpha + beta measures how quickly volatility reverts to its long-run level. Higher persistence means slower mean reversion.

**Half-life of volatility shocks:** The number of periods for a volatility shock to decay by half:

```
h = -ln(2) / ln(alpha + beta)
```

Since alpha + beta < 1, ln(alpha + beta) < 0, and h is positive.

**Multi-step forecasts:** The h-step-ahead GARCH(1,1) forecast:

```
E[sigma^2_{t+h}] = V_L + (alpha + beta)^h * (sigma^2_t - V_L)
```

The forecast converges to V_L as h approaches infinity.

### Implied Volatility
The volatility value that, when plugged into an option pricing model (typically Black-Scholes), produces a theoretical price equal to the observed market price.

For a European call under Black-Scholes:

```
C = S * N(d1) - K * exp(-rT) * N(d2)

d1 = [ln(S/K) + (r + sigma^2/2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```

Implied volatility is the sigma that solves C_model(sigma) = C_market. There is no closed-form solution; it must be found numerically (e.g., Newton-Raphson, bisection).

### Volatility Smile and Skew
In practice, implied volatility varies by strike price, contradicting the constant-volatility assumption of Black-Scholes.

- **Volatility smile:** IV is higher for both deep in-the-money and deep out-of-the-money options, forming a U-shape. Common in FX markets.
- **Volatility skew (smirk):** IV increases for lower strikes (OTM puts have higher IV than OTM calls). This is the dominant pattern in equity markets and reflects demand for downside protection and the reality of fat left tails.
- **Skew is often quantified** as the difference in IV between a 25-delta put and a 25-delta call, or between 90% moneyness and 110% moneyness strikes.

### Volatility Term Structure
Implied volatility varies across option expiration dates.

- **Normal (upward-sloping):** Longer-dated options have higher IV. Reflects uncertainty increasing over time.
- **Inverted (downward-sloping):** Near-term IV exceeds long-term IV. Common during market stress when short-term uncertainty spikes (e.g., around earnings, elections, crises).
- **Humped:** IV peaks at an intermediate maturity. May occur around a specific anticipated event.

### Volatility Surface
The two-dimensional surface of implied volatility across both strike (or delta/moneyness) and maturity. The volatility surface is the most complete representation of the options market's view of future uncertainty.

Practitioners interpolate the surface to price options at arbitrary strike/maturity combinations. Surface dynamics (how the surface shifts, tilts, and bends) are critical for options portfolio risk management.

### Realized vs Implied Volatility: The Volatility Risk Premium
Implied volatility systematically exceeds subsequent realized volatility on average. This gap is the **volatility risk premium (VRP)**.

```
VRP = IV - RV_subsequent
```

The VRP exists because investors are willing to pay a premium for options (insurance), and option sellers demand compensation for bearing tail risk. The VRP is typically positive and has been a persistent source of return for volatility sellers.

Key considerations:
- The VRP varies over time and is larger during periods of market stress.
- Selling volatility (harvesting VRP) earns a steady premium but is exposed to large, infrequent losses.
- The VRP can turn negative during extreme events.

### VIX Index
The CBOE Volatility Index measures the market's expectation of 30-day forward volatility, derived from S&P 500 option prices.

- VIX is quoted in annualized percentage points (e.g., VIX = 20 means approximately 20% expected annualized vol).
- VIX is computed from a wide strip of OTM put and call options, not from the Black-Scholes model.
- VIX levels: 12-15 = low/complacent, 15-20 = normal, 20-30 = elevated, 30+ = high stress, 40+ = crisis.
- VIX has strong mean-reverting properties and tends to spike during market selloffs ("fear gauge").

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| EWMA Variance | sigma^2_t = lambda * sigma^2_{t-1} + (1-lambda) * r^2_{t-1} | Simple volatility forecast |
| GARCH(1,1) Variance | sigma^2_t = omega + alpha * r^2_{t-1} + beta * sigma^2_{t-1} | Mean-reverting vol forecast |
| GARCH Long-Run Variance | V_L = omega / (1 - alpha - beta) | Unconditional variance level |
| GARCH Half-Life | h = -ln(2) / ln(alpha + beta) | Speed of mean reversion |
| GARCH h-Step Forecast | V_L + (alpha+beta)^h * (sigma^2_t - V_L) | Multi-period vol forecast |
| Black-Scholes Call | S * N(d1) - K * exp(-rT) * N(d2) | Option pricing (IV extraction) |
| Volatility Risk Premium | IV - RV_subsequent | Premium earned by vol sellers |
| EWMA Effective Window | approximately 1 / (1 - lambda) | Implicit lookback period |

## Worked Examples

### Example 1: EWMA Variance Update
**Given:** Yesterday's variance estimate sigma^2_{t-1} = 0.0004 (daily vol = 2%), yesterday's return r_{t-1} = -3% (i.e., r = -0.03), and lambda = 0.94.

**Calculate:** Today's EWMA variance estimate and daily volatility.

**Solution:**

```
sigma^2_t = 0.94 * 0.0004 + (1 - 0.94) * (-0.03)^2
          = 0.94 * 0.0004 + 0.06 * 0.0009
          = 0.000376 + 0.000054
          = 0.000430
```

Daily volatility:

```
sigma_t = sqrt(0.000430) = 0.02074 = 2.074%
```

The large negative return (-3%) caused the volatility estimate to increase from 2.0% to 2.074%. The EWMA responded to the shock, but the high lambda (0.94) dampened the reaction.

### Example 2: GARCH(1,1) Long-Run Volatility and Half-Life
**Given:** GARCH(1,1) parameters estimated from daily S&P 500 returns: omega = 0.000002, alpha = 0.08, beta = 0.91.

**Calculate:** Long-run daily variance, long-run annualized volatility, and half-life of volatility shocks.

**Solution:**

**Stationarity check:** alpha + beta = 0.08 + 0.91 = 0.99 < 1 (stationary, but highly persistent).

**Long-run variance:**

```
V_L = 0.000002 / (1 - 0.99) = 0.000002 / 0.01 = 0.0002
```

**Long-run daily volatility:**

```
sigma_L = sqrt(0.0002) = 0.01414 = 1.414%
```

**Annualized:**

```
sigma_annual = 0.01414 * sqrt(252) = 22.45%
```

**Half-life:**

```
h = -ln(2) / ln(0.99) = -0.6931 / (-0.01005) = 68.97 ~ 69 trading days
```

Interpretation: After a volatility shock, it takes approximately 69 trading days (about 3 months) for the excess volatility to decay by half. This high persistence (alpha + beta = 0.99) is typical for equity index returns.

### Example 3: Implied Volatility Interpretation
**Given:** A stock trades at $100. A 3-month ATM call (K = $100) trades at $6.50. The risk-free rate is 5%. Using Black-Scholes, the implied volatility is determined (via numerical solver) to be 30%.

**Calculate:** What does this tell us, and how does it compare to realized vol of 22%?

**Solution:**

The implied volatility of 30% represents the market's consensus forecast of annualized volatility over the next 3 months, as embedded in option prices.

Comparing to realized (historical) volatility of 22%:

```
VRP = IV - RV = 30% - 22% = 8%
```

The positive 8-percentage-point gap is the volatility risk premium. Possible interpretations:
- The market expects volatility to rise above recent realized levels.
- Option sellers are demanding a premium for bearing tail risk.
- There may be an upcoming event (earnings, regulatory decision) that could cause a volatility spike.

A systematic vol-selling strategy would sell this option, expecting to profit from the VRP if realized vol remains near 22%. However, the seller bears the risk that realized vol could exceed 30%.

## Common Pitfalls
- **GARCH stationarity:** alpha + beta must be strictly less than 1 for the GARCH(1,1) process to be covariance-stationary. If alpha + beta >= 1, the long-run variance is undefined and the model is IGARCH (or explosive). Always check this condition after estimation.
- **EWMA has no mean reversion:** EWMA is equivalent to IGARCH (alpha + beta = 1), so volatility shocks never decay. This makes EWMA unsuitable for long-horizon volatility forecasts where mean reversion is expected.
- **Implied volatility is model-dependent:** IV extracted using Black-Scholes assumes log-normal returns, constant volatility, continuous trading, and no jumps. The "smile" and "skew" exist precisely because these assumptions are violated. IV is a quoting convention, not a true forecast.
- **Conflating historical vol with forward-looking vol:** Historical (realized) volatility measures what has happened. Implied volatility reflects market expectations about the future. They address different questions and can diverge substantially.
- **Using daily GARCH for long-horizon forecasts without term structure adjustment:** Daily GARCH forecasts converge to the unconditional variance at long horizons. Use the multi-step forecast formula E[sigma^2_{t+h}] = V_L + (alpha+beta)^h * (sigma^2_t - V_L) and aggregate appropriately.
- **Overfitting GARCH models:** Higher-order GARCH(p,q) models or extensions (EGARCH, TGARCH, GJR-GARCH) can overfit in-sample. GARCH(1,1) is remarkably hard to beat out-of-sample for most financial return series. Start with GARCH(1,1) and justify added complexity.
- **Lambda selection for EWMA:** The choice of lambda significantly affects responsiveness. lambda = 0.94 responds quickly to shocks (effective window approximately 17 days); lambda = 0.97 is smoother (effective window approximately 33 days). The choice should match the application's horizon.

## Cross-References
- **historical-risk** (wealth-management plugin): Close-to-close, Parkinson, and Yang-Zhang volatility estimators provide the realized volatility benchmarks against which GARCH forecasts and implied volatility are compared.
- **forward-risk** (wealth-management plugin): Volatility forecasts from EWMA and GARCH are direct inputs to parametric and Monte Carlo VaR calculations.
- **performance-metrics** (wealth-management plugin): Volatility estimates affect the denominators of Sharpe, Sortino, and other risk-adjusted ratios. Using forward-looking (GARCH) volatility can produce conditional performance ratios.

## Running the script

```
uv run scripts/volatility_modeling.py
```

The PEP 723 header resolves the numpy and scipy dependencies automatically. Alternatively run `python3 scripts/volatility_modeling.py` after `pip install numpy scipy`.

- Bare run prints a demo on synthetic GARCH-dynamics returns: EWMA volatility, GARCH(1,1) estimation and multi-step forecasts, realized and Parkinson volatility, term structure, and a volatility cone.
- `--verify` re-runs the key computations and asserts the outputs match this skill's worked examples (prints PASS/FAIL, nonzero exit on mismatch).
- `--help` lists the available class and methods.

The file is primarily meant to be imported as a module, e.g. `from volatility_modeling import VolatilityModeling`.


---

## SKILL: volatility-modeling

- Fuente: `agiprolabs/claude-trading-skills` → `skills/volatility-modeling` (MIT)
- Cuándo usarla: Volatility estimation, forecasting, and regime classification using GARCH, EWMA, realized volatility, and volatility cones
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/volatility-modeling/` (estimate_volatility.py, vol_forecast.py)

# Volatility Modeling

Volatility — the magnitude of price fluctuations — is arguably the single most
important quantity in trading.  It drives position sizing, stop placement, option
pricing, and regime detection.  This skill covers estimation, forecasting, and
practical application of volatility in crypto markets.

## Why Volatility Matters

| Use Case | How Volatility Is Used |
|---|---|
| **Position sizing** | Scale position inversely with vol so each trade risks a consistent dollar amount |
| **Stop placement** | ATR-based stops widen in high-vol regimes, tighten in low-vol |
| **Strategy selection** | Mean-reversion works in low vol; momentum works in high vol |
| **Risk budgeting** | Vol-target portfolios maintain constant portfolio-level risk |
| **Regime detection** | Vol regime shifts signal changing market dynamics |
| **Option pricing** | Implied vs realized vol gap creates trading opportunities |

## Types of Volatility

### Historical (Realized) Volatility
Computed from observed past returns.  The most common and directly measurable
form.  Multiple estimators exist with different statistical efficiency.

### Implied Volatility
Derived from option prices via Black-Scholes or similar models.  Limited in
crypto DeFi where liquid options markets are sparse, but available on Deribit
for BTC/ETH.

### Forecast Volatility
Predicted future volatility from models like EWMA or GARCH.  Used for
forward-looking position sizing and risk budgets.

---

## Estimation Methods

### 1. Close-to-Close (Standard Deviation of Log Returns)

The simplest estimator.  Compute the standard deviation of log returns and
annualize.

```python
import numpy as np

log_returns = np.log(closes[1:] / closes[:-1])
vol_daily = np.std(log_returns, ddof=1)
vol_annual = vol_daily * np.sqrt(365)  # crypto trades 365 days
```

- **Pros**: Simple, widely understood.
- **Cons**: Uses only close prices — ignores intraday range.

### 2. Parkinson (High-Low Range)

Uses the daily high-low range, which is ~5x more statistically efficient than
close-to-close.

```python
hl_ratio = np.log(highs / lows)
vol_parkinson = np.sqrt(np.mean(hl_ratio**2) / (4 * np.log(2))) * np.sqrt(365)
```

- **Pros**: More efficient, captures intraday moves.
- **Cons**: Downward bias with discrete sampling; ignores close-to-close jumps.

### 3. Garman-Klass (OHLC)

The most efficient single-day OHLC estimator.

```python
hl = np.log(highs / lows)
co = np.log(closes / opens)
gk = np.mean(0.5 * hl**2 - (2 * np.log(2) - 1) * co**2)
vol_gk = np.sqrt(gk) * np.sqrt(365)
```

- **Pros**: Best efficiency among OHLC estimators.
- **Cons**: Assumes no drift; sensitive to opening gaps.

### 4. Yang-Zhang

Combines overnight (close-to-open) and open-to-close components.  Handles
gaps properly.  Less relevant for 24/7 crypto but useful for tokens with
sporadic trading.

### 5. EWMA (Exponentially Weighted Moving Average)

RiskMetrics approach — no parameters to estimate beyond λ.

```python
lam = 0.94  # RiskMetrics default for daily
ewma_var = np.zeros(len(returns))
ewma_var[0] = returns[0] ** 2
for t in range(1, len(returns)):
    ewma_var[t] = lam * ewma_var[t - 1] + (1 - lam) * returns[t - 1] ** 2
vol_ewma = np.sqrt(ewma_var) * np.sqrt(365)
```

- λ = 0.94 for daily data (RiskMetrics).
- λ = 0.97 for weekly data.
- Higher λ → smoother, slower reaction to new information.

### 6. GARCH(1,1)

The workhorse autoregressive volatility model.  Captures volatility clustering.

```
σ²_t = ω + α · r²_{t-1} + β · σ²_{t-1}
```

- **ω**: long-run variance weight.
- **α**: reaction to recent shock (typically 0.05–0.15 for crypto).
- **β**: persistence (typically 0.80–0.90 for crypto).
- **α + β < 1**: stationarity constraint.
- **Long-run variance**: ω / (1 − α − β).

Estimated via maximum likelihood.  See `references/estimators.md` for details.

---

## Volatility Cones

Volatility cones show the percentile distribution of realized volatility at
different lookback windows, revealing whether current vol is historically
high or low.

### Construction
1. Get 1+ years of daily data.
2. For each lookback window (5, 10, 20, 60, 120 days):
   - Compute rolling realized volatility.
   - Extract percentiles: 5th, 25th, 50th, 75th, 95th.
3. Plot percentiles vs window length — the "cone" shape.
4. Overlay current realized vol at each window.

### Interpretation
- **Current vol > 75th percentile**: historically elevated — expect mean reversion.
- **Current vol < 25th percentile**: historically compressed — expect expansion.
- **Cone narrowing at longer windows**: vol mean-reverts over longer horizons.

See `references/volatility_cones.md` for full methodology and worked examples.

---

## Crypto Volatility Characteristics

Crypto vol differs from traditional assets in important ways:

| Characteristic | Detail |
|---|---|
| **Level** | 50–150% annualized is typical; TradFi equities are 15–25% |
| **Clustering** | Strong — high-vol days cluster together |
| **Weekday patterns** | Weekend vol often lower but weekend gaps can be large |
| **Volume correlation** | Vol and volume are positively correlated |
| **Regime dependence** | Bull market vol ≠ bear market vol; ranges are different |
| **Mean reversion** | Vol mean-reverts more reliably than price |
| **Tail risk** | Fat tails — more extreme moves than normal distribution predicts |

### Regime Classification by Volatility

| Regime | Annualized Vol Range | Characteristics |
|---|---|---|
| Low vol | < 40% | Range-bound, mean reversion works |
| Normal vol | 40–80% | Trending possible, balanced strategies |
| High vol | 80–120% | Strong trends or sharp reversals |
| Crisis vol | > 120% | Liquidation cascades, reduced position size |

---

## Volatility Forecasting

### EWMA Forecast
Simple and effective.  The current EWMA variance estimate *is* the 1-step
forecast.  Multi-step forecasts are flat (same as 1-step).

### GARCH Forecast
GARCH produces a term structure of variance forecasts:

```
σ²_{t+h} = V_L + (α + β)^h · (σ²_t − V_L)
```

Where V_L = ω / (1 − α − β) is the long-run variance.

- Short-horizon forecasts reflect current conditions.
- Long-horizon forecasts converge to long-run variance.
- The speed of convergence depends on α + β (persistence).

See `scripts/vol_forecast.py` for a working implementation.

---

## Practical Applications

### Position Sizing with Volatility
```python
# Vol-target position sizing
target_vol = 0.02  # 2% daily portfolio vol target
current_vol = 0.05  # 5% daily asset vol (annualized ~95%)
weight = target_vol / current_vol  # = 0.40 → 40% allocation
```

See the `position-sizing` skill for complete integration.

### ATR-Based Stop Placement
```python
atr_14 = talib.ATR(highs, lows, closes, timeperiod=14)
stop_distance = 2.0 * atr_14[-1]  # 2x ATR stop
stop_price = entry_price - stop_distance  # for longs
```

### Vol-Regime Strategy Selection
```python
vol_percentile = current_vol_percentile(token, window=30)
if vol_percentile < 25:
    strategy = "mean_reversion"
elif vol_percentile > 75:
    strategy = "momentum_breakout"
else:
    strategy = "balanced"
```

---

## Files

### References
| File | Description |
|---|---|
| `references/estimators.md` | Full derivations and details for all volatility estimators |
| `references/volatility_cones.md` | Cone construction methodology and interpretation guide |

### Scripts
| File | Description |
|---|---|
| `scripts/estimate_volatility.py` | Multi-estimator volatility computation with cone analysis |
| `scripts/vol_forecast.py` | EWMA and GARCH forecasting with term structure output |

---

## Related Skills

- **`regime-detection`** — Classify market regimes using volatility as a key input.
- **`position-sizing`** — Scale positions inversely with volatility.
- **`risk-management`** — Portfolio-level vol targeting and risk budgets.
- **`pandas-ta`** — ATR and Bollinger Bands are volatility-based indicators.
- **`custom-indicators`** — Build crypto-specific volatility indicators.

---

## Dependencies

```bash
uv pip install pandas numpy scipy
```

Optional for live data:
```bash
uv pip install httpx
```

### Referencia: references/estimators.md

# Volatility Estimators — Complete Reference

## Notation

| Symbol | Meaning |
|---|---|
| O_i, H_i, L_i, C_i | Open, High, Low, Close on day i |
| r_i = ln(C_i / C_{i-1}) | Log return |
| n | Number of observations in the estimation window |
| N | Annualization factor (365 for daily crypto, 365×24 for hourly) |

---

## 1. Close-to-Close (Standard Deviation)

The baseline estimator.  Uses only closing prices.

**Formula:**

```
r_i = ln(C_i / C_{i-1})
r̄   = (1/n) Σ r_i
σ_CC = sqrt( (1/(n-1)) Σ (r_i - r̄)² ) × sqrt(N)
```

**Worked example** (5 daily closes: 100, 103, 101, 105, 102):

```
r = [ln(103/100), ln(101/103), ln(105/101), ln(102/105)]
  = [0.02956, -0.01961, 0.03883, -0.02899]
r̄ = 0.00495
var = [(0.02461)² + (-0.02456)² + (0.03388)² + (-0.03394)²] / 3
    = 0.001105
σ_daily = sqrt(0.001105) = 0.03324
σ_annual = 0.03324 × sqrt(365) = 0.635 = 63.5%
```

**Properties:**
- Unbiased with ddof=1.
- Statistical efficiency = 1.0 (reference baseline).
- Ignores all intraday information.

---

## 2. Parkinson (High-Low Range)

Uses the daily high-low range.  More efficient because the range captures
intraday volatility that closes miss.

**Formula:**

```
σ²_P = (1 / (4 n ln2)) Σ (ln(H_i / L_i))²
σ_P  = sqrt(σ²_P) × sqrt(N)
```

**Worked example** (3 days, H/L pairs: 105/98, 103/99, 107/100):

```
ln(H/L) = [ln(105/98), ln(103/99), ln(107/100)]
         = [0.0690, 0.0396, 0.0677]
Σ (ln(H/L))² = 0.004761 + 0.001568 + 0.004583 = 0.010912
σ²_P = 0.010912 / (4 × 3 × 0.6931) = 0.010912 / 8.3178 = 0.001312
σ_daily = sqrt(0.001312) = 0.03622
σ_annual = 0.03622 × sqrt(365) = 0.692 = 69.2%
```

**Properties:**
- Efficiency ≈ 5.2 relative to close-to-close.
- Downward bias with discrete sampling (true range is wider than observed).
- Does not account for close-to-close jumps.

---

## 3. Garman-Klass (OHLC)

Uses all four OHLC prices.  The most efficient single-period estimator
assuming no drift and continuous trading.

**Formula:**

```
σ²_GK = (1/n) Σ [ 0.5 (ln(H_i/L_i))² − (2 ln2 − 1)(ln(C_i/O_i))² ]
σ_GK  = sqrt(σ²_GK) × sqrt(N)
```

Note: `2 ln2 − 1 ≈ 0.3863`.

**Worked example** (2 days, OHLC: [100,105,98,103], [103,107,100,101]):

```
Day 1: 0.5×(ln(105/98))² − 0.3863×(ln(103/100))²
      = 0.5×0.004761 − 0.3863×0.000898 = 0.002381 − 0.000347 = 0.002034
Day 2: 0.5×(ln(107/100))² − 0.3863×(ln(101/103))²
      = 0.5×0.004583 − 0.3863×0.000385 = 0.002292 − 0.000149 = 0.002143
σ²_GK = (0.002034 + 0.002143) / 2 = 0.002089
σ_daily = sqrt(0.002089) = 0.04571
σ_annual = 0.04571 × sqrt(365) = 0.873 = 87.3%
```

**Properties:**
- Efficiency ≈ 7.4 relative to close-to-close.
- Assumes no drift (mean return = 0) — reasonable for short windows.
- Sensitive to opening price accuracy.

---

## 4. Yang-Zhang

Combines overnight (close-to-open), open-to-close, and Rogers-Satchell
components.  Handles overnight gaps correctly.

**Formula:**

```
σ²_YZ = σ²_overnight + k × σ²_open-to-close + (1-k) × σ²_RS
k = 0.34 / (1.34 + (n+1)/(n-1))
```

Where σ²_RS is the Rogers-Satchell estimator:

```
σ²_RS = (1/n) Σ [ ln(H/C)×ln(H/O) + ln(L/C)×ln(L/O) ]
```

**Properties:**
- Handles opening jumps (useful for stocks).
- Less relevant for 24/7 crypto markets without gaps.
- Efficiency ≈ 8.0 relative to close-to-close.

---

## 5. EWMA (Exponentially Weighted Moving Average)

RiskMetrics approach.  Recent observations weighted more heavily.

**Formula:**

```
σ²_t = λ × σ²_{t-1} + (1 − λ) × r²_{t-1}
```

**Parameters:**
- λ = 0.94 for daily data (RiskMetrics standard).
- λ = 0.97 for weekly data.
- Higher λ → more smoothing, slower reaction.

**Half-life:** The number of periods for a shock to decay by half:

```
half_life = -ln(2) / ln(λ)
```

- λ = 0.94 → half_life ≈ 11 days.
- λ = 0.97 → half_life ≈ 23 days.

**Properties:**
- No parameters to estimate (just pick λ).
- Reacts to regime changes faster than rolling windows.
- Forecast is flat: E[σ²_{t+h}] = σ²_t for all h.
- Cannot capture mean reversion of vol to long-run level.

**Initialization:** Set σ²_0 = sample variance of first 20 observations.

---

## 6. GARCH(1,1)

Generalized Autoregressive Conditional Heteroskedasticity.

**Formula:**

```
σ²_t = ω + α × ε²_{t-1} + β × σ²_{t-1}
```

Where ε_t = r_t (return shock, assuming zero mean for simplicity).

**Constraints:**
- ω > 0, α ≥ 0, β ≥ 0.
- α + β < 1 (stationarity / finite unconditional variance).

**Long-run (unconditional) variance:**

```
V_L = ω / (1 − α − β)
```

**Multi-step forecast:**

```
E[σ²_{t+h}] = V_L + (α + β)^h × (σ²_t − V_L)
```

Converges to V_L as h → ∞.

**Estimation:** Maximum likelihood with Gaussian or Student-t innovations.

Log-likelihood (Gaussian):

```
L = −(1/2) Σ [ ln(σ²_t) + r²_t / σ²_t ]
```

Optimize over (ω, α, β) using scipy.optimize.minimize with bounds.

**Typical crypto parameters:**

| Parameter | Typical Range | Interpretation |
|---|---|---|
| α | 0.05 – 0.15 | Shock reaction speed |
| β | 0.80 – 0.90 | Persistence |
| α + β | 0.92 – 0.98 | Total persistence |

**Properties:**
- Captures volatility clustering and mean reversion.
- Produces a vol term structure (unlike EWMA).
- Requires numerical optimization.
- Student-t innovations better capture crypto fat tails.

---

## Choosing an Estimator

| Scenario | Recommended Estimator |
|---|---|
| Only closing prices available | Close-to-close |
| OHLC data available, short window | Garman-Klass |
| Need responsive real-time vol | EWMA (λ=0.94) |
| Need forecasts with term structure | GARCH(1,1) |
| Quick percentile-based regime check | Parkinson with rolling window |
| Assets with trading gaps | Yang-Zhang |

### Referencia: references/volatility_cones.md

# Volatility Cones — Reference Guide

## Overview

A volatility cone is a visualization that shows the percentile distribution of
realized volatility across multiple lookback windows.  It answers the question:
"Is current volatility unusually high or low compared to history?"

The name "cone" comes from the shape — shorter lookback windows produce wider
percentile spreads, and the distribution narrows at longer windows due to mean
reversion.

---

## Construction Steps

### Step 1: Gather Data

Collect at least 1 year (ideally 2+) of daily OHLCV data.  More history
produces more reliable percentiles.  For crypto, 1 year may be all that is
available for newer tokens.

### Step 2: Define Lookback Windows

Standard windows for crypto:

| Window | Days | Use Case |
|---|---|---|
| Very short | 5 | Intraday/swing trading |
| Short | 10 | Swing trading |
| Medium | 20 | Position trading |
| Long | 60 | Portfolio management |
| Very long | 120 | Strategic allocation |

### Step 3: Compute Rolling Realized Volatility

For each window length `w`, compute rolling close-to-close or Parkinson vol:

```python
import pandas as pd
import numpy as np

def rolling_realized_vol(
    closes: pd.Series, window: int, annualize: int = 365
) -> pd.Series:
    """Compute rolling annualized close-to-close volatility."""
    log_ret = np.log(closes / closes.shift(1))
    return log_ret.rolling(window).std() * np.sqrt(annualize)
```

This produces a time series of realized vol estimates, one for each date.

### Step 4: Extract Percentiles

For each window, compute the percentile distribution of the rolling vol series:

```python
percentiles = [5, 25, 50, 75, 95]
windows = [5, 10, 20, 60, 120]

cone = {}
for w in windows:
    rv = rolling_realized_vol(closes, w).dropna()
    cone[w] = {p: np.percentile(rv, p) for p in percentiles}
```

### Step 5: Compute Current Volatility

For each window, the current realized vol is simply the most recent value:

```python
current = {}
for w in windows:
    rv = rolling_realized_vol(closes, w)
    current[w] = rv.iloc[-1]
```

### Step 6: Determine Percentile Rank

Where does current vol sit within the historical distribution?

```python
from scipy import stats

current_percentile = {}
for w in windows:
    rv = rolling_realized_vol(closes, w).dropna()
    current_percentile[w] = stats.percentileofscore(rv, rv.iloc[-1])
```

---

## Visualization

Plot percentile bands on y-axis vs window length on x-axis:

```
Annualized Vol (%)
    |
200 |  *                           ← 95th percentile
    | * *
150 |*   *      *
    |     *   * *
100 |      * *   *    *    *       ← 75th percentile
    |       *     *  * *  * *
 80 |              **   **   *     ← 50th (median)
    |                        *
 60 |                    *    *    ← 25th percentile
    |                         *
 40 |                          *   ← 5th percentile
    |________________________________
      5d   10d   20d  60d   120d
              Window Length
```

Overlay the current vol (marked with ●) at each window length.

---

## Interpretation

### Current Vol Above 75th Percentile
- Historically elevated volatility.
- Vol tends to mean-revert → expect compression ahead.
- Reduce position sizes.
- Widen stops to avoid getting shaken out.
- Consider vol-selling strategies if available.

### Current Vol Below 25th Percentile
- Historically compressed volatility.
- Breakout likely coming → expect vol expansion.
- Can take larger positions (risk per unit is lower).
- Tighten stops — when vol is low, small moves are significant.
- Watch for range breakouts.

### Current Vol Near 50th Percentile
- Normal conditions — no special adjustments needed.
- Use standard position sizes and stop distances.

### Cone Shape Analysis

**Steep cone (wide at short windows, narrow at long):**
- Normal mean-reverting vol structure.
- Short-term vol varies widely but long-term vol is stable.

**Flat cone (similar width across windows):**
- Vol regime has been persistent.
- Long-term vol structure may be shifting.

**Inverted at current (current vol higher at long windows):**
- Sustained vol regime — not just a short-term spike.
- May indicate structural market change.

---

## Crypto-Specific Considerations

### Limited History
Many tokens have less than 1 year of trading history.  Cones built from
short histories are unreliable.  Minimum recommended: 180 days of daily data.

### Regime Changes
Bull and bear markets have structurally different vol levels.  A cone built
during a bull market will show misleadingly low percentiles during a crash.

**Mitigation:** Build separate cones for different regimes, or use only
recent history (e.g., 6 months) to capture the current regime.

### Microstructure Noise
Low-cap tokens with thin order books produce noisy price data.  High-low
based estimators (Parkinson) may be inflated by illiquidity spikes.

**Mitigation:** Use close-to-close vol for low-liquidity tokens. Filter
obvious price anomalies before computing vol.

### Multiple Timeframes
For active trading, build cones from hourly data using windows of
24h, 72h, 168h (1 week), 720h (1 month).  Annualize with sqrt(365×24).

---

## Practical Decision Framework

```
current_pctile = percentile_rank(current_vol, historical_vol_series)

if current_pctile > 90:
    action = "Significantly reduce size, widen stops 2x"
elif current_pctile > 75:
    action = "Reduce size 30%, widen stops"
elif current_pctile > 25:
    action = "Normal sizing and stops"
elif current_pctile > 10:
    action = "Can increase size, tighten stops"
else:
    action = "Low vol — watch for breakout, keep tight stops"
```

---

## Combining with Vol Forecast

Volatility cones tell you where current vol sits historically.  Combine with
GARCH forecasts to get forward-looking information:

- **Cone says high + GARCH forecast declining:** Vol likely to compress.
- **Cone says low + GARCH forecast rising:** Breakout underway.
- **Cone says high + GARCH forecast still rising:** Crisis conditions.
- **Cone says low + GARCH forecast flat:** Extended low-vol regime.

See `scripts/estimate_volatility.py` for a complete implementation that
computes cones and overlays current vol with percentile ranks.


---

## SKILL: workflow-automation

- Fuente: `JoelLewis/finance_skills` → `plugins/client-operations/skills/workflow-automation` (MIT)
- Cuándo usarla: Design human-in-the-loop workflow orchestration for securities operations: task routing, approval chains, and SLA monitoring. Use when building multi-level approval chains with dollar thresholds and delegation of authority, enforcing four-eyes (maker-checker) controls, defining escalation rules for aging work items approaching SLA breach, designing human-in-the-loop gates, selecting a workflow engine or BPM platform (Camunda, Pega, ServiceNow), modeling a process as a state machine, adding audit trails for SEC Rule 17a-3/17a-4 or FINRA supervisory obligations, or migrating from email-and-spreadsheet tracking. For zero-touch automation rates and STP measurement, see stp-automation.

# Workflow Automation

## Core Concepts

### 1. BPM Fundamentals for Financial Operations

Business process management (BPM) is the discipline of modeling, executing, monitoring, and improving operational processes. In securities operations, BPM applies to every repeatable process that involves multiple steps, multiple participants, or decision points: account opening, account maintenance requests, transfer processing, corporate action elections, reconciliation break resolution, and billing exception handling.

**Process modeling.** A workflow begins as a process model — a formal representation of the steps, decision points, roles, and data flows in an operational process. The model serves three purposes: (1) it documents how the process works for training, audit, and examination purposes, (2) it provides the blueprint for automation, and (3) it establishes the baseline for measurement and improvement.

**Process modeling notation.** BPMN 2.0 is the industry standard for process modeling; model operational processes with tasks, decision gateways, start/intermediate/end events, and swim lanes per responsible role so that handoffs between operations, compliance, and external systems are explicit and visible.

**Process decomposition.** Complex operations workflows are decomposed into sub-processes. An account opening workflow decomposes into: data collection, KYC verification, document review, custodian submission, confirmation processing, and account activation. Each sub-process can be modeled, automated, and measured independently while the parent process orchestrates the sequence.

**State machines for financial workflows.** Many operations items are best modeled as state machines — an item exists in one of several defined states, and transitions between states are triggered by events or actions. A transfer request might have states: Initiated, Validated, Submitted to ACATS, In Progress, Completed, Rejected, Cancelled. Each transition has a guard condition (e.g., the transition from Validated to Submitted requires all validation checks to pass) and an action (e.g., send ACATS message). State machines enforce that items follow valid paths and prevent invalid transitions (an item cannot move from Initiated to Completed without passing through Validated and Submitted).

### 2. Task Routing and Assignment

Task routing determines which person or team receives a work item when it enters the workflow. Effective routing minimizes queue wait time, balances workload, and ensures items reach someone with the appropriate skill and authority.

**Role-based routing.** The simplest routing strategy. Each task type is assigned to a role (e.g., "Account Opening Analyst," "Transfer Specialist," "Senior Operations Reviewer"), and any person filling that role can pick up the task. Role-based routing is sufficient when all members of a role have equivalent skills and authority.

**Skill-based routing.** Extends role-based routing by matching task attributes to individual skill profiles. A trust account opening routes to analysts certified in entity account processing. A cross-border transfer routes to analysts with international custody experience. Skill-based routing reduces rework by ensuring the first handler has the competence to resolve the item.

**Round-robin assignment.** Tasks are distributed evenly across team members in rotation. Round-robin prevents any one person from being overloaded but does not account for task complexity or individual capacity. It works well when tasks are roughly uniform in effort.

**Workload-based assignment.** Tasks are assigned to the team member with the lowest current workload, measured by the number of open items, the total estimated effort of open items, or a weighted score that considers both. Workload-based assignment adapts to variable throughput across team members and handles uneven task complexity better than round-robin.

**Queue management.** When tasks cannot be immediately assigned (because all qualified team members are at capacity), they enter a queue. Queue management includes: priority ordering within the queue (SLA deadline, dollar value, client tier), visibility into queue depth and wait time for management, and automatic re-routing if a queue exceeds a defined depth or wait-time threshold.

**Capacity planning.** Historical data on task volumes, processing times, and SLA targets feeds capacity models that determine how many staff are needed for each role. Workflow systems capture the data needed for capacity planning: arrival rate (tasks per hour/day), service rate (average processing time per task), and queue wait time.

### 3. Approval Chains and Authorization

Many operations tasks require one or more approvals before proceeding. Approval chains enforce segregation of duties, limit authority by seniority and dollar value, and create a documented decision trail.

**Multi-level approval workflows.** A simple task may require one approval (e.g., standard account maintenance reviewed by a team lead). A high-risk task may require two or three levels (e.g., a large wire transfer reviewed by an operations analyst, then a senior manager, then a compliance officer). The number of approval levels is determined by the risk profile of the task, defined in the firm's delegation of authority matrix.

**Approval matrices by dollar amount and risk level.** A delegation of authority matrix maps task types and dollar thresholds to required approval levels. Example structure:

| Task Type | Amount or Risk | Approval Required |
|---|---|---|
| Cash disbursement | Under $25,000 | Operations analyst |
| Cash disbursement | $25,000 - $100,000 | Operations analyst + team lead |
| Cash disbursement | Over $100,000 | Operations analyst + team lead + operations manager |
| Account transfer (full ACAT) | Any | Operations analyst + supervisory review |
| Journal entry (different registration) | Any | Operations analyst + compliance review |
| Fee waiver or adjustment | Under $500 | Team lead |
| Fee waiver or adjustment | Over $500 | Operations manager |

**Four-eyes principle.** A foundational control in financial services: no single individual should be able to initiate and approve a transaction. The maker-checker pattern requires one person to prepare (make) and a different person to review and approve (check). For high-value or high-risk items, a third reviewer (four-eyes plus) may be required. Workflow systems enforce the four-eyes principle by preventing the initiator from also serving as the approver for the same item.

**Delegation of authority.** When an approver is unavailable (out of office, on leave), the workflow must support delegation — the designated alternate inherits the approval authority for a defined period. Delegation must be: (1) explicitly configured in advance by the primary approver or a system administrator, (2) time-limited (auto-expires at the end of the delegation period), (3) logged (the audit trail records that the delegate approved on behalf of the primary), and (4) restricted (the delegate cannot further delegate).

**Timeout and auto-escalation.** If an approval sits unactioned beyond a defined threshold, the workflow escalates automatically. A first-level escalation sends a reminder to the assigned approver. A second-level escalation notifies the approver's manager. A third-level escalation reassigns the item to an alternate approver. Timeout thresholds are tied to the SLA for the task type — a same-day disbursement cannot wait 24 hours for approval.

### 4. Escalation Rules and SLA Monitoring

Service-level agreements define the expected completion time for each task type. Escalation rules enforce SLAs by triggering progressively urgent actions as items age toward or beyond their deadlines.

**SLA definition per task type.** Each operational task type has a defined SLA based on regulatory requirements, client expectations, and operational capacity. Examples:

| Task Type | SLA Target | Regulatory Driver |
|---|---|---|
| ACAT transfer validation | 3 business days | FINRA Rule 11870 |
| ACAT transfer completion | 6 business days | FINRA Rule 11870 |
| Account maintenance (name change) | 2 business days | Internal service standard |
| Cash disbursement | Same day (if before cutoff) | Client expectation |
| Corporate action election submission | 1 business day before DTC deadline | DTC PTOP/ATOP rules |
| Reconciliation break resolution | 5 business days (standard), 1 business day (high value) | SEC Rule 15c3-3, fiduciary obligation |
| New account opening | 3 business days | Internal service standard |

SLAs are measured from the time the task enters the workflow (not from when it is assigned to an individual) to the time it is completed or resolved.

**Aging thresholds.** Work items are classified by age relative to their SLA:
- **Green** — within the first 50% of the SLA window. No action needed beyond normal processing.
- **Yellow** — between 50% and 80% of the SLA window. The item appears on the priority list and the assigned analyst is prompted to accelerate.
- **Red** — between 80% and 100% of the SLA window. Management is notified. The item is escalated to the next tier if not actively being worked.
- **Breached** — SLA exceeded. A formal breach is recorded. The item is escalated to senior management and included in the SLA breach report.

**Escalation tiers.** Escalation follows a defined chain:
- Tier 1: Notification to the assigned analyst (automated reminder).
- Tier 2: Notification to the team lead with a request to intervene or reassign.
- Tier 3: Notification to the operations manager with a summary of the blocked item and the reason for delay.
- Tier 4: Notification to the head of operations or COO for items that represent regulatory risk or significant client impact.

Each tier includes a defined time interval. If Tier 1 does not resolve the item within the interval, Tier 2 fires automatically.

**Notification cadence.** Escalation notifications follow a frequency schedule: initial alert, then periodic reminders at defined intervals (e.g., every 2 hours for same-day SLAs, every business day for multi-day SLAs). Notification fatigue is a real risk — if escalations fire too frequently or for low-priority items, recipients learn to ignore them. Calibrate notification thresholds to match the urgency and volume of each task type.

**SLA breach handling.** When an SLA is breached, the workflow system records the breach with: the task identifier, the SLA target, the actual completion time (or that the item remains open), the root cause (if determined), and the responsible party. Breach data feeds management reporting, trend analysis, and process improvement prioritization.

**Management reporting.** SLA dashboards provide real-time and historical views:
- Current queue depth by task type and age band (green/yellow/red/breached)
- SLA compliance rate by task type (percentage completed within SLA)
- Trend analysis: SLA compliance over time, identifying improving or degrading processes
- Top breach causes: categorized root causes for the most frequent SLA misses
- Analyst-level metrics: individual throughput, average processing time, SLA compliance

### 5. Process Orchestration Patterns

Orchestration defines how individual tasks are sequenced, parallelized, and conditioned to form a complete workflow.

**Sequential processing.** Tasks execute in a defined order. Each task must complete before the next begins. Example: account maintenance request received, then validated, then executed, then confirmed. Sequential processing is appropriate when each step depends on the output of the previous step.

**Parallel processing.** Multiple tasks execute simultaneously. Example: during account opening, KYC verification, document review, and custodian pre-validation run in parallel because they are independent. A synchronization point (join gateway) waits for all parallel tasks to complete before the workflow proceeds to the next step. Parallel processing reduces total cycle time.

**Conditional branching.** The workflow takes different paths based on data conditions. Example: if the account type is individual, route to the simple opening path; if the account type is trust, route to the entity review path; if the account type is estate, route to the legal documentation review path. Conditional branching is implemented with exclusive (XOR) gateways.

**Sub-process invocation.** A parent workflow delegates a portion of its work to a self-contained sub-process. The sub-process has its own tasks, gateways, and error handling. Example: the account opening workflow invokes a "KYC verification" sub-process that handles identity verification, screening, and risk scoring. Sub-processes promote reuse (the same KYC sub-process is invoked by account opening, account maintenance, and periodic review workflows) and maintainability (changes to KYC logic are made in one place).

**Event-driven triggers.** The workflow starts or advances in response to an external event rather than a timer or human action. Example: a custodian sends a settlement confirmation message, which triggers the reconciliation workflow for that transaction. A corporate action announcement from a data vendor triggers the event setup workflow. Event-driven processing requires a message bus or event broker (Kafka, RabbitMQ, or a cloud-native equivalent) to decouple the event source from the workflow engine.

**Timer-based triggers.** The workflow starts or advances based on a schedule or elapsed time. Example: daily reconciliation runs at 7:00 AM after custodian files arrive. An account maintenance request that has been in "pending documentation" state for 30 calendar days triggers an auto-close workflow. Timer-based triggers are essential for deadline-driven processes like corporate action elections and regulatory filings.

**Human-in-the-loop gates.** At defined points in an otherwise automated workflow, the process pauses and waits for a human decision. Example: an automated KYC check returns a "review required" result; the workflow assigns the review to a compliance analyst and waits for an approve/reject decision before continuing. Human gates should be the exception, not the rule — each gate adds latency and staffing requirements. Design the workflow to minimize human gates by handling the most common cases automatically and reserving human review for genuinely ambiguous items.

### 6. Workflow Engines and Tooling for Financial Services

Selecting a workflow platform for securities operations requires evaluating both technical capabilities and financial-services-specific requirements.

**Platform categories:**
- **Enterprise BPM suites (Pega, Appian).** Full-featured platforms with visual process designers, case management, analytics, and AI-assisted routing. Strong in regulated industries. High license cost, significant implementation effort, and vendor lock-in risk.
- **Open-source workflow engines (Camunda, Flowable, Temporal).** Developer-oriented engines that provide workflow orchestration as code. Camunda supports BPMN 2.0 natively, integrates via REST APIs, and can be self-hosted or SaaS. Lower license cost, greater flexibility, but requires engineering staff to build and maintain.
- **IT service management platforms (ServiceNow).** Originally designed for IT operations but increasingly used for business process workflows. Strong in ticketing, SLA management, and escalation. May require customization to handle securities-specific workflow semantics.
- **Custom-built workflow engines.** Built in-house using state machine libraries, message queues, and database-backed task tables. Maximum flexibility and zero license cost, but high development and maintenance burden. Appropriate when the firm's workflows are highly specialized and commercial platforms cannot accommodate them without excessive customization.

**Evaluation criteria for financial services:**
- **Audit trail completeness.** Every state change, assignment, approval, and escalation must be logged with timestamp, actor, and action. The audit trail must be immutable — entries cannot be modified or deleted. This is non-negotiable for SEC Rule 17a-3/17a-4 compliance.
- **Integration capabilities.** The engine must integrate with custodian systems, portfolio management platforms, CRM, compliance screening tools, and document management systems. REST APIs, message queue connectors, and file-based integration are minimum requirements.
- **Role-based access control.** Fine-grained permissions that restrict who can view, process, approve, and administer each workflow type. FINRA's supervisory obligations (Rule 3110) require that supervisors have visibility into and control over the workflows they oversee.
- **Scalability.** The platform must handle peak volumes (quarter-end rebalancing, corporate action clusters, market volatility events) without degraded performance or SLA breaches.
- **Business continuity.** The workflow engine is a critical operations system. It must support high availability, disaster recovery, and documented failover procedures.

**Build vs. buy.** The decision depends on the firm's size, engineering capability, and workflow complexity. Firms with fewer than 50 operations staff and standard workflows typically benefit from commercial platforms. Firms with large, specialized operations teams and highly customized workflows may find that the cost of customizing a commercial platform exceeds the cost of building a purpose-fit engine.

### 7. Audit Trail and Regulatory Compliance

In regulated financial services, every workflow action is a potential examination artifact. The audit trail must be complete, immutable, and retrievable.

**Every action logged.** The workflow system must record: who performed the action (user identity, not just role), what action was performed (state change, approval, rejection, reassignment, data modification), when the action occurred (timestamp with timezone), why the action was taken (approval reason, rejection reason, override justification), and the data state before and after the action.

**Immutable records.** Audit log entries must be write-once. No user — including administrators — should be able to modify or delete audit entries. This is a direct requirement of SEC Rule 17a-4, which mandates that records be preserved in a non-rewriteable, non-erasable format. Workflow systems that store audit logs in a standard relational database must implement application-level immutability controls or use append-only storage.

**Books-and-records requirements for automated workflows.** SEC Rule 17a-3 requires broker-dealers to create and maintain specified records, including records of all orders, transactions, and communications. When workflows automate the creation, routing, or approval of these records, the workflow itself becomes part of the books and records. The automated rules, decision logic, and configuration that govern the workflow must be documented and preserved alongside the transaction records. If a workflow rule is changed (e.g., the approval threshold for cash disbursements is raised from $25,000 to $50,000), the change must be documented with the effective date, the business justification, and the approver.

**FINRA Rule 3110 (Supervision).** FINRA requires member firms to establish and maintain supervisory systems, including written supervisory procedures, reasonably designed to achieve compliance with applicable securities laws and regulations. When operations workflows enforce supervisory controls (approval chains, exception reviews, compliance gates), the workflow configuration is part of the supervisory system. The workflow design must be reviewed and approved by compliance, and the firm must be able to demonstrate that the workflow enforces the supervisory procedures as written.

**Examination defensibility.** During a regulatory examination (SEC, FINRA, state regulators), examiners may request: a description of the workflow for a specific process, the audit trail for specific transactions or time periods, evidence that approval controls were functioning as designed, documentation of any workflow rule changes, and SLA performance data. The workflow system must support efficient retrieval of this information.

### 8. Measuring Workflow Effectiveness

Quantitative measurement is essential to identify bottlenecks, justify investments, and demonstrate operational improvement.

**Cycle time.** The elapsed time from when a work item enters the workflow to when it reaches a terminal state (completed, rejected, cancelled). Cycle time includes both processing time (time actively being worked) and wait time (time in queues, awaiting approval, waiting for external input). Measuring cycle time by task type and by process step reveals where delays accumulate.

**Throughput.** The number of work items completed per unit time (per hour, per day, per month). Throughput per analyst measures individual productivity. Throughput per process measures operational capacity. Declining throughput with stable volume indicates a capacity or efficiency problem.

**Queue depth.** The number of work items waiting to be processed at any point in time. Persistently growing queue depth indicates that arrival rate exceeds processing capacity. Queue depth by task type identifies which processes are under-resourced or under-automated.

**SLA compliance rate.** The percentage of work items completed within their defined SLA. Calculated as: items completed within SLA divided by total items completed. SLA compliance below target triggers root cause analysis and process improvement.

**Rework rate.** The percentage of work items that are returned to a previous step due to errors, missing information, or rejected approvals. Rework consumes capacity without producing throughput. High rework rates indicate unclear procedures, inadequate training, or poor upstream data quality.

**Automation rate.** The percentage of work items that complete without any human intervention (fully automated, or STP). Automation rate is the inverse of the exception rate. Tracking automation rate over time measures the effectiveness of STP initiatives and rule-based processing enhancements.

**First-contact resolution rate.** The percentage of work items resolved by the first person who touches them, without reassignment or escalation. Low first-contact resolution indicates routing problems (items are reaching the wrong person) or skill gaps (the assigned person cannot resolve the item).

## Worked Examples


Three worked examples — a high-value account transfer approval matrix ($500K/$2M tiers, third-party and senior-investor triggers), Salesforce-based SLA monitoring for account maintenance requests, and a Day -10 through Day 0 escalation timeline for corporate action elections — are in [references/examples.md](references/examples.md); load it when designing a concrete approval chain, SLA program, or escalation framework.

## Common Pitfalls

- **Designing the workflow around the current org chart rather than the process.** Organization structures change. Workflow routing and approval logic should reference roles and authority levels, not named individuals. When a team lead leaves, the workflow should need only a role reassignment, not a redesign.
- **Setting SLA targets without measuring the baseline.** If the current average cycle time for account re-registrations is 8 business days, setting a 2-day SLA without process changes guarantees chronic breaches and erodes confidence in the SLA program.
- **Building approval chains that are too deep.** Each approval tier adds latency. A five-level approval chain for a routine account maintenance request slows processing without adding commensurate risk reduction. Calibrate the number of approval tiers to the actual risk of the task.
- **Ignoring the timeout and delegation problem.** Approval workflows that do not handle approver absence (vacation, illness, turnover) create bottlenecks. Every approval tier must have a configured delegate and a timeout escalation. Without these, a single absent approver can halt an entire process queue.
- **Treating workflow automation as a one-time project.** Workflows require ongoing maintenance: rules change as regulations evolve, SLA targets are adjusted based on operational experience, new task types emerge, and routing logic needs recalibration as teams grow or restructure. Budget for ongoing workflow administration.
- **Failing to log the "why" in the audit trail.** Recording that an item was approved is insufficient. The audit trail must capture the reason for the decision, especially for overrides, exceptions, and rejections. A bare approval/reject stamp without justification does not satisfy SEC or FINRA examination standards.
- **Sending too many notifications.** Escalation systems that fire alerts for every aging item, regardless of priority, train recipients to ignore alerts. Use threshold-based alerting (only alert when a meaningful percentage of the queue is at risk) and prioritize high-value, high-risk items in notifications.
- **Not integrating the workflow engine with downstream systems.** A workflow that tracks task status but requires separate manual entry into the custodian portal, CRM, and portfolio management system does not reduce effort — it adds a layer of tracking on top of the existing work. The workflow engine must trigger actions in downstream systems or the automation is illusory.
- **Modeling every process as a linear sequence.** Real operations workflows have parallel paths, conditional branches, and loops. Forcing a naturally parallel process (e.g., document review and KYC verification running concurrently during account opening) into a sequential model unnecessarily lengthens cycle time.
- **Neglecting capacity planning when volumes increase.** Workflow automation makes work visible, but it does not eliminate work. When volumes increase, queue depths grow and SLAs breach unless staffing or automation is adjusted. Use queue depth trends and arrival rate data from the workflow system to anticipate capacity needs before SLAs degrade.
- **Automating without documenting the rules.** If automated routing, approval, and escalation rules are embedded in code or configuration without corresponding written documentation, the firm cannot demonstrate to examiners how its supervisory system works. Written supervisory procedures must reflect the automated workflow logic.
- **Skipping user acceptance testing for workflow changes.** Changing an approval threshold, routing rule, or escalation timer in production without testing can cause items to route incorrectly, approvals to be skipped, or escalations to fire inappropriately. All workflow configuration changes should follow the same change management discipline as software releases.

## Cross-References

- **stp-automation** (client-operations plugin) — STP is the end goal of operations automation; workflow automation handles the exceptions and human-in-the-loop steps that STP cannot yet cover.
- **account-opening-workflow** (client-operations plugin) — Account opening is a primary domain for workflow automation, with multi-step approval chains, conditional routing by account type, and custodian submission orchestration.
- **account-maintenance** (client-operations plugin) — Maintenance requests (name changes, beneficiary updates, re-registrations) are routed, tracked, and SLA-monitored through workflow systems.
- **account-transfers** (client-operations plugin) — Transfers require multi-step approval workflows with dollar-based thresholds, FINRA-mandated timelines, and escalation for aging items.
- **corporate-actions** (client-operations plugin) — Voluntary corporate actions have deadline-driven workflows for client notification, election collection, escalation, and DTC submission.
- **reconciliation** (client-operations plugin) — Reconciliation break resolution follows escalation workflows with aging thresholds, priority routing, and management reporting.
- **operational-risk** (trading-operations plugin) — Workflow controls (approval chains, four-eyes principle, SLA monitoring) are operational risk mitigations that reduce processing errors and missed deadlines.
- **books-and-records** (compliance plugin) — Workflow audit trails are regulatory records subject to SEC Rule 17a-3/17a-4 preservation requirements and FINRA examination review.

### Referencia: references/examples.md

# Workflow Automation — Worked Examples

## Contents

1. [Example 1: Designing an Approval Workflow for High-Value Account Transfers](#example-1-designing-an-approval-workflow-for-high-value-account-transfers) — approval matrix by transfer type, value, and risk; state machine; timeout escalation
2. [Example 2: Building SLA Monitoring for Account Maintenance Requests](#example-2-building-sla-monitoring-for-account-maintenance-requests) — SLA targets per maintenance type, aging thresholds, advisor visibility
3. [Example 3: Implementing Escalation Rules for Aging Corporate Action Elections](#example-3-implementing-escalation-rules-for-aging-corporate-action-elections) — Day -10 to Day 0 escalation timeline, response-rate alerts, post-event review

## Example 1: Designing an Approval Workflow for High-Value Account Transfers

**Scenario:** A mid-size broker-dealer processes approximately 300 account transfers per month. Management has identified that high-value transfers (over $500,000) lack a consistent approval process — some receive supervisory review, others do not, depending on which analyst processes them. The compliance department has flagged this as a FINRA Rule 3110 supervisory concern. The firm needs a structured approval workflow for all account transfers, with additional controls for high-value and high-risk transfers.

**Design Considerations:**
- FINRA Rule 11870 imposes strict timelines (3 business days for validation, 6 total for completion), so the approval workflow cannot add significant delay.
- The firm processes three transfer types: full ACAT, partial ACAT, and non-ACAT (journals, wire transfers, DTC deliveries).
- Transfer risk varies by type, dollar value, and circumstances (e.g., transfers to third-party accounts, transfers from elderly clients, transfers initiated shortly after an advisor change).
- The firm has 12 operations analysts, 3 team leads, and an operations manager. Compliance has one dedicated surveillance analyst for operations reviews.

**Analysis:**

Define the approval matrix:

| Transfer Type | Value / Risk | Approvals Required | SLA Impact |
|---|---|---|---|
| Full ACAT (standard) | Under $500K | Operations analyst (self-review) + automated supervisory log | No added delay |
| Full ACAT (high-value) | $500K - $2M | Operations analyst + team lead review | Add 4 hours max |
| Full ACAT (very high value) | Over $2M | Operations analyst + team lead + operations manager | Add 8 hours max |
| Transfer to third-party account | Any value | Operations analyst + team lead + compliance review | Add 1 business day max |
| Transfer from client age 65+ | Over $100K | Operations analyst + team lead (senior investor protection review) | Add 4 hours max |
| Non-ACAT wire transfer | Over $50K | Operations analyst + team lead + verbal callback confirmation | Add 2 hours max |

Model the workflow as a state machine with states: Received, Validated, Pending Approval (Tier 1), Pending Approval (Tier 2), Pending Approval (Tier 3), Approved, Submitted to ACATS/Custodian, In Progress, Completed, Rejected. Guard conditions on each transition enforce the approval matrix — the system evaluates transfer value, transfer type, client age, and destination account ownership to determine which approval tiers are required.

Implement timeout escalation on each approval tier. If a Tier 1 approval (team lead) is not acted upon within 2 hours, send a reminder. If not acted upon within 4 hours, escalate to the operations manager for either direct approval or reassignment. These timeouts are calibrated to keep the total approval cycle within the FINRA Rule 11870 timelines.

For the compliance review tier (transfers to third-party accounts), the compliance analyst receives a structured review package: client identity verification, relationship between the client and the third-party recipient, source of the transfer instruction (client-initiated vs. advisor-initiated), and any recent account activity that may indicate exploitation or unauthorized transactions. The compliance review SLA is 1 business day, with escalation to the Chief Compliance Officer if the deadline is approaching.

The audit trail captures every approval decision: approver identity, timestamp, decision (approve/reject/request more information), and any comments or justification. This audit trail is the firm's evidence of supervisory review for FINRA Rule 3110 examination purposes.

## Example 2: Building SLA Monitoring for Account Maintenance Requests

**Scenario:** An RIA with $6 billion in AUM processes approximately 800 account maintenance requests per month, including name changes, address updates, beneficiary changes, account re-registrations, and fee schedule adjustments. The firm has no formal SLA tracking — requests are managed through a shared email inbox and a spreadsheet. Advisors frequently complain that requests "disappear" or take too long. The head of operations wants to implement SLA monitoring with real-time visibility for both operations staff and advisors.

**Design Considerations:**
- The firm uses Salesforce as its CRM and wants to leverage Salesforce's workflow capabilities rather than introducing a new platform.
- Different maintenance types have different complexity and urgency. A simple address change should complete in 1 business day. A trust re-registration may require 5-7 business days due to document collection and custodian processing.
- The firm custodies with two custodians (Schwab and Fidelity), and each custodian has different processing times and submission methods for maintenance requests.
- Advisors need visibility into request status without calling the operations team.

**Analysis:**

Step 1 — Define SLA targets per maintenance type:

| Maintenance Type | SLA Target | Rationale |
|---|---|---|
| Address change | 1 business day | Simple, no documentation required beyond client confirmation |
| Name change (marriage, divorce) | 3 business days | Requires supporting documents (marriage certificate, court order) and custodian processing |
| Beneficiary change | 2 business days | Requires signed beneficiary designation form; advisor review recommended |
| Account re-registration (individual to trust) | 5 business days | Requires trust documentation, custodian re-titling, cost basis continuity verification |
| Fee schedule adjustment | 2 business days | Requires advisor approval, billing system update, and confirmation |
| Account closure | 3 business days | Requires asset disposition (transfer or liquidation) and custodian close-out |

Step 2 — Build the workflow in Salesforce. Create a custom object (or use Salesforce Case) for maintenance requests. Each request captures: request type, requesting advisor, client account, date received, SLA deadline (auto-calculated from request type), assigned analyst, current status (Received, In Progress, Pending Documentation, Submitted to Custodian, Completed, Cancelled), and custodian.

Implement routing rules: requests are auto-assigned to the next available analyst using workload-based assignment. Complex request types (re-registrations, closures) are routed to senior analysts with the appropriate skill tag.

Step 3 — Implement SLA monitoring. Salesforce Process Builder (or Flow) evaluates each open request against its SLA deadline on a scheduled basis (every hour during business hours). The aging thresholds:
- Green: more than 50% of SLA remaining.
- Yellow: 20-50% of SLA remaining. The assigned analyst sees a yellow indicator on their dashboard.
- Red: less than 20% of SLA remaining. The team lead receives an automated notification.
- Breached: SLA exceeded. The operations manager receives a breach notification. The request is flagged for root cause documentation.

Step 4 — Advisor visibility. Build a Salesforce Experience Cloud portal (or a custom Lightning component accessible to advisors) that displays: all open requests for the advisor's clients, current status and assigned analyst, SLA deadline and color-coded aging indicator, and a comment thread for advisor-operations communication. This eliminates the need for advisors to email or call operations for status updates.

Step 5 — Management reporting. A weekly SLA dashboard displays: total requests received and completed, SLA compliance rate by maintenance type, average cycle time by maintenance type, breach count and root causes, and analyst-level throughput. The operations manager reviews the dashboard in the weekly team meeting and assigns process improvement actions for any maintenance type with SLA compliance below 90%.

## Example 3: Implementing Escalation Rules for Aging Corporate Action Elections

**Scenario:** A broker-dealer processes voluntary corporate action elections for approximately 4,000 client accounts. The firm has experienced two incidents in the past year where election deadlines were missed, resulting in clients receiving the default election on tender offers instead of their instructed election. In both cases, the root cause was a combination of late client notification and insufficient escalation when elections were not returned in time. The COO has mandated a formal escalation framework for corporate action elections.

**Design Considerations:**
- The election deadline chain runs: DTC deadline (hard deadline), custodian deadline (1 business day before DTC), firm internal deadline (2 business days before custodian), client notification (at least 5 business days before firm internal deadline).
- Election types vary in complexity: simple tender offers (tender or do not tender), mandatory with choice (cash or stock), complex events (Dutch auctions, exchange offers with multiple alternatives).
- The firm has 8 corporate actions analysts, a corporate actions manager, and a senior operations VP who oversees all processing.
- Some clients (particularly institutional accounts) require internal committee approval before submitting elections, adding time to the response cycle.

**Analysis:**

Define the escalation timeline working backward from the DTC deadline. Assume a typical tender offer with a DTC deadline of Day 0 (expressed as business days before the DTC deadline):

| Day (Before DTC Deadline) | Action | Owner |
|---|---|---|
| Day -10 | Event announced, validated, and set up in system. Client notification generated. | Corporate actions analyst |
| Day -9 | Notification sent to all affected clients and advisors via email and portal. | Automated |
| Day -5 | First follow-up to clients/advisors who have not responded. Yellow status assigned. | Automated notification, analyst monitors |
| Day -4 | Second follow-up with direct call to advisor for accounts above $100K in affected position. Team lead notified of non-responses. | Analyst (calls), automated (team lead alert) |
| Day -3 | Firm internal deadline. All received elections aggregated for submission. Non-respondents receive default election unless override is approved. | Corporate actions analyst + team lead review |
| Day -2.5 | Escalation to corporate actions manager for any account where the advisor disputes the default and requests a late election. Manager decides whether to attempt late submission. | Corporate actions manager |
| Day -2 | Elections submitted to custodian. | Corporate actions analyst |
| Day -1 | Custodian deadline. Confirm custodian has accepted the firm's election submission. Escalate to manager immediately if custodian rejects or flags any issues. | Corporate actions analyst + manager (if issues) |
| Day 0 | DTC deadline. Verify final settlement. Any issues escalated to senior VP. | Corporate actions manager + senior VP (if issues) |

Implement monitoring controls:
- A daily corporate actions dashboard shows all open voluntary events, the number of accounts requiring election, the response rate, and the days remaining until each deadline.
- Automated alerts fire at each escalation milestone. If the response rate is below 70% at Day -5, the team lead is alerted. If below 85% at Day -4, the corporate actions manager is alerted. If below 95% at Day -3 (firm internal deadline), the manager and senior VP are alerted.
- For institutional accounts requiring committee approval, the escalation timeline starts earlier — notification at Day -12 instead of Day -10 — to accommodate the approval process.

Post-event review: after each voluntary corporate action settles, the team logs the response rate, any elections that missed the internal deadline, whether late submissions were attempted and accepted, and any client impact from default elections. This data feeds a monthly review that identifies patterns (specific advisors who consistently respond late, event types that require longer lead times, clients who need proactive outreach) and drives process improvements.

Audit trail requirements: every notification, follow-up, escalation, and election submission is logged with timestamps and responsible parties. If a client later disputes that they received the default election, the firm can produce the complete communication and escalation history demonstrating that the client was notified, reminded, and escalated through the defined process. This audit trail satisfies FINRA Rule 3110 supervisory obligations and provides examination-ready documentation.


---

## SKILL: yellowstone-grpc

- Fuente: `agiprolabs/claude-trading-skills` → `skills/yellowstone-grpc` (MIT)
- Cuándo usarla: Real-time Solana transaction and account streaming via Yellowstone gRPC (Geyser plugin)
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/yellowstone-grpc/` (monitor_wallets.py, subscribe_transactions.py)

# Yellowstone gRPC — Real-Time Solana Streaming

Stream every transaction, account update, slot, and block on Solana in real-time using Yellowstone gRPC. This is the foundation for any latency-sensitive Solana trading system — replacing REST polling with push-based streaming at ~5ms slot latency.

## Why Yellowstone gRPC

| Method | Slot Latency (p90) | Use Case |
|--------|-------------------|----------|
| REST polling (`getTransaction`) | ~150ms+ | Historical lookups |
| WebSocket (`onLogs`) | ~10ms | Simple notifications |
| **Yellowstone gRPC** | **~5ms** | **Production trading systems** |

Yellowstone is a Geyser plugin that exposes Solana validator data over gRPC. Every major RPC provider runs it. You subscribe to filtered streams of transactions, account changes, slots, blocks, and entries — and the data pushes to you.

## Quick Start

### 1. Get Access

You need a gRPC-enabled RPC provider. See `references/providers.md` for full comparison.

| Provider | gRPC Entry Price | Notes |
|----------|-----------------|-------|
| Shyft | $199/mo | Best value, 7 regions, unlimited bandwidth |
| Helius | $999/mo | LaserStream, DAS APIs included |
| Triton One | ~$2,900/mo | Created Yellowstone, lowest latency |
| QuickNode | Plan-dependent | Marketplace add-on |
| Chainstack | $49/mo (1 stream) | Budget option, limited filters |
| Alchemy | Free tier available | Compute-unit metered |

### 2. Install Dependencies

```bash
# Python
uv pip install grpcio grpcio-tools protobuf base58 solders python-dotenv

# Generate Python stubs from proto files
git clone https://github.com/rpcpool/yellowstone-grpc.git
python -m grpc_tools.protoc \
  -I./yellowstone-grpc/yellowstone-grpc-proto/proto/ \
  --python_out=./generated \
  --pyi_out=./generated \
  --grpc_python_out=./generated \
  ./yellowstone-grpc/yellowstone-grpc-proto/proto/*.proto
```

```toml
# Rust — Cargo.toml
[dependencies]
yellowstone-grpc-client = "6.0.0"
yellowstone-grpc-proto = "6.0.0"
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
futures = "0.3"
bs58 = "0.5"
```

```bash
# TypeScript
npm install @triton-one/yellowstone-grpc @solana/web3.js
```

### 3. Environment Setup

```bash
export GRPC_ENDPOINT="https://grpc.ny.shyft.to"  # your provider endpoint
export GRPC_TOKEN="your-x-token-here"              # from provider dashboard
```

### 4. Connect and Subscribe

```python
import grpc
import os
from generated import geyser_pb2, geyser_pb2_grpc

endpoint = os.environ["GRPC_ENDPOINT"].replace("https://", "")
token = os.environ["GRPC_TOKEN"]

# Authenticated TLS channel
auth_creds = grpc.metadata_call_credentials(
    lambda ctx, cb: cb((("x-token", token),), None)
)
channel = grpc.secure_channel(
    endpoint,
    grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(), auth_creds
    ),
    options=[("grpc.max_receive_message_length", 64 * 1024 * 1024)],
)
stub = geyser_pb2_grpc.GeyserStub(channel)
```

## Core Concepts

### Subscription Types

| Type | What You Get | Use Case |
|------|-------------|----------|
| `transactions` | Full transaction with metadata | DEX swap monitoring, copy trading |
| `accounts` | Account data on change | Pool reserve tracking, token supply |
| `slots` | Slot progression events | Block timing, confirmation tracking |
| `blocks` | Full block contents | Block-level analysis |
| `blocks_meta` | Block metadata only | Lightweight block tracking |
| `entry` | Block entries (shred groups) | Low-level validator data |
| `transactions_status` | Tx status without full data | Lightweight confirmation |

### Filter Logic

- Multiple filter **types** (transactions + accounts) = **AND** — you get updates matching any type
- Values within arrays (multiple addresses in `account_include`) = **OR**
- Named filters let you distinguish which filter matched in the response
- Sending a new `SubscribeRequest` **replaces** all previous filters

### Commitment Levels

| Level | Speed | Safety | Use For |
|-------|-------|--------|---------|
| `PROCESSED` | Fastest | May be rolled back | Time-critical signals |
| `CONFIRMED` | ~400ms slower | Supermajority voted | Most trading use cases |
| `FINALIZED` | ~6-12s slower | Irreversible | Settlement verification |

## Common Subscription Patterns

### Watch All Swaps on a DEX Program

```python
# Filter: all non-vote, non-failed transactions involving PumpFun
request = geyser_pb2.SubscribeRequest(
    transactions={
        "pumpfun": geyser_pb2.SubscribeRequestFilterTransactions(
            account_include=["6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"],
            vote=False,
            failed=False,
        )
    },
    commitment=geyser_pb2.CommitmentLevel.PROCESSED,
)
```

### Track Specific Wallets

```python
request = geyser_pb2.SubscribeRequest(
    transactions={
        "whales": geyser_pb2.SubscribeRequestFilterTransactions(
            account_include=[
                "WalletAddress1...",
                "WalletAddress2...",
            ],
            vote=False,
            failed=False,
        )
    },
    commitment=geyser_pb2.CommitmentLevel.CONFIRMED,
)
```

### Monitor Pool Reserves (Account Subscription)

```python
request = geyser_pb2.SubscribeRequest(
    accounts={
        "raydium_pools": geyser_pb2.SubscribeRequestFilterAccounts(
            account=["PoolAddress1...", "PoolAddress2..."],
        )
    },
    commitment=geyser_pb2.CommitmentLevel.PROCESSED,
)
```

### Reduce Bandwidth with Data Slicing

```python
# Only get the first 40 bytes of account data (e.g., just the discriminator + key fields)
request = geyser_pb2.SubscribeRequest(
    accounts={
        "token_accounts": geyser_pb2.SubscribeRequestFilterAccounts(
            owner=["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"],
            filters=[
                geyser_pb2.SubscribeRequestFilterAccountsFilter(
                    token_account_state=True
                )
            ],
        )
    },
    accounts_data_slice=[
        geyser_pb2.SubscribeRequestAccountsDataSlice(offset=0, length=40)
    ],
)
```

## Parsing Transaction Updates

When you receive a `SubscribeUpdateTransaction`, extract:

```python
for update in stream:
    if update.HasField("transaction"):
        tx = update.transaction
        info = tx.transaction
        sig = base58.b58encode(info.signature).decode()
        slot = tx.slot

        msg = info.transaction.message
        account_keys = [base58.b58encode(k).decode() for k in msg.account_keys]

        # Instructions
        for ix in msg.instructions:
            program = account_keys[ix.program_id_index]
            accounts = [account_keys[i] for i in ix.accounts]
            data = ix.data  # bytes — decode per program IDL

        # Token balance changes (post-execution)
        meta = info.meta
        for tb in meta.post_token_balances:
            mint = tb.mint
            owner = tb.owner
            amount = tb.ui_token_amount.ui_amount
```

See `references/proto_reference.md` for complete field documentation.

## Production Architecture

```
[gRPC Stream] → [Bounded Channel] → [Processing Workers]
                   (1K-100K cap)      ├─ Parse instructions
                                      ├─ Update state / DB
                                      └─ Trigger actions
```

**Critical patterns:**
- Decouple I/O from processing — never block the gRPC stream
- Reconnect with exponential backoff (100ms → 60s cap)
- Use `from_slot` to resume after disconnection (subtract ~32 slots for reorg safety)
- Ping every 15-30 seconds to keep connection alive
- Filter `vote: false` always — vote transactions are ~70% of all traffic
- Set `max_receive_message_length` to 64MB+ (default 4MB is too small)

See `references/performance.md` for full production checklist.

## Key Program IDs for Trading

| Program | Address | What It Does |
|---------|---------|-------------|
| PumpFun | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` | Token launches, bonding curve trades |
| PumpSwap | `PSwapMdSai8tjrEXcxFeQth87xC4rRsa4VA5mhGhXkP` | PumpFun graduated token swaps |
| Raydium AMM | `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8` | Legacy AMM swaps |
| Raydium CLMM | `CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK` | Concentrated liquidity |
| Raydium CPMM | `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C` | Constant product MM |
| Orca Whirlpool | `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc` | Concentrated liquidity |
| Meteora DLMM | `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` | Dynamic liquidity MM |
| Jupiter V6 | `JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4` | Swap aggregator |
| Token Program | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | SPL token operations |

## Files

### References
- `references/providers.md` — Provider comparison: endpoints, pricing, auth, features
- `references/subscription_filters.md` — Complete filter reference with examples for every filter type
- `references/proto_reference.md` — Key protobuf message definitions and field documentation
- `references/performance.md` — Connection management, reconnection, backpressure, production checklist

### Scripts
- `scripts/subscribe_transactions.py` — Stream and parse transactions filtered by program ID
- `scripts/monitor_wallets.py` — Watch specific wallets for on-chain activity

### Referencia: references/performance.md

# Yellowstone gRPC — Performance & Production Guide

## Latency Benchmarks

| Method | Slot Latency (p90) | Account Latency (p90) | Notes |
|--------|-------------------|-----------------------|-------|
| REST polling | ~150ms+ | N/A | Polling overhead + HTTP |
| WebSocket (`onLogs`) | ~10ms | ~374ms | Event-based, limited filtering |
| Yellowstone gRPC | ~5ms | ~215ms | Push-based, rich filtering |
| Deshred (Triton only) | ~20ms (p90) | N/A | Pre-execution, ~6.3ms p50 |

## Data Volume Expectations

- **All Solana transactions**: ~2,000-4,000 TPS (including votes)
- **Vote transactions**: ~70% of total — always filter with `vote: false`
- **PumpFun alone**: ~20,000+ trades/hour during active periods
- **Single DEX program filter**: ~100-1,000 updates/second depending on activity
- **Single wallet filter**: ~0.01-10 updates/second depending on activity

## Connection Management

### Max Message Size

The default gRPC max message size (4MB) is too small for Solana. Set it higher:

```python
# Python
options = [("grpc.max_receive_message_length", 64 * 1024 * 1024)]  # 64MB

# For block subscriptions, go higher
options = [("grpc.max_receive_message_length", 1024 * 1024 * 1024)]  # 1GB
```

```rust
// Rust
.max_decoding_message_size(64 * 1024 * 1024)
```

```typescript
// TypeScript
{ "grpc.max_receive_message_length": 64 * 1024 * 1024 }
```

### Keep-Alive / Ping

Send pings every 15-30 seconds to prevent connection timeout:

```python
import time, threading

def ping_loop(request_iterator):
    while True:
        time.sleep(15)
        request_iterator.send(SubscribeRequest(
            ping=SubscribeRequestPing(id=int(time.time()))
        ))
```

Handle pong responses — if you receive a `SubscribeUpdatePing` from the server, respond:

```python
if update.HasField("ping"):
    request_iterator.send(SubscribeRequest(
        ping=SubscribeRequestPing(id=update.ping.id)
    ))
```

### Reconnection with Exponential Backoff

```python
import time, random

def connect_with_backoff(max_delay: float = 60.0):
    delay = 0.1  # start at 100ms
    last_slot = None

    while True:
        try:
            stream = subscribe(from_slot=last_slot)
            delay = 0.1  # reset on success

            for update in stream:
                last_slot = extract_slot(update)
                process(update)

        except grpc.RpcError as e:
            jitter = random.uniform(0, delay * 0.1)
            print(f"Disconnected: {e.code()}. Reconnecting in {delay:.1f}s")
            time.sleep(delay + jitter)
            delay = min(delay * 2, max_delay)
```

### Resume After Disconnection

Use `from_slot` to replay missed data. Subtract ~32 slots for reorg safety:

```python
request = SubscribeRequest(
    transactions={...},
    from_slot=last_processed_slot - 32,
)
```

**Important**: `from_slot` replay may produce duplicate updates. Deduplicate by transaction signature.

Replay depth varies by provider:
- Shyft: ~150 slots
- QuickNode: ~3,000 slots
- Helius: ~24 hours

## Backpressure Architecture

Never process messages in the gRPC receive loop. Decouple I/O from business logic:

```
[gRPC Stream Thread]
    │
    ▼
[Bounded Channel/Queue]  ← backpressure point (1K-100K capacity)
    │
    ▼
[Processing Worker(s)]
    ├─ Parse instructions
    ├─ Update state
    ├─ Trigger signals
    └─ Batch DB writes
```

### Python Implementation

```python
import queue
import threading

msg_queue = queue.Queue(maxsize=10_000)

def grpc_reader(stub, request):
    """Dedicated thread: reads gRPC stream into queue."""
    stream = stub.Subscribe(iter([request]))
    for update in stream:
        try:
            msg_queue.put(update, timeout=1.0)
        except queue.Full:
            print("WARNING: queue full, dropping message")

def processor():
    """Dedicated thread: processes messages from queue."""
    while True:
        update = msg_queue.get()
        handle_update(update)

threading.Thread(target=grpc_reader, args=(stub, request), daemon=True).start()
threading.Thread(target=processor, daemon=True).start()
```

### Rust Implementation

```rust
use tokio::sync::mpsc;

let (tx, mut rx) = mpsc::channel(100_000);

// Spawn gRPC reader
tokio::spawn(async move {
    while let Some(msg) = stream.next().await {
        if tx.send(msg.unwrap()).await.is_err() { break; }
    }
});

// Process in main task
while let Some(update) = rx.recv().await {
    match update.update_oneof {
        Some(UpdateOneof::Transaction(tx)) => handle_transaction(tx),
        _ => {}
    }
}
```

## Database Write Batching

Don't write every update to the database individually. Batch writes:

```python
batch = []
last_flush = time.time()

for update in process_stream():
    batch.append(to_row(update))

    if len(batch) >= 1000 or (time.time() - last_flush) > 1.0:
        db.executemany("INSERT INTO events ...", batch)
        batch.clear()
        last_flush = time.time()
```

## Multi-Connection Patterns

For high-throughput programs, split across multiple gRPC connections:

```
Connection 1: PumpFun transactions      → Worker pool A
Connection 2: Raydium + Orca swaps      → Worker pool B
Connection 3: Tracked wallet activity   → Worker pool C
Connection 4: Pool account updates      → Worker pool D
```

Each connection runs on its own thread/task with independent reconnection logic.

## Monitoring

Track these metrics in production:

| Metric | Alert Threshold | Why |
|--------|----------------|-----|
| Updates received/sec | < expected baseline | Stream may be stalled |
| Queue depth | > 80% capacity | Processing can't keep up |
| Time since last update | > 30 seconds | Connection likely dead |
| Reconnection count | > 5/hour | Provider instability |
| Processing latency | > 100ms p99 | Bottleneck in handlers |
| Dropped messages | > 0 | Queue overflow |

## Production Checklist

- [ ] `vote: false` on all transaction filters
- [ ] `max_receive_message_length` set to 64MB+
- [ ] Exponential backoff reconnection (100ms → 60s cap)
- [ ] `from_slot` resume after disconnection
- [ ] Ping/pong every 15-30 seconds
- [ ] Bounded channel between I/O and processing
- [ ] Database write batching (1000 rows or 1s flush)
- [ ] Duplicate detection on replay (by tx signature)
- [ ] Monitoring: updates/sec, queue depth, reconnection count
- [ ] Graceful shutdown (drain queue before exit)
- [ ] Error classification (retriable vs fatal gRPC errors)
- [ ] Separate connections for independent data streams

### Referencia: references/proto_reference.md

# Yellowstone gRPC — Protobuf Reference

Source: [rpcpool/yellowstone-grpc](https://github.com/rpcpool/yellowstone-grpc/blob/master/yellowstone-grpc-proto/proto/geyser.proto)

## Service Definition

```protobuf
service Geyser {
  rpc Subscribe(stream SubscribeRequest) returns (stream SubscribeUpdate) {}
  rpc Ping(PingRequest) returns (PongResponse) {}
  rpc GetLatestBlockhash(GetLatestBlockhashRequest) returns (GetLatestBlockhashResponse) {}
  rpc GetBlockHeight(GetBlockHeightRequest) returns (GetBlockHeightResponse) {}
  rpc GetSlot(GetSlotRequest) returns (GetSlotResponse) {}
  rpc IsBlockhashValid(IsBlockhashValidRequest) returns (IsBlockhashValidResponse) {}
  rpc GetVersion(GetVersionRequest) returns (GetVersionResponse) {}
}
```

`Subscribe` is bidirectional streaming — you send `SubscribeRequest` messages and receive `SubscribeUpdate` messages continuously.

## SubscribeRequest

```protobuf
message SubscribeRequest {
  map<string, SubscribeRequestFilterAccounts> accounts = 1;
  map<string, SubscribeRequestFilterSlots> slots = 2;
  map<string, SubscribeRequestFilterTransactions> transactions = 3;
  map<string, SubscribeRequestFilterTransactions> transactions_status = 10;
  map<string, SubscribeRequestFilterBlocks> blocks = 4;
  map<string, SubscribeRequestFilterBlocksMeta> blocks_meta = 5;
  map<string, SubscribeRequestFilterEntry> entry = 8;
  optional CommitmentLevel commitment = 6;
  repeated SubscribeRequestAccountsDataSlice accounts_data_slice = 7;
  optional SubscribeRequestPing ping = 9;
  optional uint64 from_slot = 11;
}
```

Map keys are user-defined labels. They appear in `SubscribeUpdate.filters` to identify which subscription matched.

## SubscribeUpdate (Response)

```protobuf
message SubscribeUpdate {
  repeated string filters = 1;  // which named filters matched
  oneof update_oneof {
    SubscribeUpdateAccount account = 2;
    SubscribeUpdateSlot slot = 3;
    SubscribeUpdateTransaction transaction = 4;
    SubscribeUpdateTransactionStatus transaction_status = 10;
    SubscribeUpdateBlock block = 5;
    SubscribeUpdatePing ping = 6;
    SubscribeUpdatePong pong = 9;
    SubscribeUpdateBlockMeta block_meta = 7;
    SubscribeUpdateEntry entry = 8;
  }
  google.protobuf.Timestamp created_at = 11;
}
```

## Transaction Update

```protobuf
message SubscribeUpdateTransaction {
  SubscribeUpdateTransactionInfo transaction = 1;
  uint64 slot = 2;
}

message SubscribeUpdateTransactionInfo {
  bytes signature = 1;            // 64 bytes, base58-encode for display
  bool is_vote = 2;
  Transaction transaction = 3;    // from solana-storage.proto
  TransactionStatusMeta meta = 4; // execution results
  uint64 index = 5;               // position within the block
}
```

### Transaction (Inner)

```protobuf
message Transaction {
  repeated bytes signatures = 1;  // first is the tx signature
  Message message = 2;
}

message Message {
  MessageHeader header = 1;
  repeated bytes account_keys = 2;    // all account pubkeys (32 bytes each)
  bytes recent_blockhash = 3;
  repeated CompiledInstruction instructions = 4;
  bool versioned = 5;
  repeated MessageAddressTableLookup address_table_lookups = 6;
}

message MessageHeader {
  uint32 num_required_signatures = 1;
  uint32 num_readonly_signed_accounts = 2;
  uint32 num_readonly_unsigned_accounts = 3;
}

message CompiledInstruction {
  uint32 program_id_index = 1;  // index into account_keys
  bytes accounts = 2;           // indices into account_keys
  bytes data = 3;               // instruction data (program-specific)
}
```

### TransactionStatusMeta (Post-Execution)

```protobuf
message TransactionStatusMeta {
  TransactionError err = 1;
  uint64 fee = 2;
  repeated uint64 pre_balances = 3;   // SOL balances before (lamports)
  repeated uint64 post_balances = 4;  // SOL balances after (lamports)
  repeated InnerInstructions inner_instructions = 5;
  repeated string log_messages = 6;
  repeated TokenBalance pre_token_balances = 7;
  repeated TokenBalance post_token_balances = 8;
  repeated Reward rewards = 9;
  repeated bytes loaded_writable_addresses = 12;
  repeated bytes loaded_readonly_addresses = 13;
  ReturnData return_data = 14;
  optional uint64 compute_units_consumed = 15;
}
```

### Token Balance

```protobuf
message TokenBalance {
  uint32 account_index = 1;  // index into account_keys
  string mint = 2;           // token mint address (base58)
  UiTokenAmount ui_token_amount = 3;
  string owner = 4;          // token account owner (base58)
}

message UiTokenAmount {
  double ui_amount = 1;      // human-readable amount
  uint32 decimals = 2;
  string amount = 3;         // raw amount as string
}
```

### Inner Instructions

```protobuf
message InnerInstructions {
  uint32 index = 1;  // which top-level instruction generated these
  repeated InnerInstruction instructions = 2;
}

message InnerInstruction {
  uint32 program_id_index = 1;
  bytes accounts = 2;
  bytes data = 3;
  optional uint32 stack_height = 4;
}
```

## Account Update

```protobuf
message SubscribeUpdateAccount {
  SubscribeUpdateAccountInfo account = 1;
  uint64 slot = 2;
  optional bool is_startup = 3;
}

message SubscribeUpdateAccountInfo {
  bytes pubkey = 1;           // 32 bytes
  uint64 lamports = 2;
  bytes owner = 3;            // program that owns this account (32 bytes)
  bool executable = 4;
  uint64 rent_epoch = 5;
  bytes data = 6;             // account data (variable length)
  uint64 write_version = 7;
  optional bytes txn_signature = 8;  // which tx caused this update
}
```

## Commitment Levels

```protobuf
enum CommitmentLevel {
  PROCESSED = 0;   // fastest, may be rolled back
  CONFIRMED = 1;   // supermajority voted
  FINALIZED = 2;   // irreversible
}
```

## Slot Status

```protobuf
enum SlotStatus {
  SLOT_PROCESSED = 0;
  SLOT_CONFIRMED = 1;
  SLOT_FINALIZED = 2;
  SLOT_FIRST_SHRED_RECEIVED = 3;
  SLOT_COMPLETED = 4;
  SLOT_CREATED_BANK = 5;
  SLOT_DEAD = 6;
}
```

## Parsing Checklist

When processing a `SubscribeUpdateTransaction`:

1. **Signature**: `base58.b58encode(info.signature).decode()`
2. **Account keys**: Decode each 32-byte entry in `message.account_keys` to base58
3. **Instructions**: For each `CompiledInstruction`:
   - Program = `account_keys[program_id_index]`
   - Accounts = `[account_keys[i] for i in accounts]`
   - Data = raw bytes, first 8 bytes are typically the instruction discriminator
4. **Inner instructions**: CPI calls generated during execution — same structure as top-level
5. **Token changes**: Compare `pre_token_balances` vs `post_token_balances` for swap amounts
6. **SOL changes**: Compare `pre_balances` vs `post_balances` for fee and SOL transfer analysis
7. **Logs**: `meta.log_messages` contain program logs (useful for debugging)
8. **Compute**: `meta.compute_units_consumed` for gas analysis

### Referencia: references/providers.md

# Yellowstone gRPC — Provider Comparison

## Shyft

- **Entry price**: $199/mo (Build plan)
- **Endpoints**: `grpc.{region}.shyft.to` — NY, VA, MIA, AMS, FRA, LON, SGP
- **Auth**: x-token from dashboard, or IP whitelisting
- **Bandwidth**: Unlimited (no metering)
- **Connections**: 10 (Build), 20 (Grow/$349), 50 (Accelerate/$649)
- **Dedicated nodes**: From $1,800/mo (unlimited connections, 5-10ms latency advantage)
- **Historical replay**: Up to 150 slots lookback
- **Unique feature**: RabbitStream — pre-execution shred-level data (transactions before confirmation, no metadata)
- **DeFi parsing examples**: [github.com/Shyft-to/solana-defi](https://github.com/Shyft-to/solana-defi) — Raydium, PumpFun, Orca, Meteora parsers
- **Connection management**: Clear stale connections via `https://grpc.{region}.shyft.to/clear-connections?xtoken=YOUR_TOKEN`
- **Best for**: Price-sensitive teams, PumpFun/DEX trading, good regional coverage

## Helius (LaserStream)

- **Entry price**: $999/mo (Professional plan, mainnet gRPC)
- **Endpoints**:
  - US East: `laserstream-mainnet-ewr.helius-rpc.com`
  - US West: `laserstream-mainnet-slc.helius-rpc.com`
  - Europe: `laserstream-mainnet-fra.helius-rpc.com`
  - Asia: `laserstream-mainnet-tyo.helius-rpc.com`
  - Devnet: `laserstream-devnet-ewr.helius-rpc.com`
- **Auth**: API key as x-token
- **Bandwidth**: Credit-based + data add-ons ($500/5TB, scaling tiers)
- **Historical replay**: Up to 24 hours
- **Unique features**: DAS API (token/NFT metadata), enhanced webhooks, auto-reconnect, multi-node failover
- **Best for**: Teams already using Helius RPC/DAS, need rich Solana APIs beyond streaming

## Triton One (Dragon's Mouth)

- **Entry price**: ~$2,900/mo (dedicated nodes)
- **Bandwidth**: ~$0.08/GB
- **Auth**: x-token
- **Created Yellowstone**: Triton built and open-sources the Yellowstone gRPC plugin
- **Unique features**:
  - **Deshred** (`SubscribeDeshred`): Pre-execution transaction streaming (~6.3ms p50, ~20ms p90). Paid beta, limited availability
  - **Fumarole**: Multi-node HA aggregator for persistent streaming
  - **Old Faithful**: Historical data replay (full archive)
  - **Whirligig**: Enhanced WebSocket proxy over Yellowstone
- **Best for**: HFT/MEV, lowest raw latency, enterprise infrastructure

## QuickNode

- **Entry price**: Marketplace add-on (price depends on base plan)
- **Port**: 10000 (separate from RPC)
- **Endpoint format**: `your-endpoint.solana-mainnet.quiknode.pro:10000`
- **Auth**: Built into endpoint URL
- **Rate limits**: Tied to plan RPS (e.g., 125 RPS on Accelerate)
- **Historical replay**: Up to 3000 slots via `from_slot`
- **Best for**: Teams already on QuickNode, flexible add-on model

## Chainstack

- **Entry price**: $49/mo (1 stream)
- **Tiers**: $49/1 stream, $149/5 streams, $449/25 streams
- **Limits**: Up to 50 accounts per stream, 5 concurrent filters of same type
- **Features**: Jito ShredStream enabled by default on all nodes
- **Best for**: Budget option, teams needing ShredStream bundled

## Alchemy

- **Entry price**: Free tier (30M compute units/mo)
- **Bandwidth**: ~$0.08/GB for gRPC
- **Pay-as-you-go**: $5 per 11M compute units
- **Best for**: Experimentation, low-volume testing

## GetBlock

- **Entry price**: Included with Dedicated Solana Node subscription
- **Auth**: Access token created after node deployment
- **Features**: Single TLS endpoint (no separate port config)
- **Best for**: Teams with existing GetBlock dedicated nodes

## Provider Selection Guide

| Priority | Recommended |
|----------|------------|
| Lowest cost with gRPC | Chainstack ($49/mo, limited) or Shyft ($199/mo, full) |
| Best value for trading | **Shyft** ($199-649/mo, unlimited bandwidth, 7 regions) |
| Rich Solana APIs + gRPC | Helius ($999/mo, DAS + webhooks + gRPC) |
| Lowest latency / HFT | **Triton One** (Deshred: ~6ms p50) |
| Free experimentation | Alchemy (free tier, CU-metered) |
| Already on QuickNode | QuickNode add-on |

## Authentication Code (All Providers)

All providers use the same x-token pattern:

```python
import grpc, os

endpoint = os.environ["GRPC_ENDPOINT"].replace("https://", "")
token = os.environ["GRPC_TOKEN"]

auth = grpc.metadata_call_credentials(
    lambda ctx, cb: cb((("x-token", token),), None)
)
channel = grpc.secure_channel(
    endpoint,
    grpc.composite_channel_credentials(grpc.ssl_channel_credentials(), auth),
    options=[("grpc.max_receive_message_length", 64 * 1024 * 1024)],
)
```

```rust
use yellowstone_grpc_client::GeyserGrpcClient;
let mut client = GeyserGrpcClient::connect(endpoint, Some(token), None).await?;
```

```typescript
import Client from "@triton-one/yellowstone-grpc";
const client = new Client(endpoint, token, {
  "grpc.max_receive_message_length": 64 * 1024 * 1024,
});
```

### Referencia: references/subscription_filters.md

# Yellowstone gRPC — Subscription Filters Reference

## How Filters Work

A `SubscribeRequest` contains named filter maps. Each map key is a label you choose — it appears in the response's `filters` field so you know which subscription matched.

- Multiple filter **types** (transactions + accounts in same request) run independently
- Values within arrays (`account_include: [A, B, C]`) are logical **OR**
- Sending a new `SubscribeRequest` **replaces** all previous filters entirely
- To unsubscribe, send empty maps for all types

## Transaction Filters

Filter real-time transactions by involved accounts, vote status, and failure status.

```protobuf
message SubscribeRequestFilterTransactions {
  optional bool vote = 1;              // include vote transactions?
  optional bool failed = 2;            // include failed transactions?
  optional string signature = 5;       // watch a specific signature
  repeated string account_include = 3; // tx must involve ANY of these
  repeated string account_exclude = 4; // tx must NOT involve ANY of these
  repeated string account_required = 6;// tx must involve ALL of these
}
```

### Filter by Program ID

Subscribe to all successful transactions involving a DEX program:

```python
transactions={
    "raydium_swaps": SubscribeRequestFilterTransactions(
        account_include=["675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"],
        vote=False,
        failed=False,
    )
}
```

### Filter by Multiple Programs

OR logic — matches transactions involving ANY listed program:

```python
transactions={
    "all_dex": SubscribeRequestFilterTransactions(
        account_include=[
            "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",  # PumpFun
            "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",  # Raydium AMM
            "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",   # Orca
        ],
        vote=False,
        failed=False,
    )
}
```

### Filter by Wallet (Copy Trading)

Watch specific wallets for any on-chain activity:

```python
transactions={
    "tracked_wallets": SubscribeRequestFilterTransactions(
        account_include=[
            "WalletPubkey1...",
            "WalletPubkey2...",
        ],
        vote=False,
        failed=False,
    )
}
```

### Exclude Known Programs

Exclude noisy programs to reduce volume:

```python
transactions={
    "clean_feed": SubscribeRequestFilterTransactions(
        account_include=["TargetWallet..."],
        account_exclude=[
            "Vote111111111111111111111111111111111111111",
            "ComputeBudget111111111111111111111111111111",
        ],
        vote=False,
        failed=False,
    )
}
```

### Require Multiple Accounts (AND logic)

Match only transactions that involve ALL listed accounts:

```python
transactions={
    "wallet_on_pumpfun": SubscribeRequestFilterTransactions(
        account_required=[
            "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",  # PumpFun
            "SpecificWalletAddress...",                         # Target wallet
        ],
        vote=False,
        failed=False,
    )
}
```

### Watch a Specific Transaction

Track confirmation of a submitted transaction:

```python
transactions={
    "my_tx": SubscribeRequestFilterTransactions(
        signature="5wHu1qwD7q8ZHqDRYBiHMk2aJ4C8tNqVNK5...",
    )
}
```

## Account Filters

Stream account data whenever it changes on-chain. Useful for tracking pool reserves, token balances, and program state.

```protobuf
message SubscribeRequestFilterAccounts {
  repeated string account = 2;    // specific account pubkeys
  repeated string owner = 3;      // accounts owned by these programs
  repeated SubscribeRequestFilterAccountsFilter filters = 4;
  optional bool nonempty_txn_signature = 5;
}
```

### Watch Specific Accounts

```python
accounts={
    "pool_reserves": SubscribeRequestFilterAccounts(
        account=["PoolAccountPubkey1...", "PoolAccountPubkey2..."],
    )
}
```

### Watch All Accounts Owned by a Program

```python
accounts={
    "all_token_accounts": SubscribeRequestFilterAccounts(
        owner=["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"],
        filters=[
            SubscribeRequestFilterAccountsFilter(token_account_state=True)
        ],
    )
}
```

**Warning**: Subscribing to all accounts owned by the Token Program produces enormous data volume. Always add filters to narrow the stream.

### Memcmp Filter (Match Bytes at Offset)

Filter accounts by specific bytes at a given offset in account data:

```python
# Match token accounts for a specific mint (mint pubkey at offset 0)
accounts={
    "sol_token_accounts": SubscribeRequestFilterAccounts(
        owner=["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"],
        filters=[
            SubscribeRequestFilterAccountsFilter(
                memcmp=SubscribeRequestFilterAccountsFilterMemcmp(
                    offset=0,
                    base58="So11111111111111111111111111111111111111112",
                )
            )
        ],
    )
}
```

### Data Size Filter

Match accounts by exact data length:

```python
accounts={
    "sized_accounts": SubscribeRequestFilterAccounts(
        owner=["YourProgramId..."],
        filters=[
            SubscribeRequestFilterAccountsFilter(datasize=165)  # SPL token account size
        ],
    )
}
```

### Lamports Filter

Filter by SOL balance:

```python
accounts={
    "whales": SubscribeRequestFilterAccounts(
        owner=["11111111111111111111111111111111"],
        filters=[
            SubscribeRequestFilterAccountsFilter(
                lamports=SubscribeRequestFilterAccountsFilterLamports(
                    gt=1_000_000_000_000  # > 1000 SOL in lamports
                )
            )
        ],
    )
}
```

## Data Slicing

Reduce bandwidth by requesting only specific byte ranges of account data:

```python
# Only first 40 bytes (discriminator + first key field)
accounts_data_slice=[
    SubscribeRequestAccountsDataSlice(offset=0, length=40)
]
```

Multiple slices are supported — you get concatenated results.

## Slot Filters

```python
slots={
    "slot_updates": SubscribeRequestFilterSlots(
        filter_by_commitment=True,
    )
}
```

Slot status values: `PROCESSED`, `CONFIRMED`, `FINALIZED`, `FIRST_SHRED_RECEIVED`, `COMPLETED`, `CREATED_BANK`, `DEAD`.

## Block and Block Meta Filters

```python
# Full blocks (high bandwidth)
blocks={
    "full_blocks": SubscribeRequestFilterBlocks(
        account_include=["ProgramId..."],  # optional: only blocks with this program
        include_transactions=True,
        include_accounts=False,
        include_entries=False,
    )
}

# Block metadata only (low bandwidth)
blocks_meta={
    "block_meta": SubscribeRequestFilterBlocksMeta()
}
```

## Multiple Named Filters

Use different labels to multiplex subscriptions on one connection:

```python
request = SubscribeRequest(
    transactions={
        "pumpfun": SubscribeRequestFilterTransactions(
            account_include=["6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"],
            vote=False, failed=False,
        ),
        "whales": SubscribeRequestFilterTransactions(
            account_include=["Whale1...", "Whale2..."],
            vote=False, failed=False,
        ),
    },
    accounts={
        "pools": SubscribeRequestFilterAccounts(
            account=["Pool1...", "Pool2..."],
        ),
    },
    commitment=CommitmentLevel.PROCESSED,
)

# In the response, update.filters tells you which matched: ["pumpfun"], ["whales"], ["pools"]
```

## Historical Replay

Resume from a specific slot (useful after disconnection):

```python
request = SubscribeRequest(
    transactions={...},
    from_slot=last_seen_slot - 32,  # subtract for reorg safety
)
```

Replay depth varies by provider: Shyft ~150 slots, QuickNode ~3000 slots, Helius ~24 hours.
