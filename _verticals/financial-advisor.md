---
layout: vertical
title: "TrueMath for Financial Advisors: Retirement Math from a Conversation"
description: "Project retirement balances, size sustainable withdrawals, and quantify fee drag in plain English — and get numbers that stand up to a client, their CPA, or compliance. Deterministic, auditable planning math."
body_class: page-vertical

# The domain library shown on the pill inside each demo frame.
name: "Financial Advisor"

# Hero. `hero_line` is the vertical-specific noun; the rest is shared framing.
hero_line: "Retirement scenarios"
hero_rest: "at the speed of conversation."
hero_accent: "With receipts."
hero_sub: "Ask in plain English. Get a number that stands up to scrutiny from your client, their CPA, or compliance."

# Where every call-to-action points.
cta_url: "https://app.truemath.ai/signup"

# ── The three demo prompts (real TrueMath output, replayed) ─────────────
demos:
  - id: "roth-conversion"
    label: "Roth conversion, $200K, 24% → 32%"
    convo_title: "A client is converting $200,000 to a Roth…"
    prompt: "A client is converting $200,000 to a Roth. They'll pay 24% tax on it now but expect to be in the 32% bracket in retirement, and they won't touch it for 20 years at a 7% return. How much more will the Roth leave them versus leaving it in a traditional account?"
    ts: "11:26 AM"
    parse:
      - ["conversion_amount", "200000 USD"]
      - ["current_tax_rate", "24%"]
      - ["future_tax_rate", "32%"]
      - ["conversion_years", "20 yr"]
      - ["investment_return_rate", "7%"]
      - ["calculate", "roth_advantage"]
    blocks:
      - type: "kv"
        h: "Traditional Account After-Tax Future Value"
        desc: "Projects the after-tax future value of keeping funds in a traditional account, growing the full pre-tax amount and applying the future tax rate at withdrawal."
        lines:
          - ["Roth Conversion Amount", "$200,000.00"]
          - ["Investment Return Rate (Roth Comparison)", "7.000%"]
          - ["Roth Conversion Holding Period (Years)", "20 yr"]
          - ["Future Marginal Tax Rate", "32.000%"]
          - ["Traditional Account After-Tax Future Value", "$526,277.09"]
      - type: "kv"
        h: "Roth After-Tax Future Value"
        desc: "Projects the future value of a Roth conversion where income tax is paid from the converted amount at the current tax rate and the remainder grows tax-free."
        lines:
          - ["Roth Conversion Amount", "$200,000.00"]
          - ["Current Marginal Tax Rate", "24.000%"]
          - ["Investment Return Rate (Roth Comparison)", "7.000%"]
          - ["Roth Conversion Holding Period (Years)", "20 yr"]
          - ["Roth After-Tax Future Value", "$588,192.04"]
      - type: "kv"
        h: "Roth Conversion Advantage"
        desc: "Calculates the dollar advantage of a Roth conversion over keeping funds in a traditional account at a given future tax rate and holding horizon."
        lines:
          - ["Roth After-Tax Future Value", "$588,192.04"]
          - ["Traditional Account After-Tax Future Value", "$526,277.09"]
          - ["Roth Conversion Advantage", "$61,914.95"]
    final: "Requested result for <b>Roth Conversion Advantage</b> is <b>$61,914.95</b>."

  - id: "drawdown"
    label: "Drawdown curve, $7K/mo for 30 yrs"
    convo_title: "A client has $150,000 saved today and adds $20,000 a year…"
    prompt: "A client has $150,000 saved today and adds $20,000 a year, growing at 7% for 20 years until retirement. Then they draw $7,000 a month for 30 years with the portfolio earning 5%. Show me the drawdown curve."
    ts: "11:28 AM"
    parse:
      - ["current_portfolio_value", "150000 USD"]
      - ["annual_contribution", "20000 USD"]
      - ["annual_return_rate", "7%"]
      - ["accumulation_years", "20 yr"]
      - ["monthly_withdrawal", "7000 USD/mo"]
      - ["withdrawal_years", "30 yr"]
      - ["withdrawal_return_rate", "5%"]
      - ["calculate", "retirement_drawdown_curve"]
    blocks:
      - type: "kv"
        h: "Retirement Portfolio Accumulation"
        desc: "Projects a portfolio to its value at retirement given current balance, annual contributions, return rate, and years to retirement."
        lines:
          - ["Current Portfolio Value", "$150,000.00"]
          - ["Annual Contribution", "$20,000.00"]
          - ["Annual Return Rate (Accumulation)", "7.000%"]
          - ["Years to Retirement", "20.0 yr"]
          - ["Retirement Starting Balance", "$1,400,362.52"]
      - type: "kv"
        h: "Annualize Monthly Withdrawal"
        desc: "Converts a monthly withdrawal into the equivalent annual withdrawal."
        lines:
          - ["Monthly Withdrawal", "7,000.00 USD/mo"]
          - ["Annual Withdrawal", "$84,000.00"]
      - type: "chart"
        h: "Retirement Drawdown Curve"
        desc: "Produces a year-by-year table of portfolio balances during the retirement distribution phase, floored at zero when the portfolio is depleted."
        lines:
          - ["Years of Retirement Income Needed", "30.0 yr"]
          - ["Retirement Starting Balance", "$1,400,362.52"]
          - ["Annual Withdrawal", "$84,000.00"]
          - ["Return Rate During Retirement", "5.000%"]
        chart_label: "Retirement Drawdown Curve"
        legend: "Portfolio Balance"
        axis_label: "Year of Retirement"
    chart: [1386380.64, 1371699.67, 1356284.66, 1340098.89, 1323103.83, 1305259.03, 1286521.98, 1266848.08, 1246190.48, 1224500.00, 1201725.00, 1177811.26, 1152701.82, 1126336.91, 1098653.75, 1069586.44, 1039065.76, 1007019.05, 973370.00, 938038.50, 900940.43, 861987.45, 821086.82, 778141.17, 733048.22, 685700.63, 635985.67, 583784.95, 528974.20, 471422.91]
    final: "Requested result for <b>Retirement Drawdown Curve</b> included above."

  - id: "fee-drag"
    label: "Fee drag, $500K, 0.25% vs 1%"
    convo_title: "On a $500,000 portfolio earning 7% before fees…"
    prompt: "On a $500,000 portfolio earning 7% before fees over 30 years, how much does the fee difference cost between an index fund at 0.25% and an advisor charging 1%?"
    ts: "11:19 AM"
    parse:
      - ["current_portfolio_value", "500000 USD"]
      - ["gross_return_rate", "7%"]
      - ["fee_comparison_years", "30 yr"]
      - ["low_fee_rate", "0.25%"]
      - ["high_fee_rate", "1%"]
      - ["calculate", "fee_drag_amount USD"]
    blocks:
      - type: "kv"
        h: "Net Return After High Fee"
        desc: "Calculates the net investment return after subtracting the higher fee rate in a fee comparison."
        lines:
          - ["Gross Return Rate (Before Fees)", "7.000%"]
          - ["High Fee Rate", "1.000%"]
          - ["Net Return After High Fee", "6.000%"]
      - type: "kv"
        h: "Portfolio Value at High Fee"
        desc: "Projects the terminal portfolio value under the higher fee scenario."
        lines:
          - ["Current Portfolio Value", "$500,000.00"]
          - ["Annual Contribution", "0.00"]
          - ["Net Return After High Fee", "6.000%"]
          - ["Fee Comparison Horizon (Years)", "30 yr"]
          - ["Portfolio Value at High Fee", "$2,871,745.59"]
      - type: "kv"
        h: "Net Return After Low Fee"
        desc: "Calculates the net investment return after subtracting the lower fee rate in a fee comparison."
        lines:
          - ["Gross Return Rate (Before Fees)", "7.000%"]
          - ["Low Fee Rate", "0.250%"]
          - ["Net Return After Low Fee", "6.750%"]
      - type: "kv"
        h: "Portfolio Value at Low Fee"
        desc: "Projects the terminal portfolio value under the lower fee scenario."
        lines:
          - ["Current Portfolio Value", "$500,000.00"]
          - ["Annual Contribution", "0.00"]
          - ["Net Return After Low Fee", "6.750%"]
          - ["Fee Comparison Horizon (Years)", "30 yr"]
          - ["Portfolio Value at Low Fee", "$3,548,187.12"]
      - type: "kv"
        h: "Fee Drag Amount"
        desc: "Calculates the dollar difference in terminal portfolio value between the low fee and high fee scenarios."
        lines:
          - ["Portfolio Value at Low Fee", "$3,548,187.12"]
          - ["Portfolio Value at High Fee", "$2,871,745.59"]
          - ["Fee Drag Amount", "$676,441.54"]
    final: "Requested result for <b>Fee Drag Amount</b> is <b>$676,441.54</b>."

