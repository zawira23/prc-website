import os, zipfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas as pdfcanvas
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter
from PIL import Image, ImageDraw, ImageFont

BASE = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\PRC_Utility_Tracker'

DB = (54,34,28); SB = (81,105,132); WG = (99,100,90)
LB = (232,238,243); OW = (245,237,232); WH = (255,255,255)
DB_H = '#36221C'; SB_H = '#516984'; WG_H = '#63645A'
LB_H = '#E8EEF3'; OW_H = '#F5EDE8'

W, H = A4

# ── PDF USER GUIDE ────────────────────────────────────────────────────────────
def S(name,**kw): return ParagraphStyle(name,**kw)

def build_pdf(path):
    h1 = S('h1', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor(DB_H), spaceBefore=12, spaceAfter=6, leading=18)
    h2 = S('h2', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor(SB_H), spaceBefore=8, spaceAfter=4)
    body = S('body', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#2D2D2D'), spaceAfter=4, leading=14)
    bullet = S('bullet', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#2D2D2D'), spaceAfter=3, leading=14, leftIndent=20)
    small = S('small', fontName='Helvetica', fontSize=8, textColor=colors.HexColor(WG_H))
    center = S('center', fontName='Helvetica', fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#2D2D2D'))
    cov_title = S('ctitle', fontName='Helvetica-Bold', fontSize=28, textColor=colors.white, alignment=TA_CENTER)
    cov_sub   = S('csub',   fontName='Helvetica',      fontSize=20, textColor=colors.white, alignment=TA_CENTER)
    cov_label = S('clabel', fontName='Helvetica',      fontSize=16, textColor=colors.white, alignment=TA_CENTER)

    def p(text, style=None): return Paragraph(text, style or body)
    def b(text): return Paragraph(f'• {text}', bullet)
    def sp(n=4): return Spacer(1, n*mm)
    def hr(): return HRFlowable(width='100%', thickness=1, color=colors.HexColor(SB_H), spaceAfter=4, spaceBefore=4)

    def callout(text):
        t = Table([[Paragraph(text, S('cb', fontName='Helvetica', fontSize=10, textColor=colors.HexColor(DB_H)))]], colWidths=[W-30*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),colors.HexColor(LB_H)),
            ('LEFTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LINEBEFORE',(0,0),(0,-1),3,colors.HexColor(SB_H)),
        ]))
        return t

    def section(title):
        return [p(f'<b>{title}</b>', h1), hr()]

    # COVER PAGE
    cover_rect = Table([[Paragraph('PRC Utility Payment Tracker', cov_title)],
                        [Paragraph('Ghana Edition', cov_sub)],
                        [Paragraph('User Guide', cov_label)]],
                       colWidths=[W-30*mm])
    cover_rect.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor(DB_H)),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.HexColor(DB_H)]),
    ]))

    story = [
        sp(8), cover_rect, sp(8),
        p('Property and Rent Consult', center),
        p('Expert Guidance on Ghana Property, Rent, and Tenancy Law', S('c2', fontName='Helvetica', fontSize=11, textColor=colors.HexColor(WG_H), alignment=TA_CENTER)),
        sp(3), p('2026 Edition', center), sp(20),
        p('© 2026 Property and Rent Consult — For purchaser use only. Not for resale.', small),
        PageBreak(),

        # TOC
        *section('Contents'),
        p('1. What This Tool Does ................. 3'),
        p('2. Getting Started ..................... 3'),
        p('3. Adding Your Tenants ................. 4'),
        p('4. Recording Payments .................. 5'),
        p('5. Generating a Receipt ................ 6'),
        p('6. Printing and Saving Receipts ........ 6'),
        p('7. Viewing Payment History ............. 7'),
        p('8. Dashboard Overview .................. 7'),
        p('9. Settings ........................... 8'),
        p('10. Frequently Asked Questions ......... 8'),
        p('11. Terms of Use ...................... 10'),
        PageBreak(),

        # SECTION 1
        *section('1. What This Tool Does'),
        p('The PRC Utility Payment Tracker is a self-contained browser-based application designed for landlords, property managers, and tenants in Ghana. It allows you to:'),
        b('Record and track electricity, water, and service charge payments for any number of tenants and units'),
        b('Know at a glance which tenants have paid and which have not for any billing period'),
        b('Generate a numbered, printable payment receipt for every transaction'),
        b('Build a complete searchable history of all payments across all periods'),
        b('Run entirely offline — no internet connection required after download'),
        sp(),
        callout('This tool does NOT connect to any external server. All your data is stored privately on your own device. Nothing is sent to Property and Rent Consult or any third party.'),
        sp(),

        # SECTION 2
        *section('2. Getting Started'),
        p('<b>Opening the tracker:</b>'),
        p('Locate the file PRC-Utility-Tracker-[Basic/Pro].html in your download folder. Double-click it. It will open in your default web browser. You do not need to install anything.'),
        sp(2),
        p('<b>Recommended browsers:</b>'),
        p('Google Chrome, Mozilla Firefox, Microsoft Edge, Safari.'),
        sp(2),
        p('<b>First-time setup:</b>'),
        b('Click the settings icon (gear ⚙) in the top-right corner.'),
        b('Enter your property name, your name, your address, and your phone number.'),
        b('This information appears on every receipt you generate.'),
        b('Click "Save settings."'),
        sp(),

        # SECTION 3
        *section('3. Adding Your Tenants'),
        p('Click the <b>Tenants</b> tab. Click the <b>Add tenant</b> button in the top-right corner.'),
        sp(2),
        p('Fill in the following:'),
        b('<b>Full name</b> — the tenant\'s full legal name as it appears on their Ghana Card'),
        b('<b>Unit / Room</b> — the specific unit they occupy (e.g. Flat 3B, Room 4, Ground Floor)'),
        b('<b>Phone number</b> — optional, for your records'),
        b('<b>Tenancy start</b> — the month their tenancy began'),
        b('<b>Property / Block</b> — if you manage more than one property (Pro tier)'),
        sp(2),
        p('<b>Monthly utility amounts:</b>'),
        p('Enter the fixed monthly amounts you charge this tenant for each utility:'),
        b('<b>Electricity (GHS)</b> — their share of the ECG/NEDCo bill'),
        b('<b>Water (GHS)</b> — their share of the Ghana Water Company bill'),
        b('<b>Service charge (GHS)</b> — any monthly maintenance or cleaning fee'),
        sp(),
        callout('Note: These amounts are fixed until you edit them. They apply to every billing period you record for this tenant. If the amounts change, edit the tenant record — the new amounts will apply from the next period you record.'),
        sp(),
        p('Click <b>Save tenant.</b> The tenant appears in your tenant list immediately.'),
        p('To edit a tenant: click the pencil ✏️ icon on their row.'),
        p('To remove a tenant: click the trash 🗑 icon. Their payment history is kept.'),
        PageBreak(),

        # SECTION 4
        *section('4. Recording Payments'),
        p('Click the <b>Billing</b> tab. Select the billing period using the month picker. Click <b>Load period.</b>'),
        p('Your full tenant list appears with their amounts and current payment status.'),
        sp(2),
        p('<b>To record a full payment:</b>'),
        b('Click <b>Mark paid</b> on the tenant\'s row.'),
        b('A payment panel opens showing the tenant\'s name, unit, billing period, itemised breakdown, and total amount due.'),
        b('Fill in: Date paid (defaults to today), Payment method (MoMo/Cash/Bank Transfer/Cheque/Other), Received by (optional), Notes (optional).'),
        b('Click <b>Confirm payment.</b> The payment is saved and a receipt is generated immediately.'),
        sp(2),
        p('<b>To record a partial payment:</b>'),
        b('Click <b>Partial</b> on the tenant\'s row.'),
        b('Enter the amount actually received. If the amount is less than the total due, status is set to "Partial."'),
        b('A receipt is still generated for the partial amount.'),
        sp(2),
        p('<b>To undo a payment:</b> Click <b>Undo</b> on a paid row. This removes the payment record. Use this only to correct errors.'),
        sp(),

        # SECTION 5
        *section('5. Generating a Receipt'),
        p('A receipt is generated automatically after every payment you confirm.'),
        sp(2),
        p('The receipt contains:'),
        b('A unique receipt number (RCP-XXXXXXXX)'),
        b('Date issued'),
        b('Tenant full name and unit'),
        b('Billing period (e.g. June 2026)'),
        b('Itemised breakdown: Electricity / Water / Service Charge'),
        b('Total due and amount paid'),
        b('Balance remaining (if partial payment)'),
        b('Payment method and date paid'),
        b('Status (Paid / Partial)'),
        b('Your property/company name from Settings'),
        sp(2),
        p('To view a receipt at any time: go to the <b>Billing</b> tab, load the relevant period, and click the receipt 🧾 icon on the tenant\'s row. Or go to <b>Payment History</b> and click the receipt icon on any record.'),
        sp(),

        # SECTION 6
        *section('6. Printing and Saving Receipts'),
        p('Click <b>Print / Save PDF</b> in the receipt window. A clean, print-ready version of the receipt opens in a new browser tab. Your browser\'s print dialog appears.'),
        sp(2),
        b('To print: select your printer and click Print.'),
        b('To save as PDF: in the print dialog, choose "Save as PDF" (or "Print to PDF") as the destination instead of a printer. Choose where to save the file.'),
        sp(),
        callout('Tip: Save receipts as PDFs on your phone or computer and send to tenants via WhatsApp, email, or SMS as proof of payment.'),
        sp(),

        # SECTION 7
        *section('7. Viewing Payment History'),
        p('Click the <b>Payment History</b> tab. All payment records appear, most recent first.'),
        sp(2),
        b('To search: type a tenant name or unit number in the search box.'),
        b('To filter by status: use the status dropdown (All / Paid / Partial / Unpaid).'),
        b('To filter by period: use the period dropdown.'),
        b('Each row shows the full payment detail. Click the receipt icon to view and print the receipt for any past payment.'),
        sp(),

        # SECTION 8
        *section('8. Dashboard Overview'),
        p('The <b>Dashboard</b> tab gives you a live summary of the current month:'),
        b('Total tenants in your tracker'),
        b('How many have paid this month'),
        b('How many have not yet paid'),
        b('Total utility charges expected this month (sum of all tenant amounts)'),
        b('Total amount collected'),
        b('Total outstanding balance'),
        sp(2),
        p('The Outstanding Payments section lists every unpaid tenant with their total due and a quick link to record their payment. Use the period selector to view the summary for any past month.'),
        sp(),

        # SECTION 9
        *section('9. Settings'),
        p('Click the gear icon ⚙ in the top-right header to open Settings.'),
        sp(2),
        b('<b>Property / Company Name:</b> appears at the top of every receipt.'),
        b('<b>Owner / Manager Name:</b> appears as "Issued by" on receipts.'),
        b('<b>Address:</b> appears on receipts.'),
        b('<b>Phone:</b> appears on receipts.'),
        sp(),
        p('If you leave Settings empty, receipts default to showing "Property and Rent Consult" as the issuing party. Recommended: fill in Settings before generating your first receipt.'),
        PageBreak(),

        # SECTION 10 — FAQ
        *section('10. Frequently Asked Questions'),
        p('<b>Q: Will I lose my data if I close the browser?</b>'),
        p('A: No. All data is saved automatically on your device using browser storage (localStorage). Your records survive closing the browser, shutting down your computer, and reopening the file another day.'),
        sp(2),
        p('<b>Q: Can I use this on my phone?</b>'),
        p('A: Yes. Open the HTML file in your phone\'s browser (Chrome or Safari). The app is responsive and works on mobile screens. For the best experience, use it in landscape orientation on smaller screens.'),
        sp(2),
        p('<b>Q: Can more than one person use this tracker at the same time?</b>'),
        p('A: The Basic and Pro apps store data on a single device. If two people need to access the same data, they would need to work from the same device or the same browser on that device. Agency-tier users receive an Excel backup template for sharing records across devices.'),
        sp(2),
        p('<b>Q: How do I back up my data?</b>'),
        p('A: Pro and Agency tier users can click the "Export data" button in the header. This downloads a JSON file of all your tenants and payment records. Keep this file as a backup. Basic tier users should note their records manually or upgrade to Pro for export functionality.'),
        sp(2),
        p('<b>Q: What happens if I clear my browser data or use a different browser?</b>'),
        p('A: Data is stored in the specific browser on the specific device you used. Clearing browser data (cookies/cache) or switching to a different browser will show an empty tracker. Always export your data before clearing browser storage.'),
        sp(2),
        p('<b>Q: Is my data shared with Property and Rent Consult?</b>'),
        p('A: No. This tool has no internet connection and sends nothing to any server. All your data stays on your device.'),
        sp(2),
        p('<b>Q: Is this tool legally required under Ghanaian tenancy law?</b>'),
        p('A: No, but it supports compliance. The Rent Act, 1963 (Act 220) requires landlords to issue written receipts for rent and utility payments. This tracker generates those receipts and maintains a record — both of which support your legal position in any dispute.'),
        sp(),

        # SECTION 11 — TERMS
        PageBreak(),
        *section('11. Terms of Use'),
        p('© 2026 Property and Rent Consult. All rights reserved.'),
        sp(2),
        p('This software is licensed for personal and internal business use only. The licence covers one user and their properties.'),
        sp(2),
        p('<b>You may:</b>'),
        b('Use this tool to track utility payments for properties you own or manage'),
        b('Generate and share receipts with your tenants'),
        b('Print, save, and archive receipts for your records'),
        sp(2),
        p('<b>You may NOT:</b>'),
        b('Resell, redistribute, or publish this tool in any form'),
        b('Modify and sell it as your own product'),
        b('Share the file with third parties outside your immediate business'),
        sp(2),
        callout('Violation of these terms may constitute infringement of Ghanaian copyright law.'),
        sp(2),
        p('<b>Limitation of liability:</b>'),
        p('This tool is provided as-is. Property and Rent Consult accepts no liability for data loss arising from browser storage clearing, device failure, or user error. Users are responsible for maintaining their own data backups.'),
        sp(2),
        p('For support or licensing enquiries: contact Property and Rent Consult at info@propertynrentconsult.com'),
    ]

    class MyTemplate(SimpleDocTemplate):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        def handle_pageBegin(self):
            super().handle_pageBegin()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
    doc.build(story)
    print(f'PDF: {path}')

