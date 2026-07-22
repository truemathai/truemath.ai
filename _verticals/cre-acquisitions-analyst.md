---
layout: vertical
title: "TrueMath for CRE Acquisitions Analysts: Underwriting Math from a Conversation"
description: "Model levered IRR, chart equity payback, and back into yield on cost in plain English — and get numbers that stand up to an investment committee. Deterministic, auditable CRE math."
body_class: page-vertical

# The domain library shown on the pill inside each demo frame.
name: "CRE Acquisitions Analyst"

# Hero. `hero_line` is the vertical-specific noun; the rest is shared framing.
hero_line: "CRE analysis"
hero_rest: "at the speed of conversation."
hero_accent: "<em>With receipts.</em>"
hero_sub: "Ask in plain English. Get a number that stands up to your investment committee."

# Where every call-to-action points.
cta_url: "https://app.truemath.ai/signup"

# ── The three demo prompts (real TrueMath output, replayed) ─────────────
demos:
  - id: "levered-irr"
    label: "Levered IRR, $7M deal, 5-yr hold"
    convo_title: "A $7M deal: NOI 450K growing 3%, 5-year hold…"
    prompt: "A 7,000,000 deal: NOI 450,000 growing 3%, 5-year hold, 65% LTV at 7% on 30-year am, closing 1.5%, exit cap 6.5%, selling costs 2%. What's my levered IRR?"
    ts: "9:12 AM"
    parse:
      - ["property_value", "7000000 USD"]
      - ["noi", "450000 USD"]
      - ["noi_growth_rate", "3%"]
      - ["hold_period_years", "5 yr"]
      - ["ltv_ratio", "65%"]
      - ["note_rate", "7%"]
      - ["loan_term_months", "360"]
      - ["closing_cost_rate", "1.5%"]
      - ["exit_cap_rate", "6.5%"]
      - ["selling_cost_rate", "2%"]
      - ["calculate", "irr_result"]
    blocks:
      - type: "kv"
        h: "Loan Amount from LTV"
        desc: "Calculates loan amount, property value, or LTV ratio given the other two values."
        lines:
          - ["Property Value / Purchase Price", "$7,000,000"]
          - ["Loan-to-Value Ratio (LTV)", "65.0%"]
          - ["Loan Amount", "$4,550,000"]
      - type: "kv"
        h: "Hold Period in Months"
        desc: "Expresses the hold period in months for the loan payoff calculation."
        lines:
          - ["Hold Period (Years)", "5 yr"]
          - ["Hold Period (Months)", "60"]
      - type: "kv"
        h: "Loan Payoff at Sale"
        desc: "Calculates the remaining loan balance at the end of the hold period."
        lines:
          - ["Hold Period (Months)", "60"]
          - ["Loan Amount", "$4,550,000"]
          - ["Interest Rate (Note Rate)", "7.00%"]
          - ["Loan Amortization Term (Months)", "360"]
          - ["Loan Payoff at Sale", "$4,282,987"]
      - type: "kv"
        h: "Hold Period as Scalar Years"
        desc: "Expresses the hold period as a bare number of years for use as a loop bound and in series index arithmetic."
        lines:
          - ["Hold Period (Years)", "5 yr"]
          - ["Hold Period (Scalar Years)", "5"]
      - type: "table"
        h: "Projected NOI Series"
        desc: "Projects NOI year-by-year over the hold period at a compound annual growth rate."
        lines:
          - ["Hold Period (Scalar Years)", "5"]
          - ["Net Operating Income (NOI)", "$450,000"]
          - ["NOI Growth Rate (Annual)", "3.0%"]
        table_label: "Projected NOI Series"
        table_col: "NOI"
        table_start: 1
        table_rows: ["$450,000", "$463,500", "$477,405", "$491,727", "$506,479"]
      - type: "kv"
        h: "Terminal / Reversion Value"
        desc: "Calculates the projected sale price at end of hold period by applying the exit cap rate to Year N+1 NOI, where the year-after-exit growth is taken from the final-period growth of the projected NOI series itself."
        lines:
          - ["Exit Cap Rate", "6.50%"]
          - ["Projected NOI Series", "See table above"]
          - ["Terminal / Reversion Value", "$8,025,744"]
      - type: "kv"
        h: "Net Sale Proceeds"
        desc: "Calculates net proceeds from sale after selling costs and loan payoff."
        lines:
          - ["Terminal / Reversion Value", "$8,025,744"]
          - ["Selling Cost Rate", "2.0%"]
          - ["Loan Payoff at Sale", "$4,282,987"]
          - ["Net Sale Proceeds", "$3,582,241"]
      - type: "kv"
        h: "Annual Debt Service"
        desc: "Calculates annual debt service, or back-solves loan amount or note rate, based on loan terms."
        lines:
          - ["Loan Amount", "$4,550,000"]
          - ["Interest Rate (Note Rate)", "7.00%"]
          - ["Loan Amortization Term (Months)", "360"]
          - ["Annual Debt Service", "$363,255"]
      - type: "table"
        h: "Annual Cash Flows Series"
        desc: "Builds a year-by-year table of pre-tax cash flows over the hold period."
        lines:
          - ["Hold Period (Scalar Years)", "5"]
          - ["Projected NOI Series", "See table above"]
          - ["Annual Debt Service", "$363,255"]
        table_label: "Annual Cash Flows Series"
        table_col: "Cash Flow"
        table_start: 1
        table_rows: ["$86,745", "$100,245", "$114,150", "$128,472", "$143,224"]
      - type: "kv"
        h: "Terminal Year Cash Flow"
        desc: "Calculates the total cash flow in the final hold year, combining operating cash flow and net sale proceeds."
        lines:
          - ["Annual Cash Flows Series", "See table above"]
          - ["Net Sale Proceeds", "$3,582,241"]
          - ["Terminal Year Cash Flow", "$3,725,465"]
      - type: "kv"
        h: "Closing Costs"
        desc: "Calculates closing costs as a percentage of property value."
        lines:
          - ["Property Value / Purchase Price", "$7,000,000"]
          - ["Closing Cost Rate", "1.5%"]
          - ["Closing Costs", "$105,000"]
      - type: "kv"
        h: "Equity Required"
        desc: "Calculates equity required as purchase price minus loan proceeds plus closing costs."
        lines:
          - ["Loan Amount", "$4,550,000"]
          - ["Property Value / Purchase Price", "$7,000,000"]
          - ["Closing Costs", "$105,000"]
          - ["Equity Required", "$2,555,000"]
      - type: "table"
        h: "IRR Cash Flow Vector"
        desc: "Constructs the full IRR cash flow vector: initial equity outflow, annual operating cash flows, and terminal year cash flow."
        lines:
          - ["Equity Required", "$2,555,000"]
          - ["Annual Cash Flows Series", "See table above"]
          - ["Hold Period (Scalar Years)", "5"]
          - ["Terminal Year Cash Flow", "$3,725,465"]
        table_label: "IRR Cash Flow Vector"
        table_col: "Cash Flow"
        table_start: 0
        table_rows: ["$-2,555,000", "$86,745", "$100,245", "$114,150", "$128,472", "$3,725,465"]
      - type: "kv"
        h: "Internal Rate of Return"
        desc: "Calculates the levered IRR from the full hold period cash flow vector."
        lines:
          - ["IRR Cash Flow Vector", "See table above"]
          - ["Internal Rate of Return (IRR)", "10.85%"]
    final: "Requested result for <b>Internal Rate of Return (IRR)</b> is <b>10.85%</b>."

  - id: "equity-payback"
    label: "Equity payback chart, $7.2M deal"
    convo_title: "NOI 484,800, price 7,200,000 — the equity payback…"
    prompt: "NOI 484,800, price 7,200,000, 65% LTV at 7% on 30-year am, closing 1.5%, NOI grows 3%, 5-year hold, exit cap 6.5%, selling 2%. Show me the equity payback chart."
    ts: "11:36 AM"
    parse:
      - ["noi", "484800 USD"]
      - ["property_value", "7200000 USD"]
      - ["ltv_ratio", "65%"]
      - ["note_rate", "7%"]
      - ["loan_term_months", "360"]
      - ["closing_cost_rate", "1.5%"]
      - ["noi_growth_rate", "3%"]
      - ["hold_period_years", "5 yr"]
      - ["exit_cap_rate", "6.5%"]
      - ["selling_cost_rate", "2%"]
      - ["calculate", "cumulative_return_chart"]
    blocks:
      - type: "kv"
        h: "Closing Costs"
        desc: "Calculates closing costs as a percentage of property value."
        lines:
          - ["Property Value / Purchase Price", "$7,200,000"]
          - ["Closing Cost Rate", "1.5%"]
          - ["Closing Costs", "$108,000"]
      - type: "kv"
        h: "Loan Amount from LTV"
        desc: "Calculates loan amount, property value, or LTV ratio given the other two values."
        lines:
          - ["Property Value / Purchase Price", "$7,200,000"]
          - ["Loan-to-Value Ratio (LTV)", "65.0%"]
          - ["Loan Amount", "$4,680,000"]
      - type: "kv"
        h: "Equity Required"
        desc: "Calculates equity required as purchase price minus loan proceeds plus closing costs."
        lines:
          - ["Loan Amount", "$4,680,000"]
          - ["Property Value / Purchase Price", "$7,200,000"]
          - ["Closing Costs", "$108,000"]
          - ["Equity Required", "$2,628,000"]
      - type: "kv"
        h: "Hold Period as Scalar Years"
        desc: "Expresses the hold period as a bare number of years for use as a loop bound and in series index arithmetic."
        lines:
          - ["Hold Period (Years)", "5 yr"]
          - ["Hold Period (Scalar Years)", "5"]
      - type: "table"
        h: "Equity Invested Reference Series"
        desc: "Builds a flat reference line equal to the equity invested in every year of the hold."
        lines:
          - ["Hold Period (Scalar Years)", "5"]
          - ["Equity Required", "$2,628,000"]
        table_label: "Equity Invested Reference Series"
        table_col: "Equity Invested"
        table_start: 1
        table_rows: ["$2,628,000", "$2,628,000", "$2,628,000", "$2,628,000", "$2,628,000"]
      - type: "kv"
        h: "Annual Debt Service"
        desc: "Calculates annual debt service, or back-solves loan amount or note rate, based on loan terms."
        lines:
          - ["Loan Amount", "$4,680,000"]
          - ["Interest Rate (Note Rate)", "7.00%"]
          - ["Loan Amortization Term (Months)", "360"]
          - ["Annual Debt Service", "$373,634"]
      - type: "table"
        h: "Projected NOI Series"
        desc: "Projects NOI year-by-year over the hold period at a compound annual growth rate."
        lines:
          - ["Hold Period (Scalar Years)", "5"]
          - ["Net Operating Income (NOI)", "$484,800"]
          - ["NOI Growth Rate (Annual)", "3.0%"]
        table_label: "Projected NOI Series"
        table_col: "NOI"
        table_start: 1
        table_rows: ["$484,800", "$499,344", "$514,324", "$529,754", "$545,647"]
      - type: "kv"
        h: "Hold Period in Months"
        desc: "Expresses the hold period in months for the loan payoff calculation."
        lines:
          - ["Hold Period (Years)", "5 yr"]
          - ["Hold Period (Months)", "60"]
      - type: "kv"
        h: "Loan Payoff at Sale"
        desc: "Calculates the remaining loan balance at the end of the hold period."
        lines:
          - ["Hold Period (Months)", "60"]
          - ["Loan Amount", "$4,680,000"]
          - ["Interest Rate (Note Rate)", "7.00%"]
          - ["Loan Amortization Term (Months)", "360"]
          - ["Loan Payoff at Sale", "$4,405,358"]
      - type: "kv"
        h: "Terminal / Reversion Value"
        desc: "Calculates the projected sale price at end of hold period by applying the exit cap rate to Year N+1 NOI, where the year-after-exit growth is taken from the final-period growth of the projected NOI series itself."
        lines:
          - ["Exit Cap Rate", "6.50%"]
          - ["Projected NOI Series", "See table above"]
          - ["Terminal / Reversion Value", "$8,646,401"]
      - type: "kv"
        h: "Net Sale Proceeds"
        desc: "Calculates net proceeds from sale after selling costs and loan payoff."
        lines:
          - ["Terminal / Reversion Value", "$8,646,401"]
          - ["Selling Cost Rate", "2.0%"]
          - ["Loan Payoff at Sale", "$4,405,358"]
          - ["Net Sale Proceeds", "$4,068,115"]
      - type: "table"
        h: "Cumulative Distributions Including Sale Series"
        desc: "Builds a running total of operating cash flow over the hold and adds the net sale proceeds in the final year."
        lines:
          - ["Hold Period (Scalar Years)", "5"]
          - ["Projected NOI Series", "See table above"]
          - ["Annual Debt Service", "$373,634"]
          - ["Net Sale Proceeds", "$4,068,115"]
        table_label: "Cumulative Distributions Including Sale Series"
        table_col: "Cumulative + Sale"
        table_start: 1
        table_rows: ["$111,166", "$236,876", "$377,567", "$533,687", "$4,773,814"]
      - type: "chart"
        h: "Cumulative Return vs. Equity Invested Chart"
        desc: "Produces a year-by-year chart comparing cumulative distributions, including sale proceeds in the final year, against the equity invested. The year the bars overtake the line is the equity payback year; the final bar over the line shows the equity multiple."
        legend: "Cumulative Distributions"
        legend2: "Equity Invested"
        axis_label: "Year"
    chart: [[111166.12, 2628000], [236876.24, 2628000], [377566.68, 2628000], [533686.84, 2628000], [4773814.30, 2628000]]
    final: "Requested result for <b>Cumulative Return vs. Equity Invested Chart</b> included above."

  - id: "yield-on-cost"
    label: "Yield on cost, $12M value-add"
    convo_title: "Going-in NOI 980K on a $12M deal, stabilize to 1.2M…"
    prompt: "Going-in NOI is 980,000 on a 12,000,000 deal. I'll spend 600,000 to stabilize at 1,200,000 NOI, closing 1.5%. What's my yield on cost?"
    ts: "4:05 PM"
    parse:
      - ["noi", "980000 USD"]
      - ["property_value", "12000000 USD"]
      - ["initial_capex", "600000 USD"]
      - ["stabilized_noi", "1200000 USD"]
      - ["closing_cost_rate", "1.5%"]
      - ["calculate", "yield_on_cost"]
    blocks:
      - type: "kv"
        h: "Closing Costs"
        desc: "Calculates closing costs as a percentage of property value."
        lines:
          - ["Property Value / Purchase Price", "$12,000,000"]
          - ["Closing Cost Rate", "1.5%"]
          - ["Closing Costs", "$180,000"]
      - type: "kv"
        h: "Total Basis"
        desc: "Calculates total cost basis as purchase price plus closing costs plus any immediate acquisition CapEx."
        lines:
          - ["Property Value / Purchase Price", "$12,000,000"]
          - ["Closing Costs", "$180,000"]
          - ["Initial Acquisition CapEx", "$600,000"]
          - ["Total Basis", "$12,780,000"]
      - type: "kv"
        h: "Yield on Cost"
        desc: "Calculates the unlevered yield on total invested cost at stabilization."
        lines:
          - ["Stabilized NOI", "$1,200,000"]
          - ["Total Basis", "$12,780,000"]
          - ["Yield on Cost", "9.39%"]
    final: "Requested result for <b>Yield on Cost</b> is <b>9.39%</b>."

# ── The comparison ("02 The comparison") ───────────────────────────────
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
  text: "Underwrite a deal in plain English, and stand behind every number, down to the last decimal, in front of any investment committee."
  cta_label: "Start free"
---
