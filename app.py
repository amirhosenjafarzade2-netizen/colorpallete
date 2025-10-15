import streamlit as st
import re
import random
import json
from colors import COLORS
from utils import generate_palette

# Cache palette generation
@st.cache_data
def cached_generate_palette(base_hex, style, num_colors, hue_shift=0.1, saturation_boost=0.5):
    try:
        return generate_palette(base_hex, style, num_colors, hue_shift, saturation_boost)
    except Exception as e:
        st.error(f"Palette generation failed: {str(e)}")
        return [base_hex]

# Validate hex code
def is_valid_hex(hex_str):
    return bool(re.match(r'^#[0-9A-Fa-f]{6}$', hex_str))

# Session state
if 'custom_colors' not in st.session_state:
    st.session_state.custom_colors = []
if 'saved_palettes' not in st.session_state:
    st.session_state.saved_palettes = []
if 'palette' not in st.session_state:
    st.session_state.palette = None
if 'show_library' not in st.session_state:
    st.session_state.show_library = False

all_colors = COLORS + st.session_state.custom_colors

# Custom CSS for enhanced visuals
st.markdown("""
<style>
.stApp { 
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4, #45B7D1);
    font-family: 'Arial', sans-serif;
}
.palette-box { 
    transition: all 0.3s ease; 
    box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
    border-radius: 10px; 
    text-align: center;
}
.copy-hex { 
    cursor: pointer; 
    background: rgba(255,255,255,0.8); 
    border: none; 
    padding: 5px 10px; 
    border-radius: 5px;
}
.hexagon { 
    clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
    width: 80px; 
    height: 80px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
}
.spiral { 
    border-radius: 50%;
}
.color-wheel { 
    position: relative; 
    width: 300px; 
    height: 300px; 
    margin: auto;
}
.cube-face { 
    transform-style: preserve-3d; 
    width: 100px; 
    height: 100px; 
    position: absolute;
}
.library-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); 
    gap: 10px; 
}
</style>
<script>
function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
    alert('Copied: ' + text);
}
</script>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Ultimate Color Palette", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>🌈 ULTIMATE 430+ COLOR PALETTE GENERATOR</h1>", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("Add Custom Color")
    custom_name = st.text_input("Name")
    custom_hex = st.color_picker("Color", "#FF6B6B")
    if st.button("Add"):
        if custom_name and is_valid_hex(custom_hex):
            st.session_state.custom_colors.append({'name': custom_name, 'hex': custom_hex.upper(), 'vibe': 'Custom', 'why_underrated': 'User Creation'})
            st.success(f"Added {custom_name}!")
        else:
            st.error("Please enter a valid hex code (#RRGGBB)")
    st.metric("Total Colors", len(all_colors))
    st.metric("Custom Colors", len(st.session_state.custom_colors))

# MAIN
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Select Base")
    base_options = {c['name']: c['hex'] for c in all_colors}
    selected_name = st.selectbox("Base Color", list(base_options.keys()))
    base_hex = base_options[selected_name]
    
    st.markdown(f"<div class='palette-box' style='background-color:{base_hex}; width:100%; height:80px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;'>{selected_name}</div>", unsafe_allow_html=True)
    
    style = st.selectbox("Style", [
        'random', 'complementary', 'analogous', 'triadic', 'monochrome', 'wes_anderson', 
        'warm', 'cool', 'pastel', 'vibrant', 'earth_tones', 'split_complementary', 
        'tetradic', 'square', 'gradient', 'shades', 'tints', 'tones', 'neutral', 
        'high_contrast', 'split_analogous', 'double_complementary', 'golden_ratio', 
        'random_harmony', 'biomimicry'
    ])
    num_colors = st.slider("Number of Colors", 3, 20, 5)
    hue_shift = st.slider("Hue Shift Range", 0.0, 1.0, 0.1, help="Controls hue variation")
    saturation_boost = st.slider("Saturation Boost", 0.0, 1.0, 0.5, help="Adjusts color intensity")
    display_style = st.selectbox("Display Style", [
        'rectangle_bars', 'hexagon_grid', 'spiral_swirl', 'mosaic_tiles', 'color_wheel', 
        '3d_cube', 'rainbow_arc', 'chevron', 'circles', 'squares', 
        'gradient_strip', 'zigzag', 'waves', 'dots', 'tiles'
    ])

if st.button("Generate Palette"):
    with st.spinner("Generating palette..."):
        try:
            palette = cached_generate_palette(base_hex, style, num_colors, hue_shift, saturation_boost)
            if not palette or len(palette) < num_colors:
                palette += random.sample([c['hex'] for c in COLORS], num_colors - len(palette))
                st.warning("Palette padded with random colors due to generation constraints.")
            st.session_state.palette = palette
        except Exception as e:
            st.error(f"Error generating palette: {str(e)}")
            st.session_state.palette = None

# Display generated palette
if st.session_state.palette:
    with col2:
        st.header(f"{style.replace('_', ' ').upper()} Palette")
        
        try:
            # Rectangle Bars
            if display_style == 'rectangle_bars':
                st.markdown("Rectangle Bars")
                cols = st.columns(len(st.session_state.palette))
                for i, color in enumerate(st.session_state.palette):
                    with cols[i]:
                        name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                        st.markdown(
                            f"<div class='palette-box' style='background:{color}; height:150px; text-align:center; color:white; padding:10px;'><b>{name}</b><br>{color}<br><button class='copy-hex' onclick='copyToClipboard(\"{color}\")'>Copy Hex</button></div>",
                            unsafe_allow_html=True
                        )
            
            # Hexagon Grid
            elif display_style == 'hexagon_grid':
                st.markdown("Hexagon Grid")
                cols = st.columns(5)
                for i, color in enumerate(st.session_state.palette):
                    with cols[i % 5]:
                        name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                        st.markdown(
                            f"<div class='hexagon palette-box' style='background:{color}; color:white;'><b>{name}</b><br>{color}</div>",
                            unsafe_allow_html=True
                        )
            
            # Spiral Swirl
            elif display_style == 'spiral_swirl':
                st.markdown("Spiral Swirl")
                html = "<div style='position:relative; width:300px; height:300px; margin:auto;'>"
                for i, color in enumerate(st.session_state.palette):
                    angle = i * 137.5  # Golden angle
                    radius = 20 * (i + 1) ** 0.5
                    x = 150 + radius * 0.5 * (i + 1) * 0.1 * (angle % 360)
                    y = 150 + radius * 0.5 * (i + 1) * 0.1 * (angle % 360)
                    name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                    html += f"<div class='palette-box spiral' style='background:{color}; width:50px; height:50px; position:absolute; left:{x}px; top:{y}px; color:white; text-align:center;'><b>{name}</b></div>"
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            
            # Mosaic Tiles
            elif display_style == 'mosaic_tiles':
                st.markdown("Mosaic Tiles")
                html = "<div style='display:grid; grid-template-columns: repeat(auto-fill, minmax(50px, 1fr)); gap:5px;'>"
                for i, color in enumerate(st.session_state.palette):
                    width = random.randint(50, 100)
                    height = random.randint(50, 100)
                    name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                    html += f"<div class='palette-box' style='background:{color}; width:{width}px; height:{height}px; color:white; padding:5px;'><b>{name}</b><br>{color}</div>"
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            
            # Color Wheel
            elif display_style == 'color_wheel':
                st.markdown("Color Wheel")
                html = "<div class='color-wheel'>"
                for i, color in enumerate(st.session_state.palette):
                    angle = i * (360 / len(st.session_state.palette))
                    x = 150 + 100 * (angle * 3.14159 / 180)
                    y = 150 + 100 * (angle * 3.14159 / 180)
                    name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                    html += f"<div class='palette-box' style='background:{color}; width:60px; height:60px; border-radius:50%; position:absolute; left:{x}px; top:{y}px; color:white; text-align:center;'><b>{name}</b></div>"
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            
            # 3D Cube
            elif display_style == '3d_cube':
                st.markdown("3D Cube")
                html = "<div style='perspective:1000px; width:200px; height:200px; margin:auto;'>"
                faces = min(len(st.session_state.palette), 6)
                for i in range(faces):
                    color = st.session_state.palette[i]
                    name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                    transform = {
                        0: "rotateY(0deg) translateZ(100px)",
                        1: "rotateY(90deg) translateZ(100px)",
                        2: "rotateY(180deg) translateZ(100px)",
                        3: "rotateY(-90deg) translateZ(100px)",
                        4: "rotateX(90deg) translateZ(100px)",
                        5: "rotateX(-90deg) translateZ(100px)"
                    }.get(i, "translateZ(100px)")
                    html += f"<div class='palette-box cube-face' style='background:{color}; width:100px; height:100px; position:absolute; transform:{transform}; color:white; display:flex; align-items:center; justify-content:center;'><b>{name}</b><br>{color}</div>"
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            
            # Fallback for other styles (e.g., rainbow_arc, chevron, etc.)
            else:
                st.markdown(f"{display_style.replace('_', ' ').title()}")
                cols = st.columns(len(st.session_state.palette))
                for i, color in enumerate(st.session_state.palette):
                    with cols[i]:
                        name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                        st.markdown(
                            f"<div class='palette-box' style='background:{color}; height:100px; text-align:center; color:white; padding:10px;'><b>{name}</b><br>{color}</div>",
                            unsafe_allow_html=True
                        )
            
            # Save palette
            if st.button("Save Palette"):
                st.session_state.saved_palettes.append(st.session_state.palette)
                st.success("Palette saved!")
            
            # Download palette
            palette_data = [{"name": next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated"), "hex": color} for color in st.session_state.palette]
            st.download_button("Download JSON", json.dumps(palette_data, indent=2), "palette.json")
            
            # Debug: Show raw palette
            st.write("Raw Palette Hex Codes:", st.session_state.palette)
        
        except Exception as e:
            st.error(f"Error displaying palette: {str(e)}")
            st.write("Raw Palette Hex Codes:", st.session_state.palette)

# DISPLAY SAVED PALETTES
if st.session_state.saved_palettes:
    st.header("Saved Palettes")
    for i, saved_palette in enumerate(st.session_state.saved_palettes):
        st.markdown(f"**Palette {i+1}**")
        cols = st.columns(len(saved_palette))
        for j, color in enumerate(saved_palette):
            with cols[j]:
                st.markdown(f"<div style='background:{color}; height:50px; border-radius:5px;'></div>", unsafe_allow_html=True)

# COLOR LIBRARY TOGGLE
if st.button("Toggle Color Library"):
    st.session_state.show_library = not st.session_state.show_library

if st.session_state.show_library:
    with st.expander("Color Library", expanded=True):
        st.markdown("**Color Library**")
        html = "<div class='library-grid'>"
        for color in all_colors:
            html += f"<div class='palette-box' style='background:{color['hex']}; padding:10px; color:white;'><b>{color['name']}</b><br>{color['hex']}<br>Vibe: {color['vibe']}<br>Why: {color['why_underrated']}</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
