# 📊 Dashboard Visualisasi Monitoring & Evaluasi

Aplikasi web interaktif untuk membuat visualisasi data monitoring dan evaluasi dengan berbagai jenis plot yang dapat dikustomisasi dan diunduh.

## ✨ Fitur Utama

### 🎯 Jenis Visualisasi yang Tersedia:
1. **📡 Radar/Spider Chart** - Untuk menampilkan multi-indikator dalam bentuk radar
2. **📊 Bar Chart Horizontal** - Grafik batang horizontal untuk perbandingan kategori
3. **📈 Bar Chart Vertikal** - Grafik batang vertikal dengan nilai di atas batang
4. **📉 Histogram** - Distribusi data dengan kurva densitas
5. **🥧 Pie Chart** - Diagram lingkaran dengan persentase
6. **📊 Grouped Bar Chart** - Perbandingan multi-grup dalam satu kategori
7. **📚 Stacked Bar Chart** - Grafik batang bertumpuk

### 🎨 Kustomisasi:
- ✅ Pilihan skema warna (Biru, Hijau, Ungu, Merah, atau Custom)
- ✅ Atur ukuran gambar (lebar & tinggi)
- ✅ Pilih resolusi (DPI: 100-300)
- ✅ Edit judul grafik
- ✅ Input data manual atau upload Excel (.xlsx, .xls)

### 💾 Download Options:
- PNG (High Quality)
- PDF (Vector Format)
- SVG (Scalable Vector Graphics)

## 🚀 Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
streamlit run streamlit_monev_app.py
```

### 3. Buka Browser
Aplikasi akan otomatis terbuka di browser pada alamat:
```
http://localhost:8501
```

## 📝 Cara Menggunakan

### Input Data Manual:

#### Untuk Radar Chart / Pie Chart:
1. Pilih jenis visualisasi di sidebar
2. Masukkan **Labels** (pisahkan dengan koma)
   - Contoh: `Keselarasan VMTS, Pemanfaatan VMTS, Mekanisme VMTS`
3. Masukkan **Nilai** (pisahkan dengan koma)
   - Contoh: `4, 3, 4`
4. Atur judul dan pengaturan tampilan
5. Klik tombol Download untuk menyimpan

#### Untuk Bar Chart:
1. Pilih Bar Chart (Horizontal/Vertikal)
2. Masukkan **Kategori**
   - Contoh: `Dosen, Mahasiswa, Tendik`
3. Masukkan **Nilai**
   - Contoh: `88, 72, 85`
4. Kustomisasi warna dan ukuran
5. Download hasil visualisasi

#### Untuk Histogram:
1. Pilih Histogram
2. Masukkan **Data** (nilai-nilai numerik pisahkan dengan koma)
   - Contoh: `65, 70, 75, 80, 85, 90, 72, 68, 88, 92`
3. Atur jumlah bins (5-30)
4. Download dalam format yang diinginkan

#### Untuk Grouped/Stacked Bar:
1. Pilih jenis chart
2. Masukkan **Kategori**
3. Tentukan jumlah grup data
4. Isi nama dan nilai untuk setiap grup
5. Visualisasi otomatis ter-generate

### Upload Excel:

#### Format Excel yang Didukung:

**Untuk Radar/Pie/Bar Chart:**

| Indikator | Skor |
|-----------|------|
| Keselarasan VMTS | 4 |
| Pemanfaatan VMTS | 3 |
| Mekanisme VMTS | 4 |
| Pelibatan Stakeholder | 2 |

**Untuk Histogram:**

| Nilai |
|-------|
| 65 |
| 70 |
| 75 |
| 80 |
| 85 |

**Untuk Grouped/Stacked Bar:**

| Kategori | Grup1 | Grup2 | Grup3 |
|----------|-------|-------|-------|
| Dosen | 85 | 90 | 75 |
| Mahasiswa | 75 | 80 | 70 |
| Tendik | 80 | 85 | 72 |

#### Langkah Upload:
1. Klik tab "📁 Upload Excel"
2. Upload file Excel Anda (.xlsx atau .xls)
3. Pilih kolom untuk Label dan Nilai
4. Visualisasi otomatis dibuat
5. Download sesuai kebutuhan

**💡 Tips:**
- Pastikan file Excel memiliki **header di baris pertama**
- Gunakan format **.xlsx** (Excel 2007+) untuk kompatibilitas terbaik
- Data harus dalam bentuk tabel yang rapi (tidak ada merged cells)
- File contoh disediakan untuk referensi

## 🎨 Pengaturan Tampilan

### Di Sidebar:
- **Skema Warna**: Pilih dari 5 opsi atau buat custom
- **Lebar Gambar**: 8-20 (default: 12)
- **Tinggi Gambar**: 6-18 (default: 8)
- **Resolusi (DPI)**: 100-300 (default: 150)
- **Format Download**: PNG/PDF/SVG

### Tips Ukuran:
- **Presentasi**: 12x8, DPI 150
- **Print Quality**: 16x12, DPI 300
- **Web Display**: 10x6, DPI 100

## 📊 Contoh Penggunaan

### Contoh 1: Radar Chart VMTS
```
Labels: Keselarasan VMTS, Pemanfaatan VMTS, Mekanisme VMTS, Pelibatan Stakeholder, Pemahaman Dosen, Pemahaman Mahasiswa, Pemahaman Tendik, Evaluasi VMTS

