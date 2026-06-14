from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os, shutil

DEEP_BROWN = colors.HexColor('#36221C')
STEEL_BLUE = colors.HexColor('#516984')
WARM_GREY  = colors.HexColor('#63645A')
LIGHT_BLUE = colors.HexColor('#E8EEF3')
OFF_WHITE  = colors.HexColor('#F5EDE8')
WHITE      = colors.white
W, H = A4

def S(name, **kw): return ParagraphStyle(name, **kw)

body_s  = S('body',  fontName='Helvetica', fontSize=9,  textColor=colors.HexColor('#2D2D2D'), spaceAfter=4, leading=13)
bold_s  = S('bold',  fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#2D2D2D'), spaceAfter=4, leading=13)
h1_s    = S('h1',    fontName='Helvetica-Bold', fontSize=11, textColor=DEEP_BROWN, spaceAfter=4, spaceBefore=10)
h2_s    = S('h2',    fontName='Helvetica-Bold', fontSize=10, textColor=STEEL_BLUE, spaceAfter=3, spaceBefore=8)
cw_s    = S('cw',    fontName='Helvetica-Bold', fontSize=13, textColor=WHITE, alignment=TA_CENTER)
sub_s   = S('sub',   fontName='Helvetica', fontSize=10, textColor=WHITE, alignment=TA_CENTER)
small_s = S('small', fontName='Helvetica', fontSize=7,  textColor=WARM_GREY, spaceAfter=2)
note_s  = S('note',  fontName='Helvetica-Oblique', fontSize=8, textColor=WARM_GREY, spaceAfter=3)

def cover(title, sub, legal):
    def on_page(canvas, doc):
        pass
    t = Table([[Paragraph(title, cw_s)], [Paragraph(sub, sub_s)], [Paragraph(legal, sub_s)]], colWidths=[W-30*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), DEEP_BROWN),
        ('BACKGROUND', (0,1), (0,2), STEEL_BLUE),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
    ]))
    return t

def sec_bar(text):
    t = Table([[Paragraph(text, S('sb', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE))]], colWidths=[W-30*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),STEEL_BLUE),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LEFTPADDING',(0,0),(-1,-1),8)]))
    return t

def field(label):
    return Paragraph(f'<b>{label}:</b> {"_"*55}', body_s)

def check(label):
    return Paragraph(f'[ ] {label}', body_s)

def p(text): return Paragraph(text, body_s)
def pb(text): return Paragraph(f'<b>{text}</b>', body_s)
def sp(): return Spacer(1, 4*mm)
def hr(): return HRFlowable(width='100%', thickness=0.5, color=STEEL_BLUE, spaceAfter=4, spaceBefore=4)

def footer_para():
    return Paragraph('© 2026 Property and Rent Consult — For personal/internal business use only. Not for resale.', small_s)

def exec_block():
    return [
        sec_bar('EXECUTION'),
        sp(),
        pb('SIGNED by the LANDLORD:'),
        field('Full Name'), field('Signature'), field('Date'),
        field('Witness Name'), field('Witness Signature'),
        sp(),
        pb('SIGNED by the TENANT:'),
        field('Full Name'), field('Signature'), field('Date'),
        field('Witness Name'), field('Witness Signature'),
    ]

