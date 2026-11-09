# 15-disciplina-psicologia — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: journal-entry-review

- Fuente: `SYasJ/claude-business-skills` → `plugins/accounting/skills/journal-entry-review` (MIT)
- Cuándo usarla: Review manual journals for purpose, support, and unusual patterns without accusing anyone on a hunch. Use when the user mentions journal entry review, manual journals, unusual entries, JE support, or asks for a journal entry review. Accounting skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'journal-entry-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Journal Entry Review

Review manual journals for purpose, support, and unusual patterns without accusing anyone on a hunch.

## When to use this skill

Use this skill when the user:

- journal entry review
- manual journals
- unusual entries
- JE support

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not an audit opinion, compilation, or tax advice. Do not invent accounting standards. Use the policy, framework, and chart of accounts the organization actually follows.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Population of manual journals
- Materiality
- Who can post
- Known top-side entries

## Workflow


### 1. Define the population

Manual versus system-generated, for the period. Do not review a sample and call it the population.
### 2. Support test

Each sampled entry needs a purpose and a source. Missing support is the finding, even if the amount looks ordinary.
### 3. Unusual items

Round numbers, late posting, entries to cash or revenue, and entries by people who rarely post. Unusual means 'review', not 'misconduct'.
### 4. Top-side entries

Management adjustments need the estimate memo. A verbal reason is a gap.
### 5. Segregation

Note if the preparer and poster are the same person for material entries, using their described process.
### 6. Write questions, not charges

The output is a review list for the controller. Do not allege fraud.

## Output

Deliver a **journal entry review**.

- Purpose of this journal entry review, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Priya Shah, controller at Northline Studio in Calgary, needs a journal entry review by 30 September 2026. Several round-dollar journals hit revenue on the last day of the quarter.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Several round-dollar journals hit revenue on the last day of the quarter.

Population of manual journals: Operating cash. Stated in the ask, not documented anywhere else
Materiality: Undeposited funds, recorded 14 September 2026. No supporting file attached
Who can post: Priya Shah, controller
Known top-side entries: Undeposited funds. Stated in the ask, not documented anywhere else
```

### Example outcome

**Journal entry review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Flag those entries for support and purpose, without alleging misconduct.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Population of manual journals | Operating cash. Stated in the ask, not documented anywhere else | Needs confirmation |
| Materiality | Undeposited funds, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Who can post | Priya Shah, controller | Carried into the draft |
| Known top-side entries | Undeposited funds. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Define the population**  
Manual versus system-generated, for the period. Do not review a sample and call it the population.

**2. Support test**  
Each sampled entry needs a purpose and a source. Missing support is the finding, even if the amount looks ordinary.

**3. Unusual items**  
Round numbers, late posting, entries to cash or revenue, and entries by people who rarely post. Unusual means 'review', not 'misconduct'.

**4. Top-side entries**  
Management adjustments need the estimate memo. A verbal reason is a gap.

**5. Segregation**  
Note if the preparer and poster are the same person for material entries, using their described process.

**Deliberately not done**
- Calling an unusual entry fraud.
- A sample described as a full review.
- No interest in support as long as the amount is small but over their threshold.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Calling an unusual entry fraud.
- A sample described as a full review.
- No interest in support as long as the amount is small but over their threshold.

## Related skills

- `internal-controls-walkthrough`
- `revenue-recognition-review`
- `month-end-close`


---

## SKILL: pre-trade-discipline-gate

- Fuente: `tradermonty/claude-trading-skills` → `skills/pre-trade-discipline-gate` (MIT)
- Cuándo usarla: Evaluate a local pre-trade checklist before manual order entry, blocking planless, oversized, revenge-risk, market-regime-blocked, or circuit-breaker-blocked entries while journaling the decision for trader-memory-core review.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/pre-trade-discipline-gate/` (requirements.txt, check_pre_trade_discipline.py)

# Pre-Trade Discipline Gate

## Overview

Evaluate whether a planned manual order should proceed before it is placed at the broker. This skill reads a local checklist plus optional market-regime, circuit-breaker, and trader-memory-core artifacts. It produces a `pre_trade_discipline_decision` artifact and can link that artifact back to the related thesis without changing the thesis review schedule.

The gate is intentionally offline. It does not place orders, cancel orders, call a broker API, or fetch market data.

## When to Use

- Immediately before placing any manual entry order
- When a candidate has passed chart validation and position sizing
- After a recent loss, to avoid revenge trades during the cooldown window
- When the workflow has an upstream `exposure_decision` and `circuit_breaker_decision`
- When you want checklist adherence to be visible in later trader-memory-core reviews

## Prerequisites

- Python 3.9+
- A local JSON or YAML answers file with candidate-level checklist answers
- Optional trader-memory-core thesis state under `state/theses/`
- Optional `exposure_decision` JSON from market-regime-daily / exposure-coach
- Optional `circuit_breaker_decision` JSON from drawdown-circuit-breaker

## Workflow

### Step 1: Prepare the Checklist

Create a JSON or YAML file with candidate answers. Only actionable manual-order intents are gated. Watchlist and ignore intents are journaled as `NO_ACTIONABLE_ORDERS`.

```json
{
  "candidates": [
    {
      "symbol": "AAPL",
      "thesis_id": "th_aapl_gm_20260703_0001",
      "order_intent": "ENTRY_READY",
      "entry_in_written_plan": true,
      "stop_predefined": true,
      "size_within_plan": true,
      "planned_risk_dollars": 500,
      "actual_risk_dollars": 500,
      "notes": "Entry matches the journaled breakout plan."
    }
  ]
}
```

Actionable intents are `ENTRY_READY`, `ACTIONABLE`, `ACTIONABLE_DAY1`, and `MANUAL_ORDER`. Non-actionable intents such as `WATCHLIST`, `DELAYED_EP_WATCH`, `PEAD_HANDOFF`, `IGNORE`, and `REJECTED` are recorded but do not create an order permission.

Provide both `planned_risk_dollars` and `actual_risk_dollars` for every actionable candidate. Use a finite, non-negative number or numeric string; zero is valid. Treat missing values, booleans, non-numeric strings, `NaN`, infinities, and negative values as `REVIEW_REQUIRED` inputs and review them before placing an order.

### Step 2: Run the Gate

```bash
python3 skills/pre-trade-discipline-gate/scripts/check_pre_trade_discipline.py \
  --answers-file state/manual-entry-checklist.json \
  --state-dir state/theses \
  --market-regime-decision reports/exposure_decision_latest.json \
  --circuit-breaker-decision reports/circuit_breaker_decision_latest.json \
  --output-dir reports/pre-trade-discipline \
  --journal-dir state/journal/pre-trade-discipline
```

Set `--as-of` for deterministic testing or backfills:

```bash
python3 skills/pre-trade-discipline-gate/scripts/check_pre_trade_discipline.py \
  --answers-file state/manual-entry-checklist.json \
  --as-of 2026-07-03T12:00:00-04:00
```

### Step 3: Interpret the Decision

| Decision | Meaning |
|---|---|
| `GO` | All actionable manual-order candidates passed the checklist and upstream gates |
| `REVIEW_REQUIRED` | Inputs are missing, unknown, or journaling failed; do not place orders until reviewed |
| `NO_GO` | At least one actionable candidate violated a discipline rule |
| `NO_ACTIONABLE_ORDERS` | The file contains no actionable manual orders; nothing should be placed |

By default the CLI exits `0` for every valid decision and exits `1` only for input or runtime errors. Use `--fail-on-non-go` when a shell pipeline should return `2` for any non-`GO` decision.

## Rules

The gate blocks an actionable candidate when:

- The entry is not confirmed in the written plan
- The stop is not predefined
- The size is not confirmed within plan
- Either risk-dollar field is missing or is not a finite, non-negative number (`REVIEW_REQUIRED`)
- `actual_risk_dollars` exceeds `planned_risk_dollars`
- trader-memory-core has a losing exit or partial loss inside the revenge window
- exposure-coach recommendation is `REDUCE_ONLY` or `CASH_PRIORITY`
- drawdown-circuit-breaker recommendation is `COOLDOWN`, `HALTED`, or `TRADING_HALTED`

Missing or unreadable market-regime or circuit-breaker artifacts produce `REVIEW_REQUIRED` for actionable orders. If no actionable order exists, the result remains `NO_ACTIONABLE_ORDERS`.

## Outputs

The script writes:

- `pre_trade_discipline_decision_YYYY-MM-DD_HHMMSS.json`
- A matching markdown report unless `--json-only` is set
- A JSONL journal row under `state/journal/pre-trade-discipline/` when `--journal-dir` is provided

Each candidate result includes a `checklist_answers` object with the written-plan, stop, size, risk-dollar, and notes answers used for the decision, so later reviews can audit what was answered at order time. Invalid risk-dollar values are stored as JSON `null`. Valid JSON decimals that cannot round-trip through a binary float are retained as numeric strings so underflow or precision loss cannot change the gate decision.

If a candidate includes `thesis_id` and `--state-dir` is provided, the JSON report is linked into the thesis `linked_reports` list using trader-memory-core `link_report`. The skill does not call `mark_reviewed` and does not change monitoring review dates.

## Resources

- `scripts/check_pre_trade_discipline.py` - Main CLI and rule engine
- `references/discipline_gate_framework.md` - Rule definitions and integration notes
- `skills/trader-memory-core/schemas/thesis.schema.json` - Thesis state schema

## Key Principles

1. **Manual execution only** - The output is a pre-broker checklist gate, not an order router.
2. **Written plan first** - No written entry plan, stop, or size confirmation means no manual entry.
3. **Producer-compatible state reading** - Revenge-risk detection follows trader-memory-core timestamp and outcome behavior.
4. **Journal without review side effects** - The gate links reports to theses without advancing review schedules.

### Referencia: references/discipline_gate_framework.md

# Pre-Trade Discipline Gate Framework

## Purpose

The pre-trade discipline gate sits after thesis registration and before any manual broker order. It is designed to stop planless, oversized, revenge-risk, or upstream-blocked entries while leaving watchlist decisions recordable.

The skill is advisory and journal-focused. It does not automate execution.

## Decision Model

Overall decisions are ranked:

1. `GO`
2. `NO_ACTIONABLE_ORDERS`
3. `REVIEW_REQUIRED`
4. `NO_GO`

`NO_GO` outranks `REVIEW_REQUIRED` so explicit rule violations are visible even when another candidate only needs review.

## Actionable Intents

Manual-order gate applies to:

- `ENTRY_READY`
- `ACTIONABLE`
- `ACTIONABLE_DAY1`
- `MANUAL_ORDER`

The following intents are journaled but do not imply a broker order:

- `WATCHLIST`
- `DELAYED_EP_WATCH`
- `PEAD_HANDOFF`
- `IGNORE`
- `REJECTED`

If all candidates are non-actionable, the output is `NO_ACTIONABLE_ORDERS`.

## Blocking Rules

An actionable candidate is `NO_GO` when:

- `entry_in_written_plan` is not true
- `stop_predefined` is not true
- `size_within_plan` is not true
- `actual_risk_dollars` is greater than `planned_risk_dollars`
- A losing exit or partial trim exists inside the revenge window
- Market-regime recommendation is `REDUCE_ONLY` or `CASH_PRIORITY`
- Circuit-breaker recommendation is `COOLDOWN`, `HALTED`, or `TRADING_HALTED`

Market-regime recommendation `NEW_ENTRY_ALLOWED` and circuit-breaker recommendation `TRADING_ALLOWED` are the only explicit pass values. Unknown or missing upstream artifacts produce `REVIEW_REQUIRED` for actionable orders.

