import openpyxl, os, zipfile
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter
from PIL import Image, ImageDraw, ImageFont

LP = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Ghana_Lease_Pack'
CS = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Communication_Scripts'

# ── BRAND ────────────────────────────────────────────────────────────────────
DEEP_BROWN = '36221C'; STEEL_BLUE = '516984'; LIGHT_BLUE = 'E8EEF3'
OFF_WHITE  = 'F5EDE8'; WHITE = 'FFFFFF'; WARM_GREY = '63645A'
DB = (54,34,28); SB = (81,105,132); LB = (232,238,243)
OW = (245,237,232); WH = (255,255,255); WG = (99,100,90)

def fill(h): return PatternFill('solid', fgColor=h)
def font(h='000000', bold=False, sz=10): return Font(name='Calibri', color=h, bold=bold, size=sz)
def center(): return Alignment(horizontal='center', vertical='center', wrap_text=True)
def left():   return Alignment(horizontal='left',   vertical='center', wrap_text=True)
def thin():
    s = Side(style='thin', color='AAAAAA')
    return Border(left=s, right=s, top=s, bottom=s)

def hdr(ws, row, cols_vals, widths, bg=DEEP_BROWN, fc=WHITE):
    for i, (val, w) in enumerate(zip(cols_vals, widths), 1):
        c = ws.cell(row=row, column=i, value=val)
        c.fill = fill(bg); c.font = font(fc, True, 9)
        c.alignment = center(); c.border = thin()
        ws.column_dimensions[get_column_letter(i)].width = w

def data_rows(ws, start, n_rows, n_cols, widths, bg1=LIGHT_BLUE, bg2=WHITE):
    for r in range(start, start + n_rows):
        bg = bg1 if r % 2 == 0 else bg2
        for c in range(1, n_cols + 1):
            cell = ws.cell(row=r, column=c)
            cell.fill = fill(bg); cell.border = thin()
            cell.alignment = left(); cell.font = font(sz=9)
        ws.row_dimensions[r].height = 18

def dv(ws, formula, cells):
    v = DataValidation(type='list', formula1=formula, allow_blank=True)
    ws.add_data_validation(v)
    for c in cells: v.add(c)

