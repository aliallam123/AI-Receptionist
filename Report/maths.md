# Business case maths (how each number was derived)

This note documents the arithmetic used in the Business Case section so the figures can be traced back to explicit assumptions.

## 1) Base assumptions used in the model

### Call volumes and missed calls
- Monthly inbound calls (example baseline): **100 calls/month**
- Missed-call baseline: **25%** (Paperclip cross-sector average, 2025)
- Target answer rate with AI: **95%** (so missed rate becomes 5%)
- Subscription price: **£99/month**

### Revenue model
- Expected value per inbound call (EV/call) is modelled as:

`EV_per_call = average_job_value * conversion_rate`

In the base case, EV/call is backed out from the leakage figure shown in the report (see next section).

---

## 2) Revenue leakage (how £562/month and £6,744/year were derived)

### Missed calls per month
`missed_calls = calls_per_month * missed_rate`

`missed_calls = 100 * 0.25 = 25 missed calls/month`

### Monthly leakage
The report states: **25 missed opportunities worth ~£562/month**.

This implies an expected value per missed call of:

`EV_per_call = leakage_per_month / missed_calls`

`EV_per_call = 562 / 25 = £22.48 per missed call (expected value)`

### Annual leakage
`annual_leakage = monthly_leakage * 12`

`annual_leakage = 562 * 12 = £6,744 per year`

---

## 3) Recovered revenue at 95% answer rate (how ~£5,400/year was derived)

### Missed calls after AI (5% missed)
`missed_calls_after = calls_per_month * 0.05`

`missed_calls_after = 100 * 0.05 = 5 missed calls/month`

### Calls recovered
`recovered_calls = missed_calls_before - missed_calls_after`

`recovered_calls = 25 - 5 = 20 calls/month recovered`

### Recovered value per month
`recovered_value_month = recovered_calls * EV_per_call`

`recovered_value_month = 20 * 22.48 = £449.60/month`

### Recovered value per year
`recovered_value_year = recovered_value_month * 12`

`recovered_value_year = 449.60 * 12 = £5,395.20/year ≈ £5,400/year`

---

## 4) Payback and ROI (how "within one month" and the ROI figure were derived)

### Annual subscription cost
`annual_cost = 99 * 12 = £1,188/year`

### Payback period (months)
`payback_months = monthly_fee / recovered_value_month`

`payback_months = 99 / 449.60 = 0.22 months`

0.22 months is about 6 to 7 days, so reporting "within one month" is conservative.

### ROI reporting (be explicit about definition)
There are two common ways to express ROI. Pick one and use it consistently.

1) **Benefit-to-cost ratio (multiple)**
`ROI_multiple = recovered_value_year / annual_cost`

`ROI_multiple = 5,395.20 / 1,188 = 4.54x`

This is often reported as "about 4.5x".

2) **Net ROI percent**
`net_ROI_percent = (recovered_value_year - annual_cost) / annual_cost`

`net_ROI_percent = (5,395.20 - 1,188) / 1,188 = 3.54 = 354%`

If you want a single clean line in the report, "about 4.5x" is usually the least ambiguous.

---

## 5) Unit economics (how £0.28 per answered call was derived)

### Assumptions
- Monthly calls: **150 calls/month**
- Average call length: **2 minutes**
- Percent handled autonomously: **70%**
- Monthly platform costs (as listed in the report example):
  - Telephony: **£2.55**
  - Transcription: **£4**
  - Text-to-speech: **£18**
  - Orchestration: **£4**
  - Storage: **£1** (upper bound for "under £1")

### Answered calls per month (autonomous)
`answered_calls = total_calls * autonomous_rate`

`answered_calls = 150 * 0.70 = 105 answered calls/month`

### Total monthly platform cost
`monthly_cost = 2.55 + 4 + 18 + 4 + 1 = £29.55/month`

### Cost per answered call
`cost_per_answered_call = monthly_cost / answered_calls`

`cost_per_answered_call = 29.55 / 105 = £0.2814 ≈ £0.28`

---

## 6) Higher volume cost per answered call (example showing how it can drop toward ~£0.19)

If you state a lower unit cost at scale (for example ~£0.19), you should tie it to a specific scale scenario.

Example scale scenario using the shared infrastructure figure from the report:
- Shared infrastructure cost across 10 clinics: **£420/month**
- Calls per clinic: **315/month**
- Autonomous rate: **70%**

Total calls across 10 clinics:
`total_calls = 10 * 315 = 3,150 calls/month`

Answered calls:
`answered_calls = 3,150 * 0.70 = 2,205 answered calls/month`

Cost per answered call:
`cost_per_answered_call = 420 / 2,205 = £0.1905 ≈ £0.19`

Note: this assumes the £420 shared cost holds at that utilisation. If costs scale linearly with usage, the unit cost will not fall as quickly.

---

## 7) Cost saving vs live answering (how "~75% saving" can be justified)

To compare fairly, convert the live answering price to the same basis (per call).

If live answering is priced **per minute** at £0.85 to £1.40 and calls average **2 minutes**:
- Cost per call range: `2 * £0.85 = £1.70` to `2 * £1.40 = £2.80`

Saving vs AI unit cost (base case £0.28):
- Saving vs £1.70: `1 - (0.28 / 1.70) = 83.5%`
- Saving vs £2.80: `1 - (0.28 / 2.80) = 90.0%`

If you want to report a conservative "about 75%", you can compare to a lower per-call benchmark such as £1.20:
- Saving vs £1.20: `1 - (0.28 / 1.20) = 76.7%` (rounds to ~75%)

---

## 8) Savings vs receptionist salary (how "over £20,000" is supported)

If a receptionist salary is £28,220/year (Indeed, London average) and the AI subscription is £1,188/year:
`saving = 28,220 - 1,188 = £27,032/year`

So "over £20,000" is conservative.

---

## 9) Pilot cost (3 months, 1 clinic) (how ~£335 was derived)

Monthly platform cost in pilot: **£45/month**
One-off setup: **£200**

Total 3-month cost:
`pilot_total = (45 * 3) + 200 = 135 + 200 = £335`

---

## 10) Scale phase (10 clinics) (how the monthly and per-clinic figures were derived)

Shared infrastructure cost stated: **~£420/month across 10 clinics**
Per-clinic monthly infra:
`per_clinic_month = 420 / 10 = £42/month`

Per-clinic annual infra:
`per_clinic_year = 42 * 12 = £504/year` (often rounded up to ~£550 to include misc overheads)

---

## 11) Sensitivity analysis (template)

General structure:

`annual_benefit = (calls_per_month * (missed_base - missed_target) * EV_per_call) * 12`

Where:
- `missed_base` is baseline missed-call rate (example 0.25)
- `missed_target` is post-AI missed-call rate (example 0.05)
- `EV_per_call` is expected value per inbound call (job value * conversion rate)

You can vary:
- job value
- conversion rate
- call volume
- baseline missed-call rate
- achieved answer rate
- subscription price

Then compute:
- `ROI_multiple = annual_benefit / annual_cost`
- `payback_months = monthly_fee / (annual_benefit / 12)`
