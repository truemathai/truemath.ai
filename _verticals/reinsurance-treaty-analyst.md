---
layout: vertical
title: "TrueMath for Reinsurance Treaty Analysts: Treaty Math from a Conversation"
description: "Price a treaty, model ceding commissions, and test loss scenarios in plain English — and get numbers that stand up to a broker, an actuary, or the underwriting committee. Deterministic, auditable reinsurance math."
body_class: page-vertical

# The domain library shown on the pill inside each demo frame.
name: "Reinsurance Treaty Analyst"

# Hero. `hero_line` is the vertical-specific noun; the rest is shared framing.
hero_line: "Treaty economics"
hero_rest: "at the speed of conversation."
hero_accent: "With receipts."
hero_sub: "Ask in plain English. Get a number that stands up to your broker, your actuary, and the underwriting committee."

# Where every call-to-action points.
cta_url: "https://app.truemath.ai/signup"

# ── The three demo prompts (real TrueMath output, replayed) ─────────────
demos:
  - id: "payback"
    label: "Payback period, $5M excess layer"
    convo_title: "We're quoting a $5M excess layer. The basic limits loss cost…"
    prompt: "We're quoting a $5M excess layer. The basic limits loss cost is $250,000, the ILF at the attachment is 1.85, and the ILF at the policy limit is 2.60. What's the payback period on this layer?"
    ts: "3:04 PM"
    parse:
      - ["xl_layer_limit", "5000000 USD"]
      - ["basic_limits_loss_cost", "250000 USD"]
      - ["ilf_at_retention", "1.85"]
      - ["ilf_at_policy_limit", "2.60"]
      - ["calculate", "xl_payback_period yr"]
    blocks:
      - type: "kv"
        h: "Layer ILF"
        desc: "Calculates the ILF for a specific XL layer as the difference in ILFs at the policy limit and retention, normalized to the basic limit ILF."
        lines:
          - ["ILF at Policy Limit", "2.6000"]
          - ["ILF at Retention", "1.8500"]
          - ["ILF at Basic Limit", "1.0000"]
          - ["Layer ILF", "0.7500"]
      - type: "kv"
        h: "Layer Loss Cost"
        desc: "Calculates the expected loss cost for an XL layer by applying the layer ILF to the basic limits loss cost."
        lines:
          - ["Basic Limits Loss Cost", "$250,000"]
          - ["Layer ILF", "0.7500"]
          - ["Layer Loss Cost", "$187,500"]
      - type: "kv"
        h: "Indicated Rate on Line"
        desc: "Calculates the indicated rate on line (ROL) for an XL layer: layer loss cost rate plus reinsurer expense ratio and profit load."
        lines:
          - ["Layer Loss Cost", "$187,500"]
          - ["XL Layer Limit", "$5,000,000"]
          - ["Reinsurer Expense Ratio", "12.000%"]
          - ["Reinsurer Profit Load", "5.000%"]
          - ["Indicated Rate on Line", "4.5181%"]
      - type: "kv"
        h: "XL Layer Premium"
        desc: "Calculates the reinsurance premium for an XL layer by applying the ROL to the layer limit."
        lines:
          - ["Indicated Rate on Line", "4.5181%"]
          - ["XL Layer Limit", "$5,000,000"]
          - ["XL Layer Premium", "$225,904"]
      - type: "kv"
        h: "XL Layer Payback Period"
        desc: "Calculates the number of loss-free years required to pay back a total loss in the XL layer."
        lines:
          - ["XL Layer Limit", "$5,000,000"]
          - ["XL Layer Premium", "$225,904"]
          - ["XL Layer Payback Period", "22.13 yr"]
    final: "Requested result for <b>XL Layer Payback Period</b> is <b>22.13 yr</b>."

  - id: "uw-profit"
    label: "UW profit, 30% quota share"
    convo_title: "On a 30% quota share, the cedent writes $40M subject premium…"
    prompt: "On a 30% quota share, the cedent writes $40M subject premium with $21M in losses and we're paying 30% ceding commission. What's our underwriting profit on the treaty?"
    ts: "3:05 PM"
    parse:
      - ["quota_share_cession", "30%"]
      - ["subject_premium", "40000000 USD"]
      - ["subject_losses", "21000000 USD"]
      - ["ceding_commission_rate", "30%"]
      - ["calculate", "treaty_underwriting_profit"]
    blocks:
      - type: "kv"
        h: "Ceded Premium (Quota Share)"
        desc: "Calculates the ceded premium under a quota share treaty."
        lines:
          - ["Subject Premium", "$40,000,000"]
          - ["Quota Share Cession", "30.000%"]
          - ["Ceded Premium", "$12,000,000"]
      - type: "kv"
        h: "Sliding-Scale Ceding Commission Amount"
        desc: "Calculates the dollar amount of sliding-scale ceding commission paid to the cedent."
        lines:
          - ["Ceding Commission Rate", "30.000%"]
          - ["Ceded Premium", "$12,000,000"]
          - ["Sliding-Scale Ceding Commission Amount", "$3,600,000"]
      - type: "kv"
        h: "Ceded Losses (Quota Share)"
        desc: "Calculates the ceded losses under a quota share treaty."
        lines:
          - ["Subject Losses", "$21,000,000"]
          - ["Quota Share Cession", "30.000%"]
          - ["Ceded Losses", "$6,300,000"]
      - type: "kv"
        h: "Treaty Underwriting Profit"
        desc: "Calculates the reinsurer's underwriting profit on the treaty."
        lines:
          - ["Ceded Premium", "$12,000,000"]
          - ["Ceded Losses", "$6,300,000"]
          - ["Sliding-Scale Ceding Commission Amount", "$3,600,000"]
          - ["Reinsurer Expense Ratio", "12.000%"]
          - ["Treaty Underwriting Profit", "$660,000"]
    final: "Requested result for <b>Treaty Underwriting Profit</b> is <b>$660,000</b>."

  - id: "combined-ratio"
    label: "Combined ratio breakdown, 30% QS"
    convo_title: "Show me the combined ratio breakdown on a 30% quota share where…"
    prompt: "Show me the combined ratio breakdown on a 30% quota share where the cedent writes $40M subject premium against $21M in losses, with a 30% ceding commission."
    ts: "4:06 PM"
    parse:
      - ["quota_share_cession", "30%"]
      - ["subject_premium", "40000000 USD"]
      - ["subject_losses", "21000000 USD"]
      - ["ceding_commission_rate", "30%"]
      - ["calculate", "combined_ratio_waterfall"]
    blocks:
      - type: "kv"
        h: "Ceded Premium (Quota Share)"
        desc: "Calculates the ceded premium under a quota share treaty."
        lines:
          - ["Subject Premium", "$40,000,000"]
          - ["Quota Share Cession", "30.000%"]
          - ["Ceded Premium", "$12,000,000"]
      - type: "kv"
        h: "Ceded Losses (Quota Share)"
        desc: "Calculates the ceded losses under a quota share treaty."
        lines:
          - ["Subject Losses", "$21,000,000"]
          - ["Quota Share Cession", "30.000%"]
          - ["Ceded Losses", "$6,300,000"]
      - type: "kv"
        h: "Reinsurer Loss Ratio"
        desc: "Calculates the reinsurer's loss ratio on the treaty: ceded losses divided by ceded premium."
        lines:
          - ["Ceded Losses", "$6,300,000"]
          - ["Ceded Premium", "$12,000,000"]
          - ["Reinsurer Loss Ratio", "52.500%"]
      - type: "chart"
        h: "Combined Ratio Waterfall Chart"
        desc: "Builds a stacked bar chart showing the reinsurer combined ratio components: loss ratio, ceding commission, and expense ratio."
        lines:
          - ["Reinsurer Loss Ratio", "52.500%"]
          - ["Ceding Commission Rate", "30.000%"]
          - ["Reinsurer Expense Ratio", "12.000%"]
        chart_label: "Combined Ratio Waterfall Chart"
        chart_type: "stacked-pct"
        legend: "Loss Ratio"
        legend2: "Ceding Commission"
        legend3: "Expense Ratio"
        axis_label: "Component"
    chart: [0.525, 0.3, 0.12]
    final: "Requested result for <b>Combined Ratio Waterfall Chart</b> included above."

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
  text: "Price and structure a treaty in plain English, and stand behind every number, down to the last decimal, in front of the underwriting committee."
  cta_label: "Start free"
---
