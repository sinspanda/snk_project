import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
const require=createRequire('C:/Users/SAYID/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const {Workbook,SpreadsheetFile}=require('@oai/artifact-tool');
const dir='E:/Panda/Hogy/outputs/contract-payroll-20261025';
const raw=JSON.parse(await fs.readFile(dir+'/source.json','utf8'));
const wb=Workbook.create();
const s=wb.worksheets.add('Klasifikasi'), ex=wb.worksheets.add('Contoh Rumus'), src=wb.worksheets.add('Data Sumber');
const K=[1,2,10,20,21,33,34,35,53], T=[14,15,16,18,30,31,32,37,43,47,49,50,52], G=[3,7,38];
const details={
1:['Nominal basic salary individu','Ambil basic salary kontrak × faktor prorate','Nominal berdasarkan jabatan; tetapkan masa berlaku.'],
2:['Nominal basic salary hasil tabel gaji','Ambil basic salary kontrak × faktor prorate','Satu jenis Basic Salary dengan No. 1; cegah pembayaran ganda.'],
4:['Rate/nominal umum dan rule kehadiran','Nominal tunjangan × faktor eligibility kehadiran','Gugur seluruhnya atau berkurang bertahap?'],
5:['Rate umum dan eligibility','Rate × unit eligible, atau nominal jika kondisi terpenuhi','Konfirmasi trigger dan unit pembayaran.'],
6:['Rate makan dan hari hadir eligible','Hari hadir eligible × rate makan','Konfirmasi cuti, dinas, izin, dan hari libur.'],
8:['Rate transport umum','Unit transport eligible × 12.190','Konfirmasi unit: hari atau perjalanan.'],
9:['Rate transport motor','Unit transport eligible × 13.190','Menggantikan atau menambah No. 8?'],
10:['Nominal transport tetap individu','Ambil Fix Transport kontrak','Jika seragam berdasarkan grade, gunakan tabel payroll.'],
11:['Rate transport lembur dan realisasi','Unit lembur eligible × rate transport lembur','Per jam, hari, atau kejadian? Pisahkan dari overtime.'],
12:['Rate shift 2 dan shift aktual','Jumlah shift 2 eligible × 7.000','Konfirmasi 7.000 per shift.'],
13:['Rate PJ shift dan schedule','Jumlah penugasan eligible × rate PJ shift','Konfirmasi rate dan unit penugasan.'],
14:['Pengajuan approved; nominal master 800.000','Kejadian approved × nominal master','Konfirmasi frekuensi dan syarat pengajuan.'],
15:['Pengajuan approved; nominal master 1.000.000','Kejadian approved × nominal master','Konfirmasi syarat kelahiran dan penerima.'],
16:['Upload kejadian atau nominal approved','Jumlah kejadian approved × 20.000','Konfirmasi 20.000 per kejadian atau nilai upload total.'],
17:['Rate makan Ramadhan dan attendance','Hari hadir eligible selama Ramadhan × rate','Menggantikan atau menambah makan reguler?'],
18:['Nilai klaim approved; master 500.000','Nilai approved sesuai policy klaim','Konfirmasi 500.000 sebagai plafon atau nominal tetap.'],
19:['Tabel nominal berdasarkan jabatan/kelompok','Lookup nominal sesuai eligibility','Jika nominal khusus per individu, simpan di kontrak.'],
20:['Nominal tunjangan jabatan individu','Ambil Position Allow kontrak','Jika seragam per jabatan, dapat menggunakan tabel payroll.'],
21:['Nominal incentive tetap individu','Ambil Incentive kontrak','File menyebut Fix/bln; konfirmasi tidak berdasarkan pencapaian.'],
22:['Nominal umum 60.000 dan eligibility','Jika eligible, 60.000; selainnya 0','Khusus karyawan tetap; jika nominal individual berbeda, gunakan kontrak.'],
23:['Nominal umum 60.000 dan status keluarga','Jika eligible, 60.000; selainnya 0','Konfirmasi status keluarga yang memenuhi syarat.'],
24:['Rate umum 40.000 dan data anak','40.000 × jumlah anak eligible ATAU 40.000 jika eligible','Konfirmasi per anak atau total; batas usia/jumlah anak.'],
25:['Nominal umum 40.000 dan status individu','Jika eligible, 40.000; selainnya 0','Menggantikan atau menambah tunjangan keluarga?'],
26:['Metode tunjangan pajak dan basis bruto','Hasil kalkulasi tunjangan pajak sesuai metode','Bukan otomatis persentase flat basic salary; konfirmasi metode.'],
27:['Policy premi, rate, dan basis upah','Rate premi × basis upah sesuai policy','Konfirmasi pembayar premi dan employee/employer share.'],
28:['Enrollment dan rule iuran','Rule basis upah, rate, dan batas berlaku','Pisahkan employer contribution dan employee deduction.'],
29:['Enrollment dan rule per program','Rule iuran masing-masing program','Pisahkan program dan employee/employer share.'],
30:['Nominal koreksi approved','Input nominal positif/negatif sesuai koreksi','Simpan alasan, komponen asal, dan periode asal.'],
31:['Nilai award approved','Upload nominal bonus approved','Jika rule bonus pasti, dapat dihitung otomatis.'],
32:['Nominal THR approved sesuai proses sumber','Upload hasil THR; dapat otomatis setelah rule disepakati','Sumber menyebut upload; konfirmasi basis dan formula.'],
33:['Nominal allowance individu dan currency USD','Ambil nominal kontrak; konversi jika diperlukan','Konfirmasi kurs, tanggal kurs, dan currency pembayaran.'],
34:['Sementara: nominal sales insentif individu','Ambil nominal kontrak jika tetap bulanan','Jika berdasarkan target/penjualan, pindahkan ke formula payroll.'],
35:['Nominal skill allowance individu','Ambil nominal kontrak selama assignment berlaku','Jika tarif seragam per skill, gunakan tabel payroll.'],
36:['Saldo cuti approved dan basis nilai harian','Hari cuti yang diuangkan × nilai per hari','Konfirmasi saldo eligible dan pembagi nilai harian.'],
37:['Tagihan koperasi aktual per periode','Upload potongan approved','Jika cicilan tetap, bisa gunakan schedule potongan terpisah.'],
39:['Reason keluar, masa kerja, dan basis','Rule settlement sesuai eligibility mengundurkan diri','Nama pesangon di sumber belum menetapkan jenis hak.'],
40:['Reason PHK, masa kerja, dan basis','Rule settlement berdasarkan alasan PHK','Formula dan basis perlu persetujuan; bukan rumus legal final.'],
41:['Eligibility pensiun, masa kerja, dan basis','Rule settlement pensiun','Konfirmasi jenis manfaat dan ketentuan.'],
42:['Eligibility pensiun dini dan basis','Rule settlement pensiun dini','Konfirmasi policy dan approval.'],
43:['Nominal kompensasi approved dari upload','Upload hasil settlement; otomatis jika rule telah pasti','Konfirmasi jenis kompensasi dan pemicu pembayaran.'],
44:['Unit absen dan basis potongan','Unit absen yang dipotong × nilai per unit','Cegah pengurangan ganda dengan prorate.'],
45:['Rule prorate dan komponen yang terkena','Nilai komponen × faktor prorate','Mekanisme pengali; jangan membuat earning tambahan ganda.'],
46:['Jam lembur approved dan basis upah','Fungsi jam eligible, basis upah, dan multiplier','Konfirmasi jenis hari, basis, dan approval; formula belum final.'],
47:['Nilai potongan dari serikat per periode','Upload potongan approved','Jika seragam, dapat menggunakan master rate dan membership.'],
48:['Eligibility dan rule program pajak','Hasil rule insentif pajak pada periode berlaku','Konfirmasi program dan periode berlaku.'],
49:['Koreksi insentif pajak periode asal','Upload/hitung selisih terhadap perhitungan asal','Referensikan periode dan kalkulasi asal.'],
50:['Nilai manfaat atau pajak dari upload','Input sesuai definisi komponen yang disepakati','Konfirmasi apakah nilai natura atau nilai pajaknya.'],
51:['Master biaya 9.000 dan pemicu transaksi','Jumlah kejadian dikenakan biaya × 9.000','Konfirmasi arti Other Bank dan pihak penanggung.'],
52:['Nominal approved','Upload nilai approved','Pisahkan bonus remunerasi dengan dividen; dividen perlu proses finance.'],
53:['Nominal UO individu','Ambil nominal kontrak selama assignment berlaku','Jika tarif seragam bagi semua UO, gunakan master payroll.']};
const rows=raw.slice(4).map((r,i)=>{const n=i+1;const label=[r[1],r[2],r[3]].filter(Boolean).join(' / ');const dest=G.includes(n)?'Judul kelompok':K.includes(n)?'Kontrak individu':T.includes(n)?'Transaksi payroll':'Setting payroll'; const d=details[n]??['Tidak ada nilai','Tidak dihitung','Judul kelompok, bukan komponen pembayaran.'];return [n,label,dest,r[6],r[7],r[8],d[0],d[1],d[2],G.includes(n)?'Tidak berlaku':'Belum dikonfirmasi',null,null];});
s.getRange('A2').values=[['HOGY — Penempatan Nilai Komponen Gaji']];
s.getRange('A3').values=[['Draft diskusi • 25 Oktober 2026 • Semua rumusan adalah usulan, bukan kebijakan final HOGY.']];
s.getRange('A5:D5').values=[['Kontrak individu','Setting payroll','Transaksi payroll','Judul kelompok']];
for(let i=0;i<4;i++)s.getCell(5,i).formulas=[[`=COUNTIFS(C11:C63,${String.fromCharCode(65+i)}5)`]];
s.getRange('A8').values=[['Nominal umum disimpan di setting payroll; nominal khusus individu di kontrak. Kolom K–L untuk keputusan dan jawaban HOGY.']];
s.getRange('A10:L10').values=[['No. sumber','Komponen','Usulan tempat nilai','Nilai sumber','Metode sumber','Kriteria sumber','Data yang disimpan/input','Usulan rumusan / proses','Konfirmasi / catatan','Status review','Keputusan HOGY','Jawaban / catatan HOGY']];
s.getRange('A11:L63').values=rows;
s.tables.add('A10:L63',true,'KlasifikasiKomponen');
s.getRange('J11:J63').dataValidation={rule:{type:'list',values:['Belum dikonfirmasi','Disetujui','Perlu revisi','Tidak berlaku']}};
s.getRange('K11:K63').dataValidation={rule:{type:'list',values:['Kontrak individu','Setting payroll','Transaksi payroll','Judul kelompok']}};
s.getRange('J11:J63').conditionalFormats.add('containsText',{text:'Perlu revisi',format:{fill:'#FCE4D6',font:{color:'#9C0006'}}});
for(const [name,color] of [['Kontrak individu','#DCEAF7'],['Setting payroll','#E2EFDA'],['Transaksi payroll','#FCE4D6'],['Judul kelompok','#E7E6E6']])s.getRange('C11:C63').conditionalFormats.add('containsText',{text:name,format:{fill:color}});
ex.getRange('A2').values=[['Contoh Rumus — Simulasi, Bukan Rate Kebijakan HOGY']];
ex.getRange('A4:E4').values=[['Contoh','Basis / nominal','Rate / faktor / quantity','Hasil payroll','Keterangan']];
ex.getRange('A5:E9').values=[['Persentase basic salary',5000000,0.002,null,'0,2% hanya contoh dari diskusi; bukan rate aktual komponen.'],['Nominal tetap kontrak',500000,1,null,'Nominal transport individu ilustratif; faktor 1 = bulan penuh.'],['Transport berbasis kehadiran',12190,22,null,'Rate dari sumber; 22 hari dan unit per hari adalah asumsi contoh.'],['Perumahan nominal umum',60000,1,null,'Eligibility contoh: 1 = eligible, 0 = tidak eligible.'],['Prorate nominal kontrak',5000000,0.5,null,'Faktor 50% ilustratif; rule prorate HOGY belum ditetapkan.']];
for(let r=5;r<=9;r++)ex.getRange(`D${r}`).formulas=[[`=B${r}*C${r}`]];
ex.getRange('B5:C9').format.fill='#FFF2CC';ex.getRange('B5:B9').setNumberFormat('#,##0');ex.getRange('D5:D9').setNumberFormat('#,##0');ex.getRange('C5').setNumberFormat('0.0%');ex.getRange('C9').setNumberFormat('0.0%');
ex.getRange('A12').values=[['Sel kuning = input simulasi. Ubah basis/rate untuk melihat hasil. Sel hasil berisi formula Excel.']];
ex.getRange('A13').values=[['Rate statutory, pajak, dan settlement belum ditetapkan dalam workbook ini.']];
src.getRange('A1:J57').values=raw;
src.getRange('L2').values=[['Sumber: Salary Componen (Penjelasan).xlsx — Sheet1!A1:J57']];
src.getRange('L3').values=[['E:/Panda/Hogy/ERP Phase 2/Payroll/Salary Componen (Penjelasan).xlsx']];
src.getRange('L4').values=[['Salinan nilai sumber. Nomor formula sumber disalin sebagai hasil nilai. File asli tidak diubah.']];
src.getRange('L5').values=[['Kolom UPAH dipertahankan sesuai sumber; maknanya belum dikonfirmasi.']];
function base(sh,range){sh.showGridLines=false;sh.getRange(range).format.font={name:'Arial',size:10,color:'#243746'};sh.getRange(range).format.verticalAlignment='top';}
function header(sh,r){sh.getRange(r).format={fill:'#203864',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:32,horizontalAlignment:'center',verticalAlignment:'center'};}
base(s,'A1:L63');base(ex,'A1:E13');base(src,'A1:L57');
s.getRange('A2').format.font={size:15,bold:true};ex.getRange('A2').format.font={size:15,bold:true};
header(s,'A10:L10');header(s,'A5:D5');header(ex,'A4:E4');header(src,'A4:J4');
s.getRange('A11:L63').format.wrapText=true;s.getRange('A11:L63').format.rowHeight=78;
const widths=[7,31,22,23,16,24,38,45,54,22,23,42];widths.forEach((w,i)=>s.getRangeByIndexes(0,i,63,1).format.columnWidth=w);
s.getRange('J11:L63').format.fill='#FFF2CC';s.getRange('A6:D6').format.font={size:15,bold:true};s.getRange('A6:D6').format.rowHeight=25;
s.freezePanes.freezeRows(10);s.freezePanes.freezeColumns(2);s.tabColor='#203864';
ex.getRange('A1:A13').format.columnWidth=31;ex.getRange('B1:C13').format.columnWidth=22;ex.getRange('D1:D13').format.columnWidth=21;ex.getRange('E1:E13').format.columnWidth=65;ex.getRange('A5:E9').format.wrapText=true;ex.getRange('A5:E9').format.rowHeight=48;
src.getRange('A1:A57').format.columnWidth=7;src.getRange('B1:D57').format.columnWidth=29;src.getRange('E1:E57').format.columnWidth=10;src.getRange('F1:J57').format.columnWidth=29;src.getRange('A5:J57').format.wrapText=true;src.getRange('A5:J57').format.rowHeight=47;src.getRange('L1:L57').format.columnWidth=100;src.freezePanes.freezeRows(4);
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Klasifikasi!A5:D6',include:'values,formulas',maxChars:1500,tableMaxRows:2,tableMaxCols:4})).ndjson);
console.log((await wb.inspect({kind:'table',range:"'Contoh Rumus'!B5:D9",include:'values,formulas',maxChars:1600,tableMaxRows:5,tableMaxCols:3})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
for(const [name,range,file] of [['Klasifikasi','A10:D15','classification'],['Klasifikasi','G10:L14','review'],['Contoh Rumus','A2:E9','examples'],['Data Sumber','A4:J9','source']]){const b=await wb.render({sheetName:name,range,scale:1.2,format:'png'});await fs.writeFile(dir+'/'+file+'.png',new Uint8Array(await b.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(wb)).save(dir+'/HOGY_Klasifikasi_Komponen_Kontrak_Payroll.xlsx');
console.log('Export completed: 53 numbered rows, 50 components, 3 headings.');
