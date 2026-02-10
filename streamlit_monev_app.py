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
    # Konversi skor ke list dan pastikan numerik
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
    
    # Menghitung batas maksimal untuk padding label
    max_score = max(scores)
    
    # Label di luar lingkaran dengan padding dinamis
    label_radius = max_score * 1.2  # Memberi ruang 20% lebih luas dari skor maks
    for angle, label in zip(angles[:-1], labels):
        ax.text(angle, label_radius, label, ha='center', va='center',
                fontsize=14, weight='bold', color='#2c3e50')
    
    # Skala radial
    ax.set_rlabel_position(30)
    ax.set_yticks(range(1, max_score + 1))
    ax.set_yticklabels([str(i) for i in range(1, max_score + 1)],
                       fontsize=12, color='#7f8c8d', weight='bold')
    ax.set_ylim(0, max_score * 1.1) # Tambahkan limit agar garis terluar tidak mepet frame
    
    # Grid
    ax.grid(color='#bdc3c7', linestyle='--', linewidth=1, alpha=0.7)
    ax.spines['polar'].set_color('#34495e')
    
    # Plot Skor Aktual
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
    
    # PERBAIKAN UTAMA: Judul dengan padding lebih besar
    plt.title(title, fontsize=18, weight='bold', color='#2c3e50', pad=50) 
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.15), fontsize=12)
    
    # Sesuaikan margin atas agar judul tidak terpotong saat di-render
    plt.subplots_adjust(top=0.85) 
    
    return fig

