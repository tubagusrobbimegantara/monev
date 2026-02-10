import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from matplotlib.backends.backend_pdf import PdfPages

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Visualisasi Monev",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk estetika
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #3498db;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    .stDownloadButton button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stDownloadButton button:hover {
        background-color: #2980b9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 Dashboard Visualisasi Monitoring & Evaluasi</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/3498db/ffffff?text=MONEV+Dashboard", use_container_width=True)
    
    # Credit section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        <p style='color: white; font-size: 0.85rem; margin: 0; text-align: center;'>
            <strong>👨‍💻 Developed by</strong><br>
            Tubagus Robbi Megantara
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Pilih Jenis Visualisasi")
    
    viz_type = st.selectbox(
        "Tipe Visualisasi",
        [
            "📡 Radar/Spider Chart",
            "📊 Bar Chart (Horizontal)",
            "📈 Bar Chart (Vertikal)",
            "📉 Histogram",
            "🥧 Pie Chart",
            "📊 Grouped Bar Chart",
            "📚 Stacked Bar Chart"
        ]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan Tampilan")
    
    # Pengaturan warna
    color_scheme = st.selectbox(
        "Skema Warna",
        ["Biru Profesional", "Hijau Natural", "Ungu Elegan", "Merah Dinamis", "Custom"]
    )
    
    if color_scheme == "Custom":
        custom_color = st.color_picker("Pilih Warna", "#3498db")
    
    # Pengaturan ukuran
    fig_width = st.slider("Lebar Gambar", 8, 20, 12)
    fig_height = st.slider("Tinggi Gambar", 6, 18, 8)
    dpi = st.slider("Resolusi (DPI)", 100, 300, 150)
    
    st.markdown("---")
    st.markdown("### 💾 Download Options")
    download_format = st.radio("Format File", ["PNG", "PDF", "SVG"])

# Fungsi untuk mendapatkan warna
def get_color_palette(scheme, custom=None):
    palettes = {
        "Biru Profesional": "#3498db",
        "Hijau Natural": "#16a085",
        "Ungu Elegan": "#8e44ad",
        "Merah Dinamis": "#e74c3c",
        "Custom": custom if custom else "#3498db"
    }
    return palettes.get(scheme, "#3498db")

# Fungsi untuk membuat Radar Chart
def create_radar_chart(labels, scores, title, color, width, height, dpi_val):
    scores = [int(s) if isinstance(s, (int, float)) and s == int(s) else float(s) for s in scores]
    
    scores_plot = scores + scores[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(width, height), facecolor='white', dpi=dpi_val)
    ax = plt.subplot(111, polar=True)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    
    # Label di luar lingkaran dengan padding dinamis
    max_score = max(scores)
    label_radius = max_score * 1.2
    for angle, label in zip(angles[:-1], labels):
        ax.text(angle, label_radius, label, ha='center', va='center',
                fontsize=14, weight='bold', color='#2c3e50')
    
    # Skala radial
    ax.set_rlabel_position(30)
    ax.set_yticks(range(1, max_score + 1))
    ax.set_yticklabels([str(i) for i in range(1, max_score + 1)],
                       fontsize=12, color='#7f8c8d', weight='bold')
    ax.set_ylim(0, max_score * 1.1)
    
    # Grid
    ax.grid(color='#bdc3c7', linestyle='--', linewidth=1, alpha=0.7)
    ax.spines['polar'].set_color('#34495e')
    
    # Plot
    ax.plot(angles, scores_plot, 'o-', linewidth=3, color=color,
            markersize=10, markerfacecolor='white', markeredgewidth=2.5,
            markeredgecolor=color, label='Skor Aktual')
    ax.fill(angles, scores_plot, alpha=0.25, color=color)
    
    # Nilai di titik
    for angle, score in zip(angles[:-1], scores):
        ax.text(angle, score, str(score), ha='center', va='center',
                fontsize=14, weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                         edgecolor=color, linewidth=2, alpha=0.9))
    
    # Target line
    target = [max_score] * len(angles)
    ax.plot(angles, target, 'r--', linewidth=2, alpha=0.5, label='Target')
    
    # FIX: Padding judul lebih besar dan adjust top margin
    plt.title(title, fontsize=18, weight='bold', color='#2c3e50', pad=50)
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.15), fontsize=12)
    
    plt.subplots_adjust(top=0.85, bottom=0.1)
    
    return fig

