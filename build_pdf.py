from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

# Brand colours
DEEP_BROWN = colors.HexColor('#36221C')
STEEL_BLUE = colors.HexColor('#516984')
WARM_GREY  = colors.HexColor('#63645A')
OFF_WHITE  = colors.HexColor('#F5EDE8')
LIGHT_BLUE = colors.HexColor('#E8EEF3')
WHITE      = colors.white
BLACK      = colors.black
GREEN      = colors.HexColor('#2D7A3A')
YELLOW     = colors.HexColor('#C8A000')
ORANGE     = colors.HexColor('#C86400')
RED        = colors.HexColor('#C82020')

W, H = A4

def build_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm)

    styles = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    h1 = S('H1', fontName='Helvetica-Bold', fontSize=16, textColor=DEEP_BROWN,
            spaceAfter=6, spaceBefore=12)
    h2 = S('H2', fontName='Helvetica-Bold', fontSize=13, textColor=STEEL_BLUE,
            spaceAfter=4, spaceBefore=8)
    body = S('Body', fontName='Helvetica', fontSize=10, textColor=BLACK,
             spaceAfter=4, leading=14)
    small = S('Small', fontName='Helvetica', fontSize=8, textColor=WARM_GREY,
              spaceAfter=2, leading=11)
    center_bold = S('CB', fontName='Helvetica-Bold', fontSize=11,
                    alignment=TA_CENTER, textColor=WHITE)
    cover_title = S('CT', fontName='Helvetica-Bold', fontSize=20,
                    alignment=TA_CENTER, textColor=WHITE, spaceAfter=8)
    cover_sub = S('CS', fontName='Helvetica', fontSize=12,
                  alignment=TA_CENTER, textColor=DEEP_BROWN, spaceAfter=6)
    note = S('Note', fontName='Helvetica-Oblique', fontSize=9,
             textColor=WARM_GREY, spaceAfter=4)

    def page_break():
        from reportlab.platypus import PageBreak
        return PageBreak()

    def hr():
        return HRFlowable(width='100%', thickness=1, color=STEEL_BLUE, spaceAfter=6, spaceBefore=6)

    def header_table(text):
        t = Table([[Paragraph(text, center_bold)]], colWidths=[W - 30*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), DEEP_BROWN),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    def section_heading(text):
        t = Table([[Paragraph(text, S('SH', fontName='Helvetica-Bold', fontSize=11,
                                       textColor=WHITE))]], colWidths=[W - 30*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), STEEL_BLUE),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = []

    # ── PAGE 1: COVER ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 20*mm))
    story.append(header_table('TENANT SCREENING CHECKLIST & SCORECARD'))
    story.append(Spacer(1, 12*mm))
    story.append(Paragraph('Ghana Edition', S('GE', fontName='Helvetica-Bold', fontSize=18,
                                               alignment=TA_CENTER, textColor=DEEP_BROWN)))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('For Landlords, Agents &amp; Property Managers',
                            S('Sub', fontName='Helvetica', fontSize=13, alignment=TA_CENTER,
                              textColor=STEEL_BLUE)))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph('Reduce tenancy risk with structured, evidence-based screening',
                            S('Tag', fontName='Helvetica-Oblique', fontSize=11,
                              alignment=TA_CENTER, textColor=WARM_GREY)))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('2026 Edition | Property and Rent Consult',
                            S('Ver', fontName='Helvetica', fontSize=10, alignment=TA_CENTER,
                              textColor=WARM_GREY)))
    story.append(Spacer(1, 40*mm))

    footer_t = Table([[Paragraph('For personal/internal business use only. Not for resale.',
                                 S('Ft', fontName='Helvetica', fontSize=9, textColor=WHITE,
                                   alignment=TA_CENTER))]], colWidths=[W - 30*mm])
    footer_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), STEEL_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(footer_t)
    story.append(page_break())

    # ── PAGE 2: INSTRUCTIONS ───────────────────────────────────────────────────
    story.append(header_table('HOW TO USE THIS SCORECARD'))
    story.append(Spacer(1, 6*mm))
    steps = [
        'Collect all required documents from the applicant BEFORE scoring.',
        'Complete Section 1 (Minimum Requirements). If ANY item fails — Reject immediately.',
        'Complete the Scoring Table in Section 2. Total the score out of 25.',
        'Match the score to the Risk Category in Section 3.',
        'Complete the Verification Checklist in Section 4 — ALL items must be checked.',
        'Record the final decision and sign Section 5.',
    ]
    for i, s in enumerate(steps, 1):
        story.append(Paragraph(f'<b>{i}.</b> {s}', body))
    story.append(Spacer(1, 6*mm))
    story.append(section_heading('DOCUMENTS TO COLLECT FROM APPLICANT'))
    story.append(Spacer(1, 3*mm))
    docs = [
        'Ghana Card or valid Passport (mandatory)',
        'Recent payslip or 3-month bank statement (self-employed: business registration + MoMo/bank record)',
        'Utility bill in applicant\'s name (ECG/NEDCO or Ghana Water Company, not older than 3 months)',
        'Guarantor\'s Ghana Card + proof of address + employment letter or business evidence',
        'Written consent for reference checks',
    ]
    for d in docs:
        story.append(Paragraph(f'• {d}', body))
    story.append(page_break())

    # ── PAGE 3: SECTION 1 ──────────────────────────────────────────────────────
    story.append(header_table('SECTION 1 — MINIMUM REQUIREMENTS (GATE CHECK)'))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('<i>If ANY item below is not met, STOP. Do not proceed to scoring. Issue a polite rejection.</i>', note))
    story.append(Spacer(1, 4*mm))

    mr_data = [
        [Paragraph('<b>Ref</b>', body), Paragraph('<b>Criterion</b>', body), Paragraph('<b>Pass / Fail</b>', body)],
        ['MR-01', 'Valid Ghana Card or Passport presented and verified', '  Pass  /  Fail'],
        ['MR-02', 'Applicant aged 21 years or above', '  Pass  /  Fail'],
        ['MR-03', 'Monthly income verified at 3x the monthly rent', '  Pass  /  Fail'],
        ['MR-04', 'No prior eviction record (self-declared and cross-checked with previous landlord)', '  Pass  /  Fail'],
        ['MR-05', 'Employed (minimum 6 months continuous) OR verifiable business income', '  Pass  /  Fail'],
    ]
    mr_table = Table(mr_data, colWidths=[25*mm, 110*mm, 40*mm])
    mr_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DEEP_BROWN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [OFF_WHITE, WHITE]),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])
    mr_table.setStyle(mr_style)
    story.append(mr_table)
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph('<b>If ALL five criteria are met → proceed to Section 2.</b>', body))
    story.append(page_break())

    # ── PAGE 4: SECTION 2 ──────────────────────────────────────────────────────
    story.append(header_table('SECTION 2 — SCORING CRITERIA (Maximum Score: 25)'))
    story.append(Spacer(1, 4*mm))

    score_data = [
        [Paragraph('<b>Criteria</b>', body), Paragraph('<b>0 pts</b>', body),
         Paragraph('<b>1–2 pts</b>', body), Paragraph('<b>3–4 pts</b>', body),
         Paragraph('<b>5 pts</b>', body), Paragraph('<b>Score</b>', body), Paragraph('<b>Notes</b>', body)],
        ['Employment\nStatus', 'Unemployed', 'Casual/part-time,\n<6 months', 'Permanent,\n6–24 months', 'Permanent,\n>2 years', '___', ''],
        ['Income-to-Rent\nRatio', 'Income\n<2× rent', 'Exactly\n2× rent', 'Between\n2× and 2.5×', 'Income\n3× or above', '___', ''],
        ['Previous Landlord\nReference', 'Declined/hostile/\neviction confirmed', 'Mixed or\nneutral', 'Good; ended\nby relocation', 'Excellent\nlong-term', '___', ''],
        ['Guarantor\nQuality', 'None offered', 'Unverified/\ninsufficient', 'Verified stable\nemployment', 'Professional/\nproperty owner', '___', ''],
        ['Utility Bill\nPayment History', 'Frequent\ndisconnections', 'Occasional\nlate payments', 'Mostly\non time', 'Consistent\non-time', '___', ''],
        [Paragraph('<b>TOTAL SCORE</b>', body), '', '', '', '', Paragraph('<b>___ / 25</b>', body), ''],
    ]
    cw = [32*mm, 26*mm, 26*mm, 26*mm, 26*mm, 16*mm, 23*mm]
    score_table = Table(score_data, colWidths=cw, rowHeights=None)
    score_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DEEP_BROWN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [OFF_WHITE, WHITE, OFF_WHITE, WHITE, OFF_WHITE]),
        ('BACKGROUND', (0,-1), (-1,-1), LIGHT_BLUE),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('SPAN', (0,-1), (4,-1)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])
    score_table.setStyle(score_style)
    story.append(score_table)
    story.append(page_break())

    # ── PAGE 5: SECTION 3 + 4 ─────────────────────────────────────────────────
    story.append(header_table('SECTION 3 — RISK CATEGORY & RECOMMENDED ACTION'))
    story.append(Spacer(1, 4*mm))

    risk_data = [
        [Paragraph('<b>Score Range</b>', body), Paragraph('<b>Risk Level</b>', body),
         Paragraph('<b>Recommended Action</b>', body), Paragraph('<b>Notes</b>', body)],
        ['20 – 25', 'Low Risk', 'Approve on standard terms', 'Proceed with standard deposit'],
        ['15 – 19', 'Medium Risk', 'Approve with conditions', 'Require larger deposit (2 months) or additional guarantor'],
        ['10 – 14', 'High Risk', 'Consider with significant conditions only', 'Require 6 months rent paid in advance; guarantor mandatory'],
        ['Below 10', 'Very High Risk', 'Reject', 'Politely decline; do not negotiate exceptions'],
    ]
    risk_colours = [None, GREEN, YELLOW, ORANGE, RED]
    risk_table = Table(risk_data, colWidths=[22*mm, 28*mm, 60*mm, 65*mm])
    rs = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DEEP_BROWN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ])
    for i, c in enumerate(risk_colours[1:], 1):
        rs.add('BACKGROUND', (1,i), (1,i), c)
        rs.add('TEXTCOLOR', (1,i), (1,i), WHITE)
        rs.add('FONTNAME', (1,i), (1,i), 'Helvetica-Bold')
    risk_table.setStyle(rs)
    story.append(risk_table)
    story.append(Spacer(1, 6*mm))

    story.append(section_heading('SECTION 4 — VERIFICATION CHECKLIST (Must Complete All Before Final Decision)'))
    story.append(Spacer(1, 4*mm))

    vc_data = [
        [Paragraph('<b>Ref</b>', body), Paragraph('<b>Item</b>', body),
         Paragraph('<b>Done?</b>', body), Paragraph('<b>Date</b>', body), Paragraph('<b>Notes</b>', body)],
        ['VC-01', 'Called employer; confirmed position, start date, and salary', '___', '___', ''],
        ['VC-02', 'Spoke directly to previous landlord (not just WhatsApp); no red flags', '___', '___', ''],
        ['VC-03', 'Verified guarantor Ghana Card, address, and income in person or video call', '___', '___', ''],
        ['VC-04', 'Reviewed utility bills — name matches applicant; 3 months minimum reviewed', '___', '___', ''],
        ['VC-05', 'Conducted eviction/court record check via Rent Control contacts or network', '___', '___', ''],
    ]
    vc_table = Table(vc_data, colWidths=[15*mm, 75*mm, 18*mm, 20*mm, 47*mm])
    vc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DEEP_BROWN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [OFF_WHITE, WHITE]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(vc_table)
    story.append(page_break())

    # ── PAGE 6: SECTION 5 FINAL DECISION ──────────────────────────────────────
    story.append(header_table('SECTION 5 — FINAL DECISION RECORD'))
    story.append(Spacer(1, 5*mm))

    fields = [
        ('Property Address', '_' * 55),
        ('Unit / Apartment', '_' * 55),
        ('Applicant Full Name', '_' * 55),
        ('Ghana Card Number', '_' * 55),
        ('Application Date', '_' * 55),
        ('Total Score', '___ / 25'),
        ('Risk Category', '_' * 55),
        ('Deposit Required', 'GHS ' + '_' * 40),
        ('Additional Conditions', '_' * 55),
    ]
    for label, blank in fields:
        story.append(Paragraph(f'<b>{label}:</b>  {blank}', body))
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph('<b>DECISION (tick one):</b>', body))
    story.append(Spacer(1, 3*mm))

    decision_data = [
        [Paragraph('[ ]  APPROVED — Standard terms apply', S('D', fontName='Helvetica-Bold', fontSize=11, textColor=GREEN))],
        [Paragraph('[ ]  CONDITIONALLY APPROVED — See conditions noted above', S('D2', fontName='Helvetica-Bold', fontSize=11, textColor=ORANGE))],
        [Paragraph('[ ]  REJECTED — Applicant does not meet required threshold', S('D3', fontName='Helvetica-Bold', fontSize=11, textColor=RED))],
    ]
    dt = Table(decision_data, colWidths=[W - 30*mm])
    dt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(dt)
    story.append(Spacer(1, 6*mm))
    story.append(section_heading('SIGNATURE BLOCK'))
    story.append(Spacer(1, 3*mm))
    for lbl in ['Property Manager / Agent Name', 'Signature', 'Date', 'Stamp / Company']:
        story.append(Paragraph(f'<b>{lbl}:</b>  {"_" * 50}', body))
        story.append(Spacer(1, 3*mm))
    story.append(page_break())

    # ── PAGE 7: REFERENCE CALL SCRIPT ─────────────────────────────────────────
    story.append(header_table('BONUS — PREVIOUS LANDLORD REFERENCE CALL SCRIPT'))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('<i>Use this script when calling the previous landlord. Do not skip this call — WhatsApp messages alone are insufficient.</i>', note))
    story.append(Spacer(1, 4*mm))
    script = [
        '"Good [morning/afternoon], please may I speak with [Landlord Name]?',
        '',
        'My name is [Your Name] and I am a property manager at [Company Name]. I am screening [Applicant Name] who has applied to rent one of my properties. They have listed you as a previous landlord.',
        '',
        'I have just a few quick questions — it should take about two minutes.',
        '',
        '1. Did [Applicant Name] occupy a property managed or owned by you? From when to when?',
        '2. Did they pay rent on time, in full?',
        '3. Were there any complaints from neighbours or other tenants?',
        '4. Did they leave the property in good condition?',
        '5. Would you rent to them again?',
        '6. Is there anything else I should know before I make a decision?',
        '',
        'Thank you very much. I appreciate your time."',
    ]
    for line in script:
        story.append(Paragraph(line if line else '&nbsp;', body))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('<i>Note: Record responses in the Notes field of VC-02 in Section 4.</i>', note))
    story.append(page_break())

    # ── PAGE 8: GUARANTOR DECLARATION + TERMS ─────────────────────────────────
    story.append(header_table('BONUS — GUARANTOR DECLARATION'))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        'I, [Full Name] __________________________________, holder of Ghana Card / Passport No. _____________,<br/>'
        'residing at __________________________________, hereby declare that I am willing to act as guarantor<br/>'
        'for [Applicant Name] __________________________________ in respect of the tenancy of the premises<br/>'
        'at __________________________________.', body))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('<b>I understand that as guarantor I am liable for:</b>', body))
    for item in [
        'Any unpaid rent if the tenant defaults on payment.',
        'Any damage to the property beyond fair wear and tear.',
        'Any lawful costs incurred by the landlord as a result of the tenant\'s breach of the tenancy agreement.',
    ]:
        story.append(Paragraph(f'• {item}', body))
    story.append(Spacer(1, 5*mm))
    for lbl in ['Signed', 'Date', 'Witness Name', 'Witness Signature']:
        story.append(Paragraph(f'<b>{lbl}:</b>  {"_" * 50}', body))
        story.append(Spacer(1, 3*mm))
    story.append(Spacer(1, 8*mm))
    story.append(section_heading('TERMS OF USE'))
    story.append(Spacer(1, 4*mm))
    tos = (
        '<b>© 2026 Property and Rent Consult. All rights reserved.</b><br/><br/>'
        'This template is licensed for personal and internal business use only. You may use it to screen '
        'tenants for properties you own or manage. You may duplicate it as many times as required for '
        'your internal business operations.<br/><br/>'
        '<b>You may NOT:</b><br/>'
        '• Resell, redistribute, or republish this template in any form.<br/>'
        '• Claim authorship or ownership of this template.<br/>'
        '• Modify and sell it as your own product.<br/><br/>'
        'Violation of these terms may constitute an infringement of Ghanaian copyright law.<br/><br/>'
        'For licensing enquiries, contact Property and Rent Consult.'
    )
    story.append(Paragraph(tos, body))

    doc.build(story)
    print(f'PDF saved: {path}')

base = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs'
for tier in ['Basic_Tier', 'Pro_Tier', 'Agency_Tier']:
    build_pdf(os.path.join(base, tier, 'PRC-Tenant-Scorecard-Printable.pdf'))
print('All PDFs done.')
