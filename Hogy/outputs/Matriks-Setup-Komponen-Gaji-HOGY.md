# Matriks Setup Komponen Gaji HOGY

Matriks ini menentukan penempatan sumber nilai komponen pada kontrak individu atau komponen gaji payroll. Kolom Setup dan Alasan Setup merupakan usulan penempatan. Kolom Upah, Kriteria Posisi / Jabatan, Nilai, dan Fix Value / Formula mengikuti isi sumber.

## Matriks komponen

| No. | Komponen | Upah | Kriteria Posisi / Jabatan | Nilai | Fix Value / Formula | Setup | Alasan Setup |
|---:|---|---|---|---|---|---|---|
| 1 | Basic Salary | Ya | Sub Leader UP | input sesuai jabatan | Fix / bln | Kontrak | Nominal gaji pokok ditetapkan untuk individu. |
| 2 | Basic Salary | Ya | Operator - koordinator | input sesuai tabel gaji | Fix / bln | Kontrak | Nominal hasil penetapan tabel gaji individu. Menggunakan satu field dengan No. 1. |
| 3 | Tunjangan | — | — | — | — | — | Judul kelompok. |
| 4 | Kehadiran | Tidak | Operator - koordinator | angka fix | Formula | Komponen gaji | Pembayaran mengikuti formula kehadiran. |
| 5 | Haid | Tidak | All empoloyee | angka fix | Formula | Komponen gaji | Mengikuti rate dan kondisi pembayaran. |
| 6 | Makan | Tidak | All empoloyee | Sesuai kehadiran | Formula | Komponen gaji | Nilai mengikuti kehadiran dan rate makan. |
| 7 | Transport | — | — | — | — | — | Judul kelompok. |
| 8 | Transport I. Allowance | Tidak | Operator - Foreman/Chief | 12,190 | Formula | Komponen gaji | Rate umum dikalikan unit eligible. |
| 9 | Transport I.1. Allowance | Tidak | All empoloyee | 13,190 | Formula | Komponen gaji | Rate umum berdasarkan kondisi penerima. |
| 10 | Transport II. Fix transport | Tidak | Supervisor UP | angka fix | Fix / bln | Kontrak | Usulan nominal bulanan individu. Jika seragam per jabatan, gunakan komponen gaji. |
| 11 | Transport III. Lembur Spv up | Tidak | Supervisor - Asr Manager | Sesuai jml lembur | Formula | Komponen gaji | Nilai mengikuti realisasi lembur. |
| 12 | Shift 2 | Tidak | All empoloyee | 7,000 | Formula | Komponen gaji | Rate umum mengikuti shift aktual. |
| 13 | Penanggung jawab Shift | Tidak | Koord - Spv | Sesuai schedule | Formula | Komponen gaji | Nilai mengikuti penugasan aktual. |
| 14 | Dukacita | Tidak | All empoloyee | 800,000 | Fix value | Komponen gaji | Nominal umum, dibayar berdasarkan pengajuan/upload. |
| 15 | Sukacita (Kelahiran) | Tidak | All empoloyee | 1,000,000 | Fix value | Komponen gaji | Nominal umum, dibayar berdasarkan pengajuan/upload. |
| 16 | Extra meal | Tidak | All empoloyee | 20,000 | Fix value | Komponen gaji | Pembayaran berdasarkan upload/kejadian, bukan nominal kontrak individu. |
| 17 | Meal Ramadhan | Tidak | All empoloyee | Sesuai kehadiran | Formula | Komponen gaji | Nilai mengikuti kehadiran pada periode terkait. |
| 18 | Kacamata | Tidak | All empoloyee | 500,000 | Fix value | Komponen gaji | Pembayaran berdasarkan pengajuan. Konfirmasi nominal tetap atau plafon. |
| 19 | Komunikasi | Tidak | Spv - GM | Sesuai ketentuan | Formula | Komponen gaji | Sumber menyebut formula. Jika nominal khusus individu, dapat dipindahkan ke kontrak. |
| 20 | Position Allow | Ya | Adm Up | input sesuai jabatan | Fix / bln | Kontrak | Usulan nominal tunjangan jabatan individu. |
| 21 | Incentive | Ya | Operator - koordinator | input sesuai tabel gaji | Fix / bln | Kontrak | Nominal tetap hasil penetapan tabel gaji individu. |
| 22 | Perumahan | Ya | All empoloyee | 60,000 | Fix / bln | Komponen gaji | Nominal umum untuk penerima yang eligible. |
| 23 | keluarga | Ya | All empoloyee | 60,000 | Fix / bln | Komponen gaji | Nominal umum dengan kondisi keluarga terkait. |
| 24 | anak | Ya | All empoloyee | 40,000 | Fix / bln | Komponen gaji | Rate umum; perlu konfirmasi per anak atau total. |
| 25 | keluarga (janda) | Ya | All empoloyee | 40,000 | Fix / bln | Komponen gaji | Nominal umum untuk penerima sesuai kriteria. |
| 26 | Tunjangan pajak | Tidak | All empoloyee | Sesuai bruto | Formula | Komponen gaji | Nilai merupakan hasil kalkulasi pajak. |
| 27 | Asuransi Kesehatan swasta | Tidak | All empoloyee | Sesuai jumlah upah | Formula | Komponen gaji | Nilai mengikuti basis upah dan policy asuransi. |
| 28 | BPJS kes | Tidak | All empoloyee | Sesuai jumlah upah | Formula | Komponen gaji | Nilai dihitung berdasarkan basis dan rule iuran. |
| 29 | BPJS TK | Tidak | All empoloyee | Sesuai jumlah upah | Formula | Komponen gaji | Nilai dihitung per program dan porsi iuran. |
| 30 | Adustment | Tidak | All empoloyee | Sesuai jumlah koreksi | Fix | Komponen gaji | Input nominal koreksi aktual melalui transaksi/upload. |
| 31 | Bonus | Tidak | All empoloyee | Sesuai ketentuan | Formula | Komponen gaji | Kalkulasi atau upload pada saat pembayaran bonus. |
| 32 | THR | Tidak | All empoloyee | Sesuai jumlah upah | Fix | Komponen gaji | Pembayaran periode THR; sumber menyebut upload. |
| 33 | Allowance USD ( tunjangan USD ) | Tidak | Ekspatriat | Sesuai ketentuan | Fix / bln | Kontrak | Usulan nominal tunjangan USD bulanan individu. |
| 34 | Sales insentif | Tidak | Sales | Sesuai ketentuan | Fix / bln | Kontrak | Mengikuti keterangan Fix/bln. Jika berdasarkan pencapaian, pindahkan ke komponen gaji. |
| 35 | Tunjangan skil ( transleter, PJT ) | Tidak | Transleter & PJT | Sesuai ketentuan | Fix / bln | Kontrak | Usulan nominal individu. Jika tarif seragam per skill, gunakan komponen gaji. |
| 36 | Leave paid | Tidak | All empoloyee | Sesuai sisa cuti | Formula | Komponen gaji | Hasil perhitungan berdasarkan saldo cuti yang diuangkan. |
| 37 | Potongan koperasi | Tidak | All empoloyee | Sesuai tabel upload | Fix | Komponen gaji | Input potongan aktual setiap bulan dari koperasi. |
| 38 | Pesangon | — | — | — | — | — | Judul kelompok. |
| 39 | Pesangon - Mengundurkan diri | Tidak | All empoloyee | Sesuai ketentuan | Formula | Komponen gaji | Perhitungan settlement berdasarkan kejadian keluar. |
| 40 | Pesangon - PHK | Tidak | All empoloyee | Sesuai ketentuan | Formula | Komponen gaji | Perhitungan settlement berdasarkan alasan PHK. |
| 41 | Pesangon - Pension | Tidak | All empoloyee | Sesuai ketentuan | Formula | Komponen gaji | Perhitungan settlement saat pensiun. |
| 42 | Pesangon - Pension dini | Tidak | All empoloyee | Sesuai ketentuan | Formula | Komponen gaji | Perhitungan settlement saat pensiun dini. |
| 43 | Uang kompensasi | Tidak | All empoloyee | Sesuai ketentuan | Fix | Komponen gaji | Input/upload hasil kompensasi sesuai kejadian terkait. |
| 44 | Potongan absen | Tidak | Operator - Spv | Sesuai ketentuan | Formula | Komponen gaji | Nilai mengikuti realisasi absen dan formula potongan. |
| 45 | Prorate | Tidak | All empoloyee | Sesuai kehadiran | Formula | Komponen gaji | Mekanisme perhitungan nilai proporsional. |
| 46 | Over time | Tidak | Operator - Spv | Sesuai ketentuan | Formula | Komponen gaji | Nilai mengikuti realisasi lembur dan formula. |
| 47 | COS serikat pekerja | Tidak | All empoloyee | Sesuai tabel upload | Fix | Komponen gaji | Input potongan aktual berdasarkan data serikat. |
| 48 | Incentive Tax | Tidak | Sesuai kategori | Sesuai ketentuan | Formula | Komponen gaji | Nilai mengikuti rule dan eligibility program terkait. |
| 49 | Rapel Incentive Tax | Tidak | Sesuai kategori | Sesuai ketentuan | Formula | Komponen gaji | Koreksi perhitungan terkait periode asal. |
| 50 | Tax Natura | Tidak | BOD & Ekspatriat | Sesuai ketentuan | Fix | Komponen gaji | Input/upload nilai aktual; bukan nominal bulanan kontrak. |
| 51 | Other Bank | Tidak | All empoloyee | 9,000 | Fix | Komponen gaji | Nominal umum dengan pemicu pembayaran/potongan yang perlu dikonfirmasi. |
| 52 | Bonus Direksi (Deviden) | Tidak | BOD | Sesuai nilai bonus | Fix | Komponen gaji | Input nominal approved. Jika substansinya dividen, arahkan ke proses finance. |
| 53 | UO (Utility Operator) | Tidak | Operator | Sesuai ketentuan | Fix / bln | Kontrak | Usulan nominal individu. Jika tarif seragam untuk seluruh UO, gunakan komponen gaji. |