Both `planned_risk_dollars` and `actual_risk_dollars` are required for an actionable candidate. Each field accepts a finite, non-negative number or numeric string, including zero. A missing value, boolean, non-numeric string, `NaN`, infinity, or negative value produces `REVIEW_REQUIRED`; the audit copy is normalized to JSON `null`. When both fields are valid and actual risk exceeds planned risk, the candidate is `NO_GO`. An explicit `NO_GO` rule remains higher priority than a simultaneous invalid-risk review.

## Trader Memory Integration

Revenge-risk detection reads trader-memory-core thesis YAML files:

- `status_history[].realized_pnl < 0` counts partial trims and terminal ledger events.
- Terminal theses with no ledger `realized_pnl` fall back to `outcome.pnl_dollars < 0` when a terminal date can be inferred.
- Date-only producer timestamps expanded to `YYYY-MM-DDT00:00:00+00:00` are counted on the named ET date, matching the drawdown-circuit-breaker behavior.
- Events after `--as-of` are ignored.

When `thesis_id` and `--state-dir` are provided, the skill links the generated JSON report with trader-memory-core `link_report`. It never uses `mark_reviewed`, because pre-trade checklist logging must not advance monitoring review dates.

The JSON report and JSONL journal retain candidate-level `checklist_answers` for `entry_in_written_plan`, `stop_predefined`, `size_within_plan`, `planned_risk_dollars`, `actual_risk_dollars`, and `notes`. Invalid risk-dollar values are stored as JSON `null`. Valid JSON decimals that cannot round-trip through a binary float are retained as numeric strings, preserving their exact value for the decision and audit record. This keeps GO decisions reviewable later instead of recording only failures.

## Workflow Integration

In `swing-opportunity-daily`, the gate runs after thesis registration and consumes same-workflow artifacts such as `candidate_journal_entry`, `position_sizing`, `trade_plans`, and `circuit_breaker_decision`.

In `stockbee-ep-daily`, the workflow first runs `drawdown-circuit-breaker` to produce `circuit_breaker_decision`, then runs this gate only for ACTIONABLE_DAY1 / ENTRY_READY manual-order candidates. Delayed EP, PEAD handoff, and ignored candidates are recorded as no-action orders.

`exposure_decision` remains a prerequisite workflow artifact. It should be supplied to the CLI by path; it is not listed under workflow `consumes` because strict workflow validation only permits artifacts produced earlier in the same workflow.


---

## SKILL: stanley-druckenmiller-investment

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/stanley-druckenmiller-investment` (MIT)
- Cuándo usarla: スタンレー・ドラッケンミラーの投資哲学と戦略に基づいた投資アドバイスを提供。30年間無敗、年率30%近いリターンを達成した伝説的投資家の思考法を活用し、マクロ経済分析、リスク管理、ポジション構築、市場サイクルの読み方などについて実践的な指導を行う。投資判断、市場分析、リスク管理、ポートフォリオ構築などの相談時に使用。

# スタンレー・ドラッケンミラーの投資アドバイザー

スタンレー・ドラッケンミラーの投資哲学と30年にわたる実績に基づいて、投資に関する実践的なアドバイスを提供します。

## 概要

このスキルは、以下のようなドラッケンミラーの核心的な投資原則に基づいてアドバイスを行います：

- **集中投資と忍耐**: 年に1-2回の絶好の機会を待ち、確信がある時に大きく張る
- **資本保全**: 「50%の損失を取り戻すには100%の利益が必要」- 大きな損失を避ける
- **未来志向**: 「現在に投資するな、18か月先の未来に投資せよ」
- **流動性重視**: 「市場を動かすのは企業収益ではなく中央銀行と流動性」
- **柔軟性**: 間違いに気づいたら即座に方向転換する

## 使用方法

### 基本的な質問への対応

ユーザーからの質問に対して、ドラッケンミラーの思考法を適用して回答します：

1. **市場分析の相談**
   - 現在の市場環境の評価
   - 18か月先の予測
   - 投資機会の識別

2. **リスク管理の相談**
   - ポジションサイズの決定
   - 損切りポイントの設定
   - ポートフォリオの防御策

3. **投資戦略の相談**
   - エントリータイミング
   - 資産配分の提案
   - 市場サイクルの判断

### リファレンスの活用

詳細な分析や具体的な手法については、以下のリファレンスファイルを参照します：

- **投資哲学の詳細**: `references/investment-philosophy.md` を参照
  - ポジション構築、リスク管理、ベアマーケット戦略など

- **市場分析手法**: `references/market-analysis-guide.md` を参照
  - マクロ経済分析、中央銀行政策の評価、資産配分決定など

- **実例と応用**: `references/case-studies.md` を参照
  - 歴史的成功事例、投資判断パターン、実践的応用方法など

## アドバイスの提供方法

### 1. 現状分析から始める
- ユーザーの投資目的と制約を理解
- 現在の市場環境を評価
- リスク許容度を確認

### 2. ドラッケンミラー流の視点を提供
- 18か月先を見据えた分析
- 中央銀行政策と流動性の影響
- 市場のコンセンサスとの乖離を指摘

### 3. 具体的な行動指針を示す
- 確信度に基づくポジションサイズ
- エントリーとエグジットの条件
- リスク管理の具体策

### 4. 重要な警告を含める
- 「見えない時は振るな」の原則
- 大きな損失を避ける重要性
- 柔軟性を保つ必要性

## 回答スタイル

- **明確で実践的**: 理論だけでなく具体的な行動指針を提供
- **リスク意識**: 常にダウンサイドリスクを考慮
- **謙虚さ**: 市場に対する謙虚さを忘れない
- **柔軟性**: 状況変化に応じた修正の必要性を強調

## 注意事項

1. **投資は自己責任**: このアドバイスは教育目的であり、投資判断は各自の責任で行うことを明確にする

2. **個別銘柄の推奨は避ける**: 投資の考え方や分析手法の提供に焦点を当てる

3. **リスクの強調**: ドラッケンミラー自身も強調する「資本保全」の重要性を常に伝える

4. **時代背景の考慮**: 過去の成功事例を現代の文脈で解釈する必要性を認識する

### Referencia: references/case-studies.md

# ドラッケンミラーの投資判断事例集

## 歴史的な成功事例

### 1. 1981年 ボルカー議長の金融引き締め
**状況**: インフレ率が二桁に達し、FRB議長ポール・ボルカーが強力な金融引き締めを実施

**ドラッケンミラーの分析**:
- 「この男（ボルカー）は絶対にインフレを許さない」と確信
- 市場コンセンサスはインフレ継続を予想
- 長期金利14%は将来のディスインフレを織り込んでいない

**投資行動**:
- ファンド資金の50%を年利14%の長期国債に集中投資
- 市場が予想するインフレ継続シナリオに逆張り

**結果**:
- インフレ率は急速に低下
- 長期国債価格は大幅上昇
- 巨額のリターンを獲得

**教訓**: 中央銀行の政策決意を正しく評価し、市場コンセンサスと逆の大胆な賭けをする

### 2. 1992年 ポンド危機（ブラック・ウェンズデー）
**状況**: 英国が欧州為替相場メカニズム（ERM）で無理なポンド高を維持

**ドラッケンミラーの分析**:
- 英国の経済ファンダメンタルズは弱い
- 高金利政策は持続不可能
- ドイツとの金利差が経済実態と乖離

**投資行動**:
- ソロスに「もっと大きく張るべき」と進言
- 100億ドル規模のポンド売りポジション構築

**結果**:
- 英国はERM離脱を余儀なくされる
- ポンドは急落
- 10億ドル以上の利益

**教訓**: 持続不可能な政策は必ず破綻する。確信があれば巨大なポジションも正当化される

### 3. 2007-2008年 金融危機
**状況**: 2003-2004年のFRB低金利政策が住宅バブルを生成

**ドラッケンミラーの分析**:
- FRBの「長期間低金利」約束は明らかに行き過ぎ
- 住宅価格の上昇は持続不可能
- 金融システムに深刻な歪みが蓄積

**投資行動**:
- 2005年頃から住宅市場の破綻を予見し準備
- 債券ロング、金融株ショート
- 安全資産へのシフト

**結果**:
- 2008年もプラスリターンを達成
- 市場暴落の中で資産を守り増やす

**教訓**: 中央銀行の政策ミスは数年後に大きな危機をもたらす。早期に察知し準備することが重要

### 4. 2023年 慎重姿勢の維持
**状況**: インフレ、金利上昇、地政学リスクなど不確実性が高い環境

**ドラッケンミラーの分析**:
- 「歴史上類を見ない複雑な環境」
- 明確な投資機会（fat pitch）が見当たらない
- リスク・リワードが不明確

**投資行動**:
- ポジションを極力抑制
- 日次ボラティリティを0.3-0.4%に管理
- 現金比率を高く維持

**教訓**: 見えない時は無理に振らない。機会を待つことも重要な戦略

## 投資判断のパターン分析

### パターン1: 政策転換の先読み
**特徴**:
- 中央銀行の政策が転換点に近づく
- 市場はまだ従来の政策継続を織り込む
- 転換後の影響を他者より早く認識

**アクション**:
- 政策転換で最も恩恵/打撃を受ける資産を特定
- 市場が気づく前にポジション構築
- 転換が明確になったら追加投資

### パターン2: 持続不可能な歪みの発見
**特徴**:
- 経済実態と乖離した価格・政策
- 当局や市場参加者の過信
- 破綻の触媒が見え始める

**アクション**:
- 歪みの解消で利益を得るポジション構築
- タイミングは柔軟に（早すぎることもある）
- 破綻が始まったら積極的に追撃

### パターン3: 極端なセンチメントの逆張り
**特徴**:
- 市場が一方向に極端に傾く
- 恐怖や強欲が判断を歪める
- ファンダメンタルズが無視される

**アクション**:
- 感情的な売買の反対側に立つ
- 段階的にポジション構築
- センチメント転換の兆候を待つ

### パターン4: 不確実性が高い時の様子見
**特徴**:
- 複数のシナリオが考えられる
- どの方向に動くか予測困難
- リスク・リワードが不明確

**アクション**:
- ポジションを最小化
- 流動性を確保
- 状況が明確になるまで待機

## リアルタイムでの応用方法

### ステップ1: 現状分析
1. 今、どの経済・政策サイクルにいるか？
2. 市場のコンセンサスは何か？
3. 持続不可能な歪みはないか？

### ステップ2: 18か月先の予測
1. 現在の政策・トレンドは持続可能か？
2. 転換点となりうる触媒は何か？
3. 市場は何を織り込んでいないか？

### ステップ3: 投資機会の評価
1. リスク・リワードは魅力的か？
2. 確信度はどの程度か？
3. タイミングは適切か？

### ステップ4: ポジション決定
1. 確信度に応じたサイズ設定
2. 最大損失の想定と許容確認
3. エグジット条件の事前設定

### ステップ5: 継続的モニタリング
1. 投資理由は有効か？
2. 新たな情報で判断を修正すべきか？
3. より良い機会が出現していないか？

### Referencia: references/investment-philosophy.md

# ドラッケンミラーの投資哲学と戦略

## 1. ポジション構築とリスク管理の原則

### 集中投資の哲学
- **"ブタ（pig）になる"**: 確信度の高い機会には大胆に集中投資する
- **分散投資の否定**: 「分散投資はビジネススクールで教える最も誤った概念」
- **待つ戦略**: 年に1-2回の絶好の機会を待ち、その時に大きく張る
- **格言**: 「卵を一つのかごに入れ、そのかごを注意深く見張れ」

### 資金管理の鉄則
- **資本保全が最優先**: 大きなドローダウンは絶対に避ける
- **損失の数学**: 「50%の損失を取り戻すには100%の利益が必要」
- **メリハリのある投資**:
  - 平時: 損失ゼロ～数%に抑える
  - 確信時: +50～60%の大勝を狙う
- **確信度に応じたポジションサイズ**: 見えない時はバットを振らない

### 損切りの徹底
- **即座の撤退**: 投資理由が崩れたら即座にポジションを解消
- **ソロスの教え**: 「史上最高の損失の切り手」から学んだ損切りの重要性
- **ヘッジの否定**: 「ヘッジが必要なポジションなら、そもそも持つべきではない」
- **勝ちトレードの追加**: 利益が乗っている時はより攻める

## 2. 相場観形成のプロセス

### マクロ経済分析の視点
- **18か月先を見る**: 「現在に投資するな、未来に投資せよ」
- **流動性重視**: 「市場を動かすのは企業収益ではなく中央銀行と流動性」
- **期待の重要性**: 「大事なのは人々がその企業についてこれから何を期待しているか」

### 中央銀行の政策分析
- **政策ミスの察知**: 中央銀行の行き過ぎた政策を見抜く
- **転換点の予測**: 金融政策の大きな転換点を先読み
- **歴史的事例**:
  - 1980年代初頭: ボルカー議長のインフレ抑制を確信し長期国債に集中投資
  - 2003-2004年: FRBの低金利政策の行き過ぎを警戒
  - 2007-2008年: 住宅バブル崩壊を予見し準備

### グローバル・マルチアセット視点
- **5-6つの資産バスケット**: 株式・債券・通貨・コモディティを俯瞰
- **最適な戦場選び**: 最も有利な市場・資産を選択
- **待つも相場**: 明確な機会がない時は現金比率を高める
- **ボラティリティ管理**: 日次変動を0.3-0.4%程度に抑える

## 3. ベアマーケット戦略

### 弱気相場での優位性
- **実績**: 「利益の約80%はベアマーケットで稼いだ」
- **機会の源泉**: 中央銀行の政策ミスによる市場の歪みを突く

### 具体的戦術
- **空売りの難しさ**: 「株式の空売りは非常に難しい」と認識
- **債券ロング**: 景気後退局面では長期国債で利益を狙う
- **安全資産シフト**: 国債、金、安定通貨への乗り換え
- **歪みの活用**: 過剰な悲観から生じる価格歪みを攻めの機会とする

### ベアマーケットの鉄則
1. **早期察知**: 危機の兆候をいち早く捉える
2. **防御態勢**: 株式エクスポージャーを急減
3. **逆張りの勇気**: 過剰反応による歪みに賭ける
4. **生存最優先**: 大損を避け、次の機会まで生き残る

## 4. 投資判断の心構え

### オープンマインドと柔軟性
- **市場の声を聴く**: 自分の予測に固執しない
- **即座の修正**: 誤りに気づいたら即座に方向転換
- **謙虚さ**: 市場に対する謙虚な姿勢を保つ

### メンタル管理
- **自己認識**: 「調子が良い時と悪い時を自覚せよ」
- **調子による調整**:
  - 不調時: バント程度にとどめる
  - 好調時: ホームランを狙う

### 長期的成功の秘訣
- **大胆さと慎重さの両立**: 攻めと守りのメリハリ
- **忍耐力**: 機会を待つ力
- **決断力**: チャンスと見たら最大限のリスクを取る勇気

### Referencia: references/market-analysis-guide.md

# ドラッケンミラー流市場分析ガイド

## マクロ経済分析フレームワーク

### 1. 中央銀行政策の評価

#### 分析ポイント
- **金利政策の方向性**: 緩和・中立・引き締めのサイクル位置
- **流動性の変化**: マネーサプライ、QE/QTの動向
- **政策の持続可能性**: 行き過ぎた政策の兆候を探る
- **市場期待との乖離**: 中銀の意図と市場の理解のギャップ

#### 警戒すべき政策ミスのサイン
- 長期間の極端な低金利維持
- インフレ圧力を無視した緩和継続
- 急激すぎる政策転換
- 市場との対話の失敗

### 2. 18か月先の未来予測

#### 予測の構成要素
1. **経済サイクルの位置**
   - 拡大初期・中期・後期・減速・後退のどの段階か
   - 次の転換点はいつ頃か

2. **政策サイクルとの関係**
   - 金融政策は経済に対して先行的か後追いか
   - 財政政策の影響度

3. **市場期待の織り込み度**
   - コンセンサス予想は楽観的か悲観的か
   - サプライズの可能性はどこにあるか

### 3. グローバル資産配分の決定

#### 資産クラス別評価基準

**株式**
- 流動性環境（緩和的か引き締め的か）
- 企業収益の方向性（改善か悪化か）
- バリュエーション（割高か割安か）
- センチメント（楽観か悲観か）

**債券**
- 金利の方向性予測
- イールドカーブの形状
- クレジットスプレッドの動向
- インフレ期待

**通貨**
- 金利差の動向
- 経常収支の状況
- 政治的安定性
- 資本フローの方向

**コモディティ**
- 需給バランス
- ドルの強弱
- インフレ/デフレ圧力
- 地政学リスク

## ポジション構築の実践

### 確信度の評価基準

#### 高確信度（大きく張る）の条件
1. **複数の要因が同じ方向を示す**（"ダックが列を成す"）
2. **市場のコンセンサスと大きく乖離**
3. **リスク・リワードが非常に有利**
4. **明確な触媒（カタリスト）が存在**

#### 低確信度（様子見）のサイン
- 相反するシグナルが混在
- 不確実性が極めて高い
- リスク・リワードが不明確
- タイミングが読めない

### エントリーとエグジットの判断

#### エントリー条件
1. **テクニカル確認**: トレンドの初期段階を確認
2. **ファンダメンタルズ**: 投資テーマが明確
3. **センチメント**: 過度な楽観・悲観の存在
4. **リスク管理**: 最大損失が許容範囲内

#### エグジット条件
- **投資理由の消失**: 当初のシナリオが崩れた
- **目標達成**: 想定した利益に到達
- **より良い機会**: 他により魅力的な投資機会が出現
- **リスク環境の変化**: 市場環境が大きく変化

## 危機対応プロトコル

### ベアマーケット突入の兆候

1. **金融政策の転換点**
   - 緩和から引き締めへの明確な転換
   - 流動性の急速な収縮

2. **信用市場のストレス**
   - クレジットスプレッドの急拡大
   - 銀行間市場の機能不全

3. **センチメントの極端な楽観**
   - 全員が強気
   - リスクの過小評価
   - レバレッジの過剰利用

### 危機時の行動指針

1. **即座の防御態勢**
   - リスク資産の削減
   - レバレッジの解消
   - 流動性の確保

2. **安全資産へのシフト**
   - 長期国債
   - 金
   - 安全通貨（円、スイスフラン等）

3. **逆張り機会の探索**
   - 過度な売りによる歪み
   - 質への逃避による優良資産の割安化
   - 政策対応による転換点

## 日常的なモニタリング項目

### 毎日チェックすべき指標
- 主要国の金利動向
- 株式市場の内部構造（上昇/下落銘柄数等）
- 通貨市場の動き
- VIX等のボラティリティ指標
- クレジット市場の動向

### 週次・月次でレビューすべき項目
- 経済指標の予想と実績の乖離
- 中央銀行高官の発言トーン
- 資金フローデータ
- ポジショニングデータ
- センチメント指標

### 四半期ごとの大局観チェック
- 投資テーマの妥当性確認
- 18か月先予測の修正
- ポートフォリオ全体のリスク評価
- 新たな投資機会の発掘


---

## SKILL: stanley-druckenmiller-investment

- Fuente: `tradermonty/claude-trading-skills` → `skills/stanley-druckenmiller-investment` (MIT)
- Cuándo usarla: Druckenmiller Strategy Synthesizer - Integrates 8 upstream skill outputs (Market Breadth, Uptrend Analysis, Market Top, Macro Regime, FTD Detector, VCP Screener, Theme Detector, CANSLIM Screener) into a unified conviction score (0-100), pattern classification, and allocation recommendation. Use when user asks about overall market conviction, portfolio positioning, asset allocation, strategy synthesis, or Druckenmiller-style analysis. Triggers on queries like "What is my conviction level?", "How should I position?", "Run the strategy synthesizer", "Druckenmiller analysis", "総合的な市場判断", "確信度スコア", "ポートフォリオ配分", "ドラッケンミラー分析".
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/stanley-druckenmiller-investment/` (requirements.txt, allocation_engine.py, report_generator.py, report_loader.py, scorer.py, strategy_synthesizer.py)

