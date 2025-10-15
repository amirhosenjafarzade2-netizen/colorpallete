import streamlit as st
import re
import random
import json
import matplotlib.pyplot as plt
import numpy as np
from colors import COLORS
from utils import generate_palette

# Cache palette generation
@st.cache_data
def cached_generate_palette(base_hex, style, num_colors, hue_shift=0.1, saturation_boost=0.5):
    try:
        palette = generate_palette(base_hex, style, num_colors, hue_shift, saturation_boost)
        if not palette:
            raise ValueError("Empty palette returned")
        return palette
    except Exception as e:
        st.error(f"Palette generation failed: {str(e)}")
        return [base_hex]

# Validate hex code
def is_valid_hex(hex_str):
    return bool(re.match(r'^#[0-9A-Fa-f]{6}$', hex_str))

# Convert hex to RGB for Matplotlib
def hex_to_rgb_mpl(hex_str):
    try:
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    except Exception:
        return (1.0, 1.0, 1.0)  # Fallback to white

# Matplotlib rendering functions
def render_rainbow_arc(palette):
    try:
        fig, ax = plt.subplots(figsize=(6, 2))
        for i, color in enumerate(palette):
            ax.add_patch(plt.Rectangle((i * 0.2, 0), 0.2, 1, color=hex_to_rgb_mpl(color)))
            ax.text(i * 0.2 + 0.1, 0.5, color, ha='center', va='center', fontsize=8, color='white')
        ax.set_xlim(0, len(palette) * 0.2)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig
    except Exception as e:
        st.error(f"Rainbow arc rendering failed: {str(e)}")
        return None

def render_hexagon_grid(palette):
    try:
        fig, ax = plt.subplots(figsize=(6, 6))
        for i, color in enumerate(palette):
            row = i // 5
            col = i % 5
            hexagon = plt.Polygon([
                (col + 0.5, row + 0.866), (col + 1, row + 0.5), (col + 1, row),
                (col + 0.5, row - 0.866), (col, row - 0.5), (col, row)
            ], facecolor=hex_to_rgb_mpl(color))
            ax.add_patch(hexagon)
            ax.text(col + 0.5, row, color, ha='center', va='center', fontsize=6, color='white')
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-1, len(palette) // 5 + 1)
        ax.axis('off')
        return fig
    except Exception as e:
        st.error(f"Hexagon grid rendering failed: {str(e)}")
        return None

def render_spiral_swirl(palette):
    try:
        fig, ax = plt.subplots(figsize=(6, 6))
        for i, color in enumerate(palette):
            angle = i * 137.5 * np.pi / 180
            radius = 0.5 * np.sqrt(i + 1)
            x = 3 + radius * np.cos(angle)
            y = 3 + radius * np.sin(angle)
            ax.add_patch(plt.Circle((x, y), 0.3, color=hex_to_rgb_mpl(color)))
            ax.text(x, y, color, ha='center', va='center', fontsize=6, color='white')
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.axis('off')
        return fig
    except Exception as e:
        st.error(f"Spiral swirl rendering failed: {str(e)}")
        return None

def render_color_wheel(palette):
    try:
        fig, ax = plt.subplots(figsize=(6, 6))
        for i, color in enumerate(palette):
            angle = i * 2 * np.pi / len(palette)
            x = 3 + 2 * np.cos(angle)
            y = 3 + 2 * np.sin(angle)
            ax.add_patch(plt.Circle((x, y), 0.5, color=hex_to_rgb_mpl(color)))
            ax.text(x, y, color, ha='center', va='center', fontsize=6, color='white')
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.axis('off')
        return fig
    except Exception as e:
        st.error(f"Color wheel rendering failed: {str(e)}")
        return None

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

# Custom CSS for HTML-based styles
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
.library-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); 
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
        'rectangle_bars', 'hexagon_grid', 'spiral_swirl', 'color_wheel', 'rainbow_arc'
    ])

if st.button("Generate Palette"):
    with st.spinner("Generating palette..."):
        try:
            palette = cached_generate_palette(base_hex, style, num_colors, hue_shift, saturation_boost)
            if not palette or len(palette) < num_colors:
                palette += random.sample([c['hex'] for c in COLORS], num_colors - len(palette))
                st.warning("Palette padded with random colors due to generation constraints.")
            st.session_state.palette = palette
            st.session_state.display_style = display_style
            st.success("Palette generated successfully!")
        except Exception as e:
            st.error(f"Error generating palette: {str(e)}")
            st.session_state.palette = None

# Display generated palette
if st.session_state.palette:
    with col2:
        st.header(f"{style.replace('_', ' ').upper()} Palette")
        st.write(f"Selected Display Style: {st.session_state.display_style}")
        st.write(f"Palette Colors: {st.session_state.palette}")
        
        try:
            # Matplotlib-based styles
            if st.session_state.display_style in ['rainbow_arc', 'hexagon_grid', 'spiral_swirl', 'color_wheel']:
                fig = None
                if st.session_state.display_style == 'rainbow_arc':
                    fig = render_rainbow_arc(st.session_state.palette)
                elif st.session_state.display_style == 'hexagon_grid':
                    fig = render_hexagon_grid(st.session_state.palette)
                elif st.session_state.display_style == 'spiral_swirl':
                    fig = render_spiral_swirl(st.session_state.palette)
                elif st.session_state.display_style == 'color_wheel':
                    fig = render_color_wheel(st.session_state.palette)
                
                if fig:
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.error(f"Failed to render {st.session_state.display_style}")
            
            # HTML-based style (default)
            else:
                st.markdown("Rectangle Bars")
                cols = st.columns(min(len(st.session_state.palette), 5))  # Limit columns for layout
                for i, color in enumerate(st.session_state.palette):
                    with cols[i % 5]:
                        name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                        st.markdown(
                            f"<div class='palette-box' style='background:{color}; height:120px; text-align:center; color:white; padding:10px;'><b>{name}</b><br>{color}<br><button class='copy-hex' onclick='copyToClipboard(\"{color}\")'>Copy Hex</button></div>",
                            unsafe_allow_html=True
                        )
            
            # Save palette
            if st.button("Save Palette"):
                st.session_state.saved_palettes.append(st.session_state.palette)
                st.success("Palette saved!")
            
            # Download palette
            palette_data = [{"name": next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated"), "hex": color} for color in st.session_state.palette]
            st.download_button("Download JSON", json.dumps(palette_data, indent=2), "palette.json")
        
        except Exception as e:
            st.error(f"Error displaying palette: {str(e)}")
            # Fallback text display
            st.markdown("**Fallback Display (Text)**")
            for i, color in enumerate(st.session_state.palette):
                name = next((c['name'] for c in all_colors if c['hex'].upper() == color.upper()), "Generated")
                st.write(f"Color {i+1}: {name} ({color})")

# DISPLAY SAVED PALETTES
if st.session_state.saved_palettes:
    st.header("Saved Palettes")
    for i, saved_palette in enumerate(st.session_state.saved_palettes):
        st.markdown(f"**Palette {i+1}**")
        cols = st.columns(min(len(saved_palette), 5))
        for j, color in enumerate(saved_palette):
            with cols[j % 5]:
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
