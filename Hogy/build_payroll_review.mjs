import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
const require=createRequire('C:/Users/SAYID/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const {Workbook,SpreadsheetFile}=require('@oai/artifact-tool');
const setup=JSON.parse(await fs.readFile('payroll_setup_extract.json','utf8'));
const rules=JSON.parse(await fs.readFile('payroll_rules_extract.json','utf8'));
const spec=`1|14:15|Gaji pokok = nominal kontrak aktif sesuai tanggal berlaku dan kelompok jabatan.|Batas jabatan setup dan HI berbeda; tetapkan mapping level.|Konfirmasi level
2|14:15|Gaji pokok = nominal kontrak yang ditetapkan dari tabel gaji operator yang berlaku.|Tabel gaji belum tersedia; cegah dua Basic Salary terbayar.|Konfirmasi level
3||Judul kelompok, tidak menghasilkan pembayaran.|Pertahankan sebagai struktur daftar.|Judul kelompok
4|31|Tunjangan kehadiran = nominal parameter untuk karyawan tetap Operator–Koordinator–Adm yang memenuhi syarat kehadiran.|Nominal dan kondisi gugur belum disebutkan.|Perlu parameter
5|32|Tunjangan haid = nominal parameter bagi wanita Operator–Spv, karyawan tetap yang diangkat sebelum 2016, sesuai memo yang dirujuk HI.|Kriteria all employee di setup terlalu luas; memo belum tersedia.|Konflik eligibility
6|33:34|Uang makan = jumlah kehadiran eligible × tarif makan untuk Security, Driver dan Sales; kelompok lain menerima katering.|Tarif belum ada; jangan bayar tunai sekaligus katering.|Perlu parameter
7||Judul kelompok, tidak menghasilkan pembayaran.|Pisahkan jenis transport dalam detail.|Judul kelompok
8|27:28|Transport I = Rp12.190 × jumlah unit kehadiran eligible setelah unit tarif disepakati; eligibility mengikuti mapping jabatan HI.|Unit harian belum eksplisit; Spv ke atas hanya bila tidak mengambil kendaraan inventaris.|Perlu konfirmasi unit
9|27:28|Transport I.1 = Rp13.190 × jumlah unit eligible setelah kategori penerima dan unit tarif ditetapkan.|HI tidak membedakan tarif I dan I.1; cegah duplikasi.|Perlu mapping tarif
10|25:26|Fixed transport = nominal kontrak aktif untuk Staff Office dan Spv–Pres Dir yang eligible.|Setup hanya Supervisor ke atas; Staff Office perlu dikonfirmasi.|Konflik eligibility
11|38,51:52|Tunjangan hari libur = hari masuk libur approved × Rp125.000 untuk Spv atau Rp150.000 untuk Ast Man, bila komponen ini dipastikan mewakili tunjangan hari libur HI.|Nama transport lembur belum pasti sama dengan tunjangan hari libur.|Perlu mapping komponen
12|39|Tunjangan shift 2 = jumlah shift 2 eligible × Rp7.000 untuk Operator.|Setup all employee berbeda dari HI Operator.|Konflik eligibility
13|40|Tunjangan penanggung jawab shift = jumlah shift 2 eligible × tarif jabatan untuk Sub Leader–Leader.|Setup Koord–Spv berbeda; tarif belum tersedia.|Konflik eligibility
14|36|Bayarkan nilai dukacita approved; referensi master Rp800.000 per kejadian setelah unit disepakati.|Bukti dan batas kejadian perlu ditetapkan.|Konfirmasi unit
15|37|Bayarkan nilai sukacita kelahiran approved; referensi master Rp1.000.000 per kejadian setelah unit disepakati.|HI hanya menyebut sukacita; pastikan cakupan kelahiran.|Konfirmasi cakupan
16||Bayarkan nominal extra meal approved; bila input berupa jumlah, jumlah eligible × Rp20.000 setelah unit tarif disepakati.|Rule extra meal tidak dijelaskan HI.|Perlu rule
17||Meal Ramadhan = kehadiran eligible pada periode Ramadhan × tarif yang disepakati.|Periode, tarif dan pengganti katering belum ditetapkan.|Perlu rule
18|35|Bayarkan klaim kacamata approved untuk karyawan tetap; gunakan Rp500.000 sesuai keputusan apakah nominal tetap atau plafon.|Siklus klaim dan arti Rp500.000 belum jelas.|Perlu parameter
19|22:24|Tunjangan komunikasi = tarif kelompok untuk Staff Sales, Koordinator BUS dan Spv–GM yang eligible.|Setup belum mencakup Staff Sales dan Koordinator BUS; tarif belum ada.|Konflik eligibility
20|16|Position allowance = nominal kontrak aktif untuk Adm–GM yang eligible.|Setup Adm Up lebih luas dari HI; pastikan batas GM.|Konfirmasi level
21|17|Incentive/TMK = nominal kontrak aktif berdasarkan tabel gaji bagi Operator sesuai mapping level yang disepakati.|Setup sampai Koordinator, HI hanya Operator.|Konflik eligibility
22|19|Tunjangan perumahan = Rp60.000 per bulan bagi karyawan tetap Operator–Pres Dir yang eligible.|Setup all employee; pastikan status tetap dan level.|Konfirmasi eligibility
23|18|Tunjangan keluarga = Rp60.000 per bulan bila status keluarga memenuhi ketentuan.|HI tidak merinci status keluarga atau kombinasi dengan tunjangan janda.|Perlu rule keluarga
24|18|Tunjangan anak = Rp40.000 per bulan sesuai skema yang disetujui; bila per anak, kalikan jumlah anak eligible.|Belum jelas per anak atau total serta batas anak.|Perlu rule keluarga
25|18|Tunjangan keluarga janda = Rp40.000 per bulan bagi penerima yang memenuhi status keluarga yang disetujui.|Tentukan eksklusivitas dengan tunjangan keluarga biasa.|Perlu rule keluarga
26|63:64|Tunjangan pajak = nilai pajak yang ditanggung perusahaan sesuai metode pajak yang disetujui.|Ditanggung perusahaan belum berarti gross-up; metode belum diputuskan.|Perlu metode pajak
27|93|Premi asuransi swasta = nilai premi sesuai polis bagi karyawan tetap Operator–Vice Pres.|HI tidak menetapkan tarif maupun pembagian beban.|Perlu polis
28|86:91|Dasar BPJS Kesehatan = BS + tunjangan tetap yang dipetakan; bagian perusahaan 4% dan karyawan 1% dari dasar yang telah disesuaikan batas berlaku.|Pisahkan beban perusahaan dan potongan karyawan; batas upah belum ada di HI.|Perlu batas upah
29|74:83|Dasar BPJS TK = BS + tunjangan tetap yang dipetakan. Perusahaan: JKK 0,24%, JKM 0,3%, JHT 3,7%, JP 2%. Karyawan: JHT 2%, JP 1%. Terapkan batas dasar per program yang disetujui.|Satu komponen perlu rincian program dan pihak penanggung; batas JP belum tersedia.|Perlu rincian program
30||Adjustment = nilai koreksi approved dengan tanda tambah atau kurang dan referensi periode asal.|Jangan mengubah nominal kontrak lewat koreksi payslip.|Perlu kontrol upload
31||Bonus = nominal bonus approved per karyawan dan periode.|HI tidak menjelaskan formula bonus.|Upload approved
32|95:96|THR dibayar sebesar nominal upload approved; basis kontrol HI adalah BS + tunjangan tetap, dibayar maksimal satu minggu sebelum hari raya.|Masa kerja, proporsi dan eligibility belum dirinci; tetap gunakan upload awal.|Upload approved
33||Allowance USD = nominal USD kontrak aktif; konversi dengan kurs dan tanggal kurs yang disetujui bila payroll dibayar rupiah.|HI tidak memuat kurs atau perlakuan mata uang.|Perlu kurs
34||Sales incentive = nominal tetap kontrak aktif sesuai setup awal.|Bila berbasis pencapaian, perlu rule dan data penjualan terpisah.|Konfirmasi skema
35|29:30|Tunjangan skill = nominal kontrak aktif untuk Staff PJT atau Staff Interpreter sesuai penugasan.|HI menyebut dua tunjangan; tentukan boleh diterima bersamaan.|Konfirmasi kombinasi
36|105:106|Leave paid = BS ÷ 30 × sisa cuti eligible dalam hari pada resign atau pensiun.|Batasi pada settlement dan saldo cuti sah; dukung pecahan 0,5 hari.|Konfirmasi saldo
37||Potongan koperasi = total nilai upload approved per karyawan dan periode.|Cegah upload ulang dan pisahkan jenis pinjaman bila ada.|Upload approved
38||Judul kelompok, tidak menghasilkan pembayaran.|Jangan jadikan nilai tambahan di payslip.|Judul kelompok
39|66:68,98:99|Settlement mengundurkan diri = nominal rincian hak approved dari hasil perhitungan HR.|HI hanya rujukan umum; formula hak dan PKB belum tersedia.|Upload settlement
40|66:68,98:99|Settlement PHK = nominal rincian hak approved berdasarkan alasan PHK dan masa kerja.|HI tidak memuat koefisien hak; jangan otomatisasi asumsi.|Upload settlement
41|66:68,98:99|Settlement pensiun = nominal rincian hak approved berdasarkan kebijakan yang disetujui.|Koefisien, usia dan pengurang manfaat belum tersedia.|Upload settlement
42|66:68,98:99|Settlement pensiun dini = nominal rincian hak approved sesuai persetujuan program.|Bedakan program pensiun dini dari pensiun normal.|Upload settlement
43|70:72|Uang kompensasi putus kontrak = nominal perhitungan approved yang diunggah per karyawan.|HI tidak memuat formula numerik atau masa kerja eligible.|Upload settlement
44|54:62|Potongan alfa = BS ÷ 30 × hari alfa. Potongan unpaid leave = BS ÷ 30 × hari unpaid. Keterlambatan Operator–Spv mengikuti rule sumber setelah unit dan toleransi dikonfirmasi.|Rule menit HI membagi 8 jam tanpa konversi 60; toleransi 2 menit belum jelas pengurang atau ambang.|Konflik unit keterlambatan
45||Prorate = nominal komponen yang disepakati × unit eligible ÷ unit pembagi periode yang disepakati.|HI tidak menetapkan metode prorate; jangan asumsikan ÷30 dari rule absen.|Perlu rule prorate
46|43:52|Menurut teks HI: lembur biasa = upah ÷ 173 × total lembur × 1,5; lembur libur = upah ÷ 173 × total lembur × 2. Operator–Leader: harian dan weekend; Foreman/Chief: weekend. Spv–Ast Man mengikuti tunjangan hari libur.|Basis upah, satuan dan jenjang pengali perlu validasi; teks HI belum cukup jadi rule final.|Perlu validasi lembur
47||Potongan serikat = nominal upload approved per karyawan dan periode.|HI tidak memuat tarif; cegah duplikasi potongan.|Upload approved
48||Incentive Tax = nilai insentif menurut program pajak, eligibility dan periode yang disetujui.|HI tidak memuat program atau dasar hitung.|Perlu rule pajak
49||Rapel Incentive Tax = hak insentif periode asal yang disetujui dikurangi nilai yang sudah dibayarkan untuk periode tersebut.|Perlu riwayat pembayaran dan aturan selisih negatif.|Perlu rule pajak
50||Tax Natura = nilai pajak terkait natura sesuai basis manfaat, pengecualian dan metode pajak yang disetujui.|Pastikan ini pajak atau nilai manfaat; cegah duplikasi tunjangan pajak.|Perlu definisi pajak
51||Other Bank = Rp9.000 per unit transaksi eligible setelah bank pemicu, unit dan penanggung disetujui.|Belum jelas potongan karyawan atau biaya perusahaan.|Perlu rule bank
52||Bayarkan bonus direksi approved bila diklasifikasikan remunerasi payroll.|Jika dividen, proses finance; HI tidak mengatur klasifikasi.|Konfirmasi substansi
53||UO = nominal tunjangan kontrak aktif bagi Utility Operator eligible.|HI tidak memuat rule atau eligibility UO.|Konfirmasi eligibility`;
const detail=spec.split('\n').map(x=>x.split('|'));
const sourceRows=setup[0].rows.slice(12,65);
if(detail.length!==53||sourceRows.length!==53)throw Error('Jumlah komponen tidak cocok');
const wb=Workbook.create();
const main=wb.worksheets.add('Analisis Komponen');
const guide=wb.worksheets.add('Panduan dan Isu');
const original=wb.worksheets.add('Setup Asal');
const raw=wb.worksheets.add('Data Sumber Asal');
const hi=wb.worksheets.add('Rules HI 2025');
const heads=['No.','Komponen','Upah sumber','Kriteria sumber','Nilai sumber','Metode sumber','Setup awal','Catatan setup awal','Fixed formula fungsional','Pertimbangan OP','Mapping rule HI','Status penetapan','Referensi setup'];
main.getRange('A2').values=[['Analisis Komponen Gaji HOGY']];
main.getRange('A3').values=[['53 baris dipertahankan: 50 komponen detail dan 3 judul kelompok. Formula berupa uraian bisnis.']];
main.getRange('A4').values=[['Usulan yang belum lengkap ditandai untuk konfirmasi; tarif HI 2025 tidak otomatis dianggap berlaku untuk periode berikutnya.']];
main.getRange('A6:M6').values=[heads];
const out=sourceRows.map((r,i)=>{const d=detail[i]; if(+d[0]!==r[0])throw Error('Urutan berubah');const refs=d[1]?d[1].split(',').map(a=>`Rules HI 2025!B${a.includes(':')?a.split(':')[0]+':E'+a.split(':')[1]:a+':E'+a}`).join('; '):'Tidak dijelaskan dalam HI';return [...r,d[2],d[3],refs,d[4],`Setup Asal!A${i+13}:H${i+13}`];});
main.getRange('A7:M59').values=out;main.tables.add('A6:M59',true,'AnalisisKomponen');
main.freezePanes.freezeRows(6);main.freezePanes.freezeColumns(2);main.tabColor='#203864';
const notes=[['Topik','Keputusan / tindakan'],['Cara baca','Kolom A–H menyalin setup awal; I–M berisi analisis baru. Filter Status penetapan untuk membahas keputusan yang belum lengkap.'],['Makna fixed formula','Uraian perhitungan bisnis untuk implementasi. Kalimat bersyarat dan parameter yang belum tersedia belum dapat dianggap rule final.'],['Cakupan sumber','Setup dari HOGY_Komponen Gaji_Setup_Formula_Upload_Kontrak.xlsx, dua sheet; rule dari Payroll Rules HI 2025.xls, HOGY!A1:H122. Salinan sumber berupa nilai, bukan replika format/objek.'],['Kontrol kelengkapan','53/53 baris setup dipertahankan sesuai urutan dan delapan kolom asal; 50 detail + 3 judul kelompok. Basic Salary No. 1–2 tetap dua baris, gunakan satu nominal per karyawan.'],['Konflik eligibility','Prioritaskan persetujuan mapping jabatan untuk Haid, Shift 2, Penanggung jawab Shift, Komunikasi, Fixed Transport, Basic Salary dan Incentive.'],['Keterlambatan','HI B61:C62 mencampur jam dan menit. Putuskan pembagi 60 serta arti toleransi 2 menit sebelum implementasi; jangan koreksi diam-diam.'],['Lembur','Validasi basis upah, satuan, jenjang pengali dan kategori penerima. Tunjangan hari libur Spv–Ast Man harus dipisahkan dari pembayaran lembur jam.'],['Pajak dan BPJS','Sumber HI 2025 belum memuat semua batas dasar, metode pajak dan ketentuan periode berjalan. Validasi parameter untuk periode payroll sebelum aktivasi. Tidak dilakukan penetapan hukum terkini dalam analisis ini.'],['Prorate','Tetapkan komponen yang diprorata, tanggal efektif, pembagi dan pembulatan. Hindari prorate ganda atau potongan absen ganda atas kejadian yang sama.'],['Upload','Identifikasi unik perusahaan + karyawan + periode + komponen + referensi transaksi; hanya data approved, cegah impor ulang.'],['Kontrak','Pilih kontrak aktif sesuai tanggal berlaku dan perusahaan karyawan; pastikan tidak ada dua kontrak yang menghasilkan nominal ganda.'],['Settlement','Pisahkan rincian hak, cuti dibayar dan kompensasi kontrak agar tidak terhitung dua kali; nominal approved tetap diunggah sesuai setup awal.'],['Batas sumber','Tanggal efektif/revisi HI kosong. Tabel gaji, memo haid, polis, PKB dan parameter tambahan tidak disertakan.'],['Penetapan final','HR menetapkan eligibility dan parameter. Payroll/Finance menetapkan penanggung, dasar pajak/iuran dan klasifikasi dividen. Teknikal mengimplementasikan setelah keputusan dicatat.']];
guide.getRange(`A2:B${notes.length+1}`).values=notes;
for(const [sh,data] of [[original,setup[0].rows],[raw,setup[1].rows],[hi,rules[0].rows]])sh.getRangeByIndexes(0,0,data.length,data[0].length).values=data;
for(const sh of [main,guide,original,raw,hi]){sh.showGridLines=false;const range=sh.getUsedRange();range.format.font={name:'Arial',size:10,color:'#243746'};range.format.verticalAlignment='top';range.format.wrapText=true;range.format.rowHeight=62;range.format.columnWidth=26;}
const widths=[6,32,12,28,24,20,22,52,78,58,36,28,30];widths.forEach((w,c)=>main.getRangeByIndexes(0,c,59,1).format.columnWidth=w);
main.getRange('A1:M5').format.rowHeight=24;main.getRange('A2').format.font={size:15,bold:true};main.getRange('A7:M59').format.rowHeight=112;main.getRange('E7:E59').setNumberFormat('#,##0');
for(const [sh,range] of [[main,'A6:M6'],[guide,'A2:B2'],[original,'A12:H12'],[raw,'A4:J4'],[hi,'A13:H13']])sh.getRange(range).format={fill:'#203864',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:32,horizontalAlignment:'center'};
main.getRange('L7:L59').conditionalFormats.add('notContainsText',{text:'Judul kelompok',format:{fill:'#FFF2CC'}});
guide.getRange('A1:A16').format.columnWidth=28;guide.getRange('B1:B16').format.columnWidth=115;guide.getRange('A3:B16').format.rowHeight=64;
original.getRange('H1:H65').format.columnWidth=65;original.freezePanes.freezeRows(12);raw.getRange('J1:L57').format.columnWidth=65;raw.freezePanes.freezeRows(4);hi.getRange('B1:B122').format.columnWidth=90;hi.getRange('C1:C122').format.columnWidth=65;hi.getRange('D1:D122').format.columnWidth=65;hi.getRange('A1:A122').format.columnWidth=8;hi.getRange('A1:H122').format.rowHeight=34;hi.freezePanes.freezeRows(4);
wb.recalculate();
const dir='E:/Panda/Hogy/outputs/payroll-analysis-20261102';await fs.mkdir(dir,{recursive:true});
console.log((await wb.inspect({kind:'table',range:'Analisis Komponen!I49:M52',tableMaxRows:4,tableMaxCols:5,maxChars:2500})).ndjson);
for(const [sh,range] of [[main,'A6:D12'],[main,'I48:L52'],[guide,'A2:B8'],[original,'A12:D17'],[raw,'A4:D9'],[hi,'B54:D62']]){const p=await wb.render({sheetName:sh.name,range,scale:1});await fs.writeFile(`${dir}/preview-${sh.name.replaceAll(' ','-')}-${range.split(':')[0]}.png`,new Uint8Array(await p.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/HOGY_Analisis_Formula_Komponen_Gaji.xlsx`);
console.log('Export selesai: '+out.length+' baris');
