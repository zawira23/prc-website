# CLAUDE CODE PROMPT
# Tenant Screening Checklist & Scorecard — Ghana Edition
# PRC (Property and Rent Consult) Digital Product Bundle
# ─────────────────────────────────────────────────────────────────────────────

## CONTEXT & IDENTITY

You are building a commercial digital product bundle for **Property and Rent Consult (PRC)**, a
Ghana-based property advisory brand. The brand palette is:
  - Deep Brown  : #36221C
  - Steel Blue  : #516984
  - Warm Grey   : #63645A
  - Off-White   : #F5EDE8
  - Light Blue  : #E8EEF3
  - White       : #FFFFFF

All currency is **Ghana Cedis (GHS)**. All documents are governed by the **Rent Act, 1963 (Act 220)**
and **Rent Regulations, 1964 (L.I. 369)**.

---

## WHAT TO BUILD

Produce a **3-tier product bundle** called:

> **Tenant Screening Checklist & Scorecard — Ghana Edition**
> *By Property and Rent Consult*

### TIER STRUCTURE

| Tier     | Price   | Deliverables                                                  |
|----------|---------|---------------------------------------------------------------|
| Basic    | GHS 49  | Deliverable 1 + Deliverable 2                                 |
| Pro      | GHS 99  | Deliverable 1 + 2 + 3 + 4                                    |
| Agency   | GHS 199 | Deliverable 1 + 2 + 3 + 4 + 5 + 6                            |

---

## DELIVERABLES TO BUILD

### DELIVERABLE 1 — Printable A4 PDF (all tiers)

Build using **Python + reportlab** (or fpdf2 as fallback).

