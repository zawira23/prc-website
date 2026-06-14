import openpyxl
from openpyxl.styles import (PatternFill, Font, Alignment, Border, Side,
                              GradientFill)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles.differential import DifferentialStyle
import os, shutil

# Brand colours (ARGB)
DEEP_BROWN  = '36221C'
STEEL_BLUE  = '516984'
WARM_GREY   = '63645A'
OFF_WHITE   = 'F5EDE8'
LIGHT_BLUE  = 'E8EEF3'
WHITE       = 'FFFFFF'
GREEN       = '2D7A3A'
YELLOW_C    = 'C8A000'
ORANGE_C    = 'C86400'
RED_C       = 'C82020'
BLACK       = '000000'

def fill(hex_color): return PatternFill('solid', fgColor=hex_color)
def font(hex_color='000000', bold=False, size=10, name='Calibri'):
    return Font(name=name, bold=bold, color=hex_color, size=size)
def center(): return Alignment(horizontal='center', vertical='center', wrap_text=True)
def left(): return Alignment(horizontal='left', vertical='center', wrap_text=True)
def thin_border():
    s = Side(style='thin', color='AAAAAA')
    return Border(left=s, right=s, top=s, bottom=s)

def build_excel(path):
    wb = openpyxl.Workbook()

    # ── SHEET 1: SCORECARD ───────────────────────────────────────────────────
    ws = wb.active
    ws.title = 'Scorecard'
    ws.sheet_view.showGridLines = False

    # Column widths
    col_widths = {'A':14,'B':45,'C':22,'D':22,'E':12,'F':14,'G':22,'H':22}
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    def write(row, col, value, fg=None, fc=BLACK, bold=False, align=None, border=True, size=10):
        c = ws.cell(row=row, column=col, value=value)
        if fg: c.fill = fill(fg)
        c.font = font(fc, bold, size)
        c.alignment = align or left()
        if border: c.border = thin_border()
        return c

    # Row 1 — Brand header
    ws.merge_cells('A1:H1')
    ws.row_dimensions[1].height = 30
    c = ws['A1']
    c.value = 'PROPERTY AND RENT CONSULT'
    c.fill = fill(DEEP_BROWN)
    c.font = font(WHITE, True, 14)
    c.alignment = center()

    # Row 2 — Title
    ws.merge_cells('A2:H2')
    ws.row_dimensions[2].height = 22
    c = ws['A2']
    c.value = 'TENANT SCREENING CHECKLIST & SCORECARD — GHANA EDITION'
    c.fill = fill(STEEL_BLUE)
    c.font = font(WHITE, True, 11)
    c.alignment = center()

    # Row 3 spacer
    ws.row_dimensions[3].height = 8

    # Row 4 — Section 1 heading
    ws.merge_cells('A4:H4')
    ws.row_dimensions[4].height = 20
    c = ws['A4']
    c.value = 'SECTION 1 — MINIMUM REQUIREMENTS (GATE CHECK)'
    c.fill = fill(STEEL_BLUE)
    c.font = font(WHITE, True, 10)
    c.alignment = left()

    # Headers row 5
    ws.row_dimensions[5].height = 18
    for col, val in zip('ABCD', ['Ref','Criterion','Result (Pass/Fail)','Auto-Flag']):
        write(5, ord(col)-64, val, fg=DEEP_BROWN, fc=WHITE, bold=True, align=center())

    mr_items = [
        ('MR-01','Valid Ghana Card or Passport presented and verified'),
        ('MR-02','Applicant aged 21 years or above'),
        ('MR-03','Monthly income verified at 3x the monthly rent'),
        ('MR-04','No prior eviction record (self-declared + cross-checked)'),
        ('MR-05','Employed (min. 6 months continuous) OR verifiable business income'),
    ]
    dv_passfail = DataValidation(type='list', formula1='"Pass,Fail"', allow_blank=True)
    ws.add_data_validation(dv_passfail)

    for i, (ref, criterion) in enumerate(mr_items):
        r = 6 + i
        ws.row_dimensions[r].height = 22
        bg = OFF_WHITE if i % 2 == 0 else WHITE
        write(r, 1, ref, fg=bg)
        write(r, 2, criterion, fg=bg)
        c_result = ws.cell(row=r, column=3)
        c_result.fill = fill(bg)
        c_result.border = thin_border()
        c_result.alignment = center()
        dv_passfail.add(c_result)
        # Auto-flag formula in col D
        c_flag = ws.cell(row=r, column=4)
        c_flag.value = f'=IF(C{r}="Fail","STOP — REJECT","")'
        c_flag.font = font(RED_C, True, 9)
        c_flag.alignment = center()
        c_flag.border = thin_border()
        c_flag.fill = fill(bg)

    # Conditional formatting: red fill if Fail
    red_fill = PatternFill('solid', fgColor=RED_C)
    ws.conditional_formatting.add('C6:C10',
        FormulaRule(formula=['C6="Fail"'], fill=red_fill, font=Font(color=WHITE, bold=True)))

    # Row 11 spacer
    ws.row_dimensions[11].height = 8

    # Row 12 — Section 2 heading
    ws.merge_cells('A12:H12')
    ws.row_dimensions[12].height = 20
    c = ws['A12']
    c.value = 'SECTION 2 — SCORING CRITERIA (Maximum Score: 25)'
    c.fill = fill(STEEL_BLUE)
    c.font = font(WHITE, True, 10)
    c.alignment = left()

    # Row 13 — Score table headers
    ws.row_dimensions[13].height = 18
    score_headers = ['Criteria','0 pts description','3-4 pts description','5 pts description','SCORE (0-5)','Notes']
    for col, val in enumerate(score_headers, 1):
        write(13, col, val, fg=DEEP_BROWN, fc=WHITE, bold=True, align=center())

    criteria = [
        ('Employment Status','Unemployed','Permanent 6-24 months','Permanent >2 years'),
        ('Income-to-Rent Ratio','Income <2x rent','Between 2x and 2.5x rent','Income 3x or above'),
        ('Previous Landlord Reference','Declined/hostile/eviction','Good; ended by relocation','Excellent long-term reference'),
        ('Guarantor Quality','None offered or unverified','Verified stable employment','Professional/property owner'),
        ('Utility Bill Payment History','Frequent disconnections','Mostly on time','Consistent on-time payments'),
    ]
    dv_score = DataValidation(type='whole', operator='between', formula1='0', formula2='5', allow_blank=True)
    ws.add_data_validation(dv_score)

    score_cells = []
    for i, (name, d0, d34, d5) in enumerate(criteria):
        r = 14 + i
        ws.row_dimensions[r].height = 28
        bg = OFF_WHITE if i % 2 == 0 else WHITE
        write(r, 1, name, fg=bg, bold=True)
        write(r, 2, d0, fg=bg)
        write(r, 3, d34, fg=bg)
        write(r, 4, d5, fg=bg)
        sc = ws.cell(row=r, column=5)
        sc.fill = fill(bg)
        sc.border = thin_border()
        sc.alignment = center()
        dv_score.add(sc)
        score_cells.append(f'E{r}')
        write(r, 6, '', fg=bg)

    # Row 19 — Total score
    ws.row_dimensions[19].height = 22
    ws.merge_cells('A19:D19')
    c = ws['A19']
    c.value = 'TOTAL SCORE'
    c.fill = fill(DEEP_BROWN)
    c.font = font(WHITE, True, 11)
    c.alignment = center()
    total_cell = ws['E19']
    total_cell.value = '=SUM(E14:E18)'
    total_cell.font = font(BLACK, True, 12)
    total_cell.alignment = center()
    total_cell.border = thin_border()
    total_cell.fill = fill(WHITE)
    write(19, 6, '', fg=WHITE)

    # Conditional formatting on E19
    ws.conditional_formatting.add('E19', CellIsRule(operator='between', formula=['20','25'], fill=PatternFill('solid', fgColor=GREEN), font=Font(color=WHITE, bold=True)))
    ws.conditional_formatting.add('E19', CellIsRule(operator='between', formula=['15','19'], fill=PatternFill('solid', fgColor=YELLOW_C), font=Font(bold=True)))
    ws.conditional_formatting.add('E19', CellIsRule(operator='between', formula=['10','14'], fill=PatternFill('solid', fgColor=ORANGE_C), font=Font(color=WHITE, bold=True)))
    ws.conditional_formatting.add('E19', CellIsRule(operator='between', formula=['0','9'], fill=PatternFill('solid', fgColor=RED_C), font=Font(color=WHITE, bold=True)))

    # Row 20 — Risk category
    ws.row_dimensions[20].height = 22
    ws.merge_cells('A20:B20')
    c = ws['A20']
    c.value = 'RISK CATEGORY'
    c.fill = fill(STEEL_BLUE)
    c.font = font(WHITE, True, 10)
    c.alignment = center()
    ws.merge_cells('C20:F20')
    rc = ws['C20']
    rc.value = '=IF(E19>=20,"LOW RISK — APPROVE",IF(E19>=15,"MEDIUM RISK — LARGER DEPOSIT",IF(E19>=10,"HIGH RISK — 6 MONTHS UPFRONT","VERY HIGH RISK — REJECT")))'
    rc.font = font(DEEP_BROWN, True, 10)
    rc.alignment = center()
    rc.border = thin_border()
    rc.fill = fill(LIGHT_BLUE)

    # Row 21 spacer
    ws.row_dimensions[21].height = 8

    # Section 4 heading
    ws.merge_cells('A22:H22')
    ws.row_dimensions[22].height = 20
    c = ws['A22']
    c.value = 'SECTION 4 — VERIFICATION CHECKLIST'
    c.fill = fill(STEEL_BLUE)
    c.font = font(WHITE, True, 10)
    c.alignment = left()

    # Verification headers
    ws.row_dimensions[23].height = 18
    for col, val in enumerate(['Ref','Item','Status','Notes'], 1):
        write(23, col, val, fg=DEEP_BROWN, fc=WHITE, bold=True, align=center())

    vc_items = [
        ('VC-01','Called employer; confirmed position, start date, and salary'),
        ('VC-02','Spoke directly to previous landlord (not just WhatsApp); no red flags'),
        ('VC-03','Verified guarantor Ghana Card, address, and income (in person or video call)'),
        ('VC-04','Reviewed utility bills — name matches applicant; 3 months minimum reviewed'),
        ('VC-05','Conducted eviction/court record check via Rent Control or local network'),
    ]
    dv_status = DataValidation(type='list', formula1='"Done,Pending,N/A"', allow_blank=True)
    ws.add_data_validation(dv_status)
    for i, (ref, item) in enumerate(vc_items):
        r = 24 + i
        ws.row_dimensions[r].height = 22
        bg = OFF_WHITE if i % 2 == 0 else WHITE
        write(r, 1, ref, fg=bg)
        write(r, 2, item, fg=bg)
        sc = ws.cell(row=r, column=3)
        sc.fill = fill(bg)
        sc.border = thin_border()
        sc.alignment = center()
        dv_status.add(sc)
        write(r, 4, '', fg=bg)

    # Row 29 spacer
    ws.row_dimensions[29].height = 8

    # Section 5 — Final Decision
    ws.merge_cells('A30:H30')
    ws.row_dimensions[30].height = 20
    c = ws['A30']
    c.value = 'SECTION 5 — FINAL DECISION'
    c.fill = fill(DEEP_BROWN)
    c.font = font(WHITE, True, 10)
    c.alignment = left()

    fd_fields = [
        ('Property Address',''),('Applicant Full Name',''),('Application Date',''),
        ('Total Score','=E19'),('Risk Category','=C20'),
    ]
    dv_decision = DataValidation(type='list', formula1='"Approved,Conditionally Approved,Rejected"', allow_blank=True)
    ws.add_data_validation(dv_decision)

    for i, (label, formula) in enumerate(fd_fields):
        r = 31 + i
        ws.row_dimensions[r].height = 20
        write(r, 1, label, fg=OFF_WHITE if i%2==0 else WHITE, bold=True)
        vc = ws.cell(row=r, column=2)
        if formula.startswith('='): vc.value = formula
        vc.fill = fill(OFF_WHITE if i%2==0 else WHITE)
        vc.border = thin_border()
        vc.alignment = left()

    ws.row_dimensions[36].height = 20
    write(36, 1, 'DECISION', fg=STEEL_BLUE, fc=WHITE, bold=True)
    dc = ws.cell(row=36, column=2)
    dv_decision.add(dc)
    dc.border = thin_border()
    dc.fill = fill(LIGHT_BLUE)
    dc.alignment = center()
    dc.font = font(DEEP_BROWN, True, 11)

    # ── SHEET 2: REFERENCE LOG ───────────────────────────────────────────────
    ws2 = wb.create_sheet('Reference Log')
    ws2.sheet_view.showGridLines = False
    ref_headers = ['Date Called','Landlord Name','Phone','Property Previously Rented',
                   'Rent Paid on Time (Y/N)','Damage (Y/N)','Re-let Again (Y/N)','Notes']
    ref_widths  = [16, 25, 16, 35, 22, 14, 18, 40]
    for i, (h, w) in enumerate(zip(ref_headers, ref_widths), 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
        c = ws2.cell(row=1, column=i, value=h)
        c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 10)
        c.alignment = center(); c.border = thin_border()
    for r in range(2, 22):
        bg = LIGHT_BLUE if r % 2 == 0 else WHITE
        for col in range(1, 9):
            c = ws2.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin_border()
            ws2.row_dimensions[r].height = 18

    # ── SHEET 3: GUARANTOR RECORD ────────────────────────────────────────────
    ws3 = wb.create_sheet('Guarantor Record')
    ws3.sheet_view.showGridLines = False
    g_headers = ['Guarantor Name','Ghana Card No.','Address','Employer',
                 'Monthly Income (GHS)','Verified By','Date Verified','Document Received (Y/N)']
    g_widths   = [25, 20, 35, 25, 22, 20, 18, 24]
    for i, (h, w) in enumerate(zip(g_headers, g_widths), 1):
        ws3.column_dimensions[get_column_letter(i)].width = w
        c = ws3.cell(row=1, column=i, value=h)
        c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 10)
        c.alignment = center(); c.border = thin_border()
    for r in range(2, 22):
        bg = LIGHT_BLUE if r % 2 == 0 else WHITE
        for col in range(1, 9):
            c = ws3.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin_border()
            ws3.row_dimensions[r].height = 18

    # ── SHEET 4: APPLICANT HISTORY ───────────────────────────────────────────
    ws4 = wb.create_sheet('Applicant History')
    ws4.sheet_view.showGridLines = False
    a_headers = ['Application Date','Applicant Name','Property Applied For',
                 'Total Score','Risk Category','Decision','Deposit Collected (GHS)','Notes']
    a_widths   = [18, 25, 35, 14, 25, 25, 22, 35]
    for i, (h, w) in enumerate(zip(a_headers, a_widths), 1):
        ws4.column_dimensions[get_column_letter(i)].width = w
        c = ws4.cell(row=1, column=i, value=h)
        c.fill = fill(DEEP_BROWN); c.font = font(WHITE, True, 10)
        c.alignment = center(); c.border = thin_border()
    for r in range(2, 22):
        bg = LIGHT_BLUE if r % 2 == 0 else WHITE
        for col in range(1, 9):
            c = ws4.cell(row=r, column=col)
            c.fill = fill(bg); c.border = thin_border()
            ws4.row_dimensions[r].height = 18

    wb.save(path)
    print(f'Excel saved: {path}')

base = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs'
for tier in ['Pro_Tier', 'Agency_Tier']:
    build_excel(os.path.join(base, tier, 'PRC-Tenant-Scorecard-Excel.xlsx'))
print('All Excel files done.')
