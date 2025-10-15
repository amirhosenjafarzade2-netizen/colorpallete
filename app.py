import streamlit as st
from colors import COLORS
from utils import generate_palette
import json

# Session state
if 'custom_colors' not in st.session_state:
    st.session_state.custom_colors = []

all_colors = COLORS + st.session_state.custom_colors

st.set_page_config(page_title="Ultimate Color Palette", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF6B6B;'>🌈 ULTIMATE 230+ COLOR PALETTE GENERATOR</h1>", unsafe_allow_html=True)

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
        'warm', 'cool', 'pastel', 'vibrant', 'earth_tones', 'split_complementary', 'tetradic', 'square'
    ])
    num_colors = st.slider("Colors", 3, 12, 5)

if st.button("Generate Palette"):
    palette = generate_palette(base_hex, style, num_colors)
    
    with col2:
        st.header(f"{style.upper()} Palette")
        
        # RAINBOW ARC
        st.markdown("Rainbow Arc")
        arc_html = "<div style='display:flex; justify-content:center; gap:5px;'>"
        for i, color in enumerate(palette):
            angle = (i / len(palette)) * 360
            arc_html += f"<div style='width:40px; height:120px; background:linear-gradient({angle}deg, {color} 50%, white 50%); border-radius:20px 20px 0 0;'></div>"
        arc_html += "</div>"
        st.markdown(arc_html, unsafe_allow_html=True)
        
        # RECTANGLE BARS
        st.markdown("Color Bars")
        cols = st.columns(len(palette))
        for i, color in enumerate(palette):
            with cols[i]:
                name = next((c['name'] for c in all_colors if c['hex'] == color), "Generated")
                st.markdown(f"<div style='background:{color}; height:150px; border-radius:10px; text-align:center; color:white; padding:10px;'><b>{name}</b><br>{color}</div>", unsafe_allow_html=True)
        
        # DOWNLOAD
        palette_data = [{"name": name, "hex": color} for color in palette]
        st.download_button("Download JSON", json.dumps(palette_data, indent=2), "palette.json")

# LIBRARY
st.header("Color Library")
for color in all_colors:
    st.markdown(f"**{color['name']}** ({color['hex']}) - Vibe: {color['vibe']} - Why: {color['why_underrated']}")
    st.markdown(f"<div style='background:{color['hex']}; width:50px; height:20px; border-radius:50%; border:1px solid black;'></div>", unsafe_allow_html=True)