# ── EXCEL TRACKER ────────────────────────────────────────────────────────────
def build_excel():
    wb = openpyxl.Workbook()

    # Sheet 1 — Active Agreements
    ws1 = wb.active; ws1.title = 'Active Agreements'; ws1.sheet_view.showGridLines = False
    ws1.merge_cells('A1:M1'); ws1.row_dimensions[1].height = 28
    c = ws1['A1']; c.value = 'PROPERTY AND RENT CONSULT — LEASE AGREEMENT TRACKER'
    c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 12); c.alignment = center()
    ws1.merge_cells('A2:M2'); ws1.row_dimensions[2].height = 18
    c2 = ws1['A2']; c2.value = 'Active Agreements'
    c2.fill = fill(STEEL_BLUE); c2.font = font(WHITE, True, 10); c2.alignment = center()
    ws1.row_dimensions[3].height = 6

    cols = ['Ref','Tenant/Occupant','Property/Space','Agreement Type','Start Date','End Date/Rolling',
            'Monthly Rent (GHS)','Advance Period','Advance Paid','Deposit Paid','Renewal Notice Due','Status','Notes']
    widths = [8,22,25,18,13,16,18,15,13,13,20,14,30]
    hdr(ws1, 4, cols, widths)
    data_rows(ws1, 5, 20, 13, widths)
    dv(ws1, '"Fixed-Term,Month-to-Month,Room Rental,Commercial,Kiosk/Container"', [ws1.cell(5+i,4) for i in range(20)])
    dv(ws1, '"Active,Expiring Soon,Expired,Terminated"', [ws1.cell(5+i,12) for i in range(20)])

    # Sheet 2 — Expiry Calendar
    ws2 = wb.create_sheet('Expiry Calendar'); ws2.sheet_view.showGridLines = False
    ws2.merge_cells('A1:F1'); ws2.row_dimensions[1].height = 22
    c = ws2['A1']; c.value = 'EXPIRY CALENDAR'; c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 11); c.alignment = center()
    cols2 = ['Ref','Tenant','Property','End Date','Days to Expiry','Action Required']
    widths2 = [8, 22, 28, 14, 16, 35]
    hdr(ws2, 2, cols2, widths2)
    for r in range(3, 23):
        bg = LIGHT_BLUE if r%2==0 else WHITE
        for col in range(1, 7):
            c = ws2.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin(); c.alignment = left(); c.font = font(sz=9)
        ws2.cell(r, 5).value = f'=IF(D{r}="","",D{r}-TODAY())'
        ws2.row_dimensions[r].height = 18
    from openpyxl.formatting.rule import CellIsRule
    ws2.conditional_formatting.add('E3:E22', CellIsRule(operator='lessThan',    formula=['30'], fill=PatternFill('solid', fgColor='C82020'), font=Font(color=WHITE, bold=True)))
    ws2.conditional_formatting.add('E3:E22', CellIsRule(operator='between',     formula=['30','60'], fill=PatternFill('solid', fgColor='C8A000')))
    ws2.conditional_formatting.add('E3:E22', CellIsRule(operator='greaterThan', formula=['60'], fill=PatternFill('solid', fgColor='2D7A3A'), font=Font(color=WHITE)))

    # Sheet 3 — Deposit Register
    ws3 = wb.create_sheet('Deposit Register'); ws3.sheet_view.showGridLines = False
    ws3.merge_cells('A1:I1'); ws3.row_dimensions[1].height = 22
    c = ws3['A1']; c.value = 'DEPOSIT REGISTER'; c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 11); c.alignment = center()
    cols3 = ['Ref','Tenant','Deposit Amount (GHS)','Date Received','Date Returned','Deductions (GHS)','Reason for Deduction','Balance Returned (GHS)','Status']
    widths3 = [8,22,20,15,15,18,25,20,16]
    hdr(ws3, 2, cols3, widths3)
    for r in range(3, 23):
        bg = LIGHT_BLUE if r%2==0 else WHITE
        for col in range(1, 10):
            c = ws3.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin(); c.alignment = left(); c.font = font(sz=9)
        ws3.cell(r, 8).value = f'=IF(C{r}="","",C{r}-F{r})'
        ws3.row_dimensions[r].height = 18
    dv(ws3, '"Held,Partially Returned,Fully Returned,Disputed"', [ws3.cell(3+i, 9) for i in range(20)])

    # Sheet 4 — Permit Register
    ws4 = wb.create_sheet('Permit Register'); ws4.sheet_view.showGridLines = False
    ws4.merge_cells('A1:I1'); ws4.row_dimensions[1].height = 22
    c = ws4['A1']; c.value = 'PERMIT REGISTER (Kiosk/Commercial)'; c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 11); c.alignment = center()
    cols4 = ['Occupant','Space','Municipal Assembly','Permit No.','Issue Date','Expiry Date','Renewal Due','Status','Notes']
    widths4 = [22,25,22,14,13,13,13,16,28]
    hdr(ws4, 2, cols4, widths4)
    data_rows(ws4, 3, 20, 9, widths4)
    dv(ws4, '"Valid,Expired,Pending Renewal,Not Required"', [ws4.cell(3+i, 8) for i in range(20)])

    # Sheet 5 — Agreement Log
    ws5 = wb.create_sheet('Agreement Log'); ws5.sheet_view.showGridLines = False
    ws5.merge_cells('A1:G1'); ws5.row_dimensions[1].height = 22
    c = ws5['A1']; c.value = 'AGREEMENT LOG'; c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 11); c.alignment = center()
    cols5 = ['Date Created','Agreement Type','Tenant/Occupant','Property/Space','Prepared By','Filed (Y/N)','Notes']
    widths5 = [14,20,22,28,18,12,30]
    hdr(ws5, 2, cols5, widths5)
    data_rows(ws5, 3, 20, 7, widths5)
    dv(ws5, '"Y,N"', [ws5.cell(3+i, 6) for i in range(20)])

    path = f'{LP}/Agency_Tier/PRC-Lease-Agreement-Tracker-v2.xlsx'
    wb.save(path)
    print(f'Excel saved: {path}')

