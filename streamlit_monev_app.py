import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Shadow, FancyBboxPatch
import matplotlib.patches as mpatches

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Visualisasi Monev",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set seaborn style
sns.set_theme(style="whitegrid", palette="husl")

# Custom CSS untuk estetika
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        font-weight: 600;
        margin-top: 1.5rem;
        padding-left: 10px;
        border-left: 4px solid #667eea;
    }
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 Dashboard Visualisasi Monitoring & Evaluasi</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=MONEV+Dashboard", use_container_width=True)
    
    # Credit section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.2rem; border-radius: 15px; margin-bottom: 1rem;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
        <p style='color: white; font-size: 0.9rem; margin: 0; text-align: center;'>
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
            "📚 Stacked Bar Chart",
            "✨ Interactive Plotly Chart"
        ]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan Tampilan")
    
    # Pengaturan warna dengan palette seaborn
    color_scheme = st.selectbox(
        "Skema Warna",
        [
            "🎨 Seaborn Deep",
            "🌈 Seaborn Bright", 
            "🌊 Ocean",
            "🔥 Fire",
            "🌸 Pastel",
            "💎 Jewel Tones",
            "🌅 Sunset",
            "🌲 Forest",
            "Custom"
        ]
    )
    
    if color_scheme == "Custom":
        custom_color = st.color_picker("Pilih Warna", "#667eea")
    
    # Toggle untuk efek 3D
    use_3d_effect = st.checkbox("Efek 3D & Shadow", value=True)
    use_gradient = st.checkbox("Gradient Fill", value=True)
    
    # Pengaturan ukuran
    fig_width = st.slider("Lebar Gambar", 8, 20, 14)
    fig_height = st.slider("Tinggi Gambar", 6, 18, 10)
    dpi = st.slider("Resolusi (DPI)", 100, 400, 200)
    
    st.markdown("### 🔤 Pengaturan Font")
    title_font_size = st.slider("Ukuran Font Judul", 14, 32, 20)
    label_font_size = st.slider("Ukuran Font Label", 8, 20, 13)
    value_font_size = st.slider("Ukuran Font Nilai", 8, 20, 14)
    
    st.markdown("---")
    st.markdown("### 💾 Download Options")
    download_format = st.radio("Format File", ["PNG", "PDF", "SVG"])

# Fungsi untuk mendapatkan warna palette
def get_color_palette(scheme, custom=None, n_colors=10):
    palettes = {
        "🎨 Seaborn Deep": sns.color_palette("deep", n_colors),
        "🌈 Seaborn Bright": sns.color_palette("bright", n_colors),
        "🌊 Ocean": sns.color_palette("ocean_r", n_colors),
        "🔥 Fire": sns.color_palette("flare", n_colors),
        "🌸 Pastel": sns.color_palette("pastel", n_colors),
        "💎 Jewel Tones": sns.color_palette("Set2", n_colors),
        "🌅 Sunset": sns.color_palette("Spectral", n_colors),
        "🌲 Forest": sns.color_palette("YlGn", n_colors),
        "Custom": [custom if custom else "#667eea"] * n_colors
    }
    return palettes.get(scheme, sns.color_palette("deep", n_colors))

# Fungsi untuk membuat gradient
def get_gradient_cmap(color):
    """Buat colormap gradient dari warna tunggal"""
    from matplotlib.colors import LinearSegmentedColormap
    if isinstance(color, str):
        r, g, b = plt.matplotlib.colors.to_rgb(color)
    else:
        r, g, b = color[:3]
    
    colors = [(1, 1, 1), (r, g, b)]
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
    return cmap

