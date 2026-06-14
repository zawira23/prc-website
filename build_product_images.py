from PIL import Image, ImageDraw, ImageFont
import os, zipfile

BASE = r'C:\Users\USER\Documents\PROPERTY AND RENT CONSULT\outputs'
DEEP_BROWN  = (54,  34,  28)
STEEL_BLUE  = (81, 105, 132)
WARM_GREY   = (99, 100, 90)
OFF_WHITE   = (245, 237, 232)
LIGHT_BLUE  = (232, 238, 243)
WHITE       = (255, 255, 255)

def get_font(size, bold=False):
    paths = [
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
        r'C:\Windows\Fonts\calibrib.ttf' if bold else r'C:\Windows\Fonts\calibri.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def centered(draw, text, y, W, font, color=WHITE):
    bb = draw.textbbox((0,0), text, font=font)
    x = (W - (bb[2]-bb[0])) // 2
    draw.text((x, y), text, font=font, fill=color)

def make_product_image(label, price, tag_color, out_path):
    W = H = 1080
    img = Image.new('RGB', (W, H), DEEP_BROWN)
    draw = ImageDraw.Draw(img)

    # Top brand stripe
    draw.rectangle([(0,0),(W,120)], fill=STEEL_BLUE)
    centered(draw, 'PROPERTY AND RENT CONSULT', 38, W, get_font(34, True))

    # Main content area
    centered(draw, 'TENANT SCREENING', 200, W, get_font(70, True))
    centered(draw, 'CHECKLIST &', 288, W, get_font(70, True))
    centered(draw, 'SCORECARD', 376, W, get_font(70, True))
    centered(draw, 'Ghana Edition', 480, W, get_font(44, False), OFF_WHITE)

    # Tier badge
    draw.rectangle([(140, 570),(W-140, 680)], fill=tag_color)
    centered(draw, label, 595, W, get_font(52, True))

    # Price
    centered(draw, price, 720, W, get_font(62, True), WHITE)

    # What's inside
    centered(draw, 'Tenant Screening Kit', 840, W, get_font(34, False), OFF_WHITE)

    # Bottom stripe
    draw.rectangle([(0, H-100),(W, H)], fill=STEEL_BLUE)
    centered(draw, 'propertynrentconsult.com', H-68, W, get_font(28, False))

    img.save(out_path, dpi=(96,96))
    print(f'Product image saved: {out_path}')

# ── PRODUCT IMAGES ─────────────────────────────────────────────────────────────
tiers = [
    ('BASIC TIER',  'GHS 49.00',  (45,122,58),   'Basic_Tier',  'PRC-Product-Image-Basic.png'),
    ('PRO TIER',    'GHS 99.00',  (81,105,132),   'Pro_Tier',    'PRC-Product-Image-Pro.png'),
    ('AGENCY TIER', 'GHS 199.00', (54,34,28),     'Agency_Tier', 'PRC-Product-Image-Agency.png'),
]
for label, price, color, tier, fname in tiers:
    out = os.path.join(BASE, tier, fname)
    make_product_image(label, price, color, out)

# ── ZIP BUNDLES ────────────────────────────────────────────────────────────────
def zip_tier(tier_folder, zip_name):
    tier_path = os.path.join(BASE, tier_folder)
    zip_path  = os.path.join(BASE, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(tier_path):
            if fname.endswith(('.pdf','.xlsx','.docx','.png')) and 'Product-Image' not in fname:
                full = os.path.join(tier_path, fname)
                zf.write(full, fname)
                print(f'  + {fname}')
    size = os.path.getsize(zip_path)
    print(f'ZIP saved: {zip_path}  ({size:,} bytes)')

print('\n── Zipping Basic Tier ──')
zip_tier('Basic_Tier', 'PRC-Screening-Kit-Basic.zip')
print('\n── Zipping Pro Tier ──')
zip_tier('Pro_Tier',   'PRC-Screening-Kit-Pro.zip')
print('\n── Zipping Agency Tier ──')
zip_tier('Agency_Tier','PRC-Screening-Kit-Agency.zip')
print('\nAll done.')