# Build PDF for all tiers
guide_path = os.path.join(BASE, 'PRC-Utility-Tracker-User-Guide.pdf')
build_pdf(guide_path)
for tier in ['Basic_Tier','Pro_Tier','Agency_Tier']:
    import shutil
    shutil.copy(guide_path, os.path.join(BASE, tier, 'PRC-Utility-Tracker-User-Guide.pdf'))
print('PDF guides distributed')

# ── EXCEL BACKUP TEMPLATE ─────────────────────────────────────────────────────
def fill(h): return PatternFill('solid', fgColor=h.lstrip('#'))
def font(h='000000', bold=False, sz=10): return Font(name='Calibri', color=h.lstrip('#'), bold=bold, size=sz)
def center(): return Alignment(horizontal='center', vertical='center', wrap_text=True)
def left():   return Alignment(horizontal='left',   vertical='center', wrap_text=True)
def thin():
    s = Side(style='thin', color='AAAAAA')
    return Border(left=s, right=s, top=s, bottom=s)

def build_excel():
    wb = openpyxl.Workbook()

    # Sheet 1 — Tenant Register
    ws1 = wb.active; ws1.title = 'Tenant Register'; ws1.sheet_view.showGridLines = False
    ws1.merge_cells('A1:I1'); ws1.row_dimensions[1].height = 26
    c = ws1['A1']
    c.value = 'PROPERTY AND RENT CONSULT — UTILITY PAYMENT TRACKER — TENANT REGISTER'
    c.fill = fill(DB_H); c.font = font('#FFFFFF', True, 11); c.alignment = center()

    cols1 = ['Unit','Tenant Name','Phone','Tenancy Start','Electricity (GHS)','Water (GHS)','Service Charge (GHS)','Monthly Total','Notes']
    widths1 = [14,25,14,15,18,14,20,16,30]
    ws1.row_dimensions[2].height = 18
    for i,(col,w) in enumerate(zip(cols1,widths1),1):
        c = ws1.cell(row=2, column=i, value=col)
        c.fill = fill(DB_H); c.font = font('#FFFFFF', True, 9); c.alignment = center(); c.border = thin()
        ws1.column_dimensions[get_column_letter(i)].width = w

    for r in range(3, 33):
        bg = LB_H if r%2==0 else '#FFFFFF'
        for col in range(1,10):
            c = ws1.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin(); c.alignment = left(); c.font = font(sz=9)
            ws1.row_dimensions[r].height = 18
        # Monthly Total formula
        ws1.cell(r,8).value = f'=IF(E{r}="","",E{r}+F{r}+G{r})'
    ws1.freeze_panes = 'A3'

    # Sheet 2 — Payment Log
    ws2 = wb.create_sheet('Payment Log'); ws2.sheet_view.showGridLines = False
    ws2.merge_cells('A1:O1'); ws2.row_dimensions[1].height = 26
    c = ws2['A1']
    c.value = 'PAYMENT LOG'
    c.fill = fill(DB_H); c.font = font('#FFFFFF', True, 11); c.alignment = center()

    cols2 = ['Receipt No.','Period','Tenant Name','Unit','Electricity','Water','Service Charge','Total Due','Amount Paid','Balance','Status','Date Paid','Method','Received By','Notes']
    widths2 = [14,12,22,12,13,10,16,13,14,13,12,13,18,16,25]
    ws2.row_dimensions[2].height = 18
    for i,(col,w) in enumerate(zip(cols2,widths2),1):
        c = ws2.cell(row=2, column=i, value=col)
        c.fill = fill(DB_H); c.font = font('#FFFFFF', True, 9); c.alignment = center(); c.border = thin()
        ws2.column_dimensions[get_column_letter(i)].width = w

    for r in range(3, 53):
        bg = OW_H if r%2==0 else '#FFFFFF'
        for col in range(1,16):
            c = ws2.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin(); c.alignment = left(); c.font = font(sz=9)
            ws2.row_dimensions[r].height = 18
        ws2.cell(r,10).value = f'=IF(H{r}="","",H{r}-I{r})'

    # Conditional formatting on Status column (K = col 11)
    dv = DataValidation(type='list', formula1='"Paid,Unpaid,Partial"', allow_blank=True)
    ws2.add_data_validation(dv)
    for r in range(3,53): dv.add(ws2.cell(r,11))
    ws2.conditional_formatting.add('K3:K52', CellIsRule(operator='equal', formula=['"Paid"'],    fill=PatternFill('solid',fgColor='EAF3DE'), font=Font(color='3B6D11',bold=True)))
    ws2.conditional_formatting.add('K3:K52', CellIsRule(operator='equal', formula=['"Unpaid"'],  fill=PatternFill('solid',fgColor='FCEBEB'), font=Font(color='A32D2D',bold=True)))
    ws2.conditional_formatting.add('K3:K52', CellIsRule(operator='equal', formula=['"Partial"'], fill=PatternFill('solid',fgColor='FAEEDA'), font=Font(color='854F0B',bold=True)))
    ws2.freeze_panes = 'A3'

    # Sheet 3 — Monthly Summary
    ws3 = wb.create_sheet('Monthly Summary'); ws3.sheet_view.showGridLines = False
    ws3.merge_cells('A1:H1'); ws3.row_dimensions[1].height = 26
    c = ws3['A1']; c.value = 'MONTHLY SUMMARY'
    c.fill = fill(SB_H); c.font = font('#FFFFFF', True, 11); c.alignment = center()

    ws3.merge_cells('A2:H2'); ws3.row_dimensions[2].height = 22
    note = ws3['A2']
    note.value = 'This sheet is for manual summary entry. Export full data from the PRC Utility Tracker app and paste values here as a cross-device backup record.'
    note.font = Font(name='Calibri', size=9, italic=True, color='63645A')
    note.alignment = Alignment(wrap_text=True, horizontal='left', vertical='center')

    cols3 = ['Period','Total Tenants','Total Expected (GHS)','Total Collected (GHS)','Outstanding (GHS)','Paid Count','Unpaid Count','Notes']
    widths3 = [14,15,22,22,18,13,14,30]
    ws3.row_dimensions[3].height = 18
    for i,(col,w) in enumerate(zip(cols3,widths3),1):
        c = ws3.cell(row=3, column=i, value=col)
        c.fill = fill(SB_H); c.font = font('#FFFFFF', True, 9); c.alignment = center(); c.border = thin()
        ws3.column_dimensions[get_column_letter(i)].width = w

    for r in range(4,24):
        bg = LB_H if r%2==0 else '#FFFFFF'
        for col in range(1,9):
            c = ws3.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin(); c.alignment = left(); c.font = font(sz=9)
            ws3.row_dimensions[r].height = 18
    ws3.freeze_panes = 'A4'

    path = os.path.join(BASE, 'Agency_Tier', 'PRC-Utility-Tracker-Backup-Template.xlsx')
    wb.save(path)
    print(f'Excel: {path}')

