# 🚀 Quick Start Guide - Dashboard Monev

**Panduan Cepat 5 Menit untuk Memulai**

---

## 📋 Persiapan (2 menit)

### 1. Download Semua File
Pastikan Anda sudah download:
- ✅ `streamlit_monev_app.py`
- ✅ `requirements.txt`
- ✅ `contoh_data_*.xlsx` (opsional, untuk testing)

### 2. Install Dependencies
Buka terminal/command prompt, masuk ke folder project:

```bash
cd path/to/folder
pip install -r requirements.txt
```

**Catatan:** Jika ada error, coba gunakan:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Aplikasi (30 detik)

Di terminal yang sama, jalankan:

```bash
streamlit run streamlit_monev_app.py
```

✅ **Aplikasi akan otomatis membuka di browser:** `http://localhost:8501`

---

## 🎯 Tutorial Pertama: Buat Radar Chart (2 menit)

### Step 1: Pilih Visualisasi
Di sidebar kiri, pilih: **📡 Radar/Spider Chart**

### Step 2: Input Data
Pada tab **"📋 Input Manual"**, masukkan:

**Labels:**
```
Keselarasan VMTS, Pemanfaatan VMTS, Mekanisme VMTS, Pelibatan Stakeholder
```

**Nilai:**
```
4, 3, 4, 2
```

### Step 3: Atur Tampilan
- **Judul:** Ketercapaian VMTS Program Studi
- **Skema Warna:** Biru Profesional (atau pilih yang lain)
- **Ukuran:** Biarkan default (12 x 8)

### Step 4: Lihat Hasil
Scroll ke bawah, grafik akan muncul otomatis! 🎉

### Step 5: Download
Klik tombol **"💾 Download PNG"** untuk menyimpan grafik.

---

## 📊 Tutorial Kedua: Upload Excel (1 menit)

### Step 1: Gunakan File Contoh
Gunakan file `contoh_data_radar.xlsx` yang sudah disediakan

### Step 2: Upload
- Klik tab **"📁 Upload Excel"**
- Klik tombol upload dan pilih file Excel (.xlsx atau .xls)
- Pilih kolom "Indikator" untuk Labels
- Pilih kolom "Skor" untuk Nilai

### Step 3: Selesai!
Grafik langsung muncul, tinggal download! ✅

**💡 Catatan:** File Excel harus punya header di baris pertama!

---

## 🎨 Tips Kustomisasi

### Untuk Presentasi:
- **Ukuran:** 16 x 12
- **DPI:** 150
- **Format:** PNG
- **Warna:** Biru Profesional

### Untuk Print:
- **Ukuran:** 12 x 8
- **DPI:** 300
- **Format:** PDF
- **Warna:** Sesuai brand

### Untuk Web:
- **Ukuran:** 10 x 6
- **DPI:** 100
- **Format:** PNG
- **Warna:** Custom (sesuai tema web)

---

## 🎯 Jenis Visualisasi & Kapan Menggunakannya

| Visualisasi | Gunakan Untuk | Contoh |
|-------------|---------------|---------|
| 📡 **Radar Chart** | Multi-indikator, perbandingan aspek | Ketercapaian VMTS 8 aspek |
| 📊 **Bar Chart** | Perbandingan kategori | Pemahaman Dosen vs Mahasiswa |
| 📉 **Histogram** | Distribusi data | Sebaran nilai ujian |
| 🥧 **Pie Chart** | Proporsi/komposisi | Alokasi anggaran |
| 📊 **Grouped Bar** | Perbandingan multi-periode | Semester 1 vs 2 vs 3 |
| 📚 **Stacked Bar** | Komposisi total per kategori | Target vs Realisasi |

---

## ❓ Troubleshooting Cepat

### Error: "float object cannot be interpreted as an integer"
✅ **SUDAH DIPERBAIKI!** Update ke versi terbaru.

### Grafik tidak muncul?
- Cek apakah jumlah Labels = jumlah Nilai
- Pastikan nilai berupa angka, bukan teks
- Coba refresh halaman (F5)

### Download tidak berfungsi?
- Tunggu hingga grafik muncul sempurna
- Coba format lain (PNG → PDF)
- Cek permission browser

### Aplikasi crash?
- Tutup dan jalankan ulang
- Cek apakah ada typo di input
- Pastikan semua library terinstall

---

## 📱 Contact & Support

**Developer:** Tubagus Robbi Megantara  
**Email:** tubagusrobbimegantara@gmail.com  

💡 **Ada pertanyaan atau request fitur?** Kirim email!

---

## 🎯 Next Steps

Setelah mahir, coba:
1. ✅ Buat visualisasi untuk semua jenis chart
2. ✅ Upload data real dari project Anda
3. ✅ Ekspor dalam berbagai format
4. ✅ Kombinasikan beberapa chart untuk laporan
5. ✅ Customize warna sesuai branding institusi

---

**Selamat menggunakan! 🎉**

*Dashboard Monev v1.0.1 - Tubagus Robbi Megantara - 2025*
