from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1350
DEEP_BROWN  = (54,  34,  28)
STEEL_BLUE  = (81, 105, 132)
WARM_GREY   = (99, 100, 90)
OFF_WHITE   = (245, 237, 232)
LIGHT_BLUE  = (232, 238, 243)
WHITE       = (255, 255, 255)
GREEN       = (45, 122, 58)
YELLOW_C    = (200, 160, 0)
ORANGE_C    = (200, 100, 0)
RED_C       = (200, 32, 32)
BLACK       = (0, 0, 0)

def get_font(size, bold=False):
    paths = [
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
        r'C:\Windows\Fonts\Arial Bold.ttf' if bold else r'C:\Windows\Fonts\Arial.ttf',
        r'C:\Windows\Fonts\calibrib.ttf' if bold else r'C:\Windows\Fonts\calibri.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def draw_text_centered(draw, text, y, width, font, color=WHITE):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]

def draw_text_left(draw, text, x, y, font, color=BLACK):
    draw.text((x, y), text, font=font, fill=color)

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, line = [], ''
    for word in words:
        test = (line + ' ' + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def save_card(img, name):
    out = os.path.join(r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Agency_Tier', name)
    img.save(out, dpi=(96, 96))
    print(f'Saved: {out}')

# ── CARD 1: COVER ─────────────────────────────────────────────────────────────
img = Image.new('RGB', (W, H), DEEP_BROWN)
draw = ImageDraw.Draw(img)

f_small  = get_font(32, False)
f_medium = get_font(52, True)
f_large  = get_font(72, True)
f_xlarge = get_font(88, True)
f_tag    = get_font(28, False)

draw.text((60, 60), 'PRC', font=get_font(44, True), fill=WHITE)

draw_text_centered(draw, 'TENANT SCREENING', 280, W, f_xlarge, WHITE)
draw_text_centered(draw, 'CHECKLIST &', 380, W, f_xlarge, WHITE)
draw_text_centered(draw, 'SCORECARD', 480, W, f_xlarge, WHITE)
draw_text_centered(draw, 'Ghana Edition', 620, W, get_font(54, False), tuple(c+60 if c+60<=255 else 255 for c in STEEL_BLUE))
draw_text_centered(draw, 'Screen smarter. Rent safer.', 730, W, get_font(38, False), OFF_WHITE)

# Bottom strip
draw.rectangle([(0, H-120), (W, H)], fill=STEEL_BLUE)
draw_text_centered(draw, 'Property and Rent Consult  |  propertynrentconsult.com', H-75, W, get_font(28, False), WHITE)
save_card(img, 'PRC-WhatsApp-Card-1.png')

# ── CARD 2: GATE CHECKS ────────────────────────────────────────────────────────
img = Image.new('RGB', (W, H), WHITE)
draw = ImageDraw.Draw(img)

draw.rectangle([(0, 0), (W, 160)], fill=DEEP_BROWN)
draw_text_centered(draw, 'BEFORE YOU SCORE', 25, W, get_font(54, True), WHITE)
draw_text_centered(draw, '5 GATE CHECKS', 90, W, get_font(46, True), tuple(c+80 if c+80<=255 else 255 for c in STEEL_BLUE))

checks = [
    'Valid Ghana Card or Passport',
    'Age 21 or above',
    'Income at least 3x monthly rent',
    'No prior eviction record',
    '6+ months employment or business income',
]
y = 240
for check in checks:
    draw.rectangle([(60, y), (W-60, y+90)], fill=LIGHT_BLUE, outline=tuple(c-20 if c>=20 else 0 for c in LIGHT_BLUE), width=1)
    draw.text((80, y+20), '✓', font=get_font(44, True), fill=STEEL_BLUE)
    draw.text((145, y+22), check, font=get_font(34, True), fill=DEEP_BROWN)
    y += 108

draw.rectangle([(0, H-150), (W, H)], fill=RED_C)
draw_text_centered(draw, 'Fail any one → Reject.', H-115, W, get_font(36, True), WHITE)
draw_text_centered(draw, 'Do not proceed to scoring.', H-65, W, get_font(30, False), WHITE)
save_card(img, 'PRC-WhatsApp-Card-2.png')

# ── CARD 3: SCORING ────────────────────────────────────────────────────────────
img = Image.new('RGB', (W, H), LIGHT_BLUE)
draw = ImageDraw.Draw(img)

draw.rectangle([(0, 0), (W, 180)], fill=STEEL_BLUE)
draw_text_centered(draw, '5 CRITERIA.  25 POINTS.', 30, W, get_font(52, True), WHITE)
draw_text_centered(draw, 'ONE DECISION.', 100, W, get_font(52, True), WHITE)

criteria = [
    ('Employment Status',         '0 – 5 pts'),
    ('Income-to-Rent Ratio',      '0 – 5 pts'),
    ('Previous Landlord Reference','0 – 5 pts'),
    ('Guarantor Quality',         '0 – 5 pts'),
    ('Utility Bill Payment History','0 – 5 pts'),
]
y = 230
for name, pts in criteria:
    draw.rectangle([(60, y), (W-60, y+130)], fill=WHITE)
    draw.text((90, y+20), name, font=get_font(38, True), fill=DEEP_BROWN)
    draw.text((90, y+72), pts, font=get_font(34, False), fill=STEEL_BLUE)
    y += 148

draw.rectangle([(0, H-120), (W, H)], fill=DEEP_BROWN)
draw_text_centered(draw, 'Maximum Score: 25 Points', H-80, W, get_font(36, True), WHITE)
save_card(img, 'PRC-WhatsApp-Card-3.png')

# ── CARD 4: RISK CATEGORIES ────────────────────────────────────────────────────
img = Image.new('RGB', (W, H), WHITE)
draw = ImageDraw.Draw(img)

draw.rectangle([(0, 0), (W, 170)], fill=DEEP_BROWN)
draw_text_centered(draw, 'WHAT DOES THE SCORE MEAN?', 55, W, get_font(46, True), WHITE)

bands = [
    (GREEN,    '20 – 25 pts', 'LOW RISK',       'APPROVE'),
    (YELLOW_C, '15 – 19 pts', 'MEDIUM RISK',    'LARGER DEPOSIT'),
    (ORANGE_C, '10 – 14 pts', 'HIGH RISK',      '6 MONTHS UPFRONT'),
    (RED_C,    'Below 10',    'VERY HIGH RISK', 'REJECT'),
]
band_h = (H - 270) // 4
y = 180
for color, score, risk, action in bands:
    draw.rectangle([(0, y), (W, y+band_h)], fill=color)
    mid = y + band_h // 2
    draw_text_centered(draw, f'{score}   |   {risk}   |   {action}', mid - 28, W, get_font(38, True), WHITE)
    y += band_h + 4

save_card(img, 'PRC-WhatsApp-Card-4.png')

# ── CARD 5: CTA ────────────────────────────────────────────────────────────────
img = Image.new('RGB', (W, H), DEEP_BROWN)
draw = ImageDraw.Draw(img)

draw_text_centered(draw, 'GET THE FULL', 80, W, get_font(62, True), WHITE)
draw_text_centered(draw, 'TENANT SCREENING KIT', 160, W, get_font(54, True), WHITE)

tiers = [
    ('BASIC',  'GHS 49',  'Fillable PDF + Printable A4'),
    ('PRO',    'GHS 99',  '+ Excel Workbook + Word Doc'),
    ('AGENCY', 'GHS 199', '+ WhatsApp Cards + Full Bundle'),
]
y = 310
for tier, price, desc in tiers:
    draw.rectangle([(60, y), (W-60, y+170)], fill=WHITE)
    draw.text((90, y+18), tier, font=get_font(44, True), fill=STEEL_BLUE)
    draw.text((90, y+74), price, font=get_font(54, True), fill=DEEP_BROWN)
    draw.text((90, y+134), desc, font=get_font(28, False), fill=WARM_GREY)
    y += 188

draw.rectangle([(60, y+10), (W-60, y+90)], fill=STEEL_BLUE)
draw_text_centered(draw, 'Available on Selar  |  Search: PRC Screening Kit', y+32, W, get_font(30, True), WHITE)

draw_text_centered(draw, 'Property and Rent Consult', H-60, W, get_font(30, False), OFF_WHITE)
save_card(img, 'PRC-WhatsApp-Card-5.png')

print('All PNG cards done.')