# Fungsi untuk membuat Radar Chart dengan estetika profesional tingkat tinggi
# Fungsi untuk membuat Radar Chart dengan estetika profesional tingkat tinggi
def create_radar_chart(labels, scores, title, colors, width, height, dpi_val, use_3d=True, use_grad=True, 
                       title_fontsize=20, label_fontsize=13, value_fontsize=14):
    
    # 1. SETUP DATA
    # Pastikan data float dan loop tertutup
    scores = [float(s) for s in scores]
    num_vars = len(labels)
    
    # Sudut untuk setiap sumbu
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Menutup loop grafik (titik akhir kembali ke titik awal)
    scores += scores[:1]
    angles += angles[:1]
    
    # 2. SETUP FIGURE & AXIS
    # Gunakan style default yang sangat bersih untuk laporan profesional
    plt.style.use('default') 
    fig, ax = plt.subplots(figsize=(width, height), subplot_kw=dict(polar=True), dpi=dpi_val)
    
    # Warna Background Putih Bersih (standar publikasi profesional)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fb')  # Abu sangat muda untuk kontras lembut
    
    # Putar agar label pertama ada di atas (jam 12)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # 3. CUSTOM GRID (POLYGON STYLE) - Sangat Profesional
    # Hapus grid dan spine bawaan matplotlib
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.spines['polar'].set_visible(False)
    
    # Gambar Grid Polygon Manual untuk tampilan sangat profesional
    max_val = 4  # Skala Monev: 1-4
    grid_color = '#d1d5db'  # Abu-abu medium untuk grid
    grid_light = '#e5e7eb'  # Abu-abu sangat muda untuk grid sekunder
    
    # Grid konsentris (polygon untuk setiap level)
    for i in range(1, max_val + 1):
        grid_values = [i] * (num_vars + 1)
        # Grid untuk level 4 (target) lebih tebal dan gelap
        if i == max_val:
            ax.plot(angles, grid_values, color=grid_color, linewidth=1.5, linestyle='-', zorder=0, alpha=0.6)
        else:
            ax.plot(angles, grid_values, color=grid_light, linewidth=1, linestyle='-', zorder=0, alpha=0.5)
    
    # Grid radial (garis sumbu dari pusat) - lebih halus
    for angle in angles[:-1]:
        ax.plot([angle, angle], [0, max_val], color=grid_light, linewidth=1, zorder=0, alpha=0.5)

    # 4. LABEL SUMBU (KATEGORI) - Professional Typography dengan Multi-line Support
    ax.set_xticks(angles[:-1])
    
    # Bungkus label panjang untuk keterbacaan optimal (lebih agresif)
    wrapped_labels = []
    for label in labels:
        # Jika label sangat panjang, pecah menjadi 2-3 baris
        if len(label) > 20:
            words = label.split()
            if len(words) >= 3:
                # Pecah jadi 2-3 baris
                third = len(words) // 3
                if third > 0:
                    line1 = ' '.join(words[:third])
                    line2 = ' '.join(words[third:2*third])
                    line3 = ' '.join(words[2*third:])
                    wrapped_labels.append(f'{line1}\n{line2}\n{line3}')
                else:
                    mid = len(words) // 2
                    wrapped_labels.append(' '.join(words[:mid]) + '\n' + ' '.join(words[mid:]))
            else:
                wrapped_labels.append(label)
        elif len(label) > 12:
            # Pecah kata panjang dengan newline
            words = label.split()
            if len(words) > 1:
                mid = len(words) // 2
                wrapped_labels.append(' '.join(words[:mid]) + '\n' + ' '.join(words[mid:]))
            else:
                wrapped_labels.append(label)
        else:
            wrapped_labels.append(label)
    
    ax.set_xticklabels(wrapped_labels, size=label_fontsize, color='#1e293b', weight='600')
    
    # Padding label agar tidak menempel grafik
    ax.tick_params(axis='x', pad=25)

    # 5. LABEL Y-AXIS (SKALA) - Clean & Minimal dengan angka saja
    # Tampilkan skala hanya di satu posisi (posisi 0°) untuk kesederhanaan
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4], 
               ["1", "2", "3", "4"], 
               color="#6b7280", size=11, weight='500')
    plt.ylim(0, max_val + 0.5)

    # 6. PLOT DATA (CAPAIAN) - Professional Styling
    main_color = colors[0] if isinstance(colors, list) else colors
    
    # Plot Garis Data dengan ketebalan optimal
    ax.plot(angles, scores, color=main_color, linewidth=2.5, linestyle='-', 
            label='Skor Ketercapaian SDM', zorder=10, marker='o', markersize=0)
    
    # Fill Area dengan warna lebih solid seperti contoh
    if use_grad:
        ax.fill(angles, scores, color=main_color, alpha=0.35, zorder=9)
    else:
        ax.fill(angles, scores, color=main_color, alpha=0.2, zorder=9)

    # Marker Titik Data - White center dengan border tebal (ukuran lebih kecil)
    ax.scatter(angles[:-1], scores[:-1], color='white', edgecolor=main_color, 
               s=120, linewidth=2.5, zorder=11, clip_on=False)

    # 7. TARGET LINE - PENTING: Di nilai maksimal (4) seperti contoh
    target_score = max_val  # Target di nilai maksimal (Baik Sekali = 4)
    target_values = [target_score] * (num_vars + 1)
    ax.plot(angles, target_values, color='#dc2626', linewidth=2, 
            linestyle='--', label=f'Target (Baik Sekali = {target_score})', zorder=5, alpha=0.8)

    # 8. ANNOTATION VALUES - Clean Value Labels dalam Kotak
    for angle, score in zip(angles[:-1], scores[:-1]):
        # Posisi label sedikit di luar titik untuk keterbacaan
        label_pos = score + 0.35
        
        # Kotak nilai dengan styling profesional - warna hijau untuk kotak
        ax.text(angle, label_pos, f"{score:.0f}", 
                ha='center', va='center', size=value_fontsize, weight='bold', 
                color='#065f46',
                bbox=dict(boxstyle="round,pad=0.3", fc="#d1fae5", ec="#10b981", 
                         lw=2, alpha=0.95),
                zorder=12)

    # 9. JUDUL & METADATA - Professional Document Style
    plt.title(title, size=title_fontsize, weight='bold', color='#1e293b', y=1.08, pad=15)
    
    # Tidak ada subtitle - lebih bersih seperti contoh

    # Legend dengan posisi dan styling seperti contoh (pojok kanan atas)
    legend = plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1),
                       fancybox=False, shadow=False, frameon=True, 
                       fontsize=11, markerscale=1.0, edgecolor='#e5e7eb', 
                       framealpha=1, facecolor='white')
    legend.get_frame().set_linewidth(1.5)

    # Adjustments untuk layout sempurna
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.85)
    
    return fig