build_excel()

# ── WHATSAPP CARDS ────────────────────────────────────────────────────────────
def gf(size, bold=False):
    paths = [r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
             r'C:\Windows\Fonts\calibrib.ttf' if bold else r'C:\Windows\Fonts\calibri.ttf']
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def ctext(draw, text, y, W, font, color=WH):
    bb = draw.textbbox((0,0), text, font=font)
    x = (W - (bb[2]-bb[0])) // 2
    draw.text((x, y), text, font=font, fill=color)

W2, H2 = 1080, 1350

# Card 1 — Cover
img = Image.new('RGB', (W2,H2), DB)
draw = ImageDraw.Draw(img)
draw.text((60,60), 'PRC', font=gf(44,True), fill=WH)
ctext(draw, 'GHANA LEASE AGREEMENT', 240, W2, gf(68,True))
ctext(draw, 'TEMPLATE PACK', 328, W2, gf(68,True))
ctext(draw, '5 Agreements. Every Tenancy Type.', 450, W2, gf(42,False), tuple(min(c+80,255) for c in SB))
ctext(draw, '+ Tenancy Offer Letter Included', 520, W2, gf(34,False), OW)
draw.rectangle([(0,H2-120),(W2,H2)], fill=SB)
ctext(draw, 'Property and Rent Consult  |  propertynrentconsult.com', H2-75, W2, gf(28,False))
img.save(f'{LP}/Agency_Tier/PRC-Lease-Pack-Card-1.png', dpi=(96,96))
print('Card 1 saved')

# Card 2 — 5 Agreement Types
img = Image.new('RGB', (W2,H2), WH)
draw = ImageDraw.Draw(img)
draw.rectangle([(0,0),(W2,160)], fill=DB)
ctext(draw, '5 AGREEMENT TYPES INCLUDED', 50, W2, gf(48,True))
agreements = [
    ('1', 'Fixed-Term Residential', 'For apartments, houses, and flats'),
    ('2', 'Month-to-Month Residential', 'Rolling tenancy, 1-month notice'),
    ('3', 'Room Rental', 'Shared compound & multi-occupancy'),
    ('4', 'Commercial Lease', 'Shops, offices, warehouses, clinics'),
    ('5', 'Kiosk & Container Rental', 'Temporary structure, Municipal Assembly compliant'),
]
y = 210
for num, name, desc in agreements:
    draw.rectangle([(60,y),(W2-60,y+150)], fill=LB)
    draw.text((90,y+18), num+'.', font=gf(42,True), fill=DB)
    draw.text((145,y+20), name, font=gf(36,True), fill=DB)
    draw.text((145,y+72), desc, font=gf(28,False), fill=WG)
    y += 168
draw.rectangle([(0,H2-100),(W2,H2)], fill=SB)
ctext(draw, '+ Tenancy Offer Letter in Every Tier', H2-65, W2, gf(30,False))
img.save(f'{LP}/Agency_Tier/PRC-Lease-Pack-Card-2.png', dpi=(96,96))
print('Card 2 saved')

