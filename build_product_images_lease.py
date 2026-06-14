from PIL import Image, ImageDraw, ImageFont
import os

LP = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Ghana_Lease_and_Scripts_Pack'
CS = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs\Product_Communication_Scripts'

DB = (54, 34, 28); SB = (81, 105, 132); LB = (232, 238, 243)
OW = (245, 237, 232); WH = (255, 255, 255); WG = (99, 100, 90)
GREEN = (45, 122, 58)

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

def ctext(draw, text, y, W, font, color=WH):
    bb = draw.textbbox((0, 0), text, font=font)
    x = (W - (bb[2] - bb[0])) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bb[3] - bb[1]

def make_lease_image(tier_label, price, badge_color, bullet_lines, out_path):
    W = H = 1080
    img = Image.new('RGB', (W, H), DB)
    draw = ImageDraw.Draw(img)

    # Top brand stripe
    draw.rectangle([(0, 0), (W, 110)], fill=SB)
    ctext(draw, 'PROPERTY AND RENT CONSULT', 30, W, gf(32, True))

    # Tier badge
    draw.rectangle([(W//2-140, 130), (W//2+140, 210)], fill=badge_color)
    ctext(draw, tier_label, 143, W, gf(40, True))

    # Product title
    ctext(draw, 'GHANA LEASE AGREEMENT', 240, W, gf(52, True))
    ctext(draw, 'TEMPLATE PACK', 308, W, gf(52, True))

    # Price
    ctext(draw, price, 395, W, gf(72, True), WH)

    # Divider line
    draw.line([(80, 490), (W-80, 490)], fill=SB, width=2)

    # Bullet contents
    y = 516
    for line in bullet_lines:
        draw.text((100, y), line, font=gf(30, False), fill=OW)
        y += 50

    # Bottom stripe
    draw.rectangle([(0, H-100), (W, H)], fill=SB)
    ctext(draw, 'propertynrentconsult.com', H-68, W, gf(28, False))

    img.save(out_path, dpi=(96, 96))
    print(f'Saved: {out_path}')


def make_scripts_image(tier_label, price, badge_color, bullet_lines, out_path):
    W = H = 1080
    img = Image.new('RGB', (W, H), DB)
    draw = ImageDraw.Draw(img)

    # Top brand stripe
    draw.rectangle([(0, 0), (W, 110)], fill=SB)
    ctext(draw, 'PROPERTY AND RENT CONSULT', 30, W, gf(32, True))

    # Tier badge
    draw.rectangle([(W//2-140, 130), (W//2+140, 210)], fill=badge_color)
    ctext(draw, tier_label, 143, W, gf(40, True))

    # Product title
    ctext(draw, 'LANDLORD COMMUNICATION', 240, W, gf(52, True))
    ctext(draw, 'SCRIPTS PACK', 308, W, gf(52, True))

    # Price
    ctext(draw, price, 395, W, gf(72, True), WH)

    # Divider
    draw.line([(80, 490), (W-80, 490)], fill=SB, width=2)

    # Contents
    y = 516
    for line in bullet_lines:
        draw.text((100, y), line, font=gf(30, False), fill=OW)
        y += 50

    # Bottom stripe
    draw.rectangle([(0, H-100), (W, H)], fill=SB)
    ctext(draw, 'propertynrentconsult.com', H-68, W, gf(28, False))

    img.save(out_path, dpi=(96, 96))
    print(f'Saved: {out_path}')


# ── LEASE PACK — 3 TIERS ─────────────────────────────────────────────────────

make_lease_image(
    'BASIC', 'GHS 49',
    GREEN,
    [
        '✓  Tenancy Offer Letter (DOCX)',
        '✓  Fixed-Term Residential Agreement',
        '     DOCX + PDF',
        '✓  Grounded in Act 220 & L.I. 369',
        '✓  Instant download after payment',
    ],
    f'{LP}/Basic_Tier/PRC-Lease-Pack-Product-Image-Basic.png'
)

make_lease_image(
    'PRO', 'GHS 99',
    SB,
    [
        '✓  Tenancy Offer Letter (DOCX)',
        '✓  Fixed-Term Residential (DOCX + PDF)',
        '✓  Month-to-Month Residential (DOCX + PDF)',
        '✓  Room Rental Agreement (DOCX + PDF)',
        '✓  All grounded in Act 220 & L.I. 369',
    ],
    f'{LP}/Pro_Tier/PRC-Lease-Pack-Product-Image-Pro.png'
)

make_lease_image(
    'AGENCY', 'GHS 199',
    (120, 60, 20),
    [
        '✓  Tenancy Offer Letter + 5 Agreements',
        '✓  Fixed-Term, M2M, Room, Commercial,',
        '     Kiosk/Container (DOCX + PDF each)',
        '✓  Excel Agreement Tracker (5 sheets)',
        '✓  5 Branded WhatsApp Cards',
    ],
    f'{LP}/Agency_Tier/PRC-Lease-Pack-Product-Image-Agency.png'
)

# ── SCRIPTS PACK — 2 TIERS ───────────────────────────────────────────────────

make_scripts_image(
    'BASIC', 'GHS 29',
    GREEN,
    [
        '✓  Script 1: Rent Reminder Notice',
        '✓  Script 2: Routine Inspection Notice',
        '',
        '     Each script includes:',
        '     Formal letter + WhatsApp version',
    ],
    f'{CS}/Basic_Tier/PRC-Scripts-Product-Image-Basic.png'
)

make_scripts_image(
    'PRO', 'GHS 49',
    SB,
    [
        '✓  Script 1: Rent Reminder Notice',
        '✓  Script 2: Routine Inspection Notice',
        '✓  Script 3: Eviction Warning Notice',
        '✓  Script 4: Tenancy Renewal Offer',
        '     All 4 scripts — formal + WhatsApp',
    ],
    f'{CS}/Pro_Tier/PRC-Scripts-Product-Image-Pro.png'
)

print('All product images done.')