# Fungsi untuk Bar Chart Horizontal dengan seaborn
def create_horizontal_bar(categories, values, title, colors, width, height, dpi_val, use_3d=True, use_grad=True,
                          title_fontsize=20, label_fontsize=13, value_fontsize=14):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val, facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    # Gunakan seaborn barplot untuk styling lebih baik
    if isinstance(colors, list):
        palette = colors[:len(categories)]
    else:
        palette = [colors] * len(categories)
    
    # Buat dataframe untuk seaborn
    df = pd.DataFrame({'Kategori': categories, 'Nilai': values})
    
    # Barplot dengan seaborn - TANPA gradient yang membuat pattern aneh
    bars = sns.barplot(data=df, y='Kategori', x='Nilai', palette=palette, 
                       ax=ax, edgecolor='white', linewidth=2.5, alpha=0.85)
    
    # Label nilai dengan styling menarik
    for i, (bar, val) in enumerate(zip(bars.patches, values)):
        color_idx = i % len(palette)
        ax.text(bar.get_width() + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', ha='left', va='center', fontsize=value_fontsize, weight='bold',
                color=palette[color_idx],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                         edgecolor=palette[color_idx], linewidth=2))
    
    ax.set_xlabel('Nilai', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    ax.set_ylabel('')
    
    # Judul profesional TANPA border
    ax.set_title(title, fontsize=title_fontsize, weight='bold', pad=25, color='#2c3e50')
    ax.set_xlim(0, max(values) * 1.2)
    
    # Styling axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    # Tambahkan grid untuk memudahkan pembacaan
    ax.xaxis.grid(True, linestyle='--', alpha=0.3, color='#bdc3c7')
    ax.set_axisbelow(True)
    
    # Set x-axis ticks untuk skala 1-4 jika data dalam range tersebut
    if max(values) <= 5:
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xticklabels(['1\n(Kurang)', '2\n(Cukup)', '3\n(Baik)', '4\n(Baik Sekali)'], fontsize=10)
    
    plt.tight_layout()
    return fig

# Fungsi untuk Bar Chart Vertikal dengan seaborn
def create_vertical_bar(categories, values, title, colors, width, height, dpi_val, use_3d=True, use_grad=True,
                        title_fontsize=20, label_fontsize=13, value_fontsize=14):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val, facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    if isinstance(colors, list):
        palette = colors[:len(categories)]
    else:
        palette = [colors] * len(categories)
    
    df = pd.DataFrame({'Kategori': categories, 'Nilai': values})
    
    # Barplot dengan seaborn - TANPA gradient yang membuat pattern aneh
    bars = sns.barplot(data=df, x='Kategori', y='Nilai', palette=palette,
                       ax=ax, edgecolor='white', linewidth=2.5, alpha=0.85)
    
    # Label nilai
    for i, (bar, val) in enumerate(zip(bars.patches, values)):
        color_idx = i % len(palette)
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.02,
                f'{val:.1f}', ha='center', va='bottom', fontsize=value_fontsize, weight='bold',
                color=palette[color_idx],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                         edgecolor=palette[color_idx], linewidth=2))
    
    ax.set_ylabel('Nilai', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    ax.set_xlabel('')
    
    # Judul profesional TANPA border
    ax.set_title(title, fontsize=title_fontsize, weight='bold', pad=25, color='#2c3e50')
    ax.set_ylim(0, max(values) * 1.2)
    
    plt.xticks(rotation=15, ha='right', fontsize=11)
    
    # Styling axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    # Tambahkan grid untuk memudahkan pembacaan
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#bdc3c7')
    ax.set_axisbelow(True)
    
    # Set y-axis ticks untuk skala 1-4 jika data dalam range tersebut
    if max(values) <= 5:
        ax.set_yticks([1, 2, 3, 4])
        ax.set_yticklabels(['1 (Kurang)', '2 (Cukup)', '3 (Baik)', '4 (Baik Sekali)'], fontsize=10)
    
    plt.tight_layout()
    return fig

# Fungsi untuk Histogram dengan seaborn
def create_histogram(data, bins, title, colors, width, height, dpi_val, use_grad=True,
                     title_fontsize=20, label_fontsize=13):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val, facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    color = colors[0] if isinstance(colors, list) else colors
    
    # Histogram dengan seaborn
    sns.histplot(data=data, bins=bins, kde=True, color=color, 
                edgecolor='white', linewidth=2, ax=ax, alpha=0.7)
    
    # KDE line dengan warna berbeda
    kde_color = colors[1] if isinstance(colors, list) and len(colors) > 1 else '#e74c3c'
    
    ax.set_xlabel('Nilai', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    ax.set_ylabel('Frekuensi', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    
    # Judul profesional TANPA border
    ax.set_title(title, fontsize=title_fontsize, weight='bold', pad=25, color='#2c3e50')
    
    # Styling axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    # Tambahkan statistik
    mean_val = np.mean(data)
    median_val = np.median(data)
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2.5, label=f'Mean: {mean_val:.2f}', alpha=0.8)
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2.5, label=f'Median: {median_val:.2f}', alpha=0.8)
    
    ax.legend(fontsize=12, frameon=True, shadow=True, fancybox=True)
    
    plt.tight_layout()
    return fig

# Fungsi untuk Pie Chart yang lebih cantik
def create_pie_chart(labels, values, title, colors, width, height, dpi_val, use_3d=True,
                     title_fontsize=20, label_fontsize=13):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val, facecolor='#f8f9fa')
    
    if isinstance(colors, list):
        palette = colors[:len(labels)]
    else:
        palette = sns.color_palette("husl", len(labels))
    
    # Explode untuk efek
    explode = [0.05] * len(labels)
    explode[values.index(max(values))] = 0.15  # Explode nilai terbesar
    
    # Shadow dan styling
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                       startangle=90, colors=palette,
                                       explode=explode, shadow=use_3d,
                                       textprops={'fontsize': label_fontsize, 'weight': 'bold'})
    
    # Styling teks
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(label_fontsize + 1)
        autotext.set_weight('bold')
    
    for text in texts:
        text.set_fontsize(label_fontsize)
        text.set_weight('bold')
        text.set_color('#2c3e50')
    
    # Judul profesional TANPA border
    ax.set_title(title, fontsize=title_fontsize, weight='bold', pad=25, color='#2c3e50')
    
    plt.tight_layout()
    return fig