# Fungsi untuk Bar Chart Horizontal
def create_horizontal_bar(categories, values, title, color, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    
    bars = ax.barh(categories, values, color=color, edgecolor='white', linewidth=2)
    
    # Label nilai
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(bar.get_width() + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', ha='left', va='center', fontsize=14, weight='bold')
    
    ax.set_xlabel('Nilai', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=20)
    ax.set_xlim(0, max(values) * 1.15)
    
    sns.despine()
    plt.tight_layout()
    
    return fig

# Fungsi untuk Bar Chart Vertikal
def create_vertical_bar(categories, values, title, color, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    
    bars = ax.bar(categories, values, color=color, edgecolor='white', linewidth=2)
    
    # Label nilai
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.02,
                f'{height:.1f}', ha='center', va='bottom', fontsize=14, weight='bold')
    
    ax.set_ylabel('Nilai', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=20)
    ax.set_ylim(0, max(values) * 1.15)
    
    plt.xticks(rotation=15, ha='right')
    sns.despine()
    plt.tight_layout()
    
    return fig

# Fungsi untuk Histogram
def create_histogram(data, bins, title, color, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    
    n, bins_edges, patches = ax.hist(data, bins=bins, color=color, alpha=0.7, 
                                      edgecolor='white', linewidth=1.5)
    
    # Garis KDE
    from scipy import stats
    density = stats.gaussian_kde(data)
    xs = np.linspace(min(data), max(data), 200)
    ax2 = ax.twinx()
    ax2.plot(xs, density(xs), color='red', linewidth=2.5, label='Distribusi')
    ax2.set_ylabel('Densitas', fontsize=12)
    ax2.legend(loc='upper right')
    
    ax.set_xlabel('Nilai', fontsize=14, weight='bold')
    ax.set_ylabel('Frekuensi', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=20)
    
    sns.despine()
    plt.tight_layout()
    
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
    
    ax.set_title(title, fontsize=18, weight='bold', pad=20)
    plt.tight_layout()
    
    return fig

# Fungsi untuk Grouped Bar Chart
def create_grouped_bar(categories, data_dict, title, width, height, dpi_val):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val)
    
    x = np.arange(len(categories))
    width_bar = 0.8 / len(data_dict)
    
    colors = sns.color_palette("husl", len(data_dict))
    
    for i, (label, values) in enumerate(data_dict.items()):
        offset = (i - len(data_dict)/2 + 0.5) * width_bar
        bars = ax.bar(x + offset, values, width_bar, label=label, color=colors[i])
        
        # Label nilai
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=10, weight='bold')
    
    ax.set_xlabel('Kategori', fontsize=14, weight='bold')
    ax.set_ylabel('Nilai', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=15, ha='right')
    ax.legend()
    
    sns.despine()
    plt.tight_layout()
    
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
    
    ax.set_ylabel('Nilai', fontsize=14, weight='bold')
    ax.set_title(title, fontsize=18, weight='bold', pad=20)
    ax.legend(loc='upper left')
    
    plt.xticks(rotation=15, ha='right')
    sns.despine()
    plt.tight_layout()
    
    return fig

# Fungsi untuk save figure
def save_figure(fig, format_type):
    buf = io.BytesIO()
    if format_type == "PDF":
        fig.savefig(buf, format='pdf', bbox_inches='tight')
    elif format_type == "SVG":
        fig.savefig(buf, format='svg', bbox_inches='tight')
    else:  # PNG
        fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="sub-header">📝 Input Data</div>', unsafe_allow_html=True)

# Tab untuk input method
tab1, tab2 = st.tabs(["📋 Input Manual", "📁 Upload Excel"])

with tab1:
    if "Radar" in viz_type or "Pie" in viz_type:
        st.markdown("**Masukkan label dan nilai (pisahkan dengan koma)**")
        
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            labels_input = st.text_area(
                "Labels (pisahkan dengan koma)",
                "Keselarasan VMTS, Pemanfaatan VMTS, Mekanisme VMTS, Pelibatan Stakeholder",
                height=100
            )
        
        with col_input2:
            values_input = st.text_area(
                "Nilai (pisahkan dengan koma)",
                "4, 3, 4, 2",
                height=100
            )
        
        labels = [l.strip() for l in labels_input.split(',') if l.strip()]
        try:
            values = []
            for v in values_input.split(','):
                v = v.strip()
                if v:  # Only process non-empty strings
                    # Handle both integer and float
                    if '.' in v:
                        values.append(float(v))
                    else:
                        values.append(int(v))
        except ValueError as e:
            st.error(f"❌ Nilai harus berupa angka! Error: {str(e)}")
            values = []
    
    elif "Histogram" in viz_type:
        st.markdown("**Masukkan data untuk histogram (pisahkan dengan koma)**")
        data_input = st.text_area(
            "Data (pisahkan dengan koma)",
            "65, 70, 75, 80, 85, 90, 72, 68, 88, 92, 78, 82, 76, 84, 79",
            height=100
        )
        bins = st.slider("Jumlah Bins", 5, 30, 10)
        
        try:
            data_values = []
            for v in data_input.split(','):
                v = v.strip()
                if v:
                    if '.' in v:
                        data_values.append(float(v))
                    else:
                        data_values.append(int(v))
        except ValueError as e:
            st.error(f"❌ Data harus berupa angka! Error: {str(e)}")
            data_values = []
    
    elif "Grouped" in viz_type or "Stacked" in viz_type:
        st.markdown("**Masukkan kategori dan beberapa grup data**")
        
        categories_input = st.text_input(
            "Kategori (pisahkan dengan koma)",
            "Dosen, Mahasiswa, Tendik"
        )
        
        num_groups = st.number_input("Jumlah Grup Data", 2, 5, 2)
        
        data_dict = {}
        for i in range(num_groups):
            group_name = st.text_input(f"Nama Grup {i+1}", f"Grup {i+1}", key=f"group_{i}")
            group_values = st.text_input(
                f"Nilai untuk {group_name} (pisahkan dengan koma)",
                "85, 75, 80",
                key=f"values_{i}"
            )
            try:
                parsed_values = []
                for v in group_values.split(','):
                    v = v.strip()
                    if v:
                        if '.' in v:
                            parsed_values.append(float(v))
                        else:
                            parsed_values.append(int(v))
                data_dict[group_name] = parsed_values
            except ValueError as e:
                st.error(f"❌ Nilai untuk {group_name} harus berupa angka! Error: {str(e)}")
        
        categories = [c.strip() for c in categories_input.split(',') if c.strip()]
    
    else:  # Bar charts
        st.markdown("**Masukkan kategori dan nilai (pisahkan dengan koma)**")
        
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            categories_input = st.text_area(
                "Kategori (pisahkan dengan koma)",
                "Dosen, Mahasiswa, Tendik",
                height=100
            )
        
        with col_input2:
            values_input = st.text_area(
                "Nilai (pisahkan dengan koma)",
                "88, 72, 85",
                height=100
            )
        
        categories = [c.strip() for c in categories_input.split(',') if c.strip()]
        try:
            values = []
            for v in values_input.split(','):
                v = v.strip()
                if v:
                    if '.' in v:
                        values.append(float(v))
                    else:
                        values.append(int(v))
        except ValueError as e:
            st.error(f"❌ Nilai harus berupa angka! Error: {str(e)}")
            values = []

with tab2:
    uploaded_file = st.file_uploader("Upload file Excel (.xlsx atau .xls)", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            st.success(f"✅ File berhasil diupload! ({len(df)} baris, {len(df.columns)} kolom)")
            st.dataframe(df, use_container_width=True)
            
            if "Radar" in viz_type or "Pie" in viz_type or "Bar" in viz_type:
                col_label = st.selectbox("Pilih kolom untuk Label", df.columns)
                col_value = st.selectbox("Pilih kolom untuk Nilai", df.columns)
                
                labels = df[col_label].tolist()
                values = df[col_value].tolist()
            
            elif "Histogram" in viz_type:
                col_data = st.selectbox("Pilih kolom untuk Data", df.columns)
                data_values = df[col_data].tolist()
                bins = st.slider("Jumlah Bins", 5, 30, 10)
            
            elif "Grouped" in viz_type or "Stacked" in viz_type:
                col_cat = st.selectbox("Pilih kolom untuk Kategori", df.columns)
                value_cols = st.multiselect("Pilih kolom untuk Nilai", 
                                           [c for c in df.columns if c != col_cat])
                
                categories = df[col_cat].tolist()
                data_dict = {col: df[col].tolist() for col in value_cols}
        
        except Exception as e:
            st.error(f"❌ Error membaca file Excel: {str(e)}")
            st.info("💡 Pastikan file Excel Anda memiliki header di baris pertama dan data dalam format yang benar.")

# Pengaturan tambahan
st.markdown('<div class="sub-header">🎨 Pengaturan Visualisasi</div>', unsafe_allow_html=True)

title_input = st.text_input(
    "Judul Grafik",
    "Hasil Monitoring dan Evaluasi"
)

# Generate visualization
st.markdown('<div class="sub-header">📊 Hasil Visualisasi</div>', unsafe_allow_html=True)

try:
    color = get_color_palette(color_scheme, custom_color if color_scheme == "Custom" else None)
    
    if "Radar" in viz_type:
        if len(labels) == len(values) and len(labels) > 0:
            fig = create_radar_chart(labels, values, title_input, color, 
                                    fig_width, fig_height, dpi)
            st.pyplot(fig)
            
            # Download button
            buf = save_figure(fig, download_format)
            st.download_button(
                label=f"💾 Download {download_format}",
                data=buf,
                file_name=f"radar_chart.{download_format.lower()}",
                mime=f"image/{download_format.lower()}"
            )
        else:
            st.warning("⚠️ Jumlah label dan nilai harus sama!")
    
    elif "Horizontal" in viz_type:
        if len(categories) == len(values) and len(categories) > 0:
            fig = create_horizontal_bar(categories, values, title_input, color,
                                       fig_width, fig_height, dpi)
            st.pyplot(fig)
            
            buf = save_figure(fig, download_format)
            st.download_button(
                label=f"💾 Download {download_format}",
                data=buf,
                file_name=f"horizontal_bar.{download_format.lower()}",
                mime=f"image/{download_format.lower()}"
            )
        else:
            st.warning("⚠️ Jumlah kategori dan nilai harus sama!")
    
    elif "Vertikal" in viz_type:
        if len(categories) == len(values) and len(categories) > 0:
            fig = create_vertical_bar(categories, values, title_input, color,
                                     fig_width, fig_height, dpi)
            st.pyplot(fig)
            
            buf = save_figure(fig, download_format)
            st.download_button(
                label=f"💾 Download {download_format}",
                data=buf,
                file_name=f"vertical_bar.{download_format.lower()}",
                mime=f"image/{download_format.lower()}"
            )
        else:
            st.warning("⚠️ Jumlah kategori dan nilai harus sama!")
    
    elif "Histogram" in viz_type:
        if len(data_values) > 0:
            fig = create_histogram(data_values, bins, title_input, color,
                                  fig_width, fig_height, dpi)
            st.pyplot(fig)
            
            buf = save_figure(fig, download_format)
            st.download_button(
                label=f"💾 Download {download_format}",
                data=buf,
                file_name=f"histogram.{download_format.lower()}",
                mime=f"image/{download_format.lower()}"
            )
        else:
            st.warning("⚠️ Masukkan data yang valid!")
    
    elif "Pie" in viz_type:
        if len(labels) == len(values) and len(labels) > 0:
            fig = create_pie_chart(labels, values, title_input,
                                  fig_width, fig_height, dpi)
            st.pyplot(fig)
            
            buf = save_figure(fig, download_format)
            st.download_button(
                label=f"💾 Download {download_format}",
                data=buf,
                file_name=f"pie_chart.{download_format.lower()}",
                mime=f"image/{download_format.lower()}"
            )
        else:
            st.warning("⚠️ Jumlah label dan nilai harus sama!")
    
    elif "Grouped" in viz_type:
        if len(categories) > 0 and len(data_dict) > 0:
            fig = create_grouped_bar(categories, data_dict, title_input,
                                    fig_width, fig_height, dpi)
            st.pyplot(fig)
            
            buf = save_figure(fig, download_format)
            st.download_button(
                label=f"💾 Download {download_format}",
                data=buf,
                file_name=f"grouped_bar.{download_format.lower()}",
                mime=f"image/{download_format.lower()}"
            )
        else:
            st.warning("⚠️ Masukkan kategori dan data yang valid!")
    
    elif "Stacked" in viz_type:
        if len(categories) > 0 and len(data_dict) > 0:
            fig = create_stacked_bar(categories, data_dict, title_input,
                                    fig_width, fig_height, dpi)
            st.pyplot(fig)
            
            buf = save_figure(fig, download_format)
            st.download_button(
                label=f"💾 Download {download_format}",
                data=buf,
                file_name=f"stacked_bar.{download_format.lower()}",
                mime=f"image/{download_format.lower()}"
            )
        else:
            st.warning("⚠️ Masukkan kategori dan data yang valid!")
    
    plt.close('all')

except Exception as e:
    st.error(f"❌ Terjadi kesalahan: {str(e)}")

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
