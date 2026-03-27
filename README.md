# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan Jaya Jaya Institut

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Meskipun telah mencetak banyak lulusan dengan reputasi baik, institusi ini menghadapi masalah serius berupa tingginya angka dropout mahasiswa. Dari 4.424 mahasiswa dalam dataset, sebanyak 1.421 mahasiswa (32.1%) berstatus dropout.

### Permasalahan Bisnis

1. Tingginya angka dropout mahasiswa (32.1%) yang berdampak pada reputasi dan keberlanjutan institusi.
2. Belum adanya sistem deteksi dini untuk mengidentifikasi mahasiswa yang berisiko dropout.
3. Tidak adanya dashboard monitoring yang memudahkan pemantauan performa mahasiswa.
4. Belum optimalnya alokasi sumber daya untuk program bimbingan dan retensi mahasiswa.

### Cakupan Proyek

1. Eksplorasi dan analisis data untuk memahami pola dropout.
2. Pembangunan model machine learning (Random Forest) untuk memprediksi status mahasiswa.
3. Pembuatan business dashboard untuk monitoring performa mahasiswa.
4. Deployment prototype sistem prediksi menggunakan Streamlit.

### Persiapan

Sumber data: [Students' Performance Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv)  
Dataset berisi 4.424 baris dan 37 kolom (36 fitur + 1 target), dengan delimiter `;`.

**Setup environment:**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib streamlit
```

## Business Dashboard

Dashboard interaktif telah dibuat menggunakan HTML + Chart.js dan tersedia di folder `defanggaabypn-dashboard/index.html`. Dashboard memuat 8 visualisasi utama:

- **Distribusi Status Mahasiswa** — donut chart proporsi Dropout, Graduate, Enrolled
- **Dropout Rate per Program Studi** — identifikasi prodi paling berisiko
- **Performa Akademik per Semester** — perbandingan nilai rata-rata antar status
- **Mata Kuliah Lulus per Semester** — rata-rata MK yang disetujui
- **Faktor Finansial** — pengaruh pembayaran biaya, beasiswa, dan tunggakan
- **Distribusi Gender** — pola dropout berdasarkan jenis kelamin
- **Distribusi Usia** — perbandingan usia dropout vs graduate
- **Status Perkawinan** — distribusi status mahasiswa per kategori

Untuk mengakses dashboard, buka file `defanggaabypn-dashboard/index.html` di browser.

> **Metabase (alternatif):** Jika menggunakan Metabase, jalankan dengan Docker dan ekspor database dengan:
> ```bash
> docker cp metabase:/metabase.db/metabase.db.mv.db ./
> ```
> Email: `root@mail.com` | Password: `root123`

## Menjalankan Sistem Machine Learning

Prototype sistem machine learning dibuat menggunakan Streamlit dan dapat dijalankan secara lokal maupun melalui Streamlit Community Cloud.

**Jalankan secara lokal:**
```bash
streamlit run app.py
```

**Akses via Streamlit Community Cloud:**  
[https://nurk4wczjzgbrqzeu7re2m.streamlit.app](https://nurk4wczjzgbrqzeu7re2m.streamlit.app)

Prototype ini memiliki dua tab:
1. **Prediksi Individual** — form input data mahasiswa untuk mendapatkan prediksi status beserta probabilitas dropout/graduate
2. **Informasi Model** — detail performa model dan faktor-faktor terpenting

## Conclusion

Berdasarkan analisis data dan hasil model machine learning, diperoleh beberapa kesimpulan:

1. **Model prediksi** menggunakan Random Forest berhasil mencapai accuracy **91.05%** dan ROC-AUC **0.9542**, menunjukkan kemampuan deteksi dini yang sangat baik.

2. **Faktor akademik adalah prediktor terkuat** — jumlah mata kuliah yang disetujui di semester 2 memiliki feature importance tertinggi (25.4%), diikuti semester 1 (13.4%) dan nilai rata-rata kedua semester.

3. **Faktor finansial sangat kritis** — mahasiswa yang belum melunasi biaya kuliah memiliki dropout rate 86.6%, sedangkan penerima beasiswa hanya 12.2%.

4. **Semester 1 adalah periode kritis** — sinyal dropout sudah terlihat sejak semester pertama. Deteksi dan intervensi dini di tahap ini dapat mencegah dropout secara signifikan.

5. **Program studi Biofuel Production Technologies** memiliki dropout rate tertinggi (66.7%), diikuti Equinculture (55.3%) dan Informatics Engineering (54.1%).

6. **Mahasiswa dengan usia lebih tua** (rata-rata 26 tahun) lebih rentan dropout dibanding mahasiswa muda (rata-rata 22 tahun untuk graduate), kemungkinan karena tekanan ganda antara pekerjaan dan kuliah.

### Rekomendasi Action Items

1. **Implementasi Early Warning System** — gunakan model prediksi ini untuk memantau mahasiswa secara otomatis sejak awal semester 1. Mahasiswa dengan probabilitas dropout di atas 60% perlu segera mendapat perhatian khusus dari dosen pembimbing.

2. **Program bantuan finansial darurat** — buat skema cicilan biaya kuliah yang fleksibel dan perluas kuota beasiswa, terutama untuk mahasiswa yang terindikasi kesulitan finansial (belum lunas, debitur).

3. **Intervensi akademik di semester 1** — sediakan program tutorial, bimbingan belajar, dan mentoring intensif bagi mahasiswa yang gagal lulus lebih dari 3 mata kuliah di semester pertama.

4. **Review kurikulum program studi risiko tinggi** — program seperti Biofuel Production Technologies, Equinculture, dan Informatics Engineering membutuhkan evaluasi menyeluruh pada beban studi, metode pengajaran, dan relevansi materi.

5. **Program khusus mahasiswa dewasa/pekerja** — mahasiswa berusia di atas 25 tahun sering memiliki beban ganda. Pertimbangkan kelas malam, hybrid learning, atau program part-time yang lebih fleksibel.

6. **Monitoring dashboard rutin** — gunakan dashboard yang dibuat untuk review bulanan oleh pihak manajemen institusi, sehingga tren performa mahasiswa dapat dipantau dan respons kebijakan dapat dilakukan lebih cepat.