# Druckenmiller Strategy Synthesizer

## Purpose

Synthesize outputs from 8 upstream analysis skills (5 required + 3 optional) into a single composite conviction score (0-100), classify the market into one of 4 Druckenmiller patterns, and generate actionable allocation recommendations. This is a **meta-skill** that consumes structured JSON outputs from other skills — it requires no API keys of its own.

## When to Use This Skill

**English:**
- User asks "What's my overall conviction?" or "How should I be positioned?"
- User wants a unified view synthesizing breadth, uptrend, top risk, macro, and FTD signals
- User asks about Druckenmiller-style portfolio positioning
- User requests strategy synthesis after running individual analysis skills
- User asks "Should I increase or decrease exposure?"
- User wants pattern classification (policy pivot, distortion, contrarian, wait)

**Japanese:**
- 「総合的な市場判断は？」「今のポジショニングは？」
- ブレッドス、アップトレンド、天井リスク、マクロの統合判断
- 「エクスポージャーを増やすべき？減らすべき？」
- 「ドラッケンミラー分析を実行して」
- 個別スキル実行後の戦略統合レポート

---

## Input Requirements

### Required Skills (5)

| # | Skill | JSON Prefix | Role |
|---|-------|-------------|------|
| 1 | Market Breadth Analyzer | `market_breadth_` | Market participation breadth |
| 2 | Uptrend Analyzer | `uptrend_analysis_` | Sector uptrend ratios |
| 3 | Market Top Detector | `market_top_` | Distribution / top risk (defense) |
| 4 | Macro Regime Detector | `macro_regime_` | Macro regime transition (1-2Y structure) |
| 5 | FTD Detector | `ftd_detector_` | Bottom confirmation / re-entry (offense) |

### Optional Skills (3)

| # | Skill | JSON Prefix | Role |
|---|-------|-------------|------|
| 6 | VCP Screener | `vcp_screener_` | Momentum stock setups (VCP) |
| 7 | Theme Detector | `theme_detector_` | Theme / sector momentum |
| 8 | CANSLIM Screener | `canslim_screener_` | Growth stock setups + M(Market Direction) |

Run the required skills first. The synthesizer reads their JSON output from `reports/`.

---

## Execution Workflow

### Phase 1: Verify Prerequisites

Check that the 5 required skill JSON reports exist in `reports/` and are recent (< 72 hours). If any are missing, run the corresponding skill first.

### Phase 2: Execute Strategy Synthesizer

```bash
python3 skills/stanley-druckenmiller-investment/scripts/strategy_synthesizer.py \
  --reports-dir reports/ \
  --output-dir reports/ \
  --max-age 72
```

The script will:
1. Load and validate all upstream skill JSON reports
2. Extract normalized signals from each skill
3. Calculate 7 component scores (weighted 0-100)
4. Compute composite conviction score
5. Classify into one of 4 Druckenmiller patterns
6. Generate target allocation and position sizing
7. Output JSON and Markdown reports