# Fungsi untuk Bar Chart Horizontal
def create_horizontal_bar(categories, values, title, color, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    
    bars = ax.barh(categories, values, color=color, edgecolor='white', linewidth=2)
    
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(bar.get_width() + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', ha='left', va='center', fontsize=14, weight='bold')
    
    ax.set_xlabel('Nilai', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=30)
    ax.set_xlim(0, max(values) * 1.15)
    
    sns.despine()
    plt.tight_layout(pad=3.0)
    return fig

# Fungsi untuk Bar Chart Vertikal
def create_vertical_bar(categories, values, title, color, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    
    bars = ax.bar(categories, values, color=color, edgecolor='white', linewidth=2)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + max(values)*0.02,
                f'{h:.1f}', ha='center', va='bottom', fontsize=14, weight='bold')
    
    ax.set_ylabel('Nilai', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=30)
    ax.set_ylim(0, max(values) * 1.15)
    
    plt.xticks(rotation=15, ha='right')
    sns.despine()
    plt.tight_layout(pad=3.0)
    return fig

# Fungsi untuk Histogram
def create_histogram(data, bins, title, color, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    n, bins_edges, patches = ax.hist(data, bins=bins, color=color, alpha=0.7, 
                                      edgecolor='white', linewidth=1.5)
    
    from scipy import stats
    density = stats.gaussian_kde(data)
    xs = np.linspace(min(data), max(data), 200)
    ax2 = ax.twinx()
    ax2.plot(xs, density(xs), color='red', linewidth=2.5, label='Distribusi')
    ax2.set_ylabel('Densitas', fontsize=12)
    
    ax.set_xlabel('Nilai', fontsize=14, weight='bold')
    ax.set_ylabel('Frekuensi', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=30)
    
    sns.despine()
    plt.tight_layout(pad=3.0)
    return fig

# Fungsi untuk Pie Chart
def create_pie_chart(labels, values, title, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    colors = sns.color_palette("Set2", len(labels))
    explode = [0.05] * len(labels)
    
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                       colors=colors, explode=explode,
                                       shadow=True, startangle=90,
                                       textprops={'fontsize': 12, 'weight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
    
    ax.set_title(title, fontsize=18, weight='bold', pad=40)
    plt.tight_layout(pad=3.0)
    return fig

# Fungsi untuk Grouped Bar Chart
def create_grouped_bar(categories, data_dict, title, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    
    x = np.arange(len(categories))
    width_bar = 0.8 / len(data_dict)
    colors = sns.color_palette("husl", len(data_dict))
    
    all_vals = [v for sub in data_dict.values() for v in sub]
    max_val = max(all_vals) if all_vals else 10
    
    for i, (label, values) in enumerate(data_dict.items()):
        offset = (i - len(data_dict)/2 + 0.5) * width_bar
        bars = ax.bar(x + offset, values, width_bar, label=label, color=colors[i])
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + max_val*0.02,
                    f'{h:.1f}', ha='center', va='bottom', fontsize=10, weight='bold')
    
    ax.set_title(title, fontsize=18, weight='bold', pad=30)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=15, ha='right')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0, max_val * 1.2)
    
    sns.despine()
    plt.tight_layout(pad=3.0)
    return fig

# Fungsi untuk Stacked Bar Chart
def create_stacked_bar(categories, data_dict, title, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    colors = sns.color_palette("Spectral", len(data_dict))
    bottom = np.zeros(len(categories))
    
    for i, (label, values) in enumerate(data_dict.items()):
        ax.bar(categories, values, label=label, bottom=bottom, color=colors[i])
        bottom += values
    
    ax.set_title(title, fontsize=18, weight='bold', pad=30)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=15, ha='right')
    sns.despine()
    plt.tight_layout(pad=3.0)
    return fig

# Fungsi untuk save figure
def save_figure(fig, format_type):
    buf = io.BytesIO()
    fig.savefig(buf, format=format_type.lower(), bbox_inches='tight')
    buf.seek(0)
    return buf

# --- MAIN CONTENT ---
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="sub-header">📝 Input Data</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📋 Input Manual", "📁 Upload Excel"])
# ... (Logika input data tetap sama seperti sebelumnya) ...
# [Sertakan logika tab1 & tab2 dari file asli Anda di sini]

# --- GENERATE VISUALIZATION ---
st.markdown('<div class="sub-header">📊 Hasil Visualisasi</div>', unsafe_allow_html=True)

try:
    color = get_color_palette(color_scheme, custom_color if color_scheme == "Custom" else None)
    
    fig = None
    if "Radar" in viz_type and len(labels) > 0:
        fig = create_radar_chart(labels, values, title_input, color, fig_width, fig_height, dpi)
    elif "Horizontal" in viz_type and len(categories) > 0:
        fig = create_horizontal_bar(categories, values, title_input, color, fig_width, fig_height, dpi)
    elif "Vertikal" in viz_type and len(categories) > 0:
        fig = create_vertical_bar(categories, values, title_input, color, fig_width, fig_height, dpi)
    elif "Histogram" in viz_type and len(data_values) > 0:
        fig = create_histogram(data_values, bins, title_input, color, fig_width, fig_height, dpi)
    elif "Pie" in viz_type and len(labels) > 0:
        fig = create_pie_chart(labels, values, title_input, fig_width, fig_height, dpi)
    elif "Grouped" in viz_type and len(categories) > 0:
        fig = create_grouped_bar(categories, data_dict, title_input, fig_width, fig_height, dpi)
    elif "Stacked" in viz_type and len(categories) > 0:
        fig = create_stacked_bar(categories, data_dict, title_input, fig_width, fig_height, dpi)

    if fig:
        st.pyplot(fig, use_container_width=True)
        buf = save_figure(fig, download_format)
        st.download_button(label=f"💾 Download {download_format}", data=buf, 
                           file_name=f"chart.{download_format.lower()}", mime=f"image/{download_format.lower()}")
        plt.close('all')

except Exception as e:
    st.error(f"❌ Terjadi kesalahan: {str(e)}")

# Footer ...

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
    <p><strong>📊 Dashboard Visualisasi Monitoring & Evaluasi</strong></p>
    <p>Dibuat dengan ❤️ menggunakan Streamlit & Matplotlib</p>
    <p style='margin-top: 1rem; font-size: 0.9rem;'>
        <strong>Developed by:</strong> Tubagus Robbi Megantara<br>
        <a href='mailto:tubagusrobbimegantara@gmail.com' style='color: #3498db; text-decoration: none;'>
            📧 tubagusrobbimegantara@gmail.com
        </a>
    </p>
    <p style='margin-top: 0.5rem; font-size: 0.8rem; color: #95a5a6;'>
        © 2025 - Dashboard Monev | Version 1.0
    </p>
</div>
""", unsafe_allow_html=True)