# Card 3 — What every agreement must cover
img = Image.new('RGB', (W2,H2), LB)
draw = ImageDraw.Draw(img)
draw.rectangle([(0,0),(W2,160)], fill=SB)
ctext(draw, 'WHAT EVERY GHANA', 30, W2, gf(52,True))
ctext(draw, 'AGREEMENT MUST COVER', 98, W2, gf(52,True))
elements = [
    ('Parties & ID', 'Full names, Ghana Card, GPS address'),
    ('Rent & Advance', 'Amount, interval, advance period per Act 220'),
    ('Termination Notice', 'Written notice, statutory minimum period'),
    ('Deposit Terms', '14-day return rule, itemised deductions'),
    ('Utilities Split', 'Who pays what — ECG, Ghana Water, refuse'),
    ('Dispute Route', 'Rent Control Department first step'),
]
y = 200
for i, (title, desc) in enumerate(elements):
    col = 0 if i < 3 else 570
    row_y = 200 + (i % 3) * 320
    draw.rectangle([(60+col, row_y), (510+col, row_y+300)], fill=WH)
    ctext_x = 285 + col
    bb = draw.textbbox((0,0), title, font=gf(34,True))
    tw = bb[2]-bb[0]
    draw.text((60+col+(450-tw)//2, row_y+30), title, font=gf(34,True), fill=DB)
    draw.text((80+col, row_y+100), desc, font=gf(26,False), fill=WG)
img.save(f'{LP}/Agency_Tier/PRC-Lease-Pack-Card-3.png', dpi=(96,96))
print('Card 3 saved')

# Card 4 — Residential vs Commercial
img = Image.new('RGB', (W2,H2), WH)
draw = ImageDraw.Draw(img)
draw.rectangle([(0,0),(W2,160)], fill=DB)
ctext(draw, 'RESIDENTIAL vs COMMERCIAL', 40, W2, gf(46,True))
ctext(draw, 'KEY DIFFERENCES', 105, W2, gf(40,True))
rows = [
    ('Feature', 'Residential', 'Commercial'),
    ('Advance Rent', 'Max 6 months\n(Act 220)', 'Negotiated\nfreely'),
    ('Rent Increase\nNotice', '3 months\n(L.I. 369)', 'As agreed\nin lease'),
    ('Dispute Forum', 'Rent Control\nDepartment', 'ADR / High\nCourt'),
    ('Eviction\nGrounds', 'Act 220\nspecific', 'Lease + Act 25'),
    ('Permitted Use', 'Residential\nonly', 'Business\nuse only'),
]
y = 190
col_w = [280,400,400]
for i, row in enumerate(rows):
    bg = DB if i == 0 else (LB if i%2==0 else WH)
    fc = WH if i == 0 else DB
    x = 60
    for j, (cell, cw) in enumerate(zip(row, col_w)):
        draw.rectangle([(x,y),(x+cw,y+140)], fill=bg)
        bb = draw.textbbox((0,0), cell, font=gf(26 if i>0 else 30, i==0))
        tw = bb[2]-bb[0]; th = bb[3]-bb[1]
        draw.text((x+(cw-tw)//2, y+(140-th)//2), cell, font=gf(26 if i>0 else 30, i==0), fill=fc)
        x += cw
    y += 142
img.save(f'{LP}/Agency_Tier/PRC-Lease-Pack-Card-4.png', dpi=(96,96))
print('Card 4 saved')

# Card 5 — CTA
img = Image.new('RGB', (W2,H2), DB)
draw = ImageDraw.Draw(img)
ctext(draw, 'GET THE FULL PACK', 80, W2, gf(66,True))
ctext(draw, 'Ghana Lease Agreement', 170, W2, gf(38,False), OW)
ctext(draw, '& Communication Scripts Pack', 218, W2, gf(38,False), OW)
tiers = [
    ('BASIC',  'GHS 49',  'Fixed-Term + Offer Letter'),
    ('PRO',    'GHS 99',  '3 Residential + Offer Letter'),
    ('AGENCY', 'GHS 199', 'All 5 + Offer Letter + Excel + Cards'),
]
y = 320
for tier, price, desc in tiers:
    draw.rectangle([(60,y),(W2-60,y+180)], fill=WH)
    draw.text((90,y+18), tier, font=gf(44,True), fill=SB)
    draw.text((90,y+74), price, font=gf(54,True), fill=DB)
    draw.text((90,y+138), desc, font=gf(28,False), fill=WG)
    y += 198
draw.rectangle([(60,y+10),(W2-60,y+90)], fill=SB)
ctext(draw, 'Available on Selar  |  Search: PRC Lease Pack', y+32, W2, gf(30,True))
ctext(draw, 'Property and Rent Consult', H2-60, W2, gf(30,False), OW)
img.save(f'{LP}/Agency_Tier/PRC-Lease-Pack-Card-5.png', dpi=(96,96))
print('Card 5 saved')

# ── SCRIPTS PRODUCT CARDS ─────────────────────────────────────────────────────
# Card for Communication Scripts product
img = Image.new('RGB', (W2,H2), DB)
draw = ImageDraw.Draw(img)
draw.text((60,60), 'PRC', font=gf(44,True), fill=WH)
ctext(draw, 'LANDLORD-TENANT', 240, W2, gf(62,True))
ctext(draw, 'COMMUNICATION', 318, W2, gf(62,True))
ctext(draw, 'SCRIPTS PACK', 396, W2, gf(62,True))
ctext(draw, '4 Ready-to-Use Scripts for Ghana Landlords', 500, W2, gf(36,False), OW)
draw.rectangle([(60,600),(W2-60,780)], fill=SB)
scripts = ['Rent Reminder Notice', 'Routine Inspection Notice', 'Eviction Warning Notice', 'Tenancy Renewal Offer']
y2 = 620
for s in scripts:
    ctext(draw, '• ' + s, y2, W2, gf(30,False))
    y2 += 42
draw.rectangle([(60,830),(W2-60,1010)], fill=WH)
ctext(draw, 'BASIC — GHS 29', 860, W2, gf(38,True), DB)
ctext(draw, 'Scripts 1 & 2', 918, W2, gf(28,False), WG)
ctext(draw, 'PRO — GHS 49', 970, W2, gf(38,True), SB)
ctext(draw, 'All 4 Scripts', 1028, W2, gf(28,False), WG) if False else None
draw.rectangle([(60,1050),(W2-60,1130)], fill=SB)
ctext(draw, 'Available on Selar  |  Search: PRC Scripts Pack', 1072, W2, gf(30,True))
ctext(draw, 'Property and Rent Consult', H2-60, W2, gf(30,False), OW)
img.save(f'{CS}/Pro_Tier/PRC-Scripts-Product-Image.png', dpi=(96,96))
img.save(f'{CS}/Basic_Tier/PRC-Scripts-Product-Image.png', dpi=(96,96))
print('Scripts product images saved')

# ── SELAR LISTING TEXT ────────────────────────────────────────────────────────
selar = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs'
with open(f'{selar}/Selar_Listing_Copy_Lease_Pack.txt', 'w', encoding='utf-8') as f:
    f.write("""SELAR LISTING COPY — GHANA LEASE AGREEMENT TEMPLATE PACK
==========================================================================

LISTING 1 — BASIC TIER
Product Title: Ghana Lease Agreement Template Pack — Basic
Price: GHS 49.00
Short Description: A professionally drafted, Act 220-compliant fixed-term residential tenancy agreement plus a Tenancy Offer Letter for Ghana — editable Word file and PDF, ready to sign today.

Full Description:
Every tenancy in Ghana needs a written agreement. Without one, your rights exist only in memory — and memory is unreliable when disputes arise.

The Ghana Lease Agreement Template Pack (Basic) gives you:

WHAT IS INSIDE:
Fixed-Term Residential Tenancy Agreement (DOCX + PDF) — 11-clause agreement grounded in Act 220 and L.I. 369 covering parties, term, rent, advance payment with receipt obligation, security deposit (14-day return rule), utilities, landlord and tenant obligations, condition on vacation, termination and notice, Rent Control Department dispute resolution, fixtures inventory schedule, special conditions schedule, and full execution block with witnesses.

Tenancy Offer Letter (DOCX) — set the terms in writing before the formal agreement is drawn; used to confirm an offer of tenancy to a prospective tenant.

Every clause reflects Ghanaian practice: advance rent, Ghana Card verification, ECG/NEDCo utility arrangements, and the District Magistrate Court recovery procedure.

Terms: Personal and internal business use only. Not for resale.
Produced by Property and Rent Consult.

--------------------------------------------------------------------------

LISTING 2 — PRO TIER
Product Title: Ghana Lease Agreement Template Pack — Pro
Price: GHS 99.00
Short Description: Three Ghana residential tenancy agreements plus a Tenancy Offer Letter — fixed-term, month-to-month, and room rental — all Act 220 compliant, editable Word and PDF.

Full Description:
Everything in Basic, plus two additional agreements for landlords with mixed residential portfolios.

WHAT IS INSIDE:
- Tenancy Offer Letter (DOCX)
- Fixed-Term Residential Tenancy Agreement (DOCX + PDF)
- Month-to-Month Residential Tenancy Agreement (DOCX + PDF) — rolling monthly continuation, 1-month termination notice, 3-month rent review notice per L.I. 369
- Room Rental Agreement (DOCX + PDF) — shared facilities clause, proportionate utility cost arrangement, House Rules schedule (quiet hours, visitors, shared areas)

All three are fully editable, grounded in Act 220, and use DD/MM/YYYY date format and Ghana Card identification throughout.
Produced by Property and Rent Consult.

--------------------------------------------------------------------------

LISTING 3 — AGENCY TIER
Product Title: Ghana Lease Agreement Template Pack — Agency (All 5 Agreements)
Price: GHS 199.00
Short Description: All five Ghana tenancy and lease agreements plus a Tenancy Offer Letter, Excel tracker, and branded WhatsApp cards — the complete landlord and agent agreement toolkit.

Full Description:
The Agency tier covers every letting scenario a property manager or agent in Ghana will encounter.

WHAT IS INSIDE:
- Tenancy Offer Letter (DOCX)
- Fixed-Term Residential Tenancy Agreement (DOCX + PDF)
- Month-to-Month Residential Tenancy Agreement (DOCX + PDF)
- Room Rental Agreement with House Rules Schedule (DOCX + PDF)
- Commercial Lease Agreement — 14 clauses including permitted use, signage, fit-out, insurance, and ADR (DOCX + PDF)
- Temporary Structure Rent Agreement — for kiosks and containers; structure ownership split, Municipal Assembly permit clause, utility consent, self-removal on termination (DOCX + PDF)
- Excel Agreement Tracker — 5 sheets: active agreements, expiry calendar (colour-coded 30/60-day alerts), deposit register, permit register, agreement log
- 5 WhatsApp Image Cards (1080x1350px) — branded, ready to share with your team or post to social media
- README Delivery Note

Produced by Property and Rent Consult.

--------------------------------------------------------------------------

WEBSITE BUTTON COPY:
Basic button:   Get Basic — GHS 49
Pro button:     Get Pro — GHS 99
Agency button:  Get Agency — GHS 199
Trust line:     Secure payment via Selar, Mobile Money and Card accepted
Delivery:       Instant download after payment

SELAR TAGS:
tenancy agreement Ghana, lease template Ghana, room rental Ghana, kiosk rental agreement Ghana, container rental agreement Ghana, commercial lease Ghana, Act 220, L.I. 369, landlord template, Ghana property management, rent agreement, fixed-term tenancy, month-to-month tenancy, property and rent consult, PRC Ghana, temporary structure Ghana, micro-business Ghana, trading space agreement, tenancy offer letter Ghana

==========================================================================
SELAR LISTING COPY — LANDLORD COMMUNICATION SCRIPTS PACK
==========================================================================

LISTING 1 — BASIC TIER
Product Title: Landlord Communication Scripts Pack — Basic (2 Scripts)
Price: GHS 29.00
Short Description: Two essential landlord communication scripts for Ghana — a rent reminder notice and a routine inspection notice — formal letter and WhatsApp versions of each.

Full Description:
Two documents every Ghana landlord needs before a problem escalates.

WHAT IS INSIDE:
Script 1 — Rent Reminder Notice (formal + WhatsApp version): Send when rent is 1-7 days overdue. Polite, professional, and legally appropriate as a first step before escalation.

Script 2 — Routine Inspection Notice (formal + WhatsApp version): Send at least 24-48 hours before any inspection. Satisfies the Act 220 entry notice requirement. Non-threatening in tone.

Each script includes usage notes (when to use it, legal reference, tone guidance), a full formal letter version (date, address, RE: line, body, sign-off, signature block), and a short WhatsApp/SMS version ready to send from your phone.

Terms: Personal and internal business use only. Not for resale.
Produced by Property and Rent Consult.

--------------------------------------------------------------------------

LISTING 2 — PRO TIER
Product Title: Landlord Communication Scripts Pack — Pro (All 4 Scripts)
Price: GHS 49.00
Short Description: All four essential landlord-tenant communication scripts for Ghana — rent reminder, inspection notice, eviction warning, and renewal offer — formal and WhatsApp versions.

Full Description:
Everything in Basic, plus two critical escalation and retention scripts.

WHAT IS INSIDE:
Script 1 — Rent Reminder Notice: For 1-7 days overdue rent. Polite first contact.
Script 2 — Routine Inspection Notice: Satisfies Act 220 24-hour entry notice requirement.
Script 3 — Eviction Warning Notice (First Formal Warning): For rent 14+ days overdue or tenancy breach. Triggers a 14-day remedy period. Includes both non-payment and breach versions — delete the inapplicable one before sending. Creates the paper trail required before a formal Quit Notice can be issued.
Script 4 — Tenancy Renewal Offer: Send 60-90 days before term expiry. Includes a Tenant Acceptance section so the offer can double as a written renewal record once signed.

Every script includes usage notes with legal references, a full formal letter version, and a WhatsApp/SMS short version.

Produced by Property and Rent Consult.

--------------------------------------------------------------------------

WEBSITE BUTTON COPY:
Basic button:   Get Basic — GHS 29
Pro button:     Get Pro — GHS 49
Trust line:     Secure payment via Selar, Mobile Money and Card accepted
Delivery:       Instant download after payment

SELAR TAGS:
landlord communication scripts Ghana, rent reminder Ghana, eviction warning Ghana, inspection notice Ghana, renewal offer Ghana, Act 220, L.I. 369, landlord letter Ghana, tenant notice Ghana, property and rent consult, PRC Ghana, landlord template Ghana, WhatsApp notice landlord
""")

print('Selar listing text saved')

# ── ZIP FILES ─────────────────────────────────────────────────────────────────
def make_zip(folder, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(folder):
            if fname.endswith(('.pdf','.xlsx','.docx','.png')) and 'Product-Image' not in fname:
                zf.write(os.path.join(folder, fname), fname)
    size = os.path.getsize(zip_path)
    print(f'ZIP: {zip_path} ({size:,} bytes)')

make_zip(f'{LP}/Basic_Tier',  f'{LP}/../PRC-Lease-Pack-Basic.zip')
make_zip(f'{LP}/Pro_Tier',    f'{LP}/../PRC-Lease-Pack-Pro.zip')
make_zip(f'{LP}/Agency_Tier', f'{LP}/../PRC-Lease-Pack-Agency.zip')
make_zip(f'{CS}/Basic_Tier',  f'{CS}/../PRC-Scripts-Basic.zip')
make_zip(f'{CS}/Pro_Tier',    f'{CS}/../PRC-Scripts-Pro.zip')
print('All done.')