# Fungsi untuk Grouped Bar Chart
def create_grouped_bar(categories, data_dict, title, colors, width, height, dpi_val, use_grad=True,
                       title_fontsize=20, label_fontsize=13, value_fontsize=14):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val, facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    if isinstance(colors, list):
        palette = colors[:len(data_dict)]
    else:
        palette = sns.color_palette("husl", len(data_dict))
    
    x = np.arange(len(categories))
    width_bar = 0.8 / len(data_dict)
    
    for i, (key, values) in enumerate(data_dict.items()):
        offset = (i - len(data_dict)/2) * width_bar + width_bar/2
        bars = ax.bar(x + offset, values, width_bar, label=key,
                     color=palette[i], edgecolor='white', linewidth=2)
        
        # Label nilai
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom',
                   fontsize=value_fontsize - 3, weight='bold', color=palette[i])
    
    ax.set_xlabel('Kategori', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    ax.set_ylabel('Nilai', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    
    # Judul profesional TANPA border
    ax.set_title(title, fontsize=title_fontsize, weight='bold', pad=25, color='#2c3e50')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=15, ha='right')
    
    ax.legend(fontsize=12, frameon=True, shadow=True, fancybox=True)
    
    # Styling axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    plt.tight_layout()
    return fig

# Fungsi untuk Stacked Bar Chart
def create_stacked_bar(categories, data_dict, title, colors, width, height, dpi_val,
                       title_fontsize=20, label_fontsize=13, value_fontsize=14):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi_val, facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    if isinstance(colors, list):
        palette = colors[:len(data_dict)]
    else:
        palette = sns.color_palette("husl", len(data_dict))
    
    bottom = np.zeros(len(categories))
    
    for i, (key, values) in enumerate(data_dict.items()):
        bars = ax.bar(categories, values, label=key, bottom=bottom,
                     color=palette[i], edgecolor='white', linewidth=2)
        
        # Label nilai di tengah bar
        for j, (bar, val) in enumerate(zip(bars, values)):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width()/2.,
                       bottom[j] + val/2, f'{val:.0f}',
                       ha='center', va='center', fontsize=value_fontsize - 2,
                       weight='bold', color='white')
        
        bottom += values
    
    ax.set_xlabel('Kategori', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    ax.set_ylabel('Nilai', fontsize=label_fontsize, weight='bold', color='#2c3e50')
    
    # Judul profesional TANPA border
    ax.set_title(title, fontsize=title_fontsize, weight='bold', pad=25, color='#2c3e50')
    
    plt.xticks(rotation=15, ha='right')
    ax.legend(fontsize=12, frameon=True, shadow=True, fancybox=True)
    
    # Styling axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    
    plt.tight_layout()
    return fig

# Fungsi untuk Interactive Plotly Chart
def create_plotly_chart(labels, values, title, viz_type_plotly="bar"):
    """Buat chart interaktif dengan Plotly"""
    
    if viz_type_plotly == "bar":
        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(
                    color=values,
                    colorscale='Viridis',
                    line=dict(color='white', width=2)
                ),
                text=values,
                textposition='outside',
                textfont=dict(size=14, color='#2c3e50', family='Arial Black')
            )
        ])
        
    elif viz_type_plotly == "pie":
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker=dict(
                    colors=px.colors.qualitative.Set3,
                    line=dict(color='white', width=2)
                ),
                textfont=dict(size=14, color='white', family='Arial Black'),
                pull=[0.1 if v == max(values) else 0 for v in values]
            )
        ])
    
    elif viz_type_plotly == "radar":
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values + values[:1],
            theta=labels + labels[:1],
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='rgb(102, 126, 234)', width=3),
            marker=dict(size=10, color='white', line=dict(color='rgb(102, 126, 234)', width=2)),
            name='Skor Aktual'
        ))
        
        # Target line
        max_val = max(values)
        fig.add_trace(go.Scatterpolar(
            r=[max_val] * (len(labels) + 1),
            theta=labels + labels[:1],
            line=dict(color='red', width=2, dash='dash'),
            name='Target'
        ))
    
    # Layout styling
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=24, color='#2c3e50', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='#f8f9fa',
        plot_bgcolor='white',
        font=dict(size=13, color='#2c3e50'),
        showlegend=True,
        legend=dict(
            bgcolor='white',
            bordercolor='#667eea',
            borderwidth=2,
            font=dict(size=12)
        ),
        height=600,
        margin=dict(t=100, b=50, l=50, r=50)
    )
    
    if viz_type_plotly == "radar":
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    gridcolor='#d1d8e0',
                    gridwidth=2
                ),
                angularaxis=dict(
                    gridcolor='#d1d8e0',
                    gridwidth=2
                ),
                bgcolor='white'
            )
        )
    
    return fig

