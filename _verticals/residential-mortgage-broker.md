---
layout: vertical
title: "TrueMath for Residential Mortgage Brokers: Loan Math from a Conversation"
description: "Structure buydowns, size a borrower's max purchase price, and model refi savings in plain English — and get numbers that stand up to scrutiny. Deterministic, auditable mortgage math."
body_class: page-vertical

# The domain library shown on the pill inside each demo frame.
name: "Residential Mortgage Broker"

# Hero. `hero_line` is the vertical-specific noun; the rest is shared framing.
hero_line: "Loan analysis"
hero_rest: "at the speed of conversation."
hero_accent: "With receipts."
hero_sub: "Ask in plain English. Get a number that stands up to scrutiny from anyone who matters."

# Where every call-to-action points.
cta_url: "https://app.truemath.ai/signup"

# ── The three demo prompts ─────────────────────────────────────────────
demos:
  - id: "buydown"
    label: "2-1 buydown, $600K loan, 6.75%"
    convo_title: "Structure a 2-1 buydown on a $600,000 loan…"
    prompt: "Structure a 2-1 buydown on a $600,000 loan at a 6.75% note rate, 30-year fixed. What does the seller need to deposit into escrow to fund it?"
    ts: "9:21 AM"
    parse:
      - ["loan_amount", "600000 USD"]
      - ["note_rate", "6.75%"]
      - ["loan_term", "30 yr"]
      - ["calculate", "total_buydown_subsidy_21 USD"]
    blocks:
      - type: "kv"
        h: "Year 1 Rate & Payment (2-1 Buydown)"
        desc: "Year-1 rate is 2 points below the note rate; payment computed at that rate."
        lines:
          - ["Year 1 Rate", "4.7500%"]
          - ["Year 1 PI Payment", "$3,129.88"]
      - type: "kv"
        h: "Year 2 Rate & Payment (2-1 Buydown)"
        desc: "Year-2 rate is 1 point below the note rate; payment computed at that rate."
        lines:
          - ["Year 2 Rate", "5.7500%"]
          - ["Year 2 PI Payment", "$3,501.44"]
      - type: "kv"
        h: "Note-Rate Payment"
        desc: "Monthly principal and interest at the full 6.750% note rate."
        lines:
          - ["Monthly PI Payment", "$3,891.59"]
      - type: "kv"
        h: "Year 1 & Year 2 Subsidy"
        desc: "Twelve times the monthly payment difference, for each buydown year."
        lines:
          - ["Year 1 Subsidy", "$9,140.45"]
          - ["Year 2 Subsidy", "$4,681.82"]
    final: "Requested result for <b>Total 2-1 Buydown Subsidy</b> is <b>$13,822.27</b>."

  - id: "maxprice"
    label: "Max purchase price, $12K income, 43% DTI"
    convo_title: "Sarah Chen makes 12k a month, wants to keep total DTI…"
    prompt: "Sarah Chen makes 12k a month, wants to keep total DTI at 43%, has 650 in other debt, taxes 450 ins 150, 20% down, 7.25% for 30 yrs. how much house can she get?"
    ts: "7:38 PM"
    parse:
      - ["gross_monthly_income", "12000 USD"]
      - ["target_dti", "43%"]
      - ["monthly_other_debt", "650 USD"]
      - ["monthly_property_tax", "450 USD"]
      - ["monthly_homeowners_insurance", "150 USD"]
      - ["down_payment_pct", "20%"]
      - ["note_rate", "7.25%"]
      - ["loan_term", "30 yr"]
      - ["calculate", "max_qualifying_purchase_price USD"]
    blocks:
      - type: "kv"
        h: "Loan Term in Months"
        desc: "Converts the practitioner-facing loan term into a bare month count for downstream math. A value with no unit passes through unchanged (already months); a unit-bearing value (for example 30 yr) is normalized to months."
        lines:
          - ["Loan Term (Months)", "360"]
          - ["Loan Term", "30 yr"]
      - type: "kv"
        h: "Maximum Qualifying PI Payment (PMI-Aware Final)"
        desc: "Calculates the borrower's maximum qualifying PI payment, with PMI folded in when it applies."
        lines:
          - ["Maximum Qualifying PI Payment", "$3,910.00"]
          - ["Target DTI", "43.000%"]
          - ["Gross Monthly Income", "$12,000.00"]
          - ["Monthly Other Debt Obligations", "$650.00"]
          - ["Monthly Property Tax", "$450.00"]
          - ["Monthly Homeowner's Insurance", "$150.00"]
          - ["Monthly HOA Dues", "0.00"]
      - type: "kv"
        h: "Maximum Qualifying Loan Amount Pass 1 (No PMI)"
        desc: "Calculates the loan amount that the first-pass qualifying PI payment can support."
        lines:
          - ["Maximum Qualifying Loan Amount (Pass 1, No PMI)", "$573,165.63"]
          - ["Maximum Qualifying PI Payment", "$3,910.00"]
          - ["Note Rate", "7.250%"]
          - ["Loan Term (Months)", "360"]
      - type: "kv"
        h: "Effective LTV at Qualifying"
        desc: "Calculates what the LTV would be at the borrower's maximum qualifying home price."
        lines:
          - ["Effective LTV at Qualifying", "80.000%"]
          - ["Down Payment Percent", "20.000%"]
      - type: "kv"
        h: "PMI Required at Qualifying"
        desc: "Determines whether PMI applies at the borrower's maximum qualifying home price."
        lines:
          - ["PMI Required at Qualifying", "0"]
          - ["Effective LTV at Qualifying", "80.000%"]
          - ["PMI LTV Threshold", "80.000%"]
      - type: "kv"
        h: "Estimated PMI at Qualifying"
        desc: "Estimates the monthly PMI the borrower will need to pay if they buy at the top of their qualifying range."
        lines:
          - ["Estimated PMI at Qualifying", "$0.00"]
          - ["PMI Required at Qualifying", "0"]
          - ["Maximum Qualifying Loan Amount (Pass 1, No PMI)", "$573,165.63"]
          - ["Annual PMI Rate (Estimate)", "0.5500%"]
      - type: "kv"
        h: "Maximum Qualifying Loan Amount (PMI-Aware Final)"
        desc: "Calculates the borrower's maximum qualifying loan amount, with PMI folded in when it applies."
        lines:
          - ["Maximum Qualifying Loan Amount", "$573,165.63"]
          - ["Maximum Qualifying PI Payment", "$3,910.00"]
          - ["Estimated PMI at Qualifying", "$0.00"]
          - ["Note Rate", "7.250%"]
          - ["Loan Term (Months)", "360"]
      - type: "kv"
        h: "Maximum Qualifying Purchase Price (PMI-Aware Final, From Percent Down)"
        desc: "Calculates the PMI-aware final qualifying purchase price when the practitioner states down payment as a percent of price instead of a dollar amount. Algebraically derives the price directly from the qualifying loan amount and the down payment percent without requiring a dollar down payment input."
        lines:
          - ["Maximum Qualifying Purchase Price", "$716,457.04"]
          - ["Maximum Qualifying Loan Amount", "$573,165.63"]
          - ["Down Payment Percent", "20.000%"]
    final: "Requested result for <b>Maximum Qualifying Purchase Price</b> is <b>$716,457.04</b>."

  - id: "refi"
    label: "Refi savings curve, $400K, 7.5% → 6.25%"
    convo_title: "Mark Smith owes $400k at 7.5%, 28 years left. refinancing…"
    prompt: "Mark Smith owes $400k at 7.5%, 28 years left. refinancing into a new 30-year at 6.25%, $8k in closing costs. show me the cumulative savings over a 7-year hold."
    ts: "10:58 AM"
    parse:
      - ["current_loan_balance", "400000 USD"]
      - ["current_note_rate", "7.5%"]
      - ["current_remaining_term", "28 yr"]
      - ["loan_amount", "400000 USD"]
      - ["note_rate", "6.25%"]
      - ["loan_term", "30 yr"]
      - ["total_closing_costs", "8000 USD"]
      - ["refi_hold", "7 yr"]
      - ["calculate", "refi_savings_curve"]
    blocks:
      - type: "kv"
        h: "New Loan Payment"
        desc: "Monthly PI on the new 30-year at 6.250%."
        lines:
          - ["Monthly PI (new)", "$2,462.87"]
      - type: "kv"
        h: "Current Loan Payment (Pre-Refi)"
        desc: "Computed from the existing balance, rate, and remaining term."
        lines:
          - ["Monthly PI (current)", "$2,851.47"]
      - type: "kv"
        h: "Monthly Savings from Refinance"
        desc: "Current payment minus the new payment."
        lines:
          - ["Monthly savings", "$388.60"]
      - type: "chart"
        h: "Refi Cumulative Savings Curve"
        desc: "Cumulative net savings month by month: starts at negative closing costs, climbs as the monthly savings accrue."
        legend: "Cumulative Net Savings"
        axis_label: "Month"
      - type: "kv"
        h: ""
        desc: ""
        lines:
          - ["Hold period", "84 months"]
          - ["Monthly savings", "$388.60"]
          - ["Closing costs", "$8,000.00"]
    chart: [-7611.40, -7222.80, -6834.20, -6445.59, -6056.99, -5668.39, -5279.79, -4891.19, -4502.59, -4113.98, -3725.38, -3336.78, -2948.18, -2559.58, -2170.98, -1782.38, -1393.77, -1005.17, -616.57, -227.97, 160.63, 549.23, 937.84, 1326.44, 1715.04, 2103.64, 2492.24, 2880.84, 3269.44, 3658.05, 4046.65, 4435.25, 4823.85, 5212.45, 5601.05, 5989.66, 6378.26, 6766.86, 7155.46, 7544.06, 7932.66, 8321.26, 8709.87, 9098.47, 9487.07, 9875.67, 10264.27, 10652.87, 11041.48, 11430.08, 11818.68, 12207.28, 12595.88, 12984.48, 13373.08, 13761.69, 14150.29, 14538.89, 14927.49, 15316.09, 15704.69, 16093.30, 16481.90, 16870.50, 17259.10, 17647.70, 18036.30, 18424.90, 18813.51, 19202.11, 19590.71, 19979.31, 20367.91, 20756.51, 21145.12, 21533.72, 21922.32, 22310.92, 22699.52, 23088.12, 23476.72, 23865.33, 24253.93, 24642.53]
    final: "Requested result for <b>Refi Cumulative Net Savings</b> is <b>$24,643</b>."

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
  text: "Run your numbers in plain English, and stand behind every one, down to the last decimal."
  cta_label: "Start free"
---
