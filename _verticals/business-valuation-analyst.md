---
layout: vertical
title: "TrueMath for Business Valuation Analysts: Valuation Math from a Conversation"
description: "Run a DCF, apply market multiples, and bridge enterprise to equity value in plain English — and get numbers that stand up to an auditor, the IRS, or opposing counsel. Deterministic, auditable valuation math."
body_class: page-vertical

# The domain library shown on the pill inside each demo frame.
name: "Business Valuation Analyst"

# Hero. `hero_line` is the vertical-specific noun; the rest is shared framing.
hero_line: "Conclusion of value"
hero_rest: "at the speed of conversation."
hero_accent: "With receipts."
hero_sub: "Ask in plain English. Get a number that stands up to an auditor, the IRS, or opposing counsel."

# Where every call-to-action points.
cta_url: "https://app.truemath.ai/signup"

# ── The three demo prompts (real TrueMath output, replayed) ─────────────
demos:
  - id: "subject-interest"
    label: "15% interest, build-up + DLOC/DLOM"
    convo_title: "FY24 net income was 662,500 with interest of 30,000…"
    prompt: "FY24 net income was 662,500 with interest of 30,000, taxes of 220,000, and depreciation of 75,000. The owner takes 350,000 but a hired manager runs 200,000, rent to the family LLC is 180,000 against 120,000 market, and there's 40,000 of one-time legal fees to add back. Tax rate 25%. Build up the cost of equity from a 4.5% risk-free rate, 5.5% ERP, 5.8% size premium, 1.2% industry premium, and 3 points of company-specific risk, with 3% long-term growth. Apply a 10% DLOC and a 28% DLOM. What is the value of a 15% interest?"
    ts: "12:15 PM"
    parse:
      - ["reported_net_income", "662500 USD"]
      - ["reported_interest_expense", "30000 USD"]
      - ["reported_tax_expense", "220000 USD"]
      - ["reported_depreciation_amortization", "75000 USD"]
      - ["reported_owner_compensation", "350000 USD"]
      - ["market_owner_compensation", "200000 USD"]
      - ["reported_rent_expense", "180000 USD"]
      - ["market_rent", "120000 USD"]
      - ["other_normalization_adjustments", "40000 USD"]
      - ["bv_tax_rate", "25%"]
      - ["risk_free_rate", "4.5%"]
      - ["equity_risk_premium", "5.5%"]
      - ["size_premium", "5.8%"]
      - ["industry_risk_premium", "1.2%"]
      - ["specific_company_risk_premium", "3%"]
      - ["long_term_growth_rate", "3%"]
      - ["dloc", "10%"]
      - ["dlom", "28%"]
      - ["subject_interest_pct", "15%"]
      - ["calculate", "subject_interest_value"]
    blocks:
      - type: "kv"
        h: "Build-Up Method Cost of Equity"
        desc: "Calculates cost of equity via the build-up method: risk-free rate plus equity risk premium plus size premium plus industry risk premium plus specific company risk premium."
        lines:
          - ["Specific Company Risk Premium", "3.00%"]
          - ["Risk-Free Rate", "4.50%"]
          - ["Equity Risk Premium", "5.50%"]
          - ["Size Premium", "5.80%"]
          - ["Industry Risk Premium", "1.20%"]
          - ["Cost of Equity", "20.00%"]
      - type: "kv"
        h: "Capitalization Rate"
        desc: "Calculates capitalization rate as cost of equity (or WACC, depending on basis) minus long-term sustainable growth rate."
        lines:
          - ["Long-Term Sustainable Growth Rate", "3.00%"]
          - ["Cost of Equity", "20.00%"]
          - ["Capitalization Rate", "17.00%"]
      - type: "kv"
        h: "Related-Party Rent Normalization"
        desc: "Calculates the rent normalization adjustment as reported rent less market rent."
        lines:
          - ["Reported Rent Expense", "$180,000"]
          - ["Market Rent", "$120,000"]
          - ["Rent Normalization Adjustment", "$60,000"]
      - type: "kv"
        h: "Owner Compensation Normalization"
        desc: "Calculates the owner compensation normalization adjustment as reported owner compensation less market owner compensation."
        lines:
          - ["Reported Owner Compensation", "$350,000"]
          - ["Market Owner Compensation", "$200,000"]
          - ["Owner Compensation Normalization Adjustment", "$150,000"]
      - type: "kv"
        h: "Total Normalization Adjustments"
        desc: "Sums the owner compensation, related-party rent, and other normalization adjustments."
        lines:
          - ["Owner Compensation Normalization Adjustment", "$150,000"]
          - ["Rent Normalization Adjustment", "$60,000"]
          - ["Other Normalization Adjustments", "$40,000"]
          - ["Total Normalization Adjustments", "$250,000"]
      - type: "kv"
        h: "Normalized Earnings (After-Tax)"
        desc: "Calculates after-tax normalized earnings by adding the after-tax value of normalization adjustments to reported net income."
        lines:
          - ["Reported Net Income", "$662,500"]
          - ["Total Normalization Adjustments", "$250,000"]
          - ["Income Tax Rate", "25.0%"]
          - ["Normalized Earnings (After-Tax)", "$850,000"]
      - type: "kv"
        h: "Capitalization of Earnings"
        desc: "Calculates the income approach indication by dividing normalized earnings by the capitalization rate."
        lines:
          - ["Normalized Earnings (After-Tax)", "$850,000"]
          - ["Capitalization Rate", "17.00%"]
          - ["Income Approach Indication (Cap of Earnings)", "$5,000,000"]
      - type: "kv"
        h: "Controlling Marketable Value from Capitalization of Earnings"
        desc: "Assigns the capitalization of earnings indication directly to controlling marketable value when used as the sole valuation approach."
        lines:
          - ["Income Approach Indication (Cap of Earnings)", "$5,000,000"]
          - ["Controlling Marketable Value", "$5,000,000"]
      - type: "kv"
        h: "Minority Marketable Value"
        desc: "Calculates minority marketable value by applying DLOC to controlling marketable value."
        lines:
          - ["Discount for Lack of Control (DLOC)", "10.0%"]
          - ["Controlling Marketable Value", "$5,000,000"]
          - ["Minority Marketable Value", "$4,500,000"]
      - type: "kv"
        h: "Minority Non-Marketable Value"
        desc: "Calculates minority non-marketable value by applying DLOM to minority marketable value."
        lines:
          - ["Discount for Lack of Marketability (DLOM)", "28.0%"]
          - ["Minority Marketable Value", "$4,500,000"]
          - ["Minority Non-Marketable Value", "$3,240,000"]
      - type: "kv"
        h: "Subject Interest Value"
        desc: "Calculates the pro rata subject interest value as minority non-marketable value times subject interest percentage."
        lines:
          - ["Subject Interest Percentage", "15.00%"]
          - ["Minority Non-Marketable Value", "$3,240,000"]
          - ["Subject Interest Value", "$486,000"]
    final: "Requested result for <b>Subject Interest Value</b> is <b>$486,000</b>."

  - id: "level-of-value"
    label: "Weighted conclusion → LOV waterfall"
    convo_title: "Weight the income approach at 60% on a 5,000,000 indication…"
    prompt: "Weight the income approach at 60% on a 5,000,000 indication, market at 30% on 7,800,000, and asset at 10% on 2,800,000, then apply a 10% DLOC, a 28% DLOM, and a 15% subject interest. Show me the level of value waterfall."
    ts: "12:18 PM"
    parse:
      - ["selected_income_indication", "5000000 USD"]
      - ["income_weight", "60%"]
      - ["selected_market_indication", "7800000 USD"]
      - ["market_weight", "30%"]
      - ["asset_approach_indication", "2800000 USD"]
      - ["asset_weight", "10%"]
      - ["dloc", "10%"]
      - ["dlom", "28%"]
      - ["subject_interest_pct", "15%"]
      - ["calculate", "level_of_value_waterfall"]
    blocks:
      - type: "kv"
        h: "Weighted Value Conclusion"
        desc: "Reconciles the income, market, and asset approach indications into a single controlling marketable value using the appraiser's assigned weights, deducting net debt when the indications are on an invested-capital basis."
        lines:
          - ["Selected Income Approach Indication", "$5,000,000"]
          - ["Income Approach Weight", "60.0%"]
          - ["Selected Market Approach Indication", "$7,800,000"]
          - ["Market Approach Weight", "30.0%"]
          - ["Asset Approach Indication", "$2,800,000"]
          - ["Asset Approach Weight", "10.0%"]
          - ["Net Debt", "0"]
          - ["Controlling Marketable Value", "$5,620,000"]
      - type: "kv"
        h: "Minority Marketable Value"
        desc: "Calculates minority marketable value by applying DLOC to controlling marketable value."
        lines:
          - ["Discount for Lack of Control (DLOC)", "10.0%"]
          - ["Controlling Marketable Value", "$5,620,000"]
          - ["Minority Marketable Value", "$5,058,000"]
      - type: "kv"
        h: "Minority Non-Marketable Value"
        desc: "Calculates minority non-marketable value by applying DLOM to minority marketable value."
        lines:
          - ["Discount for Lack of Marketability (DLOM)", "28.0%"]
          - ["Minority Marketable Value", "$5,058,000"]
          - ["Minority Non-Marketable Value", "$3,641,760"]
      - type: "kv"
        h: "Subject Interest Value"
        desc: "Calculates the pro rata subject interest value as minority non-marketable value times subject interest percentage."
        lines:
          - ["Subject Interest Percentage", "15.00%"]
          - ["Minority Non-Marketable Value", "$3,641,760"]
          - ["Subject Interest Value", "$546,264"]
      - type: "table"
        h: "Level of Value Waterfall"
        desc: "Builds a four-row waterfall table showing controlling marketable, minority marketable, minority non-marketable, and subject interest values."
        lines:
          - ["Controlling Marketable Value", "$5,620,000"]
          - ["Minority Marketable Value", "$5,058,000"]
          - ["Minority Non-Marketable Value", "$3,641,760"]
          - ["Subject Interest Value", "$546,264"]
        table_label: "Level of Value Waterfall"
        table_col: "Value"
        table_row_names:
          - "Controlling Marketable Value"
          - "Minority Marketable Value (after DLOC)"
          - "Minority Non-Marketable Value (after DLOM)"
          - "Subject Interest Value (Pro Rata)"
        table_rows:
          - "$5,620,000"
          - "$5,058,000"
          - "$3,641,760"
          - "$546,264"
    final: "Requested result for <b>Level of Value Waterfall</b> included above."

  - id: "dcf"
    label: "DCF value, 5-yr FCF + Gordon terminal"
    convo_title: "Discount these free cash flows at 15% over a five-year forecast…"
    prompt: "Discount these free cash flows at 15% over a five-year forecast: 800,000, 880,000, 960,000, 1,050,000, and 1,140,000, with a terminal-year cash flow of 1,175,000 growing at 3% in perpetuity. What is the DCF indicated value?"
    ts: "12:21 PM"
    parse:
      - ["fcf_table", "[800000, 880000, 960000, 1050000, 1140000] USD"]
      - ["wacc", "15%"]
      - ["dcf_periods", "5 yr"]
      - ["fcf_terminal", "1175000 USD"]
      - ["terminal_growth_rate", "3%"]
      - ["calculate", "income_approach_indication_dcf USD"]
    blocks:
      - type: "kv"
        h: "Terminal Value (Gordon Growth)"
        desc: "Calculates terminal value using the Gordon Growth Model: terminal FCF divided by WACC less terminal growth rate."
        lines:
          - ["Terminal Year FCF", "$1,175,000"]
          - ["WACC", "15.00%"]
          - ["DCF Terminal Growth Rate", "3.00%"]
          - ["Terminal Value", "$9,791,667"]
      - type: "kv"
        h: "Normalize DCF Forecast Periods"
        desc: "Converts the forecast horizon to a plain number of years for terminal value discounting."
        lines:
          - ["DCF Forecast Periods", "5 yr"]
          - ["DCF Forecast Periods (Normalized)", "5"]
      - type: "table"
        h: "PV of Projected FCFs"
        desc: "Discounts each year of the user-supplied FCF projection table at WACC and sums the results."
        table_label: "Free Cash Flow Projection Table"
        table_col: "Free Cash Flow"
        table_start: 1
        table_rows:
          - "$800,000"
          - "$880,000"
          - "$960,000"
          - "$1,050,000"
          - "$1,140,000"
        lines_after:
          - ["WACC", "15.00%"]
          - ["PV of Projected FCFs", "$3,159,397"]
      - type: "kv"
        h: "DCF Enterprise Value"
        desc: "Calculates DCF indicated value as PV of projected FCFs plus the present value of terminal value."
        lines:
          - ["PV of Projected FCFs", "$3,159,397"]
          - ["Terminal Value", "$9,791,667"]
          - ["WACC", "15.00%"]
          - ["DCF Forecast Periods (Normalized)", "5"]
          - ["Income Approach Indication (DCF)", "$8,027,585"]
    final: "Requested result for <b>Income Approach Indication (DCF)</b> is <b>$8,027,585</b>."

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
  text: "Reach a conclusion of value in plain English, and stand behind every number, down to the last decimal, in front of an auditor, the IRS, or opposing counsel."
  cta_label: "Start free"
---