### Phase 3: Present Results

Present the generated Markdown report, highlighting:
- Conviction score and zone
- Detected pattern and match strength
- Strongest and weakest components
- Target allocation (equity/bonds/alternatives/cash)
- Position sizing parameters
- Relevant Druckenmiller principle

### Phase 4: Provide Druckenmiller Context

Load appropriate reference documents to provide philosophical context:
- **High conviction:** Emphasize concentration and "fat pitch" principles
- **Low conviction:** Emphasize capital preservation and patience
- **Pattern-specific:** Apply relevant case study from `references/case-studies.md`

---

## 7-Component Scoring System

| # | Component | Weight | Source Skill(s) | Key Signal |
|---|-----------|--------|----------------|------------|
| 1 | Market Structure | **18%** | Breadth + Uptrend | Market participation health |
| 2 | Distribution Risk | **18%** | Market Top (inverted) | Institutional selling risk |
| 3 | Bottom Confirmation | **12%** | FTD Detector | Re-entry signal after correction |
| 4 | Macro Alignment | **18%** | Macro Regime | Regime favorability |
| 5 | Theme Quality | **12%** | Theme Detector | Sector momentum health |
| 6 | Setup Availability | **10%** | VCP + CANSLIM | Quality stock setups |
| 7 | Signal Convergence | **12%** | All 5 required | Cross-skill agreement |

## 4 Pattern Classifications

| Pattern | Trigger Conditions | Druckenmiller Principle |
|---------|-------------------|----------------------|
| Policy Pivot Anticipation | Transitional regime + high transition probability | "Focus on central banks and liquidity" |
| Unsustainable Distortion | Top risk >= 60 + contraction/inflationary regime | "How much you lose when wrong matters most" |
| Extreme Sentiment Contrarian | FTD confirmed + high top risk + bearish breadth | "Most money made in bear markets" |
| Wait & Observe | Low conviction + mixed signals (default) | "When you don't see it, don't swing" |

## Conviction Zone Mapping

| Score | Zone | Exposure | Guidance |
|-------|------|----------|----------|
| 80-100 | Maximum Conviction | 90-100% | Fat pitch - swing hard |
| 60-79 | High Conviction | 70-90% | Standard risk management |
| 40-59 | Moderate Conviction | 50-70% | Reduce position sizes |
| 20-39 | Low Conviction | 20-50% | Preserve capital, minimal risk |
| 0-19 | Capital Preservation | 0-20% | Maximum defense |

---

## Output Files

- `druckenmiller_strategy_YYYY-MM-DD_HHMMSS.json` — Structured analysis data
- `druckenmiller_strategy_YYYY-MM-DD_HHMMSS.md` — Human-readable report

## API Requirements

**None.** This skill reads JSON outputs from other skills. No API keys required.

## Reference Documents

### `references/investment-philosophy.md`
- Core Druckenmiller principles: concentration, capital preservation, 18-month horizon
- Quantitative rules: daily vol targets, max position sizing
- Load when providing philosophical context for conviction assessment

### `references/market-analysis-guide.md`
- Signal-to-action mapping framework
- Macro regime interpretation for allocation decisions
- Load when explaining component scores or allocation rationale

### `references/case-studies.md`
- Historical examples: 1992 GBP, 2000 tech bubble, 2008 crisis
- Pattern classification examples with actual market conditions
- Load when user asks about historical parallels

### `references/conviction_matrix.md`
- Quantitative signal-to-action mapping tables
- Market Top Zone x Macro Regime matrix
- Load when user needs precise exposure numbers for specific signal combinations

### When to Load References
- **First use:** Load `investment-philosophy.md` for framework understanding
- **Allocation questions:** Load `market-analysis-guide.md` + `conviction_matrix.md`
- **Historical context:** Load `case-studies.md`
- **Regular execution:** References not needed — script handles scoring

---

## Relationship to Other Skills

| Skill | Relationship | Time Horizon |
|-------|-------------|-------------|
| Market Breadth Analyzer | Input (required) | Current snapshot |
| Uptrend Analyzer | Input (required) | Current snapshot |
| Market Top Detector | Input (required) | 2-8 weeks tactical |
| Macro Regime Detector | Input (required) | 1-2 years structural |
| FTD Detector | Input (required) | Days-weeks event |
| VCP Screener | Input (optional) | Setup-specific |
| Theme Detector | Input (optional) | Weeks-months thematic |
| CANSLIM Screener | Input (optional) | Setup-specific |
| **This Skill** | **Synthesizer** | **Unified conviction** |

### Referencia: assets/strategy_report_template.md

<!-- Design Reference Template for report_generator.py
     NOT rendered at runtime. Update both files together. -->

# Druckenmiller Strategy Synthesizer Report

**Generated:** {{metadata.generated_at}}
**Input Skills:** {{metadata.skills_loaded}} loaded ({{metadata.required_count}} required + {{metadata.optional_count}} optional)

---

## 1. Conviction Dashboard

| Metric | Value |
|--------|-------|
| **Conviction Score** | **{{conviction.conviction_score}}/100** |
| **Zone** | {{conviction.zone}} |
| **Recommended Exposure** | {{conviction.exposure_range}} |
| **Strongest Component** | {{conviction.strongest_component.label}} ({{conviction.strongest_component.score}}) |
| **Weakest Component** | {{conviction.weakest_component.label}} ({{conviction.weakest_component.score}}) |

> **Guidance:** {{conviction.guidance}}

**Recommended Actions:**