# Fungsi untuk save figure
def save_figure(fig, format_type):
    buf = io.BytesIO()
    if format_type == "PDF":
        fig.savefig(buf, format='pdf', bbox_inches='tight', dpi=300)
    elif format_type == "SVG":
        fig.savefig(buf, format='svg', bbox_inches='tight')
    else:  # PNG
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    buf.seek(0)
    return buf

# Tab input data
st.markdown('<div class="sub-header">📝 Input Data</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✍️ Manual Input", "📁 Upload Excel"])

# Inisialisasi variabel
labels = []
values = []
categories = []
data_values = []
data_dict = {}
bins = 10

with tab1:
    if "Radar" in viz_type or "Pie" in viz_type:
        st.markdown("**Masukkan label dan nilai (pisahkan dengan koma)**")
        
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            labels_input = st.text_area(
                "Label (pisahkan dengan koma)",
                "Layanan, Proses, SDM, Infrastruktur, Kepuasan",
                height=120
            )
        
        with col_input2:
            scores_input = st.text_area(
                "Skor (pisahkan dengan koma)\n1=Kurang, 2=Cukup, 3=Baik, 4=Baik Sekali",
                "3, 4, 3, 3, 4",
                height=120
            )
        
        labels = [l.strip() for l in labels_input.split(',') if l.strip()]
        try:
            values = []
            for s in scores_input.split(','):
                s = s.strip()
                if s:
                    if '.' in s:
                        values.append(float(s))
                    else:
                        values.append(int(s))
        except ValueError as e:
            st.error(f"❌ Skor harus berupa angka! Error: {str(e)}")
            values = []
    
    elif "Histogram" in viz_type:
        st.markdown("**Masukkan data (pisahkan dengan koma)**")
        data_input = st.text_area(
            "Data",
            "23, 45, 67, 34, 56, 78, 45, 67, 89, 34, 56, 78, 90, 45, 67, 23",
            height=100
        )
        bins = st.slider("Jumlah Bins", 5, 50, 15)
        
        try:
            data_values = []
            for d in data_input.split(','):
                d = d.strip()
                if d:
                    if '.' in d:
                        data_values.append(float(d))
                    else:
                        data_values.append(int(d))
        except ValueError as e:
            st.error(f"❌ Data harus berupa angka! Error: {str(e)}")
            data_values = []
    
    elif "Grouped" in viz_type or "Stacked" in viz_type:
        st.markdown("**Masukkan kategori dan beberapa kelompok data**")
        
        categories_input = st.text_input(
            "Kategori (pisahkan dengan koma)",
            "Q1, Q2, Q3, Q4"
        )
        categories = [c.strip() for c in categories_input.split(',') if c.strip()]
        
        num_groups = st.number_input("Jumlah Kelompok Data", 2, 5, 3)
        
        data_dict = {}
        for i in range(num_groups):
            col1, col2 = st.columns(2)
            with col1:
                group_name = st.text_input(f"Nama Kelompok {i+1}", f"Series {i+1}", key=f"group_{i}")
            with col2:
                group_values = st.text_input(f"Nilai {group_name} (pisahkan dengan koma)", 
                                            "10, 20, 30, 40", key=f"values_{i}")
            
            try:
                values_list = []
                for v in group_values.split(','):
                    v = v.strip()
                    if v:
                        if '.' in v:
                            values_list.append(float(v))
                        else:
                            values_list.append(int(v))
                
                if len(values_list) == len(categories):
                    data_dict[group_name] = np.array(values_list)
                else:
                    st.warning(f"⚠️ Jumlah nilai untuk {group_name} harus sama dengan jumlah kategori!")
            except ValueError:
                st.error(f"❌ Nilai untuk {group_name} harus berupa angka!")
    
    else:  # Bar charts
        st.markdown("**Masukkan kategori dan nilai (pisahkan dengan koma)**")
        
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            categories_input = st.text_area(
                "Kategori (pisahkan dengan koma)",
                "Sangat Puas, Puas, Cukup, Kurang",
                height=100
            )
        
        with col_input2:
            values_input = st.text_area(
                "Nilai (pisahkan dengan koma)\n1=Kurang, 2=Cukup, 3=Baik, 4=Baik Sekali",
                "4, 3, 3, 2",
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

col_title, col_extra = st.columns([3, 1])

with col_title:
    title_input = st.text_input(
        "Judul Grafik",
        "Hasil Monitoring dan Evaluasi"
    )

with col_extra:
    if "Interactive" in viz_type:
        plotly_chart_type = st.selectbox(
            "Tipe Plotly",
            ["bar", "pie", "radar"]
        )

# Generate visualization
st.markdown('<div class="sub-header">📊 Hasil Visualisasi</div>', unsafe_allow_html=True)

try:
    colors = get_color_palette(color_scheme, custom_color if color_scheme == "Custom" else None)
    
    if "Interactive" in viz_type:
        # Plotly interactive chart
        if len(labels) == len(values) and len(labels) > 0:
            fig = create_plotly_chart(labels, values, title_input, plotly_chart_type)
            st.plotly_chart(fig, use_container_width=True)
            
            # Save as HTML
            buf = io.BytesIO()
            fig.write_html(buf)
            buf.seek(0)
            
            st.download_button(
                label="💾 Download HTML Interaktif",
                data=buf,
                file_name="interactive_chart.html",
                mime="text/html"
            )
        else:
            st.warning("⚠️ Jumlah label dan nilai harus sama!")
    
    elif "Radar" in viz_type:
        if len(labels) == len(values) and len(labels) > 0:
            fig = create_radar_chart(labels, values, title_input, colors, 
                                    fig_width, fig_height, dpi, use_3d_effect, use_gradient,
                                    title_font_size, label_font_size, value_font_size)
            st.pyplot(fig)
            
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
            fig = create_horizontal_bar(categories, values, title_input, colors,
                                       fig_width, fig_height, dpi, use_3d_effect, use_gradient,
                                       title_font_size, label_font_size, value_font_size)
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
            fig = create_vertical_bar(categories, values, title_input, colors,
                                     fig_width, fig_height, dpi, use_3d_effect, use_gradient,
                                     title_font_size, label_font_size, value_font_size)
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
            fig = create_histogram(data_values, bins, title_input, colors,
                                  fig_width, fig_height, dpi, use_gradient,
                                  title_font_size, label_font_size)
            st.pyplot(fig)
            
            # Tambahkan statistik deskriptif
            st.markdown("### 📈 Statistik Deskriptif")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Mean", f"{np.mean(data_values):.2f}")
            with col2:
                st.metric("Median", f"{np.median(data_values):.2f}")
            with col3:
                st.metric("Std Dev", f"{np.std(data_values):.2f}")
            with col4:
                st.metric("Range", f"{np.max(data_values) - np.min(data_values):.2f}")
            
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
            fig = create_pie_chart(labels, values, title_input, colors,
                                  fig_width, fig_height, dpi, use_3d_effect,
                                  title_font_size, label_font_size)
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
            fig = create_grouped_bar(categories, data_dict, title_input, colors,
                                    fig_width, fig_height, dpi, use_gradient,
                                    title_font_size, label_font_size, value_font_size)
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
            fig = create_stacked_bar(categories, data_dict, title_input, colors,
                                    fig_width, fig_height, dpi,
                                    title_font_size, label_font_size, value_font_size)
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
    import traceback
    st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem; 
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px; margin-top: 2rem;'>
    <p style='font-size: 1.2rem; margin-bottom: 1rem;'><strong>📊 Dashboard Visualisasi Monitoring & Evaluasi</strong></p>
    <p style='font-size: 1rem;'>Dibuat dengan ❤️ menggunakan Streamlit, Matplotlib, Seaborn & Plotly</p>
    <p style='margin-top: 1.5rem; font-size: 1rem;'>
        <strong>Developed by:</strong> Tubagus Robbi Megantara<br>
        <a href='mailto:tubagusrobbimegantara@gmail.com' style='color: #667eea; text-decoration: none; font-weight: bold;'>
            📧 tubagusrobbimegantara@gmail.com
        </a>
    </p>
    <p style='margin-top: 1rem; font-size: 0.9rem; color: #95a5a6;'>
        © 2025 - Dashboard Monev Enhanced | Version 2.0
    </p>
</div>
""", unsafe_allow_html=True)
