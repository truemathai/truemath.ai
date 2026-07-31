---
layout: vertical
title: "TrueMath for Real Estate Investors: Deal Analysis from a Conversation"
description: "Run cash-on-cash, a BRRRR cash-out refinance, and 10-year equity buildup in plain English — and get numbers that stand up to scrutiny. Deterministic, auditable real estate deal analysis."
body_class: page-vertical

# The domain library shown on the pill inside each demo frame.
name: "Real Estate Investor"

# Hero. `hero_line` is the vertical-specific noun; the rest is shared framing.
hero_line: "Cash-on-cash"
hero_rest: "at the speed of conversation."
hero_accent: "With receipts."
hero_sub: "Ask in plain English. Get a number you can stand behind before you wire the earnest money."

# Where every call-to-action points.
cta_url: "https://app.truemath.ai/signup"

# ── The three demo prompts ─────────────────────────────────────────────
demos:
  - id: "coc"
    label: "Duplex cash-on-cash, $320K, 25% down"
    date: "Jul 31, 2026"
    convo_title: "I'm looking at a $320,000 duplex that rents for $3,500 a month…"
    prompt: "I'm looking at a $320,000 duplex that rents for $3,500 a month. Figure 7% vacancy and operating expenses around 38% of rent. I'll put 25% down on a 30-year loan at 6.75%, with about $6,400 in closing costs. What's my cash-on-cash return?"
    ts: "8:47 AM"
    parse:
      - ["property_value", "320000 USD"]
      - ["gross_annual_rents", "42000 USD"]
      - ["vacancy_rate", "7%"]
      - ["expense_ratio", "38%"]
      - ["down_payment_pct", "25%"]
      - ["loan_term_years", "30 yr"]
      - ["interest_rate", "6.75%"]
      - ["closing_costs", "6400 USD"]
      - ["calculate", "cash_on_cash_return"]
    blocks:
      - type: "kv"
        h: "Effective Gross Income"
        desc: "Gross annual rents adjusted for vacancy: rents times one minus the vacancy rate."
        lines:
          - ["Effective Gross Income", "$39,060.00"]
          - ["Gross Annual Rents", "$42,000.00"]
          - ["Vacancy Rate", "7.00%"]
      - type: "kv"
        h: "Annual Operating Expenses"
        desc: "Operating expenses as a share of effective gross income; excludes debt service."
        lines:
          - ["Annual Operating Expenses", "$14,842.80"]
          - ["Effective Gross Income", "$39,060.00"]
          - ["Expense Ratio", "38.00%"]
      - type: "kv"
        h: "Net Operating Income"
        desc: "Effective gross income minus operating expenses, before debt service."
        lines:
          - ["Net Operating Income", "$24,217.20"]
          - ["Effective Gross Income", "$39,060.00"]
          - ["Annual Operating Expenses", "$14,842.80"]
      - type: "kv"
        h: "Down Payment"
        desc: "Property value times the down payment percent."
        lines:
          - ["Down Payment", "$80,000.00"]
          - ["Property Value", "$320,000.00"]
          - ["Down Payment Percent", "25.00%"]
      - type: "kv"
        h: "Loan Amount"
        desc: "Property value minus the down payment."
        lines:
          - ["Loan Amount", "$240,000.00"]
          - ["Property Value", "$320,000.00"]
          - ["Down Payment", "$80,000.00"]
      - type: "kv"
        h: "Monthly Debt Service"
        desc: "Fully amortizing principal and interest at the 6.750% rate over the 360-month term."
        lines:
          - ["Monthly PI Payment", "$1,556.64"]
          - ["Loan Amount", "$240,000.00"]
          - ["Interest Rate", "6.750%"]
          - ["Loan Term (Months)", "360"]
      - type: "kv"
        h: "Annual Debt Service"
        desc: "Monthly principal and interest times twelve."
        lines:
          - ["Annual Debt Service", "$18,679.63"]
          - ["Monthly PI Payment", "$1,556.64"]
      - type: "kv"
        h: "Cash to Close"
        desc: "Total cash invested: down payment plus closing costs plus any renovation."
        lines:
          - ["Cash to Close", "$86,400.00"]
          - ["Down Payment", "$80,000.00"]
          - ["Closing Costs", "$6,400.00"]
          - ["Renovation Cost", "$0.00"]
      - type: "kv"
        h: "Annual Net Cash Flow"
        desc: "NOI minus annual debt service."
        lines:
          - ["Annual Net Cash Flow", "$5,537.57"]
          - ["Net Operating Income", "$24,217.20"]
          - ["Annual Debt Service", "$18,679.63"]
    final: "Requested result for <b>Cash-on-Cash Return</b> is <b>6.41%</b>."

  - id: "brrrr"
    label: "BRRRR post-refi cash-on-cash, $210K in"
    date: "Jul 31, 2026"
    convo_title: "I'm $210,000 of my own cash into a BRRRR…"
    prompt: "I'm $210,000 of my own cash into a BRRRR, all in with the purchase and rehab. It appraises at $260,000, and I'm doing a 75% cash-out refinance at 7.5% on a 30-year loan, with about $5,000 in refi costs. I paid cash, so there's no acquisition loan to pay off. Stabilized, it nets $24,000 a year. After I pull my cash back out at the refinance, what's my cash-on-cash return?"
    ts: "6:12 PM"
    parse:
      - ["cash_to_close", "210000 USD"]
      - ["after_repair_value", "260000 USD"]
      - ["refinance_ltv", "75%"]
      - ["refinance_interest_rate", "7.5%"]
      - ["refinance_loan_term_years", "30 yr"]
      - ["refinance_costs", "5000 USD"]
      - ["debt_retired_at_refi", "0 USD"]
      - ["noi", "24000 USD"]
      - ["calculate", "post_refi_cash_on_cash"]
    blocks:
      - type: "kv"
        h: "Refinance Loan Amount"
        desc: "The cash-out refinance loan: after-repair value times the refinance LTV."
        lines:
          - ["Refinance Loan Amount", "$195,000"]
          - ["After-Repair Value", "$260,000"]
          - ["Refinance LTV", "75.00%"]
      - type: "kv"
        h: "Refinance Monthly Debt Service"
        desc: "Fully amortizing principal and interest on the refinance loan at 7.500% over the 360-month term."
        lines:
          - ["Refinance Monthly PI", "$1,363.47"]
          - ["Refinance Loan Amount", "$195,000"]
          - ["Refinance Interest Rate", "7.500%"]
          - ["Refinance Loan Term (Months)", "360"]
      - type: "kv"
        h: "Refinance Annual Debt Service"
        desc: "Refinance monthly payment times twelve."
        lines:
          - ["Refinance Annual Debt Service", "$16,361.62"]
          - ["Refinance Monthly PI", "$1,363.47"]
      - type: "kv"
        h: "Post-Refinance Annual Cash Flow"
        desc: "Stabilized NOI minus the refinance annual debt service."
        lines:
          - ["Post-Refinance Annual Cash Flow", "$7,638.38"]
          - ["Net Operating Income", "$24,000.00"]
          - ["Refinance Annual Debt Service", "$16,361.62"]
      - type: "kv"
        h: "Capital Recovered at Refinance"
        desc: "Cash pulled out at the refinance: the refinance loan minus debt retired minus refi costs."
        lines:
          - ["Capital Recovered", "$190,000"]
          - ["Refinance Loan Amount", "$195,000"]
          - ["Debt Retired at Refinance", "$0"]
          - ["Refinance Costs", "$5,000.00"]
      - type: "kv"
        h: "Capital Left in Deal"
        desc: "Total cash invested minus capital recovered — what's still tied up after the cash-out."
        lines:
          - ["Capital Left in Deal", "$20,000"]
          - ["Cash to Close", "$210,000.00"]
          - ["Capital Recovered", "$190,000"]
    final: "Requested result for <b>Post-Refinance Cash-on-Cash Return</b> is <b>38.19%</b>."

  - id: "equity"
    label: "Equity buildup, $320K duplex, 10-year hold"
    date: "Jul 31, 2026"
    convo_title: "A $320,000 duplex with 25% down… show me how my equity grows…"
    prompt: "A $320,000 duplex with 25% down on a 30-year loan at 6.75%. Assuming the property appreciates about 3% a year, show me how my equity grows over a 10-year hold."
    ts: "11:24 AM"
    parse:
      - ["property_value", "320000 USD"]
      - ["down_payment_pct", "25%"]
      - ["loan_term_years", "30 yr"]
      - ["interest_rate", "6.75%"]
      - ["annual_appreciation_rate", "3%"]
      - ["hold_period_years", "10 yr"]
      - ["calculate", "equity_series"]
    blocks:
      - type: "kv"
        h: "Loan Amount"
        desc: "Property value minus the 25% down payment."
        lines:
          - ["Loan Amount", "$240,000.00"]
          - ["Property Value", "$320,000.00"]
          - ["Down Payment", "$80,000.00"]
      - type: "kv"
        h: "Monthly Debt Service"
        desc: "Fully amortizing principal and interest at the 6.750% rate over the 360-month term."
        lines:
          - ["Monthly PI Payment", "$1,556.64"]
          - ["Loan Amount", "$240,000.00"]
          - ["Interest Rate", "6.750%"]
          - ["Loan Term (Months)", "360"]
      - type: "chart"
        h: "Equity Buildup Over the Hold"
        desc: "Year-by-year equity: appreciated value minus the remaining loan balance. Appreciation lifts the value while amortization pays the balance down, so equity compounds from both."
        legend: "Equity"
        axis_label: "Year"
      - type: "table"
        h: "Equity by Year"
        desc: "The full year-by-year equity position over the 10-year hold."
        table_col: "Equity"
        table_start: 1
        table_rows:
          - "$92,158"
          - "$104,782"
          - "$117,893"
          - "$131,513"
          - "$145,666"
          - "$160,376"
          - "$175,670"
          - "$191,574"
          - "$208,117"
          - "$225,331"
        lines_after:
          - ["Appreciated value, year 10", "$430,053"]
          - ["Loan balance, year 10", "$204,722"]
    chart: [92157.80, 104781.68, 117892.71, 131513.03, 145666.00, 160376.24, 175669.70, 191573.76, 208117.31, 225330.84]
    final: "Requested result for <b>Equity Series</b>: equity grows from <b>$92,158</b> in year 1 to <b>$225,331</b> by year 10."

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
  headline: "Run the deal. Trust the number."
  text: "Underwrite in plain English, and stand behind every figure, down to the last dollar."
  cta_label: "Start free"
---