## Ringkasan setup

| Setup | Jumlah baris | Keterangan |
|---|---:|---|
| Kontrak | 9 | Menjadi 8 jenis field karena No. 1 dan 2 menggunakan satu field Basic Salary. |
| Komponen gaji | 41 | Termasuk rate umum, formula, serta input transaksi/upload payroll. |
| Judul kelompok | 3 | No. 3 Tunjangan, No. 7 Transport, dan No. 38 Pesangon. |
| Total | 53 | Terdiri dari 50 komponen detail dan 3 judul kelompok. |

## Ketentuan pembacaan

- Setup menunjukkan tempat sumber nilai. Komponen yang nominalnya disimpan di kontrak tetap direferensikan oleh komponen payroll saat perhitungan gaji.
- Kriteria posisi/jabatan menentukan kelompok penerima; tidak otomatis menentukan bahwa nominal harus disimpan di kontrak.
- Nominal khusus individu ditempatkan di kontrak. Nominal/rate umum, tabel, formula, dan transaksi aktual ditempatkan pada komponen gaji.
- Status tetap atau tidak tetap menurut kebijakan HOGY berbeda dari penempatan sumber nilai pada matriks ini.
- Kolom Upah disalin dari sumber. Maknanya tidak diasumsikan sebagai penanda dasar pajak.
- Kriteria pada matriks perlu dibaca bersama kolom Keterangan di sumber; tulisan All empoloyee tidak selalu berarti seluruh karyawan menerima komponen.
- Tanda — menunjukkan kolom sumber kosong atau baris judul kelompok.

## Referensi

Salary Componen (Penjelasan).xlsx, sheet Sheet1, range A5:J57. Nomor mengikuti kolom NO sumber; nama komponen pada baris turunan diberi konteks Transport/Pesangon agar dapat dibaca mandiri.
