#!/usr/bin/env python3
"""THE WORLD - Tuesday 24 November 2026. One day of world news, one page.
Drawn entirely in code (Python + PIL). 44 date-checked stories, 8 regions:
6 illustrated leads + 38 briefs. Output: entry.png (JPEG bytes, <=1 MiB).
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W = H = 1024
PAPER = (246, 239, 221)
INK = (28, 30, 38)
RULE = (150, 30, 30)
PANEL = (255, 253, 246)
EDGE = (206, 194, 164)
MUTE = (96, 92, 80)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

REGIONS = {
    "NA": ("NORTH AMERICA", (37, 99, 235)),
    "EU": ("EUROPE", (124, 58, 237)),
    "ME": ("MIDDLE EAST", (217, 119, 6)),
    "AF": ("AFRICA", (5, 150, 105)),
    "SA": ("SOUTH ASIA", (220, 38, 38)),
    "EA": ("EAST ASIA", (219, 39, 119)),
    "SEA": ("SOUTHEAST ASIA", (8, 145, 178)),
    "OC": ("OCEANIA", (101, 163, 13)),
}

def wrap(text, font, width):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if d.textlength(t, font=font) <= width:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
    return lines

def text_block(x, y, text, font, width, fill=INK, leading=1.18, align="left"):
    for ln in wrap(text, font, width):
        if align == "center":
            d.text((x + (width - d.textlength(ln, font=font)) / 2, y), ln, font=font, fill=fill)
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * leading)
    return y

def chip(x, y, code, font):
    name, col = REGIONS[code]
    wdt = d.textlength(code, font=font) + 10
    d.rounded_rectangle([x, y, x + wdt, y + font.size + 5], 3, fill=col)
    d.text((x + 5, y + 2), code, font=font, fill=(255, 255, 255))
    return wdt

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 5], fill=RULE)
f_title = F(SERIF_B, 57)
t = "THE WORLD"
d.text(((W - d.textlength(t, font=f_title)) / 2, 10), t, font=f_title, fill=INK)
f_sub = F(SANS_B, 15.5)
left = "TUESDAY 24 NOVEMBER 2026"
right = "ONE DAY · ONE PAGE"
d.text((16, 76), left, font=f_sub, fill=RULE)
d.text((W - 16 - d.textlength(right, font=f_sub), 76), right, font=f_sub, fill=RULE)
mid = "44 date-checked stories · 8 regions"
d.text(((W - d.textlength(mid, font=f_sub)) / 2, 76), mid, font=f_sub, fill=INK)
d.line([14, 100, W - 14, 100], fill=INK, width=3)
d.line([14, 105, W - 14, 105], fill=INK, width=1)

# ---------------- lead illustrations ----------------
def ill_markets(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    for bx, bh in [(8, 46), (52, 70), (100, 38), (150, 82), (205, 55), (255, 74), (300, 44)]:
        d.rectangle([x + bx, y + h - bh, x + bx + 34, y + h], fill=(30, 48, 84))
        for wy in range(y + h - bh + 8, y + h - 8, 13):
            d.rectangle([x + bx + 7, wy, x + bx + 13, wy + 6], fill=(250, 204, 21))
    pts = [(x + 8, y + h - 26), (x + 70, y + h - 48), (x + 130, y + h - 40),
           (x + 190, y + h - 76), (x + 250, y + h - 66), (x + w - 14, y + 16)]
    d.line(pts, fill=(34, 197, 94), width=5)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(187, 247, 208))
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - 17, ay + 3), (ax - 4, ay + 15)], fill=(34, 197, 94))
    f = F(SANS_B, 15)
    d.text((x + 10, y + 8), "NIKKEI +4.5% · KOSPI +7.5%", font=f, fill=(187, 247, 208))

def ill_quake(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(252, 231, 196))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(176, 128, 84))
    d.polygon([(x + 30, y + h - 34), (x + 74, y + h - 62), (x + 118, y + h - 34)], fill=(120, 70, 40))
    d.rectangle([x + 44, y + h - 62, x + 104, y + h - 34], fill=(255, 251, 235))
    d.polygon([(x + 196, y + h - 30), (x + 238, y + h - 60), (x + 282, y + h - 30)], fill=(120, 70, 40))
    d.rectangle([x + 210, y + h - 58, x + 268, y + h - 30], fill=(254, 243, 226))
    d.line([x + 244, y + h - 58, x + 252, y + h - 30], fill=(120, 70, 40), width=3)
    crack = [(x + 6, y + h - 6), (x + 70, y + h - 12), (x + 118, y + h - 4),
            (x + 176, y + h - 14), (x + 238, y + h - 5), (x + w - 8, y + h - 12)]
    d.line(crack, fill=(69, 38, 20), width=4)
    d.ellipse([x + w - 64, y + 8, x + w - 14, y + 58], fill=RULE)
    f = F(SANS_B, 19)
    s = "M5.3"
    d.text((x + w - 39 - d.textlength(s, font=f) / 2, y + 23), s, font=f, fill=(255, 255, 255))
    f2 = F(SANS_B, 13)
    d.text((x + 10, y + 10), "07:02 · KOSHI PROVINCE", font=f2, fill=(120, 70, 40))

def ill_strike(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 28, 54))
    d.ellipse([x + w - 62, y + 12, x + w - 30, y + 44], fill=(226, 232, 240))
    d.ellipse([x + w - 52, y + 8, x + w - 24, y + 40], fill=(23, 28, 54))
    for sx, sy in [(30, 20), (90, 12), (150, 26), (210, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(203, 213, 225))
    base = y + h
    d.polygon([(x, base), (x, base - 38), (x + 60, base - 38), (x + 60, base)], fill=(10, 13, 30))
    d.polygon([(x + 70, base), (x + 70, base - 52), (x + 150, base - 52), (x + 150, base)], fill=(10, 13, 30))
    d.polygon([(x + 160, base), (x + 160, base - 30), (x + w, base - 30), (x + w, base)], fill=(10, 13, 30))
    for wx, wy in [(16, base - 26), (92, base - 40), (120, base - 22), (200, base - 20)]:
        d.rectangle([x + wx, wy, x + wx + 7, wy + 9], fill=(250, 204, 21))
    cx, cy = x + 218, y + 44
    for r, col in [(30, (249, 115, 22)), (21, (251, 146, 60)), (12, (254, 215, 170))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for dx, dy in [(-38, -14), (34, -20), (-8, -36), (22, 22), (-30, 18)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(251, 146, 60), width=3)
    d.ellipse([cx - 52, cy + 16, cx + 8, cy + 34], fill=(100, 116, 139))
    d.ellipse([cx - 30, cy + 8, cx + 26, cy + 28], fill=(120, 134, 155))

def ill_alert(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 225, 250))
    d.polygon([(x, y + h), (x, y + h - 26), (x + 110, y + h - 40), (x + 220, y + h - 24),
               (x + w, y + h - 38), (x + w, y + h)], fill=(21, 94, 60))
    jx, jy = x + 168, y + 44
    d.polygon([(jx - 66, jy + 8), (jx - 18, jy - 6), (jx + 44, jy - 2), (jx + 70, jy + 8),
               (jx + 40, jy + 14), (jx - 30, jy + 14)], fill=(51, 65, 85))
    d.polygon([(jx + 38, jy - 2), (jx + 56, jy - 22), (jx + 68, jy - 20), (jx + 58, jy + 2)], fill=(51, 65, 85))
    d.polygon([(jx - 52, jy + 10), (jx - 70, jy + 26), (jx - 56, jy + 27), (jx - 36, jy + 14)], fill=(51, 65, 85))
    for r in (18, 34, 50):
        d.arc([x + 36 - r, y + h - 46 - r, x + 36 + r, y + h - 46 + r], start=290, end=60, fill=RULE, width=3)
    d.ellipse([x + 31, y + h - 51, x + 41, y + h - 41], fill=RULE)
    f = F(SANS_B, 13)
    d.text((x + 10, y + 8), "ULLEUNG ISLAND · 07:52", font=f, fill=(30, 64, 110))

def ill_flood(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(203, 213, 225))
    d.polygon([(x, y + h), (x, y + 40), (x + 90, y + h)], fill=(100, 116, 139))
    d.polygon([(x + w, y + h), (x + w, y + 34), (x + w - 96, y + h)], fill=(100, 116, 139))
    d.polygon([(x, y + 40), (x + 22, y + 62), (x - 8, y + 64)], fill=(248, 250, 252))
    d.polygon([(x + w, y + 34), (x + w - 24, y + 58), (x + w + 6, y + 60)], fill=(248, 250, 252))
    d.polygon([(x + 60, y + h), (x + 130, y + h - 58), (x + 196, y + h - 44),
               (x + 250, y + h - 66), (x + w - 40, y + h)], fill=(146, 104, 66))
    d.polygon([(x + 84, y + h), (x + 150, y + h - 40), (x + 210, y + h - 30),
               (x + w - 70, y + h)], fill=(120, 84, 50))
    for rx in range(14, w - 10, 26):
        d.line([x + rx, y + 6, x + rx - 7, y + 24], fill=(100, 116, 139), width=2)
    hx, hy = x + w - 92, y + 26
    d.rounded_rectangle([hx, hy, hx + 44, hy + 16], 6, fill=(185, 28, 28))
    d.line([hx - 26, hy + 2, hx + 70, hy + 2], fill=(51, 65, 85), width=4)
    d.line([hx + 22, hy + 16, hx + 22, hy + 30], fill=(51, 65, 85), width=2)
    d.line([hx + 44, hy + 8, hx + 58, hy + 2], fill=(51, 65, 85), width=3)

def ill_travel(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 242, 254))
    d.ellipse([x + 16, y + 12, x + 52, y + 48], fill=(250, 204, 21))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(71, 85, 105))
    d.rectangle([x + 18, y + h - 64, x + 128, y + h - 30], fill=(148, 163, 184))
    d.rectangle([x + 60, y + 6, x + 76, y + h - 64], fill=(100, 116, 139))
    for i in range(4):
        d.rectangle([x + 28 + i * 24, y + h - 54, x + 40 + i * 24, y + h - 42], fill=(224, 242, 254))
    px, py = x + 218, y + 42
    d.polygon([(px - 62, py + 10), (px + 30, py - 6), (px + 66, py + 2), (px + 30, py + 12),
               (px - 40, py + 16)], fill=(30, 64, 175))
    d.polygon([(px + 22, py - 4), (px + 40, py - 24), (px + 52, py - 22), (px + 42, py + 2)], fill=(30, 64, 175))
    cols = [(239, 68, 68), (34, 197, 94), (59, 130, 246), (234, 179, 8), (168, 85, 247)]
    for i, col in enumerate(cols):
        qx = x + 168 + i * 26
        d.ellipse([qx, y + h - 52, qx + 11, y + h - 41], fill=(71, 50, 30))
        d.rectangle([qx + 1, y + h - 41, qx + 10, y + h - 28], fill=col)
    f = F(SANS_B, 14)
    d.text((x + 10, y + 8), "52,000 FLIGHTS TUESDAY", font=f, fill=(30, 64, 110))

# ---------------- lead panels ----------------
LEADS = [
    ("EA", ill_markets, "ASIA MARKETS ROCKET IN CHIP RALLY",
     "Tokyo +4.5%, Seoul +7.5% and Taiwan +9.1% as Jensen Huang's return to Nvidia revives the AI trade."),
    ("SA", ill_quake, "DAWN QUAKE SHAKES NEPAL",
     "A magnitude 5.3 quake hits Koshi province; tremors are felt across India, Bhutan, Bangladesh and China."),
    ("EU", ill_strike, "RUSSIAN STRIKE KILLS TWO IN ZAPORIZHZHIA",
     "An overnight attack wounds 22 people, including two children, in the frontline Ukrainian city."),
    ("EA", ill_alert, "SEOUL SOUNDS AIR ALERT OVER RUSSIAN JET",
     "An evacuation warning sounds for Ulleung Island as a Russian aircraft enters Korean airspace."),
    ("SA", ill_flood, "HIMALAYAN FLOOD LEAVES 100 MISSING",
     "A wall of mud tears down an Indian mountain valley; at least four die as the army searches."),
    ("NA", ill_travel, "AMERICA TAKES OFF FOR THANKSGIVING",
     "The FAA braces for its busiest holiday in 16 years: 81.5 million Americans on the move."),
]

PX, PY, PW, PH, GAP = 14, 108, 326, 210, 9
f_head = F(SANS_B, 16.5)
f_sum = F(SANS, 12)
f_tag = F(SANS_B, 10.5)
for i, (code, ill, head, summ) in enumerate(LEADS):
    x = PX + (i % 3) * (PW + GAP)
    y = PY + (i // 3) * (PH + GAP)
    d.rounded_rectangle([x, y, x + PW, y + PH], 6, fill=PANEL, outline=EDGE, width=1)
    ill(x + 5, y + 5, PW - 10, 94)
    ty = y + 102
    chip(x + 10, ty, code, f_tag)
    nm = REGIONS[code][0]
    d.text((x + 52, ty + 2), nm, font=f_tag, fill=MUTE)
    text_block(x + 10, ty + 18, head, f_head, PW - 20, leading=1.12)
    text_block(x + 10, ty + 58, summ, f_sum, PW - 20, leading=1.22)

# ---------------- timeline strip ----------------
TY0 = PY + 2 * PH + GAP + 8
d.line([14, TY0, W - 14, TY0], fill=INK, width=2)
f_tl = F(SANS_B, 11.5)
tl = ("THE DAY AROUND THE WORLD — 07:02 Kathmandu quake · 07:52 Seoul air alert · "
      "Tokyo markets leap 4.5% · Zaporizhzhia struck overnight · US Thanksgiving rush peaks")
text_block(14, TY0 + 5, tl, f_tl, W - 28, fill=RULE, leading=1.15)
d.line([14, TY0 + 34, W - 14, TY0 + 34], fill=INK, width=2)

# ---------------- briefs ----------------
BRIEFS = [
    ("NA", "Mexico will prosecute cartel boss 'El Chapo Isidro' at home, defying a US extradition bid"),
    ("NA", "FAA lifts ground stop at Chicago O'Hare after an air-traffic staffing snarl"),
    ("NA", "US lawmakers close ranks against Nvidia chief's return, pressing tighter China chip curbs"),
    ("NA", "Comedian roasts Trump at Toronto's journalists' dinner"),
    ("EU", "Ukraine says Neptune missiles struck a Russian drone plant in Rostov-on-Don"),
    ("EU", "EU loans for Ukraine will cost 55 billion euros in interest alone, a Commission paper shows"),
    ("EU", "Norway's supreme court voids oil licences in a landmark climate ruling"),
    ("EU", "France confirms a deadly bird-flu outbreak at a poultry farm"),
    ("EU", "Georgia plans a full ban on surrogacy over trafficking concerns"),
    ("EU", "Moldova survey finds voters backing the road to Europe"),
    ("EU", "Inter fall in seven-goal San Siro thriller as Tresoldi hits a hat-trick"),
    ("ME", "Israel arrests 10 after days of violent settler attacks in the West Bank"),
    ("ME", "Saudi-led strike on Hodeidah telecom building kills 10, Houthi media say"),
    ("ME", "UAE president takes call from Syria's al-Sharaa on deeper cooperation"),
    ("ME", "Drone attack wounds four security men in Syria's Suwayda countryside"),
    ("ME", "Gulf bourses slip as Saudi-Houthi clashes rattle investors"),
    ("ME", "Erdogan plans a first visit to Libya in 15 years"),
    ("AF", "Nigeria: governor orders probe as eight-year-old dies in Abia school collapse"),
    ("AF", "At least 24 civilians killed in South Sudan's Warrap state"),
    ("AF", "Ethiopia's central bank holds a $140m foreign-exchange auction"),
    ("AF", "Museveni accepts an invitation to visit Somalia after talks with Mohamud"),
    ("AF", "Sahel states restart dialogue with the West Africa bloc"),
    ("AF", "Kenya secures 293,600 Saudi job openings for its workers"),
    ("SA", "Bangladesh begins vaccinating 50 million children against typhoid"),
    ("SA", "Former MP Prajwal Revanna is sentenced to life in prison for rape"),
    ("SA", "India holds third place in the Asia Power Index; Modi ranked second leader"),
    ("SA", "New Saryu-Kamala Express train links Ayodhya with Janakpur in Nepal"),
    ("EA", "SoftBank to invest $2bn in Intel"),
    ("EA", "Japan creates a new government body on foreign-resident concerns"),
    ("EA", "Japan's factory activity quickens as manufacturing PMI climbs to 53.7"),
    ("EA", "Seoul seeks priority Qatari LNG cargoes as Hormuz shipping normalises"),
    ("SEA", "Philippine Senate opens plenary debates on the 2027 national budget"),
    ("SEA", "S&P tips the Philippines to be SE Asia's slowest-growing economy in 2026"),
    ("SEA", "SE Asia's AI data-centre boom faces Nvidia supply curbs"),
    ("SEA", "Jollibee plans 30 UK restaurants in a franchise expansion"),
    ("OC", "Severe heatwave warning issued for Queensland's Cape York Peninsula"),
    ("OC", "Australia to treat AI as a first-order foreign-policy challenge"),
    ("OC", "Australia rotate squad for Rugby League World Cup final vs New Zealand"),
]

BY0 = TY0 + 44
f_bh = F(SANS_B, 15)
d.text((14, BY0), "THE DAY IN BRIEF", font=f_bh, fill=INK)
d.text((14 + d.textlength("THE DAY IN BRIEF", font=f_bh) + 12, BY0 + 2),
       "38 more stories, numbered 1-38", font=F(SANS, 11.5), fill=MUTE)
# region key with counts
counts = {}
for c, _ill, _h, _s in LEADS:
    counts[c] = counts.get(c, 0) + 1
for c, _ in BRIEFS:
    counts[c] = counts.get(c, 0) + 1
kx = 14
f_key = F(SANS_B, 10.5)
for code in ["NA", "EU", "ME", "AF", "SA", "EA", "SEA", "OC"]:
    wdt = chip(kx, BY0 + 24, code, f_key)
    label = f"{REGIONS[code][0].title()} {counts[code]}"
    d.text((kx + wdt + 4, BY0 + 26), label, font=F(SANS, 10.5), fill=INK)
    kx += wdt + 8 + d.textlength(label, font=F(SANS, 10.5)) + 14

COLS = [BRIEFS[0:13], BRIEFS[13:26], BRIEFS[26:38]]
TOP = BY0 + 56
LIMIT = 986
for size in (11, 10.5, 10, 9.5):
    f_b = F(SANS, size)
    worst = 0
    for ci, col in enumerate(COLS):
        cy = TOP
        for j, (code, txt) in enumerate(col):
            lines = wrap(txt, f_b, PW - 60)
            cy += max(1, len(lines)) * int(size * 1.16) + 4
        worst = max(worst, cy)
    if worst <= LIMIT:
        break
f_bn = F(SANS_B, size)
for ci, col in enumerate(COLS):
    cx = 14 + ci * (PW + GAP)
    cy = TOP
    for j, (code, txt) in enumerate(col):
        num = (ci * 13 + j + 1) if ci < 2 else (26 + j + 1)
        d.text((cx, cy), f"{num}.", font=f_bn, fill=RULE)
        chip(cx + 24, cy, code, F(SANS_B, 9))
        cy = text_block(cx + 58, cy, txt, f_b, PW - 62, leading=1.16) + 4

# ---------------- footer ----------------
d.line([14, 990, W - 14, 990], fill=INK, width=2)
f_ft = F(SANS, 11)
foot = ("Every story on this page happened, or was first reported, on Tuesday 24 November 2026, "
        "checked against its source. Drawn in code - no photographs.")
text_block(14, 996, foot, f_ft, W - 28, fill=MUTE, align="center")

img.save("entry.png", format="JPEG", quality=90)
print("saved entry.png")
