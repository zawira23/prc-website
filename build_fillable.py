import fitz  # PyMuPDF
import os, shutil

base = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs'

def build_fillable(src, dst):
    shutil.copy(src, dst)
    doc = fitz.open(dst)

    STEEL = (81/255, 105/255, 132/255)

    def add_text_field(page, rect, name, fontsize=9):
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = name
        widget.rect = fitz.Rect(rect)
        widget.text_fontsize = fontsize
        widget.fill_color = (0.97, 0.94, 0.91)
        widget.border_color = STEEL
        widget.border_width = 0.5
        page.add_widget(widget)

    def add_checkbox(page, rect, name):
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
        widget.field_name = name
        widget.rect = fitz.Rect(rect)
        widget.fill_color = (1, 1, 1)
        widget.border_color = STEEL
        widget.border_width = 0.8
        page.add_widget(widget)

    def add_dropdown(page, rect, name, choices):
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_COMBOBOX
        widget.field_name = name
        widget.rect = fitz.Rect(rect)
        widget.choice_values = choices
        widget.fill_color = (0.91, 0.94, 0.95)
        widget.border_color = STEEL
        widget.border_width = 0.5
        page.add_widget(widget)

    # Page 2 (index 1) — no fields needed
    # Page 3 (index 2) — MR checkboxes
    p3 = doc[2]
    y_starts = [207, 234, 261, 297, 324]
    for i, y in enumerate(y_starts):
        add_checkbox(p3, (433, y, 453, y+16), f'MR-0{i+1}-Pass')
        add_checkbox(p3, (468, y, 488, y+16), f'MR-0{i+1}-Fail')

    # Page 4 (index 3) — score fields
    p4 = doc[3]
    score_rows = [134, 161, 195, 222, 249]
    for i, y in enumerate(score_rows):
        add_text_field(p4, (430, y, 466, y+22), f'Score-{i+1}')
        add_text_field(p4, (468, y, 560, y+22), f'Notes-{i+1}')

    # Page 5 (index 4) — VC checkboxes
    p5 = doc[4]
    vc_rows = [320, 347, 374, 401, 428]
    for i, y in enumerate(vc_rows):
        add_checkbox(p5, (395, y, 415, y+16), f'VC-0{i+1}-Done')
        add_text_field(p5, (417, y, 480, y+22), f'VC-0{i+1}-Date')
        add_text_field(p5, (482, y, 560, y+22), f'VC-0{i+1}-Notes')

    # Page 6 (index 5) — Final decision fields
    p6 = doc[5]
    field_rows = [111, 134, 157, 180, 203, 226, 249, 272, 295]
    field_names = ['PropertyAddress','UnitApartment','ApplicantName','GhanaCardNumber',
                   'ApplicationDate','TotalScore','RiskCategory','DepositRequired','AdditionalConditions']
    for y, name in zip(field_rows, field_names):
        add_text_field(p6, (160, y, 545, y+18), name)

    add_checkbox(p6, (50, 355, 72, 377), 'Decision-Approved')
    add_checkbox(p6, (50, 385, 72, 407), 'Decision-Conditional')
    add_checkbox(p6, (50, 415, 72, 437), 'Decision-Rejected')

    add_dropdown(p6, (160, 249, 400, 267), 'RiskCategoryDropdown',
                 ['Low Risk','Medium Risk','High Risk','Very High Risk — Reject'])
    add_dropdown(p6, (160, 355, 400, 375), 'FinalDecisionDropdown',
                 ['Approved','Conditionally Approved','Rejected'])

    sig_rows = [475, 498, 521, 544]
    sig_names = ['SignatureManagerName','Signature','SignatureDate','StampCompany']
    for y, name in zip(sig_rows, sig_names):
        add_text_field(p6, (160, y, 545, y+18), name)

    doc.save(dst, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    print(f'Fillable PDF saved: {dst}')

base_out = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs'
for tier in ['Basic_Tier', 'Pro_Tier', 'Agency_Tier']:
    src = os.path.join(base_out, tier, 'PRC-Tenant-Scorecard-Printable.pdf')
    dst = os.path.join(base_out, tier, 'PRC-Tenant-Scorecard-Fillable.pdf')
    build_fillable(src, dst)

print('All fillable PDFs done.')