def std_schedules(extras=[]):
    rows = [['Item','Condition at Commencement','Condition at Vacation','Notes']]
    for _ in range(5): rows.append(['','','',''])
    t = Table(rows, colWidths=[40*mm,45*mm,45*mm,45*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DEEP_BROWN),('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),
        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[OFF_WHITE,WHITE]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    return [
        sp(), sec_bar('SCHEDULE 1 — FIXTURES AND FITTINGS INVENTORY'),
        p('(Attach completed move-in inspection checklist)'), t,
        sp(), sec_bar('SCHEDULE 2 — SPECIAL CONDITIONS'),
        p('1. '+'_'*80), p('2. '+'_'*80), p('3. '+'_'*80),
    ] + extras

def res_parties():
    return [
        sec_bar('PARTIES'),
        p('TENANCY AGREEMENT made this ______ day of ________________, ________'),
        sp(), pb('LANDLORD'),
        field('Full Name'), field('Ghana Card / Passport No.'), field('Contact Address'), field('Phone'), field('Email'),
        p('(hereinafter referred to as "the Landlord")'),
        sp(), pb('TENANT'),
        field('Full Name'), field('Ghana Card / Passport No.'), field('Employer / Business'), field('Contact Address'), field('Phone'), field('Email'),
        p('(hereinafter referred to as "the Tenant")'),
        sp(), pb('PREMISES'),
        field('Property Address'), field('Unit / Apt No.'), field('Nearest Landmark'), field('Ghana Post GPS'),
        p('Property Type:'), check('Apartment'), check('House'), check('Flat'), check('Other: _______________'),
    ]

def recitals():
    return [
        sec_bar('RECITALS'),
        p('WHEREAS the Landlord is the owner or authorised agent of the Premises and is desirous of letting the same to the Tenant on the terms herein;'),
        p('AND WHEREAS the Tenant is desirous of taking the Premises on those terms;'),
        pb('NOW THEREFORE the parties agree as follows:'),
    ]

def std_clauses_4to11():
    return [
        Paragraph('<b>CLAUSE 4 — SECURITY DEPOSIT</b>', h1_s),
        p('4.1  The Tenant shall pay a security deposit of GHS _________________ on signing, held as security against: (a) unpaid rent; (b) damage beyond fair wear and tear; (c) any other breach.'),
        p('4.2  The deposit shall not be applied as rent.'),
        p('4.3  Within fourteen (14) days of vacation, the Landlord shall return the deposit or provide a written itemised statement of deductions and return the balance.'),
        p('4.4  Deposit disputes may be referred to the Rent Control Department.'),
        Paragraph('<b>CLAUSE 5 — UTILITIES AND SERVICE CHARGES</b>', h1_s),
        p("5.1  The following are the Tenant's direct responsibility:"), check('Electricity (ECG/NEDCo)'), check('Water'), check('Internet/Cable'), check('Refuse Collection'),
        p("5.2  The Landlord's inclusions: _______________________________________________"),
        p('5.3  Service charges: GHS _____________ per month for: _______________________________________________'),
        p('5.4  The Tenant shall not tamper with any utility meter or connection.'),
        Paragraph('<b>CLAUSE 6 — LANDLORD OBLIGATIONS</b>', h1_s),
        p('6.1  The Landlord shall: (a) keep the Premises in reasonable repair at commencement; (b) ensure structural soundness and fitness for habitation; (c) carry out structural repairs within reasonable time of written notification; (d) not interfere with the Tenant\'s quiet enjoyment; (e) give at least 24 hours\' written notice before entering except in emergency; (f) issue a written receipt for every payment.'),
        Paragraph('<b>CLAUSE 7 — TENANT OBLIGATIONS</b>', h1_s),
        p('7.1  The Tenant shall: (a) pay rent on time; (b) keep the Premises clean and in good condition; (c) not carry out structural alterations without prior written consent; (d) not sublet without prior written consent; (e) not use the Premises for unlawful purposes; (f) permit entry with 24 hours\' notice; (g) report defects promptly in writing; (h) not keep pets without consent; (i) comply with all applicable laws; (j) return all keys on vacation.'),
        Paragraph('<b>CLAUSE 8 — CONDITION ON VACATION</b>', h1_s),
        p('8.1  The Tenant shall return the Premises in the same condition as at commencement, subject to fair wear and tear.'),
        p('8.2  A joint inspection shall be conducted within 48 hours of vacation. Defects recorded in writing and signed by both parties.'),
        p('8.3  All keys, access cards, and remote controls shall be returned on the day of vacation.'),
        Paragraph('<b>CLAUSE 9 — TERMINATION AND NOTICES</b>', h1_s),
        p("9.1  Either party may terminate at the end of the fixed term by giving _______ [30/60] days' written notice."),
        p('9.2  The Landlord may terminate before term expiry on grounds permitted by Act 220, including: (a) non-payment of rent exceeding one month; (b) material breach unremedied after 14 days\' written notice; (c) illegal use; (d) serious damage.'),
        p('9.3  All notices shall be in writing and delivered personally, by registered post, or by email.'),
        p('9.4  The Tenant shall not be removed except by lawful order of a competent court or Rent Tribunal.'),
        Paragraph('<b>CLAUSE 10 — DISPUTE RESOLUTION</b>', h1_s),
        p('10.1 Disputes not resolved directly shall be referred first to the Rent Control Department of the relevant district.'),
        p('10.2 Unresolved matters may then be referred to the District Magistrate Court having jurisdiction.'),
        p('10.3 Nothing herein prevents either party seeking urgent injunctive relief from a court of competent jurisdiction.'),
        Paragraph('<b>CLAUSE 11 — GENERAL</b>', h1_s),
        p('11.1 This Agreement is the entire agreement between the parties and supersedes all prior negotiations.'),
        p('11.2 Any variation shall be in writing and signed by both parties.'),
        p('11.3 If any provision is unenforceable, the remaining provisions continue in full force.'),
        p('11.4 This Agreement is governed by the laws of the Republic of Ghana.'),
    ]

def build_pdf(path, title, sub, legal, content_fn):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
    story = [cover(title, sub, legal), sp()] + content_fn() + [sp(), footer_para()]
    doc.build(story)
    print(f'PDF: {path}')

# ── FIXED-TERM ───────────────────────────────────────────────────────────────
def ft_content():
    return [
        *res_parties(), *recitals(),
        Paragraph('<b>CLAUSE 1 — TERM</b>', h1_s),
        p('1.1  The Landlord lets and the Tenant takes the Premises for a fixed term of _______ [months/years] commencing on _______________ and ending on _______________, unless sooner determined.'),
        p('1.2  This Agreement shall not renew automatically on expiry. Renewal requires a fresh written agreement. Either party must give at least _______ [90] days\' written notice of intention to renew before the term expires.'),
        p('1.3  On expiry without renewal the Tenant shall immediately vacate and return possession of the Premises to the Landlord.'),
        Paragraph('<b>CLAUSE 2 — RENT</b>', h1_s),
        p('2.1  The Tenant shall pay rent at GHS _____________ per [month/year], payable in advance as set out in Clause 3.'),
        p('2.2  Rent shall be paid without deduction, set-off, or counterclaim except as permitted by Act 220.'),
        p("2.3  The rent shall not be increased during the fixed term without the mutual written consent of both parties, subject to Act 220 and L.I. 369."),
        p("2.4  Should a permitted increase arise after the fixed term, the Landlord shall give not less than three (3) months' written notice."),
        Paragraph('<b>CLAUSE 3 — ADVANCE PAYMENT</b>', h1_s),
        p('3.1  The Tenant shall pay _______ [months/years] rent in advance on signing this Agreement, totalling GHS _________________.'),
        p('3.2  The Landlord shall issue a written receipt upon receiving the advance, as required by section 25 of Act 220.'),
        p('3.3  The advance rent shall be applied against successive monthly rent obligations as they fall due.'),
        p('3.4  Where the advance period expires before the end of the fixed term, further advance rent is payable on written terms agreed between the parties.'),
        *std_clauses_4to11(), *exec_block(), *std_schedules(),
    ]

# ── MONTH-TO-MONTH ───────────────────────────────────────────────────────────
def m2m_content():
    return [
        *res_parties(), *recitals(),
        Paragraph('<b>CLAUSE 1 — TERM</b>', h1_s),
        p('1.1  The Landlord lets and the Tenant takes the Premises on a month-to-month basis commencing on _______________, continuing on a rolling monthly basis until terminated in accordance with this Agreement.'),
        p('1.2  There is no fixed end date. The tenancy continues each month until a valid written termination notice is served.'),
        p("1.3  Either party may terminate by giving not less than ONE (1) full calendar month's written notice, expiring at the end of a rental month."),
        p('1.4  The Landlord may terminate on the grounds set out in Clause 9.2 by giving the appropriate notice under Act 220.'),
        Paragraph('<b>CLAUSE 2 — RENT</b>', h1_s),
        p('2.1  The Tenant shall pay rent at GHS _____________ per month, payable in advance as set out in Clause 3.'),
        p('2.2  Rent shall be paid without deduction, set-off, or counterclaim except as permitted by Act 220.'),
        p('2.3  Rent may be reviewed by the Landlord on a [monthly/quarterly/annual] basis. Any proposed increase requires not less than three (3) months\' written notice, as required by L.I. 369.'),
        p("2.4  Should a permitted increase arise, the Landlord shall give not less than three (3) months' written notice before the increase takes effect."),
        p('2.5  In the event of a rent review, both parties may negotiate the revised amount. If agreement cannot be reached, either party may refer the matter to the Rent Control Department.'),
        Paragraph('<b>CLAUSE 3 — ADVANCE PAYMENT</b>', h1_s),
        p('3.1  The Tenant shall pay _______ [1/2/3] months\' rent in advance on signing, totalling GHS _________________. Advance periods exceeding three (3) months require express written agreement in this clause.'),
        p('3.2  The Landlord shall issue a written receipt upon receiving the advance, as required by section 25 of Act 220.'),
        p('3.3  The advance rent shall be applied against successive monthly rent obligations as they fall due.'),
        p('3.4  Where the advance period expires, further advance rent is payable on written terms agreed between the parties.'),
        *std_clauses_4to11(), *exec_block(), *std_schedules(),
    ]

# ── ROOM RENTAL ──────────────────────────────────────────────────────────────
def room_content():
    house_rules = [
        sp(), sec_bar('SCHEDULE 3 — HOUSE RULES'),
        p('1.  Quiet Hours: (____)PM to (____)AM daily'),
        p('2.  No cooking in the room unless a dedicated cooking space is provided'),
        p('3.  Visitors must leave the premises by 10:00 PM unless otherwise agreed in writing with the Landlord'),
        p('4.  All refuse must be deposited in designated bins only'),
        p('5.  No loud music or noise likely to disturb other occupants at any time'),
        p('6.  No modifications, nails, or fixtures to be attached to walls or fittings without consent'),
        p('7.  Shared bathrooms and kitchens must be cleaned after each use'),
        p('8.  Additional House Rules: _______________________________________________'),
    ]
    return [
        *res_parties(),
        sec_bar('ROOM DETAILS'),
        field('Room Description'), field('Floor / Location within Building'),
        pb('Shared Facilities:'), check('Kitchen'), check('Bathroom'), check('Toilet'), check('Compound/Yard'), check('Other'),
        field('Current Occupants in Building / Compound'),
        *recitals(),
        Paragraph('<b>CLAUSE 1 — TERM (Circle the applicable option)</b>', h1_s),
        pb('Option A — Fixed-Term:'), p('The Landlord lets and the Tenant takes the Room for a fixed term of _______ [months/years] commencing on _______________ and ending on _______________.'),
        pb('Option B — Month-to-Month:'), p("The Landlord lets and the Tenant takes the Room on a month-to-month basis commencing on _______________, terminable by one (1) month's written notice by either party expiring at the end of a rental month."),
        Paragraph('<b>CLAUSE 2 — RENT</b>', h1_s),
        p('2.1  The Tenant shall pay rent at GHS _____________ per [month/year], payable in advance. 2.2  Rent shall be paid without deduction except as permitted by Act 220. 2.3  The rent shall not be increased without mutual written consent, subject to Act 220 and L.I. 369. 2.4  Any permitted increase requires not less than three (3) months\' written notice.'),
        Paragraph('<b>CLAUSE 3 — ADVANCE PAYMENT</b>', h1_s),
        p('3.1  The Tenant shall pay _______ months\' rent in advance on signing, totalling GHS _________________. 3.2  The Landlord shall issue a written receipt as required by section 25 of Act 220. 3.3  The advance shall be applied against successive monthly obligations as they fall due. 3.4  Further advance is payable on written terms agreed between the parties when the advance period expires.'),
        Paragraph('<b>CLAUSE 4 — SECURITY DEPOSIT</b>', h1_s),
        p('4.1  The Tenant shall pay a security deposit of GHS _________________ on signing. 4.2  The deposit shall not be applied as rent. 4.3  Within 14 days of vacation, the Landlord shall return the deposit or provide itemised deductions. 4.4  Deposit disputes may be referred to the Rent Control Department.'),
        Paragraph('<b>CLAUSE 5 — UTILITIES</b>', h1_s),
        p('5.1  Electricity: Tenant pays directly / Included in rent / Shared cost'), p('     Water: Tenant pays directly / Included in rent / Shared cost'),
        p("5.2  Where shared, the Tenant's proportionate share is GHS _____________ per month, subject to revision if usage changes materially."),
        p('5.3  The Tenant shall not install any independent electrical connection or tap into any utility supply without prior written consent.'),
        Paragraph('<b>CLAUSE 6 — LANDLORD OBLIGATIONS</b>', h1_s),
        p("6.1  The Landlord shall: (a) keep the Room and shared areas in reasonable repair; (b) ensure the premises are fit for habitation; (c) carry out structural repairs within reasonable time of written notification; (d) not interfere with the Tenant's quiet enjoyment; (e) give at least 24 hours' written notice before entering; (f) issue a written receipt for every payment."),
        Paragraph('<b>CLAUSE 7 — TENANT OBLIGATIONS</b>', h1_s),
        p('7.1  The Tenant shall: (a) pay rent on time; (b) keep the Room clean and in good condition; (c) not carry out structural alterations without consent; (d) not sublet without consent; (e) not use the Room for unlawful purposes; (f) permit entry with 24 hours\' notice; (g) report defects promptly in writing; (h) not keep pets without consent; (i) comply with applicable laws; (j) return all keys on vacation; (k) not bring additional permanent occupants without consent; (l) comply with the House Rules in Schedule 3; (m) not store flammable, hazardous, or illegal materials.'),
        Paragraph('<b>CLAUSES 8–11 — VACATION, TERMINATION, DISPUTES, GENERAL</b>', h1_s),
        p('8.1–8.3: Return Room in same condition subject to fair wear and tear. Joint inspection within 48 hours. Return all keys on day of vacation.'),
        p('9.1–9.4: Terminate by applicable notice in Clause 1. Landlord may terminate early on grounds in Act 220. All notices in writing. Tenant removable only by lawful court order.'),
        p('10.1–10.3: Disputes referred first to Rent Control Department, then District Magistrate Court. Nothing prevents urgent injunctive relief.'),
        p('11.1–11.4: Entire agreement. Variations in writing. Severability. Governed by laws of Ghana.'),
        *exec_block(), *std_schedules(house_rules),
    ]

# ── COMMERCIAL ───────────────────────────────────────────────────────────────
def comm_content():
    return [
        sec_bar('PARTIES'),
        p('COMMERCIAL LEASE AGREEMENT made this ______ day of _______________, ________'),
        sp(), pb('LANDLORD / LESSOR'),
        field('Full Name / Company Name'), field('Ghana Card / RC Number'), field('Registered Address'), field('Phone'), field('Email'),
        p('(hereinafter referred to as "the Landlord")'),
        sp(), pb('TENANT / LESSEE'),
        field('Full Name / Company Name'), field('Ghana Card / RC Number / TIN'), field('Nature of Business'), field('Registered / Trading Address'), field('Phone'), field('Email'),
        p('(hereinafter referred to as "the Tenant")'),
        sp(), pb('PREMISES'),
        field('Property Address'), field('Total Floor Area (sqm)'), field('Floor / Level'), field('Ghana Post GPS'),
        p('Premises Type:'), check('Office'), check('Shop / Retail'), check('Warehouse'), check('Salon'), check('Clinic / Consulting Room'), check('Restaurant'), check('Other'),
        sec_bar('RECITALS'),
        p('WHEREAS the Landlord is the owner or authorised agent of the Premises and is willing to let the same for commercial use on the terms herein; AND WHEREAS the Tenant wishes to take the Premises for the purpose of conducting lawful commercial operations; NOW THEREFORE the parties agree as follows:'),
        Paragraph('<b>CLAUSE 1 — TERM</b>', h1_s),
        p('1.1  The Landlord lets and the Tenant takes the Premises for a fixed term of _______ years commencing on _______________ and ending on _______________.'),
        p("1.2  The Tenant shall notify the Landlord in writing not less than _______ [60/90] days before expiry if they wish to renew. Renewal is not automatic and requires a fresh written agreement."),
        p('1.3  On expiry without renewal, the Tenant shall immediately vacate and deliver up vacant possession of the Premises.'),
        Paragraph('<b>CLAUSE 2 — PERMITTED USE</b>', h1_s),
        p('2.1–2.4: Use solely for: _______________________________________________. Comply with all applicable laws. No residential use. Obtain and maintain all licences and permits required.'),
        Paragraph('<b>CLAUSE 3 — RENT</b>', h1_s),
        p("3.1  The Tenant shall pay rent at GHS _____________ per [month/year/quarter], payable in advance as set out in Clause 4. 3.2  Rent shall be paid without deduction. 3.3  Any rent review shall be subject to _______ [90/180] days' prior written notice. 3.4  Disputes over a proposed rent increase may be referred to arbitration or the Rent Control Department."),
        Paragraph('<b>CLAUSE 4 — ADVANCE PAYMENT AND DEPOSIT</b>', h1_s),
        p('4.1  Advance rent: _______ [months/years] totalling GHS _________________ at signing. 4.2  Security deposit: GHS _________________ at signing, held against unpaid rent, damage, and breach. 4.3  Landlord shall issue written receipts for all payments. 4.4  Deposit returned within 21 days of vacation, subject to verified deductions.'),
        Paragraph('<b>CLAUSES 5–14 — UTILITIES, OBLIGATIONS, ALTERATIONS, SIGNAGE, INSURANCE, VACATION, TERMINATION, DISPUTES, GENERAL</b>', h1_s),
        p("5: Tenant's direct responsibility: Electricity / Water / Internet / Security / Refuse / Air Con maintenance. Service charges: GHS _____________ per month. No additional fittings without consent."),
        p('6: Landlord shall deliver premises fit for permitted use, maintain structural fabric, maintain shared areas, not interfere with quiet enjoyment, give 48 hours\' entry notice.'),
        p('7: Tenant shall pay on time; keep interior clean; not alter, sublet, or assign without consent; not store hazardous goods; comply with all laws; permit entry with 48 hours\' notice; remove all equipment on termination.'),
        p('8: Alterations with prior written consent only. Carried out by qualified contractors at Tenant\'s expense. On termination, remove or leave in place as agreed in writing.'),
        p('9: Signage with prior written consent. Comply with Municipal Assembly by-laws. Remove on termination and make good.'),
        p("10: Landlord insures structural fabric. Tenant insures business contents, stock, equipment, and public liability (minimum GHS _________________ per occurrence). Evidence of insurance provided on request."),
        p("11: On vacation: vacate by vacation date, return clean, return all keys, make good damage beyond fair wear and tear. Joint exit inspection within 48 hours."),
        p("12: Terminate at end of term by _______ [6] months' written notice. Landlord may terminate early for: non-payment, material breach (21 days' notice to remedy), insolvency, illegal use. Tenant may terminate early only with Landlord's written agreement."),
        p('13: Disputes — direct negotiation first. If unresolved within 21 days, refer to arbitration under Act 798 or court of competent jurisdiction. Rent Control Department for matters within its jurisdiction.'),
        p('14: Entire agreement. Variations in writing. Governed by laws of Ghana. Severability.'),
        *exec_block(),
        sp(), sec_bar('SCHEDULE 1 — DESCRIPTION AND CONDITION OF PREMISES AT COMMENCEMENT'),
        p('(Record condition of floors, walls, ceilings, fittings, electrical points, plumbing, and any landlord-installed equipment)'),
        sp(), sec_bar('SCHEDULE 2 — APPROVED FIT-OUT WORKS (IF ANY)'),
        p('(Description of any works pre-approved at the time of signing)'),
        sp(), sec_bar('SCHEDULE 3 — SPECIAL CONDITIONS'),
        p('1. '+'_'*80), p('2. '+'_'*80), p('3. '+'_'*80),
    ]

# ── KIOSK ────────────────────────────────────────────────────────────────────
def kiosk_content():
    return [
        sec_bar('IMPORTANT NOTE TO BUYER'),
        p('This Agreement covers the rental of a space or plot of land for the placement of a kiosk, shipping container, wooden booth, or similar temporary structure for commercial purposes. It is used extensively for micro-businesses in Ghana including provision sellers, mobile money agents, phone charging stations, food vendors, phone accessories sellers, and similar traders.'),
        sec_bar('PARTIES'),
        p('TEMPORARY STRUCTURE RENT AGREEMENT made this ______ day of _______________, ________'),
        sp(), pb('SPACE OWNER / LANDLORD'),
        field('Full Name'), field('Ghana Card / Passport No.'), field('Address'), field('Phone'), field('Email'),
        p('(hereinafter referred to as "the Space Owner")'),
        sp(), pb('OCCUPANT / TRADER'),
        field('Full Name'), field('Ghana Card / Passport No.'), field('Nature of Business'), field('Phone'), field('Email'),
        p('(hereinafter referred to as "the Occupant")'),
        sp(), pb('SPACE AND STRUCTURE DETAILS'),
        field('Location of Space'), field('Ghana Post GPS'), field('Space Dimensions (metres x metres)'),
        p('Structure Type:'), check('Metal Kiosk'), check('Wooden Booth'), check('Shipping Container'), check('Converted Container'), check('Canvas/Semi-Permanent'), check('Other'),
        p('Structure Ownership:'), check('Structure belongs to the Space Owner'), check('Structure belongs to the Occupant'), check('Structure to be provided by: _______________'),
        sec_bar('RECITALS'),
        p('WHEREAS the Space Owner holds the right to let or licence the above-described space for commercial use and is willing to permit the Occupant to use it on the terms herein; AND WHEREAS the Occupant wishes to use the space for the conduct of lawful commercial activities; NOW THEREFORE the parties agree as follows:'),
        Paragraph('<b>CLAUSE 1 — TERM</b>', h1_s),
        p('1.1  The Space Owner permits and the Occupant takes occupation of the Space for a period of _______________ commencing on _______________ [and ending on _______________ / on a month-to-month basis until terminated].'),
        p('1.2  Either party may terminate this Agreement by giving _______ [7/14/30] days\' written notice to the other party.'),
        p('1.3  The Space Owner may terminate immediately, without notice, only where: (a) the Occupant conducts an illegal activity; (b) the Occupant causes serious damage.'),
        Paragraph('<b>CLAUSE 2 — RENT</b>', h1_s),
        p('2.1  Rent: GHS _____________ per [week/month], payable [in advance / on the _____ day of each period].'),
        p('2.2  Paid by: [cash / mobile money / bank transfer] to: ___________________________'),
        p('2.3  Space Owner shall issue a written receipt for every payment. 2.4  Rent shall not be increased without at least _______ [30/60] days\' written notice.'),
        Paragraph('<b>CLAUSES 3–12 — STRUCTURE OWNERSHIP, PERMITTED USE, UTILITIES, MAINTENANCE, PERMITS, OBLIGATIONS, DAMAGE, TERMINATION, DISPUTES, GENERAL</b>', h1_s),
        p('3: Where structure belongs to Space Owner: let in current condition; Occupant keeps clean; Occupant reports defects; Space Owner repairs within reasonable time. Where structure belongs to Occupant: Occupant places and maintains at own cost; removes within _______ days on termination; failure to remove entitles Space Owner to arrange removal at Occupant\'s cost. Neither party shall use structure as residential dwelling.'),
        p('4: Use solely for: _______________________________________________. No expansion without consent. Comply with all applicable laws including Municipal Assembly requirements. Obtain all necessary permits.'),
        p('5: Utility arrangements: No utility connection available / Connect to Space Owner\'s supply (GHS _____________ per month) / Arrange own independent supply. No tapping into utility supply without consent. All costs of independent supply borne solely by Occupant.'),
        p('6: Occupant shall: keep Space and structure clean; not deposit waste creating a nuisance; not block pedestrian access; carry out minor maintenance; maintain surrounding area in clean condition.'),
        p('7: Occupant solely responsible for obtaining and renewing Municipal Assembly permits. Space Owner makes no representation that Space is permitted for commercial use. Occupant shall comply with any Municipal Assembly enforcement action immediately and at own cost. This Agreement terminates automatically upon such enforcement action.'),
        p('8: Space Owner shall: permit quiet use of Space; not interfere with business operations without cause; give _______ [7/14] days\' notice before requiring temporary vacation.'),
        p('9: Occupant responsible for damage caused by their activities, employees, agents, or customers. Space Owner not liable for loss of goods, stock, or business income from any cause. Occupant shall not hold Space Owner liable for any business losses.'),
        p('10: On termination: immediately cease operations; remove structure (if Occupant-owned) within stated period; leave Space clean and in original condition. Space Owner may recover Space through self-help where Occupant has clearly abandoned, provided no force used against any person. Contested evictions follow Act 220 procedure or court relief.'),
        p('11: Disputes resolved by direct discussion first. Unresolved disputes: Rent Control Department (where Act 220 applies) or District Magistrate Court.'),
        p('12: Entire agreement. Variations in writing. Governed by laws of Ghana. Severability.'),
        *exec_block(),
        sp(), sec_bar('SCHEDULE 1 — DESCRIPTION OF SPACE AND STRUCTURE AT COMMENCEMENT'),
        p('(Record current condition, approximate dimensions, utility connections, any existing damage or defects)'),
        sp(), sec_bar('SCHEDULE 2 — PERMIT / APPROVAL DETAILS'),
        field('Municipal Assembly'), field('Permit Number (if any)'), field('Permit Expiry Date'), field('Conditions attached to permit'),
        sp(), sec_bar('SCHEDULE 3 — SPECIAL CONDITIONS'),
        p('1. '+'_'*80), p('2. '+'_'*80), p('3. '+'_'*80),
    ]

# ── SCRIPTS PDF ──────────────────────────────────────────────────────────────
def script_pdf_content(include_34=True):
    def sbar(text): return Table([[Paragraph(text, S('sb', fontName='Helvetica-Bold', fontSize=11, textColor=WHITE))]], colWidths=[W-30*mm], style=TableStyle([('BACKGROUND',(0,0),(-1,-1),DEEP_BROWN),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),8)]))
    def lbl(text): return Table([[Paragraph(text, S('lb', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE))]], colWidths=[W-30*mm], style=TableStyle([('BACKGROUND',(0,0),(-1,-1),STEEL_BLUE),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8)]))

    items = [
        sbar('SCRIPT 1 — RENT REMINDER NOTICE'), sp(),
        lbl('USAGE NOTES'),
        p('Send when rent is 1–7 days overdue. Use the Formal Version for written or postal delivery. Use the Short Version for WhatsApp or SMS. This is a reminder, not a legal notice — tone must remain polite. If rent remains unpaid after 14 days, escalate to Script 3. Reference: Rent Act, 1963 (Act 220).'),
        sp(), lbl('FORMAL VERSION'), sp(),
        p('[DATE]'), sp(), p('Dear [TENANT NAME],'), sp(),
        pb('RE: REMINDER — RENT PAYMENT DUE'),
        p('We write to draw your attention to the fact that your rent for the period [PERIOD] in the amount of GHS [AMOUNT] was due on [DUE DATE] and remains outstanding as at the date of this notice.'),
        p('We kindly request that you arrange payment of the outstanding amount within SEVEN (7) days of the date of this notice.'),
        p('If you have already made payment, please disregard this notice and forward proof of payment to us at your earliest convenience.'),
        p('Should you experience any difficulty in meeting this payment, we encourage you to contact us promptly so that we may discuss the matter. Please be aware that continued non-payment may result in further action in accordance with the Rent Act, 1963 (Act 220).'),
        sp(), p('Yours sincerely,'), sp(), p('_______________________________'), p('[LANDLORD / AGENT NAME]'), p('[PROPERTY ADDRESS]'), p('[PHONE] | [EMAIL]'), p('Date: _______________'),
        sp(), lbl('SHORT VERSION (WhatsApp / SMS)'),
        p('"Dear [Name], this is a friendly reminder that your rent of GHS [Amount] for [Period] was due on [Date]. Kindly make payment within 7 days or contact us if you need to discuss. Thank you — [Landlord/Agent Name]."'),
        hr(), sp(),

        sbar('SCRIPT 2 — ROUTINE INSPECTION NOTICE'), sp(),
        lbl('USAGE NOTES'),
        p("Send at least 24–48 hours before any inspection. Under Act 220, a landlord may not enter the premises without reasonable notice except in an emergency. This notice satisfies that legal requirement. Tone must be professional and non-threatening — inspections are routine, not punitive."),
        sp(), lbl('FORMAL VERSION'), sp(),
        p('[DATE]'), sp(), p('Dear [TENANT NAME],'), sp(),
        pb('RE: NOTICE OF ROUTINE PROPERTY INSPECTION — [PROPERTY ADDRESS]'),
        p('We write to inform you that a routine inspection of the above-referenced premises will be conducted on [DATE] at [TIME].'),
        p('The purpose of this inspection is to assess the general condition of the property, identify any maintenance requirements, and ensure that all fixtures and fittings remain in good order. This is a scheduled routine inspection and does not imply any concern regarding your tenancy.'),
        p('We kindly request that you or a responsible adult be present during the inspection. If this date and time are not convenient, please contact us within 48 hours of this notice so that we may arrange an alternative time. The inspection is expected to take approximately [30–60] minutes.'),
        sp(), p('Yours sincerely,'), sp(), p('_______________________________'), p('[LANDLORD / AGENT NAME]'), p('[PROPERTY ADDRESS]'), p('[PHONE] | [EMAIL]'), p('Date: _______________'),
        sp(), lbl('SHORT VERSION (WhatsApp / SMS)'),
        p('"Dear [Name], please be informed that a routine inspection of your premises at [Address] is scheduled for [Date] at [Time]. Kindly ensure access is available. Contact us within 48 hours if this is not convenient. — [Landlord/Agent Name]."'),
    ]

    if include_34:
        items += [
            hr(), sp(),
            sbar('SCRIPT 3 — EVICTION WARNING NOTICE (FIRST FORMAL WARNING)'), sp(),
            lbl('USAGE NOTES'),
            p('This is a FIRST FORMAL WARNING — not a Quit Notice and not a court action. Use when rent is 14 or more days overdue OR when a breach of the tenancy agreement has been identified. This notice triggers a 14-day remedy period. It must be delivered in writing. DO NOT use this as a substitute for a formal Quit Notice — that is a separate document under Act 220. This script creates the paper trail required before a Quit Notice can be issued.'),
            sp(), lbl('FORMAL VERSION'), sp(),
            p('[DATE]'), sp(), p('Dear [TENANT NAME],'), sp(),
            pb('RE: FORMAL WARNING — [NON-PAYMENT OF RENT / BREACH OF TENANCY AGREEMENT]'),
            p('We write to you in connection with the tenancy of the premises at [PROPERTY ADDRESS], held by you under the Tenancy Agreement dated [DATE OF AGREEMENT].'),
            Paragraph('<b>[SELECT AND DELETE THE INAPPLICABLE PARAGRAPH BELOW]</b>', S('bl', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#516984'), spaceAfter=4)),
            pb('[NON-PAYMENT VERSION:]'),
            p('As at the date of this notice, the following rent remains outstanding and unpaid:'),
            p('  Period: [PERIOD] | Amount Due: GHS [AMOUNT] | Original Due Date: [DATE] | Total Outstanding: GHS [TOTAL]'),
            pb('[BREACH VERSION:]'),
            p('It has come to our attention that you are in breach of Clause [CLAUSE NUMBER] of your Tenancy Agreement, specifically in that you have [DESCRIBE BREACH IN FULL].'),
            p('This constitutes a breach of your obligations under the Tenancy Agreement and the Rent Act, 1963 (Act 220).'),
            p('<b>YOU ARE HEREBY FORMALLY WARNED</b> that if the above [outstanding rent is not paid in full / breach is not remedied] within FOURTEEN (14) DAYS of the date of this notice, we shall be compelled to take further action, which may include the service of a formal Quit Notice and referral to the Rent Control Department in accordance with Act 220 and L.I. 369.'),
            p('We strongly urge you to address this matter immediately to avoid the inconvenience and cost of further proceedings.'),
            sp(), p('Yours faithfully,'), sp(), p('_______________________________'), p('[LANDLORD / AGENT NAME]'), p('[PROPERTY ADDRESS]'), p('[PHONE] | [EMAIL]'), p('Date: _______________'),
            sp(), lbl('SHORT VERSION (WhatsApp / SMS)'),
            p('"Dear [Name], this is a formal written warning regarding [unpaid rent of GHS [Amount] / breach of your tenancy agreement at [Address]]. You have 14 days to resolve this or further action will be taken under Act 220. Contact us urgently. — [Landlord/Agent]."'),
            hr(), sp(),

            sbar('SCRIPT 4 — TENANCY RENEWAL OFFER'), sp(),
            lbl('USAGE NOTES'),
            p('Send 60–90 days before the end of the fixed term. A renewal offer is not a legal obligation — it is a courtesy and a business decision. Use this script only when the landlord WISHES to renew. This script includes a Tenant Acceptance section so the offer can double as a written renewal record once signed. Reference: L.I. 369 (3-month rent increase notice requirement applies if the new rent is higher).'),
            sp(), lbl('FORMAL VERSION'), sp(),
            p('[DATE]'), sp(), p('Dear [TENANT NAME],'), sp(),
            pb('RE: OFFER OF TENANCY RENEWAL — [PROPERTY ADDRESS]'),
            p("We write with pleasure to advise you that your tenancy of the above-referenced premises, held under the Agreement dated [ORIGINAL AGREEMENT DATE], is due to expire on [EXPIRY DATE]."),
            p('We would like to offer you the opportunity to renew your tenancy on the following terms:'),
            p('  New Term: [NUMBER] [months/years] commencing [NEW START DATE]'),
            p('  New Rent: GHS [AMOUNT] per [month/year]'),
            p('  Advance Period: [NUMBER] [months/years]'),
            p('  Total Advance Payment: GHS [TOTAL ADVANCE AMOUNT]'),
            p('  Security Deposit: [Existing deposit carried forward / New deposit of GHS [AMOUNT]]'),
            p('  Special Conditions: _______________________________________________'),
            Paragraph('<b>[INCLUDE THIS PARAGRAPH ONLY IF THE RENT HAS INCREASED:]</b>', S('bl', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#516984'), spaceAfter=4)),
            p("Please note that the revised rent reflects current market conditions. In accordance with the Rent Regulations, 1964 (L.I. 369), this offer is being provided to you more than three (3) months before the proposed effective date."),
            p('To accept this offer, kindly sign and return the enclosed copy of this letter by [RESPONSE DEADLINE DATE]. Failure to respond by this date may result in the property being offered to other prospective tenants.'),
            p('We value your tenancy and look forward to your continued occupation.'),
            sp(), p('Yours sincerely,'), sp(), p('_______________________________'), p('[LANDLORD / AGENT NAME]'), p('[PROPERTY ADDRESS]'), p('[PHONE] | [EMAIL]'), p('Date: _______________'),
            sp(), lbl('TENANT ACCEPTANCE'),
            p('I, [TENANT NAME], accept the renewal terms set out in this letter.'),
            sp(), p('Signature: _______________________________________________'), p('Date: _______________________________________________'),
            sp(), lbl('SHORT VERSION (WhatsApp / SMS)'),
            p('"Dear [Name], your tenancy at [Address] expires on [Date]. We would like to offer a renewal for [Term] at GHS [Rent]/month. Please respond by [Deadline]. Contact us to discuss or confirm. — [Landlord/Agent Name]."'),
        ]
    return items

# ── RUN ──────────────────────────────────────────────────────────────────────
LP = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Ghana_Lease_Pack'
CS = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Communication_Scripts'

def mkpdf(path, title, sub, legal, content):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
    doc.build([cover(title, sub, legal), sp()] + content + [sp(), footer_para()])
    print(f'PDF: {path}')

# Agreement PDFs
for tier in ['Basic_Tier', 'Pro_Tier', 'Agency_Tier']:
    mkpdf(f'{LP}/{tier}/PRC-Fixed-Term-Residential-Tenancy-Agreement.pdf',
          'RESIDENTIAL TENANCY AGREEMENT\n(FIXED-TERM)', 'Property and Rent Consult — Ghana Edition',
          'Grounded in the Rent Act, 1963 (Act 220) and L.I. 369', ft_content())

for tier in ['Pro_Tier', 'Agency_Tier']:
    mkpdf(f'{LP}/{tier}/PRC-Month-to-Month-Residential-Tenancy-Agreement.pdf',
          'RESIDENTIAL TENANCY AGREEMENT\n(MONTH-TO-MONTH)', 'Property and Rent Consult — Ghana Edition',
          'Grounded in the Rent Act, 1963 (Act 220) and L.I. 369', m2m_content())
    mkpdf(f'{LP}/{tier}/PRC-Room-Rental-Agreement.pdf',
          'ROOM RENTAL AGREEMENT', 'For Single-Room Tenancies in Shared Compound Houses and Multi-Occupancy Buildings',
          'Grounded in the Rent Act, 1963 (Act 220) and L.I. 369', room_content())

mkpdf(f'{LP}/Agency_Tier/PRC-Commercial-Lease-Agreement.pdf',
      'COMMERCIAL LEASE AGREEMENT', 'Property and Rent Consult — Ghana Edition',
      'Subject to the Rent Act, 1963 (Act 220) and the Contracts Act, 1960 (Act 25)', comm_content())
mkpdf(f'{LP}/Agency_Tier/PRC-Temporary-Structure-Rent-Agreement.pdf',
      'TEMPORARY STRUCTURE RENT AGREEMENT', 'For Kiosk, Container, and Temporary Commercial Structure Rentals',
      'Subject to the Contracts Act, 1960 (Act 25) and applicable Municipal Assembly Permit Requirements', kiosk_content())

# Scripts PDFs
for tier, inc34 in [('Basic_Tier', False), ('Pro_Tier', True)]:
    fname = 'PRC-Communication-Scripts-Basic.pdf' if tier == 'Basic_Tier' else 'PRC-Communication-Scripts-Pro.pdf'
    title_t = 'LANDLORD-TENANT COMMUNICATION SCRIPTS\n(BASIC — 2 SCRIPTS)' if tier == 'Basic_Tier' else 'LANDLORD-TENANT COMMUNICATION SCRIPTS\n(PRO — 4 SCRIPTS)'
    mkpdf(f'{CS}/{tier}/{fname}', title_t, 'Property and Rent Consult — Core Pack',
          'Rent Act, 1963 (Act 220) | Rent Regulations, 1964 (L.I. 369)', script_pdf_content(inc34))

print('All PDFs done.')