Nilai: 4, 3, 4, 2, 3, 2, 3, 2

Judul: Ketercapaian VMTS Program Studi
Warna: Biru Profesional
Ukuran: 16x16
DPI: 150
```

### Contoh 2: Bar Chart Horizontal
```
Kategori: Dosen, Mahasiswa, Tenaga Kependidikan

Nilai: 88, 72, 85

Judul: Tingkat Pemahaman VMTS oleh Sivitas Akademika
Warna: Hijau Natural
Ukuran: 12x7
DPI: 150
```

### Contoh 3: Histogram Nilai
```
Data: 65, 70, 75, 80, 85, 90, 72, 68, 88, 92, 78, 82, 76, 84, 79, 73, 87, 91, 69, 81

Bins: 10
Judul: Distribusi Nilai Mahasiswa
Warna: Ungu Elegan
Ukuran: 12x7
DPI: 200
```

## 🔧 Troubleshooting

### Error: "Jumlah label dan nilai harus sama!"
**Solusi**: Pastikan jumlah item di Labels sama dengan jumlah item di Nilai.
- Labels: 4 item → Nilai: harus 4 item juga

### Error saat Upload Excel
**Solusi**: 
1. Pastikan file berformat .xlsx atau .xls
2. Cek apakah ada merged cells (harus di-unmerge)
3. Pastikan ada header kolom di baris pertama
4. Jangan ada sheet kosong atau data di multiple sheets
5. Install openpyxl: `pip install openpyxl`

### Grafik tidak muncul
**Solusi**:
1. Refresh halaman (F5)
2. Cek apakah data sudah diinput dengan benar
3. Pastikan tidak ada karakter spesial di input

### Download tidak berfungsi
**Solusi**:
1. Pastikan grafik sudah ter-generate
2. Coba format download yang berbeda
3. Cek izin download di browser

## 📚 Teknologi yang Digunakan

- **Streamlit** - Framework web app
- **Matplotlib** - Library visualisasi utama
- **Seaborn** - Styling dan tema
- **Pandas** - Manipulasi data & read Excel
- **NumPy** - Komputasi numerik
- **SciPy** - Statistical functions
- **OpenPyXL** - Excel file support (.xlsx)

## 💡 Tips & Trik

1. **Untuk Presentasi**: Gunakan DPI 150-200 dengan format PNG
2. **Untuk Publikasi**: Gunakan DPI 300 dengan format PDF atau SVG
3. **Untuk Web**: Gunakan DPI 100-150 dengan format PNG
4. **Warna Custom**: Gunakan color picker untuk brand matching
5. **Multiple Charts**: Buat beberapa visualisasi, download semua, lalu gabungkan di PowerPoint/Word

## 🎯 Use Cases

### 1. Laporan Monev Akademik
- Radar chart untuk ketercapaian indikator
- Bar chart untuk perbandingan antar unit
- Histogram untuk distribusi nilai

### 2. Presentasi Stakeholder
- Pie chart untuk proporsi anggaran
- Grouped bar untuk perbandingan multi-periode
- Stacked bar untuk komposisi total

### 3. Evaluasi Kinerja
- Radar chart untuk multi-aspek penilaian
- Bar chart horizontal untuk ranking
- Histogram untuk sebaran performa

## 📞 Support & Feedback

Jika menemukan bug atau punya saran fitur baru, silakan buat issue atau hubungi tim pengembang.

## 👨‍💻 Developer

**Tubagus Robbi Megantara**  
📧 Email: tubagusrobbimegantara@gmail.com

---

**Dibuat dengan ❤️ untuk Monitoring & Evaluasi yang lebih baik**  
© 2025 - Dashboard Monev v1.0