{{#each conviction.actions}}
- {{this}}
{{/each}}

---

## 2. Pattern Classification

**Detected Pattern:** {{pattern.label}} (match: {{pattern.match_strength}}%)

> {{pattern.description}}

| Pattern | Match Score |
|---------|-----------|
{{#each pattern.all_pattern_scores}}
| {{@key}} | {{this}} |
{{/each}}

---

## 3. Component Scores (7 Components)

| # | Component | Weight | Score | Weighted |
|---|-----------|--------|-------|----------|
{{#each conviction.component_scores}}
| {{@index}} | {{this.label}} | {{this.weight}} | {{this.score}} | {{this.weighted_contribution}} |
{{/each}}
| | **TOTAL** | **100%** | | **{{conviction.conviction_score}}** |

---

## 4. Input Skills Summary

### Required Skills

| Skill | Score | Zone/State | Key Signal |
|-------|-------|-----------|------------|
{{#each input_summary_required}}
| {{this.name}} | {{this.score}} | {{this.zone}} | {{this.signal}} |
{{/each}}

### Optional Skills

| Skill | Score | Key Signal |
|-------|-------|------------|
{{#each input_summary_optional}}
| {{this.name}} | {{this.score}} | {{this.signal}} |
{{/each}}

---

## 5. Target Allocation

| Asset Class | Allocation |
|-------------|-----------|
| Equity | {{allocation.target.equity}}% |
| Bonds | {{allocation.target.bonds}}% |
| Alternatives | {{allocation.target.alternatives}}% |
| Cash | {{allocation.target.cash}}% |

---

## 6. Position Sizing & Risk

| Parameter | Value |
|-----------|-------|
| Max Single Position | {{position_sizing.max_single_position}}% |
| Daily Volatility Target | {{position_sizing.daily_vol_target}}% |
| Max Open Positions | {{position_sizing.max_positions}} |

---

## 7. Druckenmiller Principle

> *"{{druckenmiller_quote}}"*
>
> — Stanley Druckenmiller

**Application:** {{druckenmiller_application}}

---

## Methodology

This report synthesizes outputs from 8 upstream analysis skills (5 required + 3 optional) into a single conviction score using Stanley Druckenmiller's investment philosophy.

**7 Components** (weighted 0-100):

1. Market Structure (18%): Breadth + Uptrend health
2. Distribution Risk (18%): Market Top risk (inverted)
3. Bottom Confirmation (12%): FTD Detector re-entry signal
4. Macro Alignment (18%): Macro Regime positioning
5. Theme Quality (12%): Theme Detector momentum
6. Setup Availability (10%): VCP + CANSLIM setups
7. Signal Convergence (12%): Cross-skill agreement

**4 Patterns:** Policy Pivot Anticipation, Unsustainable Distortion, Extreme Sentiment Contrarian, Wait & Observe

---

**Disclaimer:** This analysis is for educational and informational purposes only. Not investment advice. Past performance does not guarantee future results. Conduct your own research and consult a financial advisor before making investment decisions.

### Referencia: references/case-studies.md

# ドラッケンミラーの投資判断事例集

## 歴史的な成功事例

### 1. 1981年 ボルカー議長の金融引き締め
**Pattern Classification:** Policy Pivot Anticipation
**Conviction Level:** Maximum Conviction (estimated 90+)
**Source:** *The New Market Wizards* (Jack Schwager, 1992), Chapter on Druckenmiller

**状況**: インフレ率が二桁に達し、FRB議長ポール・ボルカーが強力な金融引き締めを実施

**ドラッケンミラーの分析**:
- 「この男（ボルカー）は絶対にインフレを許さない」と確信
- 市場コンセンサスはインフレ継続を予想
- 長期金利14%は将来のディスインフレを織り込んでいない

**投資行動**:
- ファンド資金の50%を年利14%の長期国債に集中投資
- 市場が予想するインフレ継続シナリオに逆張り

**結果**:
- インフレ率は急速に低下
- 長期国債価格は大幅上昇
- 巨額のリターンを獲得

**教訓**: 中央銀行の政策決意を正しく評価し、市場コンセンサスと逆の大胆な賭けをする

### 2. 1992年 ポンド危機（ブラック・ウェンズデー）
**Pattern Classification:** Unsustainable Distortion
**Conviction Level:** Maximum Conviction (estimated 95+)
**Source:** *Soros on Soros* (George Soros, 1995); Bloomberg profile (Sep 1992)

**状況**: 英国が欧州為替相場メカニズム（ERM）で無理なポンド高を維持

**ドラッケンミラーの分析**:
- 英国の経済ファンダメンタルズは弱い
- 高金利政策は持続不可能
- ドイツとの金利差が経済実態と乖離

**投資行動**:
- ソロスに「もっと大きく張るべき」と進言
- 100億ドル規模のポンド売りポジション構築

**結果**:
- 英国はERM離脱を余儀なくされる
- ポンドは急落
- 10億ドル以上の利益

**教訓**: 持続不可能な政策は必ず破綻する。確信があれば巨大なポジションも正当化される

### 3. 2007-2008年 金融危機
**Pattern Classification:** Unsustainable Distortion → Extreme Sentiment Contrarian (Phase 2: bottom re-entry)
**Conviction Level:** High Conviction (defense) → Maximum Conviction (post-crash re-entry)
**Source:** Duquesne Capital performance records; Bloomberg interviews (2008-2009)

**状況**: 2003-2004年のFRB低金利政策が住宅バブルを生成

**ドラッケンミラーの分析**:
- FRBの「長期間低金利」約束は明らかに行き過ぎ
- 住宅価格の上昇は持続不可能
- 金融システムに深刻な歪みが蓄積

**投資行動**:
- 2005年頃から住宅市場の破綻を予見し準備
- 債券ロング、金融株ショート
- 安全資産へのシフト

**結果**:
- 2008年もプラスリターンを達成
- 市場暴落の中で資産を守り増やす

**教訓**: 中央銀行の政策ミスは数年後に大きな危機をもたらす。早期に察知し準備することが重要

### 4. 2023年 慎重姿勢の維持
**Pattern Classification:** Wait & Observe
**Conviction Level:** Low Conviction (estimated 25-35)
**Source:** Bloomberg interview (Jun 2023); CNBC Delivering Alpha (Sep 2023)

**状況**: インフレ、金利上昇、地政学リスクなど不確実性が高い環境

**ドラッケンミラーの分析**:
- 「歴史上類を見ない複雑な環境」
- 明確な投資機会（fat pitch）が見当たらない
- リスク・リワードが不明確

**投資行動**:
- ポジションを極力抑制
- 日次ボラティリティを0.3-0.4%に管理
- 現金比率を高く維持

**教訓**: 見えない時は無理に振らない。機会を待つことも重要な戦略

## 投資判断のパターン分析

### パターン1: 政策転換の先読み
**特徴**:
- 中央銀行の政策が転換点に近づく
- 市場はまだ従来の政策継続を織り込む
- 転換後の影響を他者より早く認識

**アクション**:
- 政策転換で最も恩恵/打撃を受ける資産を特定
- 市場が気づく前にポジション構築
- 転換が明確になったら追加投資

### パターン2: 持続不可能な歪みの発見
**特徴**:
- 経済実態と乖離した価格・政策
- 当局や市場参加者の過信
- 破綻の触媒が見え始める

**アクション**:
- 歪みの解消で利益を得るポジション構築
- タイミングは柔軟に（早すぎることもある）
- 破綻が始まったら積極的に追撃

### パターン3: 極端なセンチメントの逆張り
**特徴**:
- 市場が一方向に極端に傾く
- 恐怖や強欲が判断を歪める
- ファンダメンタルズが無視される

**アクション**:
- 感情的な売買の反対側に立つ
- 段階的にポジション構築
- センチメント転換の兆候を待つ

### パターン4: 不確実性が高い時の様子見
**特徴**:
- 複数のシナリオが考えられる
- どの方向に動くか予測困難
- リスク・リワードが不明確

**アクション**:
- ポジションを最小化
- 流動性を確保
- 状況が明確になるまで待機

## リアルタイムでの応用方法

### ステップ1: 現状分析
1. 今、どの経済・政策サイクルにいるか？
2. 市場のコンセンサスは何か？
3. 持続不可能な歪みはないか？

### ステップ2: 18か月先の予測
1. 現在の政策・トレンドは持続可能か？
2. 転換点となりうる触媒は何か？
3. 市場は何を織り込んでいないか？

### ステップ3: 投資機会の評価
1. リスク・リワードは魅力的か？
2. 確信度はどの程度か？
3. タイミングは適切か？

### ステップ4: ポジション決定
1. 確信度に応じたサイズ設定
2. 最大損失の想定と許容確認
3. エグジット条件の事前設定

### ステップ5: 継続的モニタリング
1. 投資理由は有効か？
2. 新たな情報で判断を修正すべきか？
3. より良い機会が出現していないか？

### Referencia: references/conviction_matrix.md

# Conviction Matrix - Signal-to-Action Mapping

Quantitative cross-reference tables for translating multi-skill signal combinations into specific exposure and action recommendations.

## 1. Market Top Zone x Macro Regime Matrix

Recommended **equity exposure %** based on the intersection of top risk and regime:

| Market Top Zone → | Green (0-20) | Yellow (21-40) | Orange (41-60) | Red (61-80) | Critical (81-100) |
|-------------------|:---:|:---:|:---:|:---:|:---:|
| **Broadening** | 95-100% | 80-90% | 65-75% | 45-55% | 25-35% |
| **Concentration** | 85-95% | 70-80% | 55-65% | 35-45% | 15-25% |
| **Transitional** | 80-90% | 65-75% | 50-60% | 30-40% | 10-20% |
| **Inflationary** | 70-80% | 55-65% | 40-50% | 25-35% | 5-15% |
| **Contraction** | 60-70% | 45-55% | 30-40% | 15-25% | 0-10% |

**Usage:** Find the cell at the intersection of the current Market Top score zone and the Macro Regime. This gives the recommended equity allocation range.

## 2. Breadth Zone x VCP Availability Matrix

Recommended **new position entry** aggressiveness:

| Breadth Zone → | Healthy (60+) | Recovering (40-59) | Weak (20-39) | Critical (<20) |
|----------------|:---:|:---:|:---:|:---:|
| **Textbook VCP (90+)** | Full size, aggressive | 75% size | 50% size, pilot only | No new entries |
| **Strong VCP (80-89)** | Full size | 75% size | 25% size, pilot | No new entries |
| **Good VCP (70-79)** | 75% size | 50% size | Watchlist only | No new entries |
| **Developing (60-69)** | Watchlist | Watchlist | Pass | Pass |

## 3. FTD State x Market Top Risk Matrix

Recommended **re-entry behavior** after corrections:

| FTD State → | FTD Confirmed | Rally Attempt | No Signal | Rally Failed |
|-------------|:---:|:---:|:---:|:---:|
| **Top < 30 (Low Risk)** | Aggressive re-entry, 80%+ | Moderate entry, 60% | Normal operations | Monitor only |
| **Top 30-50 (Moderate)** | Measured re-entry, 60% | Small pilot, 30% | Stay cautious | Stay defensive |
| **Top 50-70 (Elevated)** | Selective entry, 40% | Watchlist only | Reduce exposure | Maximum defense |
| **Top > 70 (High Risk)** | Contrarian pilot, 25% | No new entries | Sell rallies | Full cash/hedge |

**Key insight:** FTD Confirmed + Top > 70 = Pattern 3 (Extreme Sentiment Contrarian). This is Druckenmiller's "most money made in bear markets" setup.

## 4. Macro Regime x Theme Quality Matrix

Recommended **sector/theme tilt**:

| Regime → | Broadening | Concentration | Transitional | Inflationary | Contraction |
|----------|:---:|:---:|:---:|:---:|:---:|
| **Hot themes (70+)** | Ride themes, broad | Ride themes in mega-caps | Selective theme plays | Commodity themes only | Avoid, preserve cash |
| **Moderate themes (40-69)** | Diversified across themes | Index-weighted | Wait for clarity | Real assets focus | Defensive only |
| **Cold themes (<40)** | Value/cyclical rotate | Mega-cap safety | Cash heavy | Gold/commodities | Full defensive |

## 5. Signal Convergence Interpretation

| Convergence Score | Meaning | Action |
|-------------------|---------|--------|
| 80-100 | All ducks in a row | Maximum conviction sizing |
| 60-79 | Most signals agree | Standard conviction sizing |
| 40-59 | Mixed signals | Reduced sizing, selective |
| 20-39 | Conflicting signals | Minimal positions, high cash |
| 0-19 | Complete disagreement | Sit out entirely |

## 6. Composite Conviction Decision Tree

```
Conviction >= 80 AND Convergence >= 70
  → Maximum exposure, concentrated positions
  → "Go for the jugular" - Druckenmiller

Conviction 60-79 AND Pattern = Policy Pivot
  → Overweight equity, lean into regime transition
  → "Focus on central banks and liquidity"

Conviction 40-59 AND Pattern = Unsustainable Distortion
  → Reduce to 40-50% equity, tighten all stops
  → "It's how much you lose when wrong"

Conviction < 40 AND FTD = Confirmed
  → Contrarian pilot positions (25-40% equity)
  → "Most money made in bear markets"

Conviction < 40 AND FTD != Confirmed
  → Capital preservation mode (10-30% equity)
  → "When you don't see it, don't swing"
```

## 7. Position Sizing Quick Reference

| Conviction Zone | Max Single | Max Positions | Daily Vol Target |
|----------------|:---:|:---:|:---:|
| Maximum (80-100) | 25% | 8 | 0.40% |
| High (60-79) | 15% | 12 | 0.30% |
| Moderate (40-59) | 10% | 15 | 0.25% |
| Low (20-39) | 5% | 20 | 0.15% |
| Preservation (0-19) | 3% | 25 | 0.10% |

### Referencia: references/investment-philosophy.md

# ドラッケンミラーの投資哲学と戦略

## 1. ポジション構築とリスク管理の原則

### 集中投資の哲学
- **"ブタ（pig）になる"**: 確信度の高い機会には大胆に集中投資する (Source: *The New Market Wizards*, Jack Schwager, 1992)
- **分散投資の否定**: 「分散投資はビジネススクールで教える最も誤った概念」 (Source: Lost Tree Club lecture, Jan 2015)
- **待つ戦略**: 年に1-2回の絶好の機会を待ち、その時に大きく張る (Source: Bloomberg interview, Jun 2023)
- **格言**: 「卵を一つのかごに入れ、そのかごを注意深く見張れ」

### 資金管理の鉄則
- **資本保全が最優先**: 大きなドローダウンは絶対に避ける
- **損失の数学**: 「50%の損失を取り戻すには100%の利益が必要」
- **メリハリのある投資**:
  - 平時: 損失ゼロ～数%に抑える
  - 確信時: +50～60%の大勝を狙う
- **確信度に応じたポジションサイズ**: 見えない時はバットを振らない

### 損切りの徹底
- **即座の撤退**: 投資理由が崩れたら即座にポジションを解消
- **ソロスの教え**: 「史上最高の損失の切り手」から学んだ損切りの重要性
- **ヘッジの否定**: 「ヘッジが必要なポジションなら、そもそも持つべきではない」
- **勝ちトレードの追加**: 利益が乗っている時はより攻める

## 2. 相場観形成のプロセス

### マクロ経済分析の視点
- **18か月先を見る**: 「現在に投資するな、未来に投資せよ」 (Source: Duquesne Capital Annual Letters)
- **流動性重視**: 「市場を動かすのは企業収益ではなく中央銀行と流動性」 (Source: Lost Tree Club lecture, Jan 2015)
- **期待の重要性**: 「大事なのは人々がその企業についてこれから何を期待しているか」

### 中央銀行の政策分析
- **政策ミスの察知**: 中央銀行の行き過ぎた政策を見抜く
- **転換点の予測**: 金融政策の大きな転換点を先読み
- **歴史的事例**:
  - 1980年代初頭: ボルカー議長のインフレ抑制を確信し長期国債に集中投資
  - 2003-2004年: FRBの低金利政策の行き過ぎを警戒
  - 2007-2008年: 住宅バブル崩壊を予見し準備

### グローバル・マルチアセット視点
- **5-6つの資産バスケット**: 株式・債券・通貨・コモディティを俯瞰
- **最適な戦場選び**: 最も有利な市場・資産を選択
- **待つも相場**: 明確な機会がない時は現金比率を高める
- **ボラティリティ管理**: 日次変動を0.3-0.4%程度に抑える

## 3. ベアマーケット戦略

### 弱気相場での優位性
- **実績**: 「利益の約80%はベアマーケットで稼いだ」
- **機会の源泉**: 中央銀行の政策ミスによる市場の歪みを突く

### 具体的戦術
- **空売りの難しさ**: 「株式の空売りは非常に難しい」と認識
- **債券ロング**: 景気後退局面では長期国債で利益を狙う
- **安全資産シフト**: 国債、金、安定通貨への乗り換え
- **歪みの活用**: 過剰な悲観から生じる価格歪みを攻めの機会とする

### ベアマーケットの鉄則
1. **早期察知**: 危機の兆候をいち早く捉える
2. **防御態勢**: 株式エクスポージャーを急減
3. **逆張りの勇気**: 過剰反応による歪みに賭ける
4. **生存最優先**: 大損を避け、次の機会まで生き残る

## 4. Quantitative Rules (定量ルール)

### Position Sizing
- **Maximum single position:** 25% of portfolio (Maximum Conviction only)
- **Normal conviction:** 10-15% per position
- **Pilot positions:** 3-5% per position when testing a thesis

### Volatility Management
- **Daily portfolio volatility target:** 0.3-0.4% (standard mode)
- **Reduced mode (unclear signals):** 0.1-0.2% daily vol
- **Maximum concentration:** 40% in any single asset class tilt vs benchmark

### Capital Preservation Thresholds
- **Maximum drawdown tolerance:** -5% triggers defensive mode
- **Annual target structure:** 0% in bad years, +30-60% in good years
- **"Two-strike rule":** Two consecutive losing months → cut all risk to minimum

### Entry/Exit Quantitative Criteria
- **Minimum risk/reward ratio:** 3:1 for standard entries, 5:1 for concentrated bets
- **Stop-loss framework:** Time-based (thesis timeframe) + Price-based (technical invalidation)
- **Profit target:** Let winners run; only exit on thesis change, NOT price targets

> See `references/conviction_matrix.md` for signal-to-action mapping tables.

## 5. 投資判断の心構え

### オープンマインドと柔軟性
- **市場の声を聴く**: 自分の予測に固執しない
- **即座の修正**: 誤りに気づいたら即座に方向転換
- **謙虚さ**: 市場に対する謙虚な姿勢を保つ

### メンタル管理
- **自己認識**: 「調子が良い時と悪い時を自覚せよ」
- **調子による調整**:
  - 不調時: バント程度にとどめる
  - 好調時: ホームランを狙う

### 長期的成功の秘訣
- **大胆さと慎重さの両立**: 攻めと守りのメリハリ
- **忍耐力**: 機会を待つ力
- **決断力**: チャンスと見たら最大限のリスクを取る勇気

### Referencia: references/market-analysis-guide.md

# ドラッケンミラー流市場分析ガイド

## マクロ経済分析フレームワーク

### 1. 中央銀行政策の評価

#### 分析ポイント
- **金利政策の方向性**: 緩和・中立・引き締めのサイクル位置
- **流動性の変化**: マネーサプライ、QE/QTの動向
- **政策の持続可能性**: 行き過ぎた政策の兆候を探る
- **市場期待との乖離**: 中銀の意図と市場の理解のギャップ

#### 警戒すべき政策ミスのサイン
- 長期間の極端な低金利維持
- インフレ圧力を無視した緩和継続
- 急激すぎる政策転換
- 市場との対話の失敗

### 2. 18か月先の未来予測

#### 予測の構成要素
1. **経済サイクルの位置**
   - 拡大初期・中期・後期・減速・後退のどの段階か
   - 次の転換点はいつ頃か

2. **政策サイクルとの関係**
   - 金融政策は経済に対して先行的か後追いか
   - 財政政策の影響度

3. **市場期待の織り込み度**
   - コンセンサス予想は楽観的か悲観的か
   - サプライズの可能性はどこにあるか

### 3. グローバル資産配分の決定

#### 資産クラス別評価基準

**株式**
- 流動性環境（緩和的か引き締め的か）
- 企業収益の方向性（改善か悪化か）
- バリュエーション（割高か割安か）
- センチメント（楽観か悲観か）

**債券**
- 金利の方向性予測
- イールドカーブの形状
- クレジットスプレッドの動向
- インフレ期待

**通貨**
- 金利差の動向
- 経常収支の状況
- 政治的安定性
- 資本フローの方向

**コモディティ**
- 需給バランス
- ドルの強弱
- インフレ/デフレ圧力
- 地政学リスク

## From Data to Decision (シグナル→アクション変換)

The Strategy Synthesizer uses the following rules to convert multi-skill signals into actionable decisions. See `references/conviction_matrix.md` for the full cross-reference tables.

### Green Light Conditions (Aggressive Posture)
- Breadth composite >= 60 **AND** Uptrend zone = Bull/Strong Bull
- Market Top score < 40 (low distribution risk)
- Macro Regime = broadening **AND** confidence = high
- FTD state = FTD_CONFIRMED (if applicable)
- **Action:** 80-100% equity, concentrated positions, standard stops

### Yellow Light Conditions (Cautious Posture)
- Breadth composite 40-59 **OR** Uptrend zone = Neutral
- Market Top score 40-60 (moderate risk)
- Macro Regime = transitional
- Mixed signal convergence (convergence score 40-60)
- **Action:** 50-70% equity, reduced sizing, tighter stops

### Red Light Conditions (Defensive Posture)
- Breadth composite < 40 **OR** Uptrend zone = Bear
- Market Top score >= 60 (elevated/high risk)
- Macro Regime = contraction
- FTD state = RALLY_FAILED
- **Action:** 0-30% equity, high cash, no new entries

### Pattern-Specific Overrides
- **Policy Pivot detected:** Overweight bonds + equity even if signals are mixed (anticipate regime shift)
- **Unsustainable Distortion detected:** Override green light → reduce to yellow light minimum
- **Extreme Contrarian detected:** Override red light → allow pilot equity entries (FTD confirmation)

---

## ポジション構築の実践

### 確信度の評価基準

#### 高確信度（大きく張る）の条件
1. **複数の要因が同じ方向を示す**（"ダックが列を成す"）
2. **市場のコンセンサスと大きく乖離**
3. **リスク・リワードが非常に有利**
4. **明確な触媒（カタリスト）が存在**

#### 低確信度（様子見）のサイン
- 相反するシグナルが混在
- 不確実性が極めて高い
- リスク・リワードが不明確
- タイミングが読めない

### エントリーとエグジットの判断

#### エントリー条件
1. **テクニカル確認**: トレンドの初期段階を確認
2. **ファンダメンタルズ**: 投資テーマが明確
3. **センチメント**: 過度な楽観・悲観の存在
4. **リスク管理**: 最大損失が許容範囲内

#### エグジット条件
- **投資理由の消失**: 当初のシナリオが崩れた
- **目標達成**: 想定した利益に到達
- **より良い機会**: 他により魅力的な投資機会が出現
- **リスク環境の変化**: 市場環境が大きく変化

## 危機対応プロトコル

### ベアマーケット突入の兆候

1. **金融政策の転換点**
   - 緩和から引き締めへの明確な転換
   - 流動性の急速な収縮

2. **信用市場のストレス**
   - クレジットスプレッドの急拡大
   - 銀行間市場の機能不全

3. **センチメントの極端な楽観**
   - 全員が強気
   - リスクの過小評価
   - レバレッジの過剰利用

### 危機時の行動指針

1. **即座の防御態勢**
   - リスク資産の削減
   - レバレッジの解消
   - 流動性の確保

2. **安全資産へのシフト**
   - 長期国債
   - 金
   - 安全通貨（円、スイスフラン等）

3. **逆張り機会の探索**
   - 過度な売りによる歪み
   - 質への逃避による優良資産の割安化
   - 政策対応による転換点

## 日常的なモニタリング項目

### 毎日チェックすべき指標
- 主要国の金利動向
- 株式市場の内部構造（上昇/下落銘柄数等）
- 通貨市場の動き
- VIX等のボラティリティ指標
- クレジット市場の動向

### 週次・月次でレビューすべき項目
- 経済指標の予想と実績の乖離
- 中央銀行高官の発言トーン
- 資金フローデータ
- ポジショニングデータ
- センチメント指標

### 四半期ごとの大局観チェック
- 投資テーマの妥当性確認
- 18か月先予測の修正
- ポートフォリオ全体のリスク評価
- 新たな投資機会の発掘


---

## SKILL: trade-journal

- Fuente: `agiprolabs/claude-trading-skills` → `skills/trade-journal` (MIT)
- Cuándo usarla: Structured trade logging, performance review, behavioral pattern detection, and strategy attribution for systematic improvement
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/trade-journal/` (journal_analyzer.py, trade_logger.py)

# Trade Journal

Structured trade journaling for systematic improvement. Log every trade with context, review performance at multiple cadences, detect behavioral patterns that destroy edge, and attribute returns to specific strategies.

## Why Journaling Matters

Most traders fail not from bad strategies but from bad behavior. A trade journal transforms subjective "feel" into objective data:

- **Strategy Attribution**: Know which setups actually make money vs. which feel profitable
- **Behavioral Detection**: Catch revenge trading, FOMO entries, and premature exits before they compound
- **Pattern Recognition**: Discover that your Monday morning trades lose money, or that you cut SOL winners too early
- **Accountability**: Written rationale before entry forces deliberate decision-making
- **Improvement Tracking**: Measure whether changes to your process actually improve results

Without a journal, you optimize on noise. With one, you optimize on signal.

## Trade Record Structure

Every trade record captures context at entry and outcome at exit. See `references/record_format.md` for the complete 18-field schema.

### Minimum Required Fields

```python
trade = {
    "id": "T-20250310-001",
    "token": "SOL",
    "direction": "long",
    "entry_date": "2025-03-10T14:30:00Z",
    "entry_price": 142.50,
    "size_sol": 5.0,
    "strategy": "momentum-breakout",
    "rationale": "Breaking above 4h resistance at 141.80 with volume confirmation",
    "exit_date": "2025-03-10T16:45:00Z",
    "exit_price": 146.20,
    "pnl_sol": 0.648,
    "outcome": "win",
    "lessons": "Held through initial pullback to 143.0, rewarded for patience"
}
```

### Strategy Tagging

Use consistent tags to enable performance attribution:

| Category | Tags |
|----------|------|
| Momentum | `momentum-breakout`, `trend-continuation`, `pullback-entry` |
| Mean Reversion | `range-fade`, `oversold-bounce`, `deviation-snap` |
| Event-Driven | `listing-play`, `catalyst-trade`, `news-reaction` |
| On-Chain | `whale-follow`, `wallet-copy`, `flow-signal` |
| DeFi | `lp-entry`, `yield-farm`, `arb-capture` |

### Rationale Templates

Write rationale **before** entering. Templates by setup type:

```
Momentum: "[Token] breaking [level] on [timeframe] with [confirmation]. Target [price], stop [price]."
Mean Reversion: "[Token] at [X] std devs from [mean] on [timeframe]. Expecting reversion to [target]."
On-Chain: "[Signal type] detected — [wallet/flow description]. Historical hit rate [X]%."
```

## Storage Format

The journal uses JSON for structured querying and CSV for spreadsheet compatibility.

### JSON Format (Primary)

```json
{
  "journal_version": "1.0",
  "trader_id": "anon",
  "trades": [
    {
      "id": "T-20250310-001",
      "token": "SOL",
      "direction": "long",
      "entry_date": "2025-03-10T14:30:00Z",
      "entry_price": 142.50,
      "size_sol": 5.0,
      "size_usd": 712.50,
      "strategy": "momentum-breakout",
      "setup_quality": 8,
      "rationale": "Breaking above 4h resistance with volume",
      "exit_date": "2025-03-10T16:45:00Z",
      "exit_price": 146.20,
      "pnl_sol": 0.648,
      "pnl_pct": 2.60,
      "outcome": "win",
      "hold_time_minutes": 135,
      "emotional_state": "calm",
      "lessons": "Patience through pullback paid off",
      "tags": ["high-conviction", "clean-setup"]
    }
  ]
}
```

### CSV Format (Export)

```
id,token,direction,entry_date,entry_price,size_sol,strategy,exit_date,exit_price,pnl_sol,pnl_pct,outcome,lessons
T-20250310-001,SOL,long,2025-03-10T14:30:00Z,142.50,5.0,momentum-breakout,2025-03-10T16:45:00Z,146.20,0.648,2.60,win,"Patience paid off"
```

## Analytics from Journal Data

### Win Rate by Strategy

```python
from collections import Counter

def win_rate_by_strategy(trades: list[dict]) -> dict[str, float]:
    """Compute win rate grouped by strategy tag."""
    strategy_outcomes: dict[str, list[str]] = {}
    for t in trades:
        strat = t["strategy"]
        strategy_outcomes.setdefault(strat, []).append(t["outcome"])

    return {
        strat: outcomes.count("win") / len(outcomes)
        for strat, outcomes in strategy_outcomes.items()
        if len(outcomes) >= 5  # minimum sample size
    }
```

### Performance by Time of Day

```python
from datetime import datetime

def pnl_by_hour(trades: list[dict]) -> dict[int, float]:
    """Aggregate P&L by entry hour (UTC)."""
    hourly: dict[int, float] = {}
    for t in trades:
        hour = datetime.fromisoformat(t["entry_date"].rstrip("Z")).hour
        hourly[hour] = hourly.get(hour, 0.0) + t.get("pnl_sol", 0.0)
    return dict(sorted(hourly.items()))
```

### Profit Factor by Token Type

```python
def profit_factor(trades: list[dict], group_key: str = "token") -> dict[str, float]:
    """Compute profit factor (gross wins / gross losses) by grouping key."""
    groups: dict[str, dict[str, float]] = {}
    for t in trades:
        key = t.get(group_key, "unknown")
        groups.setdefault(key, {"wins": 0.0, "losses": 0.0})
        pnl = t.get("pnl_sol", 0.0)
        if pnl > 0:
            groups[key]["wins"] += pnl
        else:
            groups[key]["losses"] += abs(pnl)

    return {
        k: v["wins"] / v["losses"] if v["losses"] > 0 else float("inf")
        for k, v in groups.items()
    }
```

## Behavioral Pattern Detection

The journal enables detection of destructive trading patterns. See `references/review_framework.md` for the full framework.

### Revenge Trading

Rapid re-entry after a loss, often with larger size:

```python
def detect_revenge_trades(trades: list[dict], max_gap_minutes: int = 15) -> list[dict]:
    """Find trades entered within max_gap_minutes of a losing exit."""
    sorted_trades = sorted(trades, key=lambda t: t["entry_date"])
    revenge = []
    for i in range(1, len(sorted_trades)):
        prev, curr = sorted_trades[i - 1], sorted_trades[i]
        if prev["outcome"] == "loss":
            prev_exit = datetime.fromisoformat(prev["exit_date"].rstrip("Z"))
            curr_entry = datetime.fromisoformat(curr["entry_date"].rstrip("Z"))
            gap = (curr_entry - prev_exit).total_seconds() / 60
            if gap <= max_gap_minutes:
                revenge.append(curr)
    return revenge
```

### FOMO Detection

Entering after large moves without proper setup:

- Entry rationale is vague or missing
- Setup quality self-rated below 5/10
- Entry during a move that already exceeded 1 ATR

### Cutting Winners / Riding Losers

```python
def winner_loser_hold_times(trades: list[dict]) -> dict[str, float]:
    """Compare average hold time for wins vs losses."""
    win_times = [t["hold_time_minutes"] for t in trades if t["outcome"] == "win"]
    loss_times = [t["hold_time_minutes"] for t in trades if t["outcome"] == "loss"]
    return {
        "avg_win_hold_min": sum(win_times) / len(win_times) if win_times else 0,
        "avg_loss_hold_min": sum(loss_times) / len(loss_times) if loss_times else 0,
    }
    # RED FLAG: if avg_loss_hold > avg_win_hold, you're cutting winners and riding losers
```

### Tilt Detection

Size escalation after losses suggests emotional trading:

```python
def detect_tilt(trades: list[dict], threshold: float = 1.5) -> list[dict]:
    """Flag trades where size increased >threshold after a loss."""
    tilt_trades = []
    for i in range(1, len(trades)):
        prev, curr = trades[i - 1], trades[i]
        if prev["outcome"] == "loss" and curr["size_sol"] > prev["size_sol"] * threshold:
            tilt_trades.append(curr)
    return tilt_trades
```

## Review Cadence

### Daily Review (5 minutes)

- How many trades today? P&L?
- Did I follow my rules on every trade?
- Any emotional decisions?
- One thing I did well, one thing to improve

### Weekly Review (30 minutes)

- Win rate and profit factor by strategy
- Behavioral pattern check (revenge trades, tilt, FOMO)
- Best and worst trade of the week — what made them different?
- Strategy performance vs. expectations
- Adjust position sizing if needed

### Monthly Review (2 hours)

- Full strategy attribution analysis
- Equity curve review — drawdown periods and recovery
- Compare actual vs. planned risk per trade
- Performance by token type, time of day, day of week
- Are any strategies consistently losing? Consider dropping them
- Review and update strategy parameters

See `references/review_framework.md` for detailed review checklists and questions.

## Partial Exits and Scaled Entries

Real trading involves scaling in and out. The journal handles this with child records:

```python
# Parent trade with two scale-out exits
parent = {
    "id": "T-20250310-001",
    "token": "BONK",
    "direction": "long",
    "entry_date": "2025-03-10T14:30:00Z",
    "entry_price": 0.000023,
    "size_sol": 10.0,
    "strategy": "momentum-breakout",
    "exits": [
        {"date": "2025-03-10T15:00:00Z", "price": 0.000025, "size_pct": 50, "reason": "first-target"},
        {"date": "2025-03-10T16:30:00Z", "price": 0.000028, "size_pct": 50, "reason": "trailing-stop"},
    ]
}
```

See `references/record_format.md` for full documentation of partial exit handling.

## Files

### References
- `references/record_format.md` — Complete 18-field trade record schema, field descriptions, tagging taxonomy, CSV/JSON examples, partial exit handling
- `references/review_framework.md` — Daily/weekly/monthly review checklists, behavioral red flags, performance decay detection

### Scripts
- `scripts/trade_logger.py` — CLI trade logger: add, list, update, compute stats, filter, demo mode (stdlib only)
- `scripts/journal_analyzer.py` — Journal analysis: strategy performance, behavioral patterns, time-based analysis, demo mode (stdlib only)

## Dependencies

Both scripts use Python standard library only (`json`, `datetime`, `argparse`, `collections`). No external packages required.

```bash
# No installation needed — stdlib only
python scripts/trade_logger.py --demo
python scripts/journal_analyzer.py --demo
```

## Disclaimer

This skill provides tools for trade record-keeping and performance analysis. It does not provide financial advice, trading recommendations, or guarantee any trading outcomes. All analysis is informational and for personal review purposes only.

### Referencia: references/record_format.md

# Trade Record Format — Complete Schema

## Overview

Every trade is a structured record capturing context at entry, outcome at exit, and reflective notes. The schema supports single-fill trades, scaled entries, and partial exits.

## Complete Field Schema (18 Fields)

### Required Fields

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | `id` | string | Unique trade ID. Format: `T-YYYYMMDD-NNN` |
| 2 | `token` | string | Token symbol (e.g., `SOL`, `BONK`, `JUP`) |
| 3 | `direction` | string | `long` or `short` |
| 4 | `entry_date` | string | ISO 8601 UTC timestamp of entry |
| 5 | `entry_price` | float | Entry price in USD or SOL |
| 6 | `size_sol` | float | Position size in SOL |
| 7 | `strategy` | string | Strategy tag from taxonomy |
| 8 | `rationale` | string | Written reason for the trade, recorded before entry |
| 9 | `outcome` | string | `win`, `loss`, or `breakeven` |

### Recommended Fields

| # | Field | Type | Description |
|---|-------|------|-------------|
| 10 | `exit_date` | string | ISO 8601 UTC timestamp of final exit |
| 11 | `exit_price` | float | Exit price (or VWAP for scaled exits) |
| 12 | `pnl_sol` | float | Realized P&L in SOL |
| 13 | `pnl_pct` | float | Realized P&L as percentage |
| 14 | `hold_time_minutes` | int | Total hold time in minutes |

### Optional Fields

| # | Field | Type | Description |
|---|-------|------|-------------|
| 15 | `size_usd` | float | Position size in USD at entry |
| 16 | `setup_quality` | int | Self-rated 1-10 quality of the setup |
| 17 | `emotional_state` | string | Emotional state at entry: `calm`, `anxious`, `excited`, `frustrated`, `fomo`, `revenge` |
| 18 | `lessons` | string | Post-trade reflection on what was learned |
| — | `tags` | list[str] | Freeform tags for filtering: `high-conviction`, `scalp`, `swing`, etc. |
| — | `stop_price` | float | Planned stop-loss price |
| — | `target_price` | float | Planned take-profit price |
| — | `risk_reward` | float | Planned risk:reward ratio |
| — | `fees_sol` | float | Transaction fees paid |
| — | `slippage_bps` | float | Observed slippage in basis points |
| — | `exits` | list | Partial exit records (see below) |
| — | `entries` | list | Scaled entry records (see below) |
| — | `screenshot_path` | string | Path to chart screenshot at entry |

## Strategy Tagging Taxonomy

Use a two-level hierarchy: `category-subcategory`.

### Momentum

| Tag | Description |
|-----|-------------|
| `momentum-breakout` | Price breaks key level with volume confirmation |
| `trend-continuation` | Entry on pullback within established trend |
| `pullback-entry` | Buy the dip in an uptrend |
| `volume-spike` | Unusual volume triggers entry |
| `new-high` | Token making new highs, riding momentum |

### Mean Reversion

| Tag | Description |
|-----|-------------|
| `range-fade` | Fade the edges of an established range |
| `oversold-bounce` | RSI/BB-based oversold entry |
| `deviation-snap` | Entry when price deviates N std devs from VWAP |
| `gap-fill` | Trading a gap fill |

### Event-Driven

| Tag | Description |
|-----|-------------|
| `listing-play` | New CEX/DEX listing momentum |
| `catalyst-trade` | Known upcoming catalyst (airdrop, launch) |
| `news-reaction` | Trading the reaction to news/announcement |

### On-Chain

| Tag | Description |
|-----|-------------|
| `whale-follow` | Following large wallet activity |
| `wallet-copy` | Copying a tracked profitable wallet |
| `flow-signal` | DEX flow imbalance signal |
| `holder-shift` | Significant change in holder distribution |

### DeFi

| Tag | Description |
|-----|-------------|
| `lp-entry` | Providing liquidity to a pool |
| `yield-farm` | Yield farming position |
| `arb-capture` | Arbitrage opportunity |

### Discretionary

| Tag | Description |
|-----|-------------|
| `gut-feel` | No formal setup — mark these for review |
| `revenge` | Re-entry after loss — always flag |
| `fomo` | Fear of missing out entry — always flag |

## Rationale Templates

Record rationale **before** placing the trade to enforce deliberation.

### Momentum Template

```
[TOKEN] breaking [LEVEL] on [TIMEFRAME] with [CONFIRMATION].
Volume is [X]x average. Target [PRICE] ([X]% up), stop [PRICE] ([X]% down).
R:R = [X]:1. Sizing [X] SOL ([X]% of portfolio).
```

### Mean Reversion Template

```
[TOKEN] at [X] standard deviations from [MEAN_TYPE] on [TIMEFRAME].
Historical reversion rate at this level: [X]%. Target reversion to [PRICE].
Stop beyond [PRICE] ([X] additional std devs). R:R = [X]:1.
```

### On-Chain Template

```
[SIGNAL_TYPE] detected: [DESCRIPTION].
Wallet [ADDRESS_PREFIX] has [X]% historical accuracy on similar trades.
Entry at [PRICE], target [PRICE], stop [PRICE].
```

### Event-Driven Template

```
Catalyst: [EVENT] expected [DATE/TIME].
Historical precedent: [SIMILAR_EVENTS] resulted in [X]% avg move.
Entry at [PRICE], exit plan: [DESCRIPTION].
```

## Partial Exits

When scaling out of a position, use the `exits` array:

```json
{
  "id": "T-20250310-001",
  "token": "SOL",
  "entry_price": 142.50,
  "size_sol": 10.0,
  "exits": [
    {
      "date": "2025-03-10T15:00:00Z",
      "price": 145.00,
      "size_pct": 33,
      "size_sol": 3.3,
      "reason": "first-target",
      "pnl_sol": 0.058
    },
    {
      "date": "2025-03-10T16:00:00Z",
      "price": 148.00,
      "size_pct": 33,
      "size_sol": 3.3,
      "reason": "second-target",
      "pnl_sol": 0.127
    },
    {
      "date": "2025-03-10T17:30:00Z",
      "price": 144.00,
      "size_pct": 34,
      "size_sol": 3.4,
      "reason": "trailing-stop",
      "pnl_sol": 0.036
    }
  ],
  "pnl_sol": 0.221,
  "exit_price": 145.67
}
```

The parent `exit_price` is the VWAP of all exits. The parent `pnl_sol` is the sum.

## Scaled Entries

When scaling into a position, use the `entries` array:

```json
{
  "id": "T-20250310-002",
  "token": "JUP",
  "entries": [
    {"date": "2025-03-10T10:00:00Z", "price": 0.85, "size_sol": 3.0, "reason": "initial"},
    {"date": "2025-03-10T11:00:00Z", "price": 0.82, "size_sol": 3.0, "reason": "add-on-dip"},
    {"date": "2025-03-10T12:30:00Z", "price": 0.80, "size_sol": 4.0, "reason": "final-add"}
  ],
  "entry_price": 0.821,
  "size_sol": 10.0
}
```

The parent `entry_price` is the VWAP of all entries.

## JSON Storage Format

```json
{
  "journal_version": "1.0",
  "trader_id": "anon",
  "created": "2025-01-01T00:00:00Z",
  "updated": "2025-03-10T14:30:00Z",
  "trades": []
}
```

## CSV Export Format

CSV uses flat columns. Partial exits are collapsed to summary values.

```csv
id,token,direction,entry_date,entry_price,size_sol,size_usd,strategy,setup_quality,rationale,exit_date,exit_price,pnl_sol,pnl_pct,outcome,hold_time_minutes,emotional_state,lessons
T-20250310-001,SOL,long,2025-03-10T14:30:00Z,142.50,5.0,712.50,momentum-breakout,8,"4h resistance break with volume",2025-03-10T16:45:00Z,146.20,0.648,2.60,win,135,calm,"Patience through pullback"
```

## Field Validation Rules

| Field | Validation |
|-------|-----------|
| `id` | Must match `T-YYYYMMDD-NNN` pattern |
| `direction` | Must be `long` or `short` |
| `entry_price` | Must be > 0 |
| `size_sol` | Must be > 0 |
| `outcome` | Must be `win`, `loss`, or `breakeven` |
| `setup_quality` | Must be 1-10 |
| `emotional_state` | Must be from allowed list |
| `pnl_pct` | Computed: `(exit_price - entry_price) / entry_price * 100` for longs |
| `hold_time_minutes` | Computed from entry/exit dates |

### Referencia: references/review_framework.md

# Review Framework — Daily, Weekly, Monthly

## Overview

Consistent review cadence is what transforms raw trade data into actionable improvement. Each level of review serves a different purpose: daily catches immediate behavioral issues, weekly reveals strategy-level patterns, and monthly drives structural changes.

## Daily Review (5 Minutes)

Perform at end of trading day or after last trade closes.

### Checklist

- [ ] How many trades today? What was net P&L?
- [ ] Did every trade have a written rationale before entry?
- [ ] Did I follow my position sizing rules on every trade?
- [ ] Did I honor my stop-losses without moving them?
- [ ] Were any trades emotional (FOMO, revenge, boredom)?
- [ ] One thing I did well today
- [ ] One thing to improve tomorrow

### Quick Stats to Compute

```python
daily_stats = {
    "trade_count": len(today_trades),
    "wins": sum(1 for t in today_trades if t["outcome"] == "win"),
    "losses": sum(1 for t in today_trades if t["outcome"] == "loss"),
    "net_pnl_sol": sum(t.get("pnl_sol", 0) for t in today_trades),
    "largest_win": max((t.get("pnl_sol", 0) for t in today_trades), default=0),
    "largest_loss": min((t.get("pnl_sol", 0) for t in today_trades), default=0),
}
```

### Red Flags — Immediate Action Required

| Flag | Signal | Action |
|------|--------|--------|
| 3+ losses in a row | Possible tilt | Stop trading for the day |
| Trade without rationale | Discipline breakdown | Write rationale retroactively, add to improvement list |
| Size > max allowed | Risk violation | Review position sizing rules |
| Trade entered < 10 min after loss | Revenge trading | Mark trade, review in weekly |

## Weekly Review (30 Minutes)

Perform every Sunday or on your designated review day.

### Checklist

- [ ] Total trades this week, win rate, net P&L
- [ ] Win rate and P&L by strategy — which strategies performed?
- [ ] Any revenge trades detected? (re-entry within 15 min of loss)
- [ ] Any tilt trades? (size increase > 1.5x after loss)
- [ ] Best trade of the week — what made it good?
- [ ] Worst trade of the week — what went wrong?
- [ ] Compare planned R:R vs actual R:R
- [ ] Are my self-rated setup quality scores predictive? (Do high-quality setups actually win more?)
- [ ] Any new patterns noticed?

### Questions to Ask

1. **Strategy performance**: Which strategies have positive expectancy over the last 20+ trades? Any strategies I should pause?
2. **Behavioral check**: Am I trading more after losses? Am I cutting winners short?
3. **Risk adherence**: Did I exceed my max daily loss on any day? Did I stick to position limits?
4. **Edge validation**: Is my overall profit factor above 1.5? If not, what is dragging it down?
5. **Improvement tracking**: Did the thing I said I would improve last week actually improve?

### Key Metrics to Compute

```python
weekly_metrics = {
    "total_trades": len(week_trades),
    "win_rate": wins / total if total > 0 else 0,
    "profit_factor": gross_wins / gross_losses if gross_losses > 0 else float("inf"),
    "avg_win_sol": avg(t["pnl_sol"] for t in wins),
    "avg_loss_sol": avg(abs(t["pnl_sol"]) for t in losses),
    "expectancy_sol": (win_rate * avg_win) - ((1 - win_rate) * avg_loss),
    "max_consecutive_losses": max_streak(week_trades, "loss"),
    "revenge_trade_count": len(detect_revenge_trades(week_trades)),
    "avg_setup_quality_winners": avg(t["setup_quality"] for t in wins),
    "avg_setup_quality_losers": avg(t["setup_quality"] for t in losses),
}
```

## Monthly Review (2 Hours)

Comprehensive analysis on the first weekend of each month.

### Checklist

- [ ] Full P&L breakdown by strategy, token, and time period
- [ ] Equity curve — any significant drawdowns?
- [ ] Strategy attribution — which strategies earned their keep?
- [ ] Behavioral pattern summary — trends in emotional trading?
- [ ] Compare this month to previous months — improving or declining?
- [ ] Review and update strategy parameters if needed
- [ ] Set specific improvement goals for next month

### Deep Analysis Questions

1. **Strategy lifecycle**: Are any strategies decaying? Compare last 30 trades vs prior 30 trades per strategy.
2. **Time analysis**: What hours/days are most profitable? Should I restrict trading to certain windows?
3. **Token analysis**: Am I better at trading certain token types? Large caps vs small caps?
4. **Hold time analysis**: Am I holding winners long enough? Am I cutting losses quickly enough?
5. **Sizing analysis**: Am I sizing correctly? Larger on high-conviction, smaller on speculative?
6. **Fee analysis**: What percentage of gross P&L goes to fees and slippage?

### Performance Decay Detection

Track rolling metrics to detect when a strategy or your overall trading is deteriorating.

```python
def detect_decay(trades: list[dict], window: int = 20) -> dict:
    """Compare recent window to prior window."""
    if len(trades) < window * 2:
        return {"status": "insufficient_data"}

    recent = trades[-window:]
    prior = trades[-window * 2:-window]

    recent_wr = sum(1 for t in recent if t["outcome"] == "win") / window
    prior_wr = sum(1 for t in prior if t["outcome"] == "win") / window

    recent_pf = compute_profit_factor(recent)
    prior_pf = compute_profit_factor(prior)

    return {
        "win_rate_change": recent_wr - prior_wr,
        "profit_factor_change": recent_pf - prior_pf,
        "decaying": recent_wr < prior_wr * 0.8 or recent_pf < prior_pf * 0.7,
        "recent_win_rate": recent_wr,
        "prior_win_rate": prior_wr,
    }
```

**Decay thresholds**:
- Win rate drops > 20% relative: investigate
- Profit factor drops > 30% relative: pause the strategy
- 3 consecutive losing weeks: full strategy review required

## Behavioral Red Flags

### Revenge Trading

**Definition**: Entering a new trade within 15 minutes of a losing exit, often with equal or larger size.

**Detection**: Compare `entry_date` of trade N to `exit_date` of trade N-1 when N-1 was a loss.

**Severity levels**:
- Mild: 1-2 revenge trades per week — note and monitor
- Moderate: 3-5 per week — implement mandatory 30-minute cooldown after losses
- Severe: Daily occurrence — stop live trading, review process

### FOMO (Fear of Missing Out)

**Indicators**:
- Setup quality self-rated < 5
- Rationale mentions "already moved" or "catching up"
- Entry after token already moved > 1 ATR from prior level
- No clear stop-loss defined

**Detection**: Correlate low setup quality scores with outcomes.

### Cutting Winners

**Definition**: Average hold time for winning trades is significantly shorter than for losing trades.

**Threshold**: If `avg_win_hold / avg_loss_hold < 0.7`, you are likely cutting winners.

**Fix**: Use trailing stops instead of fixed targets. Review exits on winners that continued moving favorably.

### Riding Losers

**Definition**: Holding losing trades far beyond the planned stop.

**Detection**: Compare actual exit price on losses to the recorded `stop_price`.

**Threshold**: If > 30% of losses exceed the planned stop by > 50%, there is a stop-honoring problem.

### Tilt / Emotional Sizing

**Definition**: Increasing position size after losses, driven by desire to "make it back."

**Detection**: Size of trade N vs trade N-1 when N-1 was a loss. Increase > 1.5x is a red flag.

**Impact analysis**: Compute P&L of tilt trades separately — they almost always have negative expectancy.

### Overtrading

**Definition**: Taking trades that do not meet setup criteria, often from boredom.

**Detection**:
- Trade count per day significantly above your baseline
- Setup quality scores trending downward through the day
- Trades without complete rationale

**Threshold**: More than 2x your average daily trade count without proportional increase in opportunities.

## Improvement Goal Setting

After monthly review, set 1-3 specific, measurable goals:

**Good goals**:
- "Reduce revenge trades from 4/week to 1/week"
- "Increase average setup quality of entries from 6.2 to 7.0"
- "Hold winning momentum trades for at least 2x the current average hold time"
- "Stop trading the `gut-feel` strategy until I can define entry criteria"

**Bad goals**:
- "Make more money" (not specific)
- "Be more disciplined" (not measurable)
- "Never have a losing trade" (not realistic)

Track goals in the journal metadata and review progress weekly.
