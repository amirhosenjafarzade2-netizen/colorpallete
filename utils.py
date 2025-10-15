import colorsys
import random
from colors import COLORS

# WES ANDERSON INSPIRED HARD-CODED PALETTES (FROM SEARCH)
WES_PALETTES = [
    ['#E27505', '#9C1425', '#827B82', '#3B3332', '#CDC1BD'],  # Darjeeling
    ['#8D4D1E', '#A4755F', '#55332C', '#F4A701', '#5C1F00'],  # Fox
    ['#BFB17C', '#6A4021', '#D88A3B', '#849585'],  # Moonrise
    ['#390C1E', '#C41311', '#C6645F', '#854D65'],  # Grand Budapest
]

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hls(r, g, b)

def hsl_to_rgb(hsl):
    return tuple(int(x * 255) for x in colorsys.hls_to_rgb(*hsl))

def complementary_color(hex_color):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    comp_h = (hsl[0] + 0.5) % 1.0
    return rgb_to_hex(hsl_to_rgb((comp_h, hsl[1], hsl[2])))

def analogous_colors(hex_color, num=2):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    analogs = []
    for i in range(1, num + 1):
        for direction in [0.0833, -0.0833]:  # ±30°
            ana_h = (hsl[0] + i * direction) % 1.0
            analogs.append(rgb_to_hex(hsl_to_rgb((ana_h, hsl[1], hsl[2]))))
    return analogs[:num]

def triadic_colors(hex_color):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    tri1_h = (hsl[0] + 1/3) % 1.0
    tri2_h = (hsl[0] + 2/3) % 1.0
    return [
        rgb_to_hex(hsl_to_rgb((tri1_h, hsl[1], hsl[2]))),
        rgb_to_hex(hsl_to_rgb((tri2_h, hsl[1], hsl[2])))
    ]