# ── The comparison ("02 The comparison") ───────────────────────────────
# Shared proof point, identical across verticals.
proof:
  headline: "Watch how LLMs really work."
  sub: "One prompt. Ten runs each. Nothing staged."
  prompt: "A 7,000,000 deal: NOI 450,000 growing 3%, 5-year hold, 65% LTV at 7% on 30-year am, closing 1.5%, exit cap 6.5%, selling costs 2%. What's my levered IRR?"
  exact_label: "The exact answer · 5-year levered IRR"
  exact_value: "10.8463781499708%"
  raw:
    label: "RAW LLM"
    score: "0"
    score_unit: "/10 exact"
    rows:
      - ["methods", "10 distinct"]
      - ["avg time", "29.7 s"]
      - ["energy / call", "~1.5 Wh"]
  good:
    label: "TRUEMATH"
    score: "10"
    score_unit: "/10 exact"
    rows:
      - ["method", "1, auditable"]
      - ["avg time", "3.1 s", "9.6× faster"]
      - ["energy / call", "~0.003 Wh", "~500× less"]
  methnote: "Claude Opus 4.8 vs TrueMath via natural language, 10 runs each. Energy is inference-only; datacenter cooling widens the gap."
  caption: "TrueMath was 9.6x faster, 500x more energy efficient, and delivered 10 identically precise answers using one fixed auditable method."
  receipt: "That's the receipt."

# ── Closing CTA (rendered with the site's shared CTA styling) ───────────
resolve:
  headline: "Just ask. Trust the answer."
  text: "Run a client's numbers in plain English, and stand behind every one, down to the last decimal, in front of the client, their CPA, or compliance."
  cta_label: "Start free"
---