**Page 1 — Cover**
- PRC brand header bar (Deep Brown #36221C full-width)
- Title: "TENANT SCREENING CHECKLIST & SCORECARD"
- Subtitle: "Ghana Edition — For Landlords, Agents & Property Managers"
- Tag line: "Reduce tenancy risk with structured, evidence-based screening"
- Version: "2026 Edition | Property and Rent Consult"
- Footer: "For personal/internal business use only. Not for resale."

**Page 2 — Instructions & Documents Required**
Section heading: "HOW TO USE THIS SCORECARD"
Steps (numbered):
1. Collect all required documents from the applicant BEFORE scoring.
2. Complete Section 1 (Minimum Requirements). If ANY item fails → Reject immediately.
3. Complete the Scoring Table in Section 2. Total the score out of 25.
4. Match the score to the Risk Category in Section 3.
5. Complete the Verification Checklist in Section 4 — ALL items must be checked.
6. Record the final decision and sign Section 5.

Sub-section: "Documents to Collect from Applicant"
- Ghana Card or valid Passport (mandatory)
- Recent payslip or 3-month bank statement (self-employed: business registration + MoMo/bank record)
- Utility bill in applicant's name (ECG/NEDCO or Ghana Water Company, not older than 3 months)
- Guarantor's Ghana Card + proof of address + employment letter or business evidence
- Written consent for reference checks

**Page 3 — Section 1: Minimum Requirements**
Heading: "SECTION 1 — MINIMUM REQUIREMENTS (GATE CHECK)"
Sub-note: "If ANY item below is not met, STOP. Do not proceed to scoring. Issue a polite rejection."

Checkbox table (3 columns: Ref | Criterion | Pass / Fail):
  MR-01 | Valid Ghana Card or Passport presented and verified
  MR-02 | Applicant aged 21 years or above
  MR-03 | Monthly income verified at ≥ 3× the monthly rent
  MR-04 | No prior eviction record (self-declared and cross-checked with previous landlord)
  MR-05 | Employed (minimum 6 months continuous) OR verifiable business income

Footer of section: "If ALL five criteria are met → proceed to Section 2."

**Page 4 — Section 2: Scoring Table**
Heading: "SECTION 2 — SCORING CRITERIA (Maximum Score: 25)"

Full scoring table (7 columns: Criteria | 0 pts | 1–2 pts | 3–4 pts | 5 pts | Score | Notes):

Row 1 — Employment Status
  0: Unemployed
  1–2: Casual or part-time, less than 6 months in role
  3–4: Permanent position, 6–24 months in role
  5: Permanent position, over 2 years in role

Row 2 — Income-to-Rent Ratio (verified)
  0: Verified income less than 2× monthly rent
  1–2: Exactly 2× monthly rent
  3–4: Between 2× and 2.5× monthly rent
  5: Verified income 3× or above monthly rent

Row 3 — Previous Landlord Reference
  0: Reference declined, hostile, or eviction confirmed
  1–2: Mixed or neutral reference; no strong endorsement
  3–4: Good reference; tenancy ended due to relocation or property sale
  5: Excellent long-term reference; landlord would re-let immediately

Row 4 — Guarantor Quality
  0: No guarantor offered or required but not provided
  1–2: Guarantor unverified; income insufficient or unconfirmed
  3–4: Guarantor verified; stable employment; adequate income
  5: Guarantor is a professional, property owner, or senior public servant; fully verified

Row 5 — Utility Bill & Payment History
  0: Frequent disconnections or late payments confirmed
  1–2: Occasional late payments; no disconnection
  3–4: Mostly on time; minor irregularities only
  5: Consistent, on-time payments across full review period

Total score row: "TOTAL SCORE (add all five rows): ___ / 25"

**Page 5 — Section 3: Risk Categories & Section 4: Verification Checklist**

Section 3 heading: "SECTION 3 — RISK CATEGORY & RECOMMENDED ACTION"

Risk table (4 columns: Score Range | Risk Level | Recommended Action | Notes):
  20–25 | Low Risk     | Approve on standard terms                                      | Proceed with standard deposit
  15–19 | Medium Risk  | Approve with conditions                                        | Require larger deposit (2 months) or additional guarantor
  10–14 | High Risk    | Consider with significant conditions only                      | Require 6 months' rent paid in advance; guarantor mandatory
  Below 10 | Very High | Reject                                                         | Politely decline; do not negotiate exceptions

Section 4 heading: "SECTION 4 — VERIFICATION CHECKLIST (Must Complete All Before Final Decision)"

Verification items (checkbox + field for date/notes):
  VC-01 | Called applicant's employer and confirmed position, start date, and salary
  VC-02 | Spoke directly to previous landlord (not just by text/WhatsApp); no red flags identified
  VC-03 | Verified guarantor's Ghana Card, address, and income evidence in person or by video call
  VC-04 | Reviewed utility bills — confirmed name matches applicant, reviewed 3 months minimum
  VC-05 | Conducted court/eviction record check through Rent Control contacts or local network (if accessible)

**Page 6 — Section 5: Final Decision Page**

Heading: "SECTION 5 — FINAL DECISION RECORD"

Fields:
- Property Address: ___________________________________
- Unit/Apartment: ___________________________________
- Applicant Full Name: ___________________________________
- Ghana Card Number: ___________________________________
- Application Date: ___________________________________
- Total Score: ___ / 25
- Risk Category: ___________________________________
- Deposit Required: GHS ___________________________________
- Additional Conditions (if any): ___________________________________

Decision boxes (large, clearly printed):
  [ ] APPROVED — Standard terms apply
  [ ] CONDITIONALLY APPROVED — See conditions noted above
  [ ] REJECTED — Applicant does not meet required threshold

Signature block:
- Property Manager / Agent Name: ___________________________________
- Signature: ___________________________________
- Date: ___________________________________
- Stamp / Company: ___________________________________

**Page 7 — Bonus: Reference Call Script**

Heading: "BONUS — PREVIOUS LANDLORD REFERENCE CALL SCRIPT"
Sub-note: "Use this script when calling the previous landlord. Do not skip this call — WhatsApp messages alone are insufficient."

Script:
"Good [morning/afternoon], please may I speak with [Landlord Name]?

My name is [Your Name] and I am a property manager at [Company Name]. I am screening [Applicant Name] who has applied to rent one of my properties. They have listed you as a previous landlord.

I have just a few quick questions — it should take about two minutes.

1. Did [Applicant Name] occupy a property managed or owned by you? From when to when?
2. Did they pay rent on time, in full?
3. Were there any complaints from neighbours or other tenants?
4. Did they leave the property in good condition?
5. Would you rent to them again?
6. Is there anything else I should know before I make a decision?

Thank you very much. I appreciate your time."

Note: Record responses in the Notes field of VC-02 in Section 4.

**Page 8 — Bonus: Guarantor Declaration Template**

Heading: "BONUS — GUARANTOR DECLARATION"

I, [Full Name] __________________________________, holder of Ghana Card / Passport No. _____________,
residing at __________________________________, hereby declare that I am willing to act as guarantor
for [Applicant Name] __________________________________ in respect of the tenancy of the premises
at __________________________________.

I understand that as guarantor I am liable for:
- Any unpaid rent if the tenant defaults on payment.
- Any damage to the property beyond fair wear and tear.
- Any lawful costs incurred by the landlord as a result of the tenant's breach of the tenancy agreement.

Signed: ___________________________________
Date: ___________________________________
Witness Name: ___________________________________
Witness Signature: ___________________________________

**Last Page — Terms of Use**

Heading: "TERMS OF USE"
Text:
"© 2026 Property and Rent Consult. All rights reserved.

This template is licensed for personal and internal business use only. You may use it to screen
tenants for properties you own or manage. You may duplicate it as many times as required for
your internal business operations.

You may NOT:
- Resell, redistribute, or republish this template in any form.
- Claim authorship or ownership of this template.
- Modify and sell it as your own product.

Violation of these terms may constitute an infringement of Ghanaian copyright law.

For licensing enquiries, contact Property and Rent Consult."

---

### DELIVERABLE 2 — Fillable PDF (all tiers)

Take the Printable A4 PDF above and add fillable form fields using **PyMuPDF (fitz)** or **pdfrw + reportlab**.

Add these interactive field types:
- Text fields on all blank lines (name, date, score, address, etc.)
- Checkboxes on all checkbox positions
- Dropdown field for Risk Category (options: Low Risk, Medium Risk, High Risk, Very High Risk — Reject)
- Dropdown field for Final Decision (options: Approved, Conditionally Approved, Rejected)
- Signature field on the signature line in Section 5

Save as: "PRC-Tenant-Scorecard-Fillable.pdf"

---

### DELIVERABLE 3 — Excel Workbook (.xlsx) (Pro + Agency)

Build using **openpyxl**.

**Sheet 1 — "Scorecard"** (main scoring sheet)
Layout:
- Row 1: PRC brand header (merged cells, Deep Brown fill, white text)
- Row 2: "TENANT SCREENING CHECKLIST & SCORECARD — GHANA EDITION"
- Rows 4–8: Minimum Requirements (checkboxes via data validation: Pass / Fail dropdowns)
  - If any Fail is selected, display red warning: "STOP — DO NOT PROCEED TO SCORING"
- Rows 10–16: Scoring table with dropdown input per row (score 0–5 per criterion)
  - Use data validation for each score cell (integer 0–5 only)
  - Auto-sum total in a merged "Total Score" row
  - Conditional formatting: 0–9 = red, 10–14 = orange, 15–19 = yellow, 20–25 = green
- Row 18: Auto-calculated Risk Category (formula):
  =IF(TotalScore>=20,"LOW RISK — APPROVE",IF(TotalScore>=15,"MEDIUM RISK — LARGER DEPOSIT",IF(TotalScore>=10,"HIGH RISK — 6 MONTHS UPFRONT","VERY HIGH RISK — REJECT")))
- Rows 20–24: Verification Checklist (dropdowns: Done / Pending / N/A)
- Rows 26–32: Final Decision block (text fields, dropdown for decision)

**Sheet 2 — "Reference Log"**
Columns: Date Called | Landlord Name | Phone | Property Previously Rented | Rent Paid on Time (Y/N) | Damage (Y/N) | Re-let Again (Y/N) | Notes

**Sheet 3 — "Guarantor Record"**
Columns: Guarantor Name | Ghana Card No. | Address | Employer | Monthly Income | Verified By | Date Verified | Document Received (Y/N)

**Sheet 4 — "Applicant History"**
Columns: Application Date | Applicant Name | Property Applied For | Total Score | Risk Category | Decision | Deposit Collected | Notes

Apply PRC brand colours (Deep Brown headers, Steel Blue sub-headers, alternating Light Blue/White row fills).
Lock all formula cells. Protect sheets with password "PRC2026" but allow data entry in input cells only.

Save as: "PRC-Tenant-Scorecard-Excel.xlsx"

---

### DELIVERABLE 4 — Word Document (.docx) (Pro + Agency)

Build using **docx (npm package)**.

Produce the same content as the Printable PDF (all 8 pages / sections) but as a fully editable
Word document using the docx library. Apply these styles:

- Font: Calibri throughout
- Page size: A4 (11906 × 16838 DXA)
- Margins: 1080 DXA all sides
- Heading 1: Deep Brown #36221C, bold, 28pt
- Heading 2: Steel Blue #516984, bold, 22pt
- Body: #2D2D2D, 20pt
- Table header rows: Deep Brown fill, white text, bold
- Alternating table rows: Light Blue #E8EEF3 and White
- All tables use WidthType.DXA with explicit columnWidths (never PERCENTAGE)
- Use LevelFormat.BULLET for all bulleted lists — never unicode bullets
- Running header: "Property and Rent Consult | Tenant Screening Scorecard — Ghana Edition"
- Running footer: Left = "© 2026 Property and Rent Consult", Right = Page number

Include ALL sections from the Printable PDF spec above, including both bonus sections.

Save as: "PRC-Tenant-Scorecard-Editable.docx"

---

### DELIVERABLE 5 — WhatsApp Image Set / 5 PNG cards (Agency)

Build using **Pillow (PIL)** in Python.

Produce 5 image cards, each **1080 × 1350 pixels (portrait)**, 300 DPI.

**Card 1 — Cover Card**
- Deep Brown background (#36221C)
- PRC wordmark top-left (white text, bold)
- Title: "TENANT SCREENING CHECKLIST & SCORECARD"
- Subtitle: "Ghana Edition"
- Tagline: "Screen smarter. Rent safer."
- Bottom strip: Steel Blue, text = "Property and Rent Consult | propertyandrentconsult.com"

**Card 2 — Minimum Requirements**
- White background
- Deep Brown header bar: "BEFORE YOU SCORE — 5 GATE CHECKS"
- 5 bullet items (large, with checkbox icons in Steel Blue):
  ✓ Valid Ghana Card or Passport
  ✓ Age 21 or above
  ✓ Income ≥ 3× monthly rent
  ✓ No prior eviction record
  ✓ 6+ months of employment or business income
- Footer: "Fail any one → Reject. Do not proceed."

**Card 3 — Scoring Table Summary**
- Light blue background (#E8EEF3)
- Steel Blue header: "5 CRITERIA. 25 POINTS. ONE DECISION."
- List of 5 criteria with icon indicators:
  📋 Employment Status (0–5 pts)
  💰 Income-to-Rent Ratio (0–5 pts)
  🏠 Previous Landlord Reference (0–5 pts)
  🤝 Guarantor Quality (0–5 pts)
  💡 Utility Bill Payment History (0–5 pts)
- Footer row: "Maximum Score: 25"

**Card 4 — Risk Categories**
- Four colored bands stacked vertically:
  Green band: 20–25 pts → LOW RISK → APPROVE
  Yellow band: 15–19 pts → MEDIUM RISK → LARGER DEPOSIT
  Orange band: 10–14 pts → HIGH RISK → 6 MONTHS UPFRONT
  Red band: Below 10 pts → VERY HIGH → REJECT
- Header: "WHAT DOES THE SCORE MEAN?"

**Card 5 — CTA / Product Offer Card**
- Deep Brown background
- Title: "GET THE FULL TENANT SCREENING KIT"
- Three tier boxes:
  BASIC — GHS 49 (Fillable PDF + Printable A4)
  PRO — GHS 99 (+ Excel + Word)
  AGENCY — GHS 199 (+ WhatsApp Cards + Full Bundle)
- CTA: "Available on Selar | Search: PRC Screening Kit"
- Footer: "Property and Rent Consult"

Save as: "PRC-WhatsApp-Card-1.png" through "PRC-WhatsApp-Card-5.png"

---

### DELIVERABLE 6 — Product README / Delivery Note (.docx) (Agency)

A short Word document (1–2 pages) that is included in every tier as the "Welcome" file.

Content:
- Title: "Thank You for Your Purchase — What's Inside This Package"
- Brief paragraph: what PRC is, what this product is for
- Table listing what is included in their tier (Basic / Pro / Agency — tailor per tier)
- How to use each file (one line per file)
- Canva template note: "The Canva template link is provided as a separate text file named
  'Canva-Template-Link.txt' in this folder. Click the link, sign in to Canva (free), and
  select 'Use Template' to customise."
- Google Sheets note: "Open 'Google-Sheets-Link.txt', click the link, then go to
  File > Make a Copy to get your own editable version."
- Terms of use (single paragraph)
- Contact: "Questions? Contact Property and Rent Consult."

Apply PRC branding. Save as: "PRC-READ-ME-FIRST.docx"

---

## OUTPUT FOLDER STRUCTURE

Produce all files and place them in the output directory as follows:

```
/outputs/
├── Basic_Tier/
│   ├── PRC-READ-ME-FIRST.docx
│   ├── PRC-Tenant-Scorecard-Printable.pdf
│   └── PRC-Tenant-Scorecard-Fillable.pdf
│
├── Pro_Tier/
│   ├── PRC-READ-ME-FIRST.docx
│   ├── PRC-Tenant-Scorecard-Printable.pdf
│   ├── PRC-Tenant-Scorecard-Fillable.pdf
│   ├── PRC-Tenant-Scorecard-Excel.xlsx
│   └── PRC-Tenant-Scorecard-Editable.docx
│
└── Agency_Tier/
    ├── PRC-READ-ME-FIRST.docx
    ├── PRC-Tenant-Scorecard-Printable.pdf
    ├── PRC-Tenant-Scorecard-Fillable.pdf
    ├── PRC-Tenant-Scorecard-Excel.xlsx
    ├── PRC-Tenant-Scorecard-Editable.docx
    ├── PRC-WhatsApp-Card-1.png
    ├── PRC-WhatsApp-Card-2.png
    ├── PRC-WhatsApp-Card-3.png
    ├── PRC-WhatsApp-Card-4.png
    └── PRC-WhatsApp-Card-5.png
```

---

## TECHNICAL REQUIREMENTS

- Python 3.x for: reportlab / fpdf2 (PDF), openpyxl (Excel), Pillow (PNG images), PyMuPDF (fillable PDF)
- Node.js for: docx npm package (Word documents)
- All pip installs must use: `pip install <package> --break-system-packages`
- All files must be self-contained — no external font downloads at runtime
- Use only system-safe fonts: Helvetica / Arial (PDFs), Calibri (DOCX), DejaVu or Liberation (PNG)
- Validate every .docx with: `python scripts/office/validate.py <file>`
- Validate every .xlsx opens cleanly (openpyxl load_workbook check)
- All PDFs must be A4 (210mm × 297mm)
- All PNG cards must be exactly 1080 × 1350px

---

## EXECUTION ORDER

Build in this order (simplest → most dependent):
1. Printable A4 PDF (Deliverable 1) — master content source
2. Word DOCX (Deliverable 4) — same content, different format
3. Excel workbook (Deliverable 3) — structured data, formulas
4. Fillable PDF (Deliverable 2) — based on Printable PDF
5. WhatsApp PNG cards (Deliverable 5) — visual distillations
6. README DOCX (Deliverable 6) — packaging document

After building all files, assemble into the three output folders listed above.

---

## QUALITY CHECKS BEFORE FINISHING

- [ ] All 6 deliverables exist and are non-zero file size
- [ ] PDF opens correctly and all pages display without error
- [ ] Fillable PDF has working checkboxes and text fields
- [ ] Excel formulas calculate correctly (test with score=22 → should show "LOW RISK — APPROVE")
- [ ] Excel conditional formatting shows correct colour for each score range
- [ ] DOCX validates with no errors
- [ ] All 5 PNG cards are exactly 1080×1350px and visually readable
- [ ] Output folder structure matches the tree above exactly
- [ ] No file contains placeholder "[YOUR NAME]" text — use "Property and Rent Consult" throughout
- [ ] All copyright footers read "© 2026 Property and Rent Consult"

---

## SELAR PRODUCT LISTINGS — TITLES, DESCRIPTIONS & PRICES

After building the files, produce a plain text file named `Selar_Listing_Copy.txt` in the
root of the output folder. This file contains the exact copy to paste into Selar when
creating the three product listings. Content:

─────────────────────────────────────────────────────────────────────────────
LISTING 1 — BASIC TIER
─────────────────────────────────────────────────────────────────────────────

PRODUCT TITLE (paste into Selar "Product Name" field):
Tenant Screening Checklist & Scorecard — Ghana Edition (Basic)

PRICE (paste into Selar "Price" field):
GHS 49.00

SHORT DESCRIPTION (paste into Selar "Short Description" / tagline field —
this is the one-liner that appears in search results and product cards):
A structured, evidence-based tenant screening tool built for Ghana —
gate checks, a 25-point scorecard, risk categories, and a verification
checklist, all in one professionally designed, ready-to-use document.

FULL DESCRIPTION (paste into Selar "Product Description" field — supports
basic formatting; use line breaks as shown):

Are you a landlord or property manager in Ghana who has ever rented to the
wrong tenant? A bad tenancy costs far more than the rent you lose —
it costs time, legal fees, stress, and damage to your property.

The Tenant Screening Checklist & Scorecard (Ghana Edition) gives you a
structured, professional system for evaluating every rental applicant before
you sign an agreement. It replaces guesswork with a documented, defensible
process that you can use on every application, for every property.

WHAT IS INSIDE THE BASIC TIER:

✔ Printable A4 PDF — Clean, print-ready layout for physical tenant folders.
  Print one copy per applicant and file it with their documents.

✔ Fillable PDF — Type directly into the form on your phone, tablet, or
  computer. Save a digital copy for each applicant — no printing needed.

WHAT THE SCORECARD COVERS:

• 5 mandatory gate checks — fail any one and the applicant is rejected
  before scoring begins (income threshold, Ghana Card verification,
  employment status, eviction history, and age requirement)

• 5 scored criteria (0–5 points each, 25 points maximum):
  Employment status · Income-to-rent ratio · Previous landlord reference ·
  Guarantor quality · Utility bill payment history

• 4 risk categories with recommended actions:
  Low Risk (approve) · Medium Risk (larger deposit) ·
  High Risk (6 months upfront) · Very High Risk (reject)

• Verification checklist — confirms all reference calls and document checks
  were completed before the final decision was recorded

• Final decision page with signature block — creates a paper trail

• BONUS: Previous Landlord Reference Call Script — exact wording to use
  when calling a prior landlord by phone

• BONUS: Guarantor Declaration Template — a ready-to-sign guarantor
  commitment form

GROUNDED IN GHANAIAN LAW:
This tool is aligned with the Rent Act, 1963 (Act 220) and the Rent
Regulations, 1964 (L.I. 369). Document requirements, income thresholds,
and procedural steps reflect Ghanaian tenancy practice.

TERMS OF USE:
For personal and internal business use. You may use it for as many
applicants as you need. Redistribution or resale is not permitted.

Produced by Property and Rent Consult — Expert Guidance on Ghana Property,
Rent, and Tenancy Law.

─────────────────────────────────────────────────────────────────────────────
LISTING 2 — PRO TIER
─────────────────────────────────────────────────────────────────────────────

PRODUCT TITLE:
Tenant Screening Checklist & Scorecard — Ghana Edition (Pro)

PRICE:
GHS 99.00

SHORT DESCRIPTION:
The complete tenant screening system for agents and growing portfolios —
PDFs, auto-scoring Excel workbook, and an editable Word document, all
grounded in Ghana's Rent Act.

FULL DESCRIPTION:

Everything in the Basic tier, plus two powerful tools that make the
screening process faster, more consistent, and fully editable for your
business.

WHAT IS INSIDE THE PRO TIER:

✔ Printable A4 PDF — Print one per applicant for physical filing.

✔ Fillable PDF — Complete screenings digitally on any device.

✔ Auto-Scoring Excel Workbook (.xlsx) — The most powerful tool in the
  bundle. Features include:
  - Score dropdowns (0–5) for each criterion — no manual calculation
  - Total score auto-calculated with a formula
  - Risk category generated automatically from the total score
  - Conditional formatting: green (approve), yellow (medium risk),
    orange (high risk), red (reject) — the colour tells you the answer
  - Four sheets: Scorecard · Reference Log · Guarantor Record ·
    Applicant History register
  - Data validation prevents invalid entries
  - Password-protected formulas — input cells remain editable

✔ Editable Word Document (.docx) — The full scorecard in a Word file
  you can customise: add your company name and logo, adjust scoring
  weights, add property-specific questions, or print on your letterhead.

IDEAL FOR:
Letting agents, property managers handling multiple units, or any landlord
who wants a digital record of every screening decision in one workbook.

GROUNDED IN GHANAIAN LAW:
Aligned with the Rent Act, 1963 (Act 220) and Rent Regulations, 1964
(L.I. 369). All document requirements and procedural steps reflect
Ghanaian tenancy practice.

Produced by Property and Rent Consult.

─────────────────────────────────────────────────────────────────────────────
LISTING 3 — AGENCY TIER
─────────────────────────────────────────────────────────────────────────────

PRODUCT TITLE:
Tenant Screening Checklist & Scorecard — Ghana Edition (Agency)

PRICE:
GHS 199.00

SHORT DESCRIPTION:
The full professional screening kit for property management companies and
agencies — every format, including a branded WhatsApp image set for
team sharing and client-facing use.

FULL DESCRIPTION:

The Agency tier is the complete bundle — every format included, designed
for property management companies, real estate agencies, and teams who
screen tenants at volume and need tools they can share with colleagues,
send to clients, and use across the business.

WHAT IS INSIDE THE AGENCY TIER:

✔ Printable A4 PDF — For physical tenant folders.

✔ Fillable PDF — For digital, paperless screening on any device.

✔ Auto-Scoring Excel Workbook (.xlsx) — Four-sheet workbook with
  automatic score calculation, risk category formula, conditional
  colour formatting, and an Applicant History register for your full
  screening pipeline.

✔ Editable Word Document (.docx) — Fully customisable for your company
  branding and specific requirements.

✔ WhatsApp Image Set — 5 professionally designed image cards
  (1080 × 1350px) covering:
  Card 1: Product cover and brand identity
  Card 2: The 5 mandatory gate checks
  Card 3: The 5 scoring criteria explained
  Card 4: Risk category colour chart
  Card 5: Tier pricing and where to buy
  Share with your team on WhatsApp, post to Instagram Stories, or use
  in client onboarding materials. Ready to forward immediately.

✔ README Delivery Note — A clear welcome document listing what is
  included and how to use each file.

IDEAL FOR:
Property management companies, real estate agencies, letting firms,
housing developers, and any team screening more than 10 applicants
per month.

GROUNDED IN GHANAIAN LAW:
Aligned with the Rent Act, 1963 (Act 220) and Rent Regulations, 1964
(L.I. 369).

Produced by Property and Rent Consult — Expert Guidance on Ghana Property,
Rent, and Tenancy Law.

─────────────────────────────────────────────────────────────────────────────
WEBSITE BUTTON COPY (for PRC website "Buy" buttons linking to Selar)
─────────────────────────────────────────────────────────────────────────────

Basic Tier button text:   Get Basic — GHS 49
Pro Tier button text:     Get Pro — GHS 99
Agency Tier button text:  Get Agency — GHS 199

Trust line below buttons: Secure payment via Selar · Mobile Money & Card accepted
Delivery line:            Instant download after payment

─────────────────────────────────────────────────────────────────────────────
SELAR TAGS (add to each listing for discoverability)
─────────────────────────────────────────────────────────────────────────────

tenant screening, landlord tools, Ghana rental, property management Ghana,
rent Act 220, tenant scorecard, landlord checklist, property forms Ghana,
rental template, PRC, property and rent consult, Accra landlord,
tenant vetting, Ghana lease, screening checklist