def monochrome_colors(hex_color, num=4):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    monos = []
    for l in range(20, 90, 70 // num):  # Vary lightness
        mono_hsl = (hsl[0], hsl[1], l / 100.0)
        monos.append(rgb_to_hex(hsl_to_rgb(mono_hsl)))
    return monos

def wes_anderson_colors(base_hex, num=5):
    # Pick a random Wes palette and adjust to match base hue
    wes = random.choice(WES_PALETTES)
    rgb = hex_to_rgb(base_hex)
    base_hsl = rgb_to_hsl(rgb)
    adjusted = []
    for c in wes:
        c_rgb = hex_to_rgb(c)
        c_hsl = rgb_to_hsl(c_rgb)
        adj_hsl = (base_hsl[0], c_hsl[1] * 0.8, c_hsl[2] * 0.9)  # Pastel-ize
        adjusted.append(rgb_to_hex(hsl_to_rgb(adj_hsl)))
    return random.sample(adjusted, min(num, len(adjusted)))

def warm_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    warm_h = 0.0833  # Shift to orange/red
    warm = []
    for i in range(num):
        w_hsl = ((hsl[0] + warm_h) % 1.0, hsl[1], hsl[2] + i*0.05 - 0.1)
        warm.append(rgb_to_hex(hsl_to_rgb(w_hsl)))
    return warm

def cool_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    cool_h = 0.5  # Shift to blue/green
    cool = []
    for i in range(num):
        c_hsl = ((hsl[0] + cool_h) % 1.0, hsl[1] * 0.8, hsl[2] - i*0.05)
        cool.append(rgb_to_hex(hsl_to_rgb(c_hsl)))
    return cool

def pastel_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    pastels = []
    for i in range(num):
        p_hsl = (hsl[0], hsl[1] * 0.5, min(0.9, hsl[2] + 0.2 + i*0.05))
        pastels.append(rgb_to_hex(hsl_to_rgb(p_hsl)))
    return pastels

def vibrant_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    vibrants = []
    for i in range(num):
        v_hsl = (hsl[0], min(1.0, hsl[1] + 0.3), hsl[2])
        vibrants.append(rgb_to_hex(hsl_to_rgb(v_hsl)))
    return vibrants

def earth_tones(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    earth = []
    for i in range(num):
        e_hsl = (0.0833, hsl[1] * 0.4, hsl[2] * 0.6 + i*0.1 - 0.2)
        earth.append(rgb_to_hex(hsl_to_rgb(e_hsl)))
    return earth

def split_complementary_colors(hex_color, num=3):
    comp = complementary_color(hex_color)
    analogs = analogous_colors(comp)
    return [hex_color, comp] + analogs[:num-2]

def tetradic_colors(hex_color):
    comp = complementary_color(hex_color)
    tri1 = triadic_colors(hex_color)[0]
    tri2 = complementary_color(tri1)
    return [hex_color, comp, tri1, tri2]

def square_colors(hex_color):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    squares = []
    for i in [1,2,3]:
        s_h = (hsl[0] + i*0.25) % 1.0
        squares.append(rgb_to_hex(hsl_to_rgb((s_h, hsl[1], hsl[2]))))
    return [hex_color] + squares

# NEW: Gradient (smooth transitions from base to complement)
def gradient_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    gradients = []
    for i in range(num):
        g_hsl = (hsl[0], hsl[1], hsl[2] * (1 - i/(num*1.5)))
        gradients.append(rgb_to_hex(hsl_to_rgb(g_hsl)))
    return gradients

# NEW: Shades (darker variations)
def shades_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    shades = []
    for i in range(num):
        s_hsl = (hsl[0], hsl[1], max(0.1, hsl[2] - i*0.15))
        shades.append(rgb_to_hex(hsl_to_rgb(s_hsl)))
    return shades

# NEW: Tints (lighter variations)
def tints_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    tints = []
    for i in range(num):
        t_hsl = (hsl[0], hsl[1], min(0.95, hsl[2] + i*0.1))
        tints.append(rgb_to_hex(hsl_to_rgb(t_hsl)))
    return tints

# NEW: Tones (grayer, desaturated variations)
def tones_colors(hex_color, num=5):
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    tones = []
    for i in range(num):
        t_hsl = (hsl[0], max(0.2, hsl[1] - i*0.2), hsl[2])
        tones.append(rgb_to_hex(hsl_to_rgb(t_hsl)))
    return tones

# NEW: Neutral (desaturated complements for balance)
def neutral_colors(hex_color, num=5):
    comp = complementary_color(hex_color)
    rgb = hex_to_rgb(comp)
    hsl = rgb_to_hsl(rgb)
    neutrals = []
    for i in range(num):
        n_hsl = (hsl[0], hsl[1] * 0.3, hsl[2] * 0.7 + i*0.05)
        neutrals.append(rgb_to_hex(hsl_to_rgb(n_hsl)))
    return [hex_color] + neutrals[:num-1]

# NEW: High Contrast (optimized for accessibility, e.g., WCAG contrast)
def high_contrast_colors(hex_color, num=5):
    # Simple simulation: alternate light/dark with high saturation
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(rgb)
    contrasts = []
    for i in range(num):
        c_hsl = ((hsl[0] + i*0.1) % 1.0, min(1.0, hsl[1] + 0.2), 0.3 if i % 2 == 0 else 0.7)
        contrasts.append(rgb_to_hex(hsl_to_rgb(c_hsl)))
    return contrasts

def generate_palette(base_hex, style='random', num_colors=5):
    if style == 'random':
        return random.sample([c['hex'] for c in COLORS], min(num_colors, len(COLORS)))
    elif style == 'complementary':
        return [base_hex, complementary_color(base_hex)] + analogous_colors(base_hex, num_colors-2)
    elif style == 'analogous':
        return [base_hex] + analogous_colors(base_hex, num_colors-1)
    elif style == 'triadic':
        return [base_hex] + triadic_colors(base_hex) + analogous_colors(base_hex, num_colors-3)
    elif style == 'monochrome':
        return [base_hex] + monochrome_colors(base_hex, num_colors-1)
    elif style == 'wes_anderson':
        return wes_anderson_colors(base_hex, num_colors)
    elif style == 'warm':
        return warm_colors(base_hex, num_colors)
    elif style == 'cool':
        return cool_colors(base_hex, num_colors)
    elif style == 'pastel':
        return pastel_colors(base_hex, num_colors)
    elif style == 'vibrant':
        return vibrant_colors(base_hex, num_colors)
    elif style == 'earth_tones':
        return earth_tones(base_hex, num_colors)
    elif style == 'split_complementary':
        return split_complementary_colors(base_hex, num_colors)
    elif style == 'tetradic':
        return tetradic_colors(base_hex)[:num_colors]
    elif style == 'square':
        return square_colors(base_hex)[:num_colors]
    # NEW STYLES
    elif style == 'gradient':
        return gradient_colors(base_hex, num_colors)
    elif style == 'shades':
        return shades_colors(base_hex, num_colors)
    elif style == 'tints':
        return tints_colors(base_hex, num_colors)
    elif style == 'tones':
        return tones_colors(base_hex, num_colors)
    elif style == 'neutral':
        return neutral_colors(base_hex, num_colors)
    elif style == 'high_contrast':
        return high_contrast_colors(base_hex, num_colors)
    return [base_hex]
