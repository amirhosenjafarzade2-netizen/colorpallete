import streamlit as st
from colors import COLORS
from utils import generate_palette
import json

# Session state
if 'custom_colors' not in st.session_state:
    st.session_state.custom_colors = []

all_colors = COLORS + st.session_state.custom_colors

st.set_page_config(page_title="Ultimate Color Palette", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF6B6B;'>🌈 ULTIMATE 330+ COLOR PALETTE GENERATOR</h1>", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("Add Custom Color")
    custom_name = st.text_input("Name")
    custom_hex = st.color_picker("Color", "#FF6B6B")
    if st.button("Add"):
        if custom_name:
            st.session_state.custom_colors.append({'name': custom_name, 'hex': custom_hex.upper(), 'vibe': 'Custom', 'why_underrated': 'User Creation'})
            st.success(f"Added {custom_name}!")
    st.metric("Total Colors", len(all_colors))
    st.metric("Custom", len(st.session_state.custom_colors))

# MAIN
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Select Base")
    base_options = {c['name']: c['hex'] for c in all_colors}
    selected_name = st.selectbox("Base Color", list(base_options.keys()))
    base_hex = base_options[selected_name]
    
    st.markdown(f"<div style='background-color:{base_hex}; width:100%; height:80px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;'>{selected_name}</div>", unsafe_allow_html=True)
    
    style = st.selectbox("Style", [
        'random', 'complementary', 'analogous', 'triadic', 'monochrome', 'wes_anderson', 
        'warm', 'cool', 'pastel', 'vibrant', 'earth_tones', 'split_complementary', 'tetradic', 'square',
        'gradient', 'shades', 'tints', 'tones', 'neutral', 'high_contrast'  # NEW STYLES
    ])
    num_colors = st.slider("Colors", 3, 20, 5)  # Increased max to 20
    display_style = st.selectbox("Display Style", [
        'rainbow_arc', 'rectangle_bars', 'chevron', 'circles', 'squares', 
        'gradient_strip', 'zigzag', 'waves', 'dots', 'tiles'
    ])  # NEW: User chooses depiction

if st.button("Generate Palette"):
    palette = generate_palette(base_hex, style, num_colors)
    
    with col2:
        st.header(f"{style.upper()} Palette")
        
        # Render based on selected display style
        if display_style == 'rainbow_arc':
            st.markdown("Rainbow Arc")
            arc_html = "<div style='display:flex; justify-content:center; gap:5px;'>"
            for i, color in enumerate(palette):
                angle = (i / len(palette)) * 360
                arc_html += f"<div style='width:40px; height:120px; background:linear-gradient({angle}deg, {color} 50%, white 50%); border-radius:20px 20px 0 0;'></div>"
            arc_html += "</div>"
            st.markdown(arc_html, unsafe_allow_html=True)
        
        elif display_style == 'rectangle_bars':
            st.markdown("Color Bars")
            cols = st.columns(len(palette))
            for i, color in enumerate(palette):
                with cols[i]:
                    name = next((c['name'] for c in all_colors if c['hex'] == color), "Generated")
                    st.markdown(f"<div style='background:{color}; height:150px; border-radius:10px; text-align:center; color:white; padding:10px;'><b>{name}</b><br>{color}</div>", unsafe_allow_html=True)
        
        elif display_style == 'chevron':
            st.markdown("Chevron Pattern")
            chevron_html = "<div style='display:flex; flex-wrap:wrap; justify-content:center; gap:5px;'>"
            for i, color in enumerate(palette):
                chevron_html += f"<div style='width:0; height:0; border-left:30px solid transparent; border-right:30px solid transparent; border-bottom:60px solid {color}; transform:rotate({i*30}deg);'></div>"
            chevron_html += "</div>"
            st.markdown(chevron_html, unsafe_allow_html=True)
        
        elif display_style == 'circles':
            st.markdown("Circle Pattern")
            circle_html = "<div style='display:flex; justify-content:center; gap:10px;'>"
            for color in palette:
                circle_html += f"<div style='width:80px; height:80px; background:{color}; border-radius:50%;'></div>"
            circle_html += "</div>"
            st.markdown(circle_html, unsafe_allow_html=True)
        
        elif display_style == 'squares':
            st.markdown("Square Grid")
            square_html = "<div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(80px, 1fr)); gap:10px;'>"
            for color in palette:
                square_html += f"<div style='background:{color}; height:80px;'></div>"
            square_html += "</div>"
            st.markdown(square_html, unsafe_allow_html=True)
        
        elif display_style == 'gradient_strip':
            st.markdown("Gradient Strip")
            gradient_colors = ','.join(palette)
            gradient_html = f"<div style='width:100%; height:100px; background:linear-gradient(to right, {gradient_colors}); border-radius:10px;'></div>"
            st.markdown(gradient_html, unsafe_allow_html=True)
        
        elif display_style == 'zigzag':
            st.markdown("Zigzag Pattern")
            zigzag_html = "<div style='display:flex; flex-direction:column; align-items:center;'>"
            for i, color in enumerate(palette):
                direction = 'left' if i % 2 == 0 else 'right'
                zigzag_html += f"<div style='width:200px; height:20px; background:{color}; transform:translateX({'20px' if direction == 'right' else '-20px'});'></div>"
            zigzag_html += "</div>"
            st.markdown(zigzag_html, unsafe_allow_html=True)
        
        elif display_style == 'waves':
            st.markdown("Wave Pattern")
            wave_html = "<div style='display:flex; justify-content:center; gap:5px;'>"
            for i, color in enumerate(palette):
                wave_html += f"<div style='width:50px; height:100px; background:{color}; border-radius:50% 50% 0 0 / 100% 100% 0 0; transform:rotate({i*45}deg);'></div>"
            wave_html += "</div>"
            st.markdown(wave_html, unsafe_allow_html=True)
        
        elif display_style == 'dots':
            st.markdown("Dot Pattern")
            dot_html = "<div style='display:flex; flex-wrap:wrap; justify-content:center; gap:10px;'>"
            for color in palette:
                dot_html += f"<div style='width:40px; height:40px; background:{color}; border-radius:50%;'></div>"
            dot_html += "</div>"
            st.markdown(dot_html, unsafe_allow_html=True)
        
        elif display_style == 'tiles':
            st.markdown("Tile Mosaic")
            tile_html = "<div style='display:grid; grid-template-columns:repeat(auto-fit, minmax(60px, 1fr)); gap:5px;'>"
            for color in palette:
                tile_html += f"<div style='background:{color}; height:60px; border:1px solid #000;'></div>"
            tile_html += "</div>"
            st.markdown(tile_html, unsafe_allow_html=True)
        
        # DOWNLOAD
        palette_data = [{"name": next((c['name'] for c in all_colors if c['hex'] == color), "Generated"), "hex": color} for color in palette]
        st.download_button("Download JSON", json.dumps(palette_data, indent=2), "palette.json")

# LIBRARY
st.header("Color Library")
for color in all_colors:
    st.markdown(f"**{color['name']}** ({color['hex']}) - Vibe: {color['vibe']} - Why: {color['why_underrated']}")
    st.markdown(f"<div style='background:{color['hex']}; width:50px; height:20px; border-radius:50%; border:1px solid black;'></div>", unsafe_allow_html=True)