build_excel()

# ── WHATSAPP CARDS ────────────────────────────────────────────────────────────
def gf(size, bold=False):
    paths = [
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
        r'C:\Windows\Fonts\calibrib.ttf' if bold else r'C:\Windows\Fonts\calibri.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def ctext(draw, text, y, W, fnt, color=WH):
    bb = draw.textbbox((0,0), text, font=fnt)
    x = (W - (bb[2]-bb[0])) // 2
    draw.text((x, y), text, font=fnt, fill=color)

W2, H2 = 1080, 1350

# Card 1 — Cover
img = Image.new('RGB', (W2,H2), DB)
draw = ImageDraw.Draw(img)
draw.text((60,60), 'PROPERTY AND RENT CONSULT', font=gf(30,False), fill=OW)
ctext(draw, 'Utility Payment', 260, W2, gf(72,True))
ctext(draw, 'Tracker', 350, W2, gf(72,True))
# Ghana Edition pill
pill_w, pill_h = 320, 60
pill_x = (W2-pill_w)//2
draw.rounded_rectangle([(pill_x,440),(pill_x+pill_w,440+pill_h)], radius=30, fill=SB)
ctext(draw, 'Ghana Edition', 452, W2, gf(32,True))
draw.rectangle([(0,H2-120),(W2,H2)], fill=SB)
ctext(draw, 'Know who has paid. Know who hasn\'t.', H2-80, W2, gf(30,True))
img.save(os.path.join(BASE,'Agency_Tier','PRC-Tracker-Card-1.png'), dpi=(96,96))
print('Card 1')

# Card 2 — Problem
img = Image.new('RGB', (W2,H2), WH)
draw = ImageDraw.Draw(img)
draw.rectangle([(0,0),(W2,160)], fill=DB)
ctext(draw, 'THE PROBLEM WITH', 30, W2, gf(46,True))
ctext(draw, 'MANUAL TRACKING', 88, W2, gf(46,True))
problems = [
    ('📋', 'Receipts get lost\nor never issued'),
    ('❓', 'Can\'t remember who\npaid last month'),
    ('⏱', 'Chasing payments\ntakes too long'),
]
y = 220
for icon, text in problems:
    draw.rectangle([(80,y),(W2-80,y+260)], fill=OW)
    draw.text((120,y+30), icon, font=gf(60), fill=DB)
    lines = text.split('\n')
    ty = y+110
    for line in lines:
        draw.text((120,ty), line, font=gf(38,True), fill=DB)
        ty += 50
    y += 290
draw.rectangle([(0,H2-120),(W2,H2)], fill=LB)
ctext(draw, 'There is a better way.', H2-80, W2, gf(36,False), SB)
img.save(os.path.join(BASE,'Agency_Tier','PRC-Tracker-Card-2.png'), dpi=(96,96))
print('Card 2')

# Card 3 — Features
img = Image.new('RGB', (W2,H2), OW)
draw = ImageDraw.Draw(img)
draw.rectangle([(0,0),(W2,140)], fill=SB)
ctext(draw, 'WHAT THE TRACKER DOES', 50, W2, gf(48,True))
features = [
    'Track electricity, water\n& service charge',
    'Unlimited tenants\nand units',
    'Instant payment\nreceipts',
    'Full payment\nhistory',
    'Offline — no internet\nneeded',
    'Works on phone\nand computer',
]
x_starts = [60, 560]
y = 180
for i, feat in enumerate(features):
    col = i % 2
    row = i // 2
    x = x_starts[col]
    fy = y + row * 240
    draw.rounded_rectangle([(x,fy),(x+440,fy+210)], radius=12, fill=WH)
    draw.text((x+20, fy+20), '✓', font=gf(44,True), fill=SB)
    lines = feat.split('\n')
    ty = fy+22
    for line in lines:
        draw.text((x+80, ty), line, font=gf(30,True), fill=DB)
        ty += 42
draw.rectangle([(0,H2-100),(W2,H2)], fill=DB)
ctext(draw, 'Property and Rent Consult', H2-65, W2, gf(28,False))
img.save(os.path.join(BASE,'Agency_Tier','PRC-Tracker-Card-3.png'), dpi=(96,96))
print('Card 3')

# Card 4 — Receipt Preview
img = Image.new('RGB', (W2,H2), WH)
draw = ImageDraw.Draw(img)
ctext(draw, 'EVERY PAYMENT.', 80, W2, gf(58,True), DB)
ctext(draw, 'A RECEIPT.', 150, W2, gf(58,True), DB)
# Receipt mockup
rx, ry, rw, rh = 120, 260, W2-240, 760
draw.rounded_rectangle([(rx,ry),(rx+rw,ry+rh)], radius=16, fill=WH, outline=DB, width=2)
draw.rounded_rectangle([(rx,ry),(rx+rw,ry+80)], radius=16, fill=DB)
ctext(draw, 'PAYMENT RECEIPT', ry+25, W2, gf(34,True))
lines = [
    ('Tenant', 'Akosua Mensah'),('Unit','Flat 2A'),
    ('Period','June 2026'),('Electricity','GHS 85.00'),
    ('Water','GHS 25.00'),('Svc Charge','GHS 30.00'),
    ('Total Due','GHS 140.00'),('Amount Paid','GHS 140.00'),
]
ly = ry+110
for label, val in lines:
    draw.text((rx+30, ly), label, font=gf(24,False), fill=WG)
    draw.text((rx+rw-200, ly), val, font=gf(24,True), fill=DB)
    ly += 72
    draw.line([(rx+20,ly-20),(rx+rw-20,ly-20)], fill=LB, width=1)
# PAID stamp
stamp_x, stamp_y = rx+rw-180, ry+rh-110
draw.rounded_rectangle([(stamp_x,stamp_y),(stamp_x+140,stamp_y+60)], radius=8, fill=(45,122,58))
ctext_local_x = stamp_x + 70
bb = draw.textbbox((0,0),'PAID',font=gf(28,True))
draw.text((stamp_x+(140-(bb[2]-bb[0]))//2, stamp_y+12), 'PAID', font=gf(28,True), fill=WH)
ctext(draw, 'Professional. Numbered. Printable.', 1060, W2, gf(36,False), WG)
draw.rectangle([(0,H2-100),(W2,H2)], fill=DB)
ctext(draw, 'Property and Rent Consult', H2-65, W2, gf(28,False))
img.save(os.path.join(BASE,'Agency_Tier','PRC-Tracker-Card-4.png'), dpi=(96,96))
print('Card 4')

# Card 5 — CTA
img = Image.new('RGB', (W2,H2), DB)
draw = ImageDraw.Draw(img)
ctext(draw, 'GET THE TRACKER', 100, W2, gf(68,True))
tiers = [('BASIC','GHS 49','Up to 10 tenants'),('PRO','GHS 99','Unlimited tenants'),('AGENCY','GHS 179','Full bundle')]
y = 240
for tier, price, desc in tiers:
    draw.rounded_rectangle([(80,y),(W2-80,y+200)], radius=12, fill=WH)
    draw.text((120,y+24), tier, font=gf(38,True), fill=SB)
    draw.text((120,y+78), price, font=gf(52,True), fill=DB)
    draw.text((120,y+148), desc, font=gf(28,False), fill=WG)
    y += 220
draw.rounded_rectangle([(80,y+10),(W2-80,y+90)], radius=8, fill=SB)
ctext(draw, 'Available on Selar', y+30, W2, gf(34,True))
ctext(draw, 'Search: PRC Utility Tracker', y+74, W2, gf(28,False), OW)
ctext(draw, 'Property and Rent Consult  |  propertynrentconsult.com', H2-60, W2, gf(26,False), OW)
img.save(os.path.join(BASE,'Agency_Tier','PRC-Tracker-Card-5.png'), dpi=(96,96))
print('Card 5')

# ── README TXT ────────────────────────────────────────────────────────────────
readme_templates = {
    'Basic_Tier': """WHAT IS IN THIS PACKAGE
---------------------------------------------------------
  PRC-Utility-Tracker-Basic.html  -- The tracker app (up to 10 tenants)
  PRC-Utility-Tracker-User-Guide.pdf  -- Full user guide
  PRC-READ-ME-FIRST.txt  -- This file""",
    'Pro_Tier': """WHAT IS IN THIS PACKAGE
---------------------------------------------------------
  PRC-Utility-Tracker-Pro.html  -- The tracker app (unlimited tenants)
  PRC-Utility-Tracker-User-Guide.pdf  -- Full user guide
  PRC-READ-ME-FIRST.txt  -- This file""",
    'Agency_Tier': """WHAT IS IN THIS PACKAGE
---------------------------------------------------------
  PRC-Utility-Tracker-Pro.html  -- The tracker app (unlimited tenants)
  PRC-Utility-Tracker-User-Guide.pdf  -- Full user guide
  PRC-Utility-Tracker-Backup-Template.xlsx  -- Excel cross-device backup
  PRC-Tracker-Card-1.png through Card-5.png  -- WhatsApp image set
  PRC-READ-ME-FIRST.txt  -- This file"""
}
readme_common = """
HOW TO START
---------------------------------------------------------
1. Double-click the .html file. It opens in your browser.
2. Click the gear icon (top-right) and enter your property details.
3. Go to the Tenants tab and add your tenants.
4. Go to Billing, select the current month, and start recording payments.

Your data is saved automatically. No internet needed.

PRINTING RECEIPTS
---------------------------------------------------------
After recording a payment, click "Print / Save PDF" in the receipt window.
Choose "Save as PDF" in your browser's print dialog to save a PDF copy.

SUPPORT
---------------------------------------------------------
Read the full User Guide (PDF) for detailed instructions and FAQ.
For other queries, contact Property and Rent Consult at info@propertynrentconsult.com

TERMS OF USE
---------------------------------------------------------
Licensed for personal and internal business use only.
Do not resell, redistribute, or share this file.
(c) 2026 Property and Rent Consult. All rights reserved."""

for tier, what_inside in readme_templates.items():
    content = f"""
===============================================================
PROPERTY AND RENT CONSULT
PRC Utility Payment Tracker -- Ghana Edition
Thank you for your purchase.
===============================================================

{what_inside}
{readme_common}

===============================================================
"""
    with open(os.path.join(BASE, tier, 'PRC-READ-ME-FIRST.txt'), 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f'README: {tier}')

# ── SELAR LISTING ─────────────────────────────────────────────────────────────
selar_text = """SELAR LISTING COPY -- PRC UTILITY PAYMENT TRACKER
==========================================================================

LISTING 1 -- BASIC TIER
==========================================================================
Title: PRC Utility Payment Tracker -- Ghana Edition (Basic, up to 10 tenants)
Price: GHS 49.00

Short Description:
Track electricity, water, and service charge payments for up to 10 tenants --
generate numbered receipts instantly, see who has paid, runs offline on any device.

Full Description:
Do you know exactly which of your tenants paid their utilities last month?
Can you produce a receipt for a specific payment from three months ago in under a minute?

If not, the PRC Utility Payment Tracker is built for you.

This is a self-contained browser application -- a single file you open in Chrome,
Firefox, or any browser on your phone or computer. No installation. No subscription.
No internet required after download.

What it does:
+ Add up to 10 tenants with their unit, monthly electricity, water, and service charge amounts
+ Record payments month by month -- full payment, partial payment, or mark unpaid
+ Generate a numbered payment receipt (RCP-XXXXXXXX) for every transaction, instantly and automatically
+ Print or save receipts as PDF directly from your browser
+ View your full payment history -- searchable by tenant name, unit, status, or billing period
+ Dashboard shows total expected, collected, and outstanding for the current month
+ All data saved automatically on your device -- no cloud, no server, completely private

What is inside the download:
+ PRC-Utility-Tracker-Basic.html -- the tracker app (open in any browser)
+ PRC-Utility-Tracker-User-Guide.pdf -- 10-page illustrated user guide
+ PRC-READ-ME-FIRST.txt -- quick-start instructions

Under Ghanaian tenancy law (Rent Act, 1963 -- Act 220), landlords are required to issue receipts
for payments received. This tracker makes that requirement effortless for every utility payment.

Terms: Personal and internal business use only. Not for resale.
Produced by Property and Rent Consult.

==========================================================================
LISTING 2 -- PRO TIER
==========================================================================
Title: PRC Utility Payment Tracker -- Ghana Edition (Pro, unlimited tenants)
Price: GHS 99.00

Short Description:
Unlimited tenants, unlimited properties, full data export -- the complete utility payment
tracking system for property managers and growing portfolios.

Full Description:
Everything in the Basic tier, with no limits.

The Pro version removes the 10-tenant cap entirely and adds:
+ Unlimited tenants and units -- manage a 50-unit block or multiple properties in a single tracker
+ Property / Block field on each tenant -- organise tenants by building or property name
+ Export data button -- downloads all your tenants and payment records as a JSON file for backup
+ All features from Basic (receipts, history, dashboard, settings, print)

What is inside the download:
+ PRC-Utility-Tracker-Pro.html -- the full Pro tracker (no tenant limit)
+ PRC-Utility-Tracker-User-Guide.pdf -- 10-page illustrated user guide
+ PRC-READ-ME-FIRST.txt -- quick-start instructions

Produced by Property and Rent Consult.

==========================================================================
LISTING 3 -- AGENCY TIER
==========================================================================
Title: PRC Utility Payment Tracker -- Ghana Edition (Agency, Full Bundle)
Price: GHS 179.00

Short Description:
The complete utility tracker bundle for property management companies -- unlimited tenants,
Excel backup, WhatsApp image set, and the full Pro app.

Full Description:
Everything in Pro, plus three additional tools for property management teams.

What is added in Agency:
+ PRC-Utility-Tracker-Pro.html -- the full Pro tracker (unlimited tenants)
+ PRC-Utility-Tracker-Backup-Template.xlsx -- a three-sheet Excel workbook:
  Sheet 1 -- Tenant Register (all tenants and their amounts)
  Sheet 2 -- Payment Log (all payments with conditional colour coding: green/red/amber by status)
  Sheet 3 -- Monthly Summary (period-by-period collection overview)
+ WhatsApp Image Set -- 5 professionally designed 1080 x 1350px cards
+ PRC-Utility-Tracker-User-Guide.pdf -- full user guide
+ PRC-READ-ME-FIRST.txt -- quick-start instructions

Produced by Property and Rent Consult.

==========================================================================
WEBSITE BUTTON COPY
==========================================================================
Basic button:   Get Basic -- GHS 49
Pro button:     Get Pro -- GHS 99
Agency button:  Get Agency -- GHS 179
Trust line:     Secure payment via Selar, Mobile Money and Card accepted
Delivery:       Instant download after payment -- works offline on any device

==========================================================================
SELAR TAGS
==========================================================================
utility tracker Ghana, landlord tools Ghana, rent receipt Ghana, payment tracker
Ghana, electricity bill tracker, water bill tracker, service charge Ghana,
property management Ghana, receipt generator Ghana, offline tool Ghana,
property and rent consult, PRC Ghana, Act 220 receipt, tenant payment tracker,
Ghana landlord app, utility payment record Ghana
"""
selar_path = os.path.join(BASE, '..', 'Selar_Listing_Copy_Utility_Tracker.txt')
with open(selar_path, 'w', encoding='utf-8') as f:
    f.write(selar_text)
print(f'Selar listing saved')

# ── PRODUCT IMAGES ────────────────────────────────────────────────────────────
tiers_img = [
    ('BASIC','GHS 49','Up to 10 tenants\nPDF receipts + history','Basic_Tier','PRC-Tracker-Product-Image-Basic.png',(45,122,58)),
    ('PRO','GHS 99','Unlimited tenants\n+ Data export','Pro_Tier','PRC-Tracker-Product-Image-Pro.png',SB),
    ('AGENCY','GHS 179','Full bundle\nExcel + WhatsApp cards','Agency_Tier','PRC-Tracker-Product-Image-Agency.png',DB),
]
for label, price, desc, tier_folder, fname, badge_color in tiers_img:
    img = Image.new('RGB', (1080,1080), DB)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0,0),(1080,110)], fill=SB)
    ctext(draw, 'PROPERTY AND RENT CONSULT', 30, 1080, gf(30,True))
    draw.rounded_rectangle([(1080//2-140,130),(1080//2+140,210)], radius=30, fill=badge_color)
    ctext(draw, label, 143, 1080, gf(40,True))
    ctext(draw, 'UTILITY PAYMENT', 250, 1080, gf(52,True))
    ctext(draw, 'TRACKER', 318, 1080, gf(52,True))
    ctext(draw, price, 405, 1080, gf(72,True), WH)
    draw.line([(80,500),(1080-80,500)], fill=SB, width=2)
    y = 526
    for line in desc.split('\n'):
        draw.text((100, y), line, font=gf(30,False), fill=OW)
        y += 50
    draw.text((100,y+20), '✓ Instant numbered receipts', font=gf(28,False), fill=OW)
    draw.text((100,y+68), '✓ Offline — no internet needed', font=gf(28,False), fill=OW)
    draw.rectangle([(0,1080-100),(1080,1080)], fill=SB)
    ctext(draw, 'propertynrentconsult.com', 1080-68, 1080, gf(28,False))
    img.save(os.path.join(BASE, tier_folder, fname), dpi=(96,96))
    print(f'Product image: {fname}')

# ── ZIP FILES ─────────────────────────────────────────────────────────────────
for tier in ['Basic_Tier','Pro_Tier','Agency_Tier']:
    tier_path = os.path.join(BASE, tier)
    zip_name = f'PRC-Utility-Tracker-{tier.replace("_Tier","")}.zip'
    zip_path = os.path.join(BASE, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(tier_path):
            if not fname.endswith('.zip'):
                zf.write(os.path.join(tier_path, fname), fname)
    print(f'ZIP: {zip_path} ({os.path.getsize(zip_path):,} bytes)')

print('\nAll done.')
