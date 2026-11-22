# Bike Sharing Analysis Dashboard 🚲

Proyek analisis data eksploratif (*Exploratory Data Analysis*) dan *dashboard* interaktif berbasis **Streamlit** menggunakan **Bike Sharing Dataset** (`day.csv` dan `hour.csv`) untuk periode **2011–2012**.

## Pertanyaan Bisnis
1. **Pola Penyewaan Berdasarkan Jam & Jenis Hari:** Bagaimana perbandingan rata-rata jumlah penyewaan sepeda (`cnt`) per jam pada hari kerja (`workingday`) dibandingkan akhir pekan/hari libur sepanjang periode tahun 2011–2012, dan pada jam berapa puncak permintaannya?
2. **Pengaruh Musim & Kondisi Cuaca Terhadap Penyewaan:** Seberapa besar perbedaan rata-rata total penyewaan sepeda harian (`cnt`) antar musim (`season`) dan kondisi cuaca (`weathersit`) sepanjang tahun 2011–2012?
3. **Tren Bulanan & Komposisi Pengguna (*Casual* vs *Registered*):** Bagaimana tren total penyewaan sepeda bulanan serta proporsi pengguna terdaftar (`registered`) dibandingkan pengguna kasual (`casual`) dari tahun 2011 ke tahun 2012?

## Struktur Direktori
```text
submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   └── bike-sharing-dataset
│       ├── day.csv
│       └── hour.csv
├── Proyek_Analisis_Data.ipynb
├── README.md
└── requirements.txt
```

## Setup Environment & Instalasi
1. Buka terminal dan arahkan direktori kerja ke folder utama proyek (`submission`).
2. Buat dan aktifkan *virtual environment* (opsional namun disarankan):
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Instal seluruh *library* yang dibutuhkan menggunakan `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan Dashboard Streamlit
Jalankan perintah berikut dari folder utama proyek (`submission`):
```bash
streamlit run dashboard/dashboard.py
```
Setelah server berjalan, aplikasi *dashboard* akan terbuka otomatis di *browser* atau dapat diakses melalui tautan lokal `http://localhost:8501`.