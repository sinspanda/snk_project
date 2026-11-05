import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
const require=createRequire('C:/Users/SAYID/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const {Workbook,SpreadsheetFile}=require('@oai/artifact-tool');
const dir='E:/Panda/Hogy/outputs/payroll-setup-20261028';
const raw=JSON.parse(await fs.readFile('E:/Panda/Hogy/outputs/contract-payroll-20261025/source.json','utf8'));
const contracts=new Set([1,2,10,20,21,33,34,35,53]);
const uploads=new Set([14,15,16,18,30,31,32,37,39,40,41,42,43,47,52]);
const groups=new Set([3,7,38]);
const notes={1:'Basic Salary No. 1 dan 2 menggunakan satu field kontrak.',2:'Basic Salary No. 1 dan 2 menggunakan satu field kontrak.',10:'Nominal individu; jika tarif seragam per jabatan, gunakan parameter komponen gaji.',14:'Upload kejadian atau nominal approved. Nominal master 800,000.',15:'Upload kejadian atau nominal approved. Nominal master 1,000,000.',16:'Upload quantity atau nominal approved; konfirmasi unit rate 20,000.',18:'Upload klaim approved; konfirmasi 500,000 sebagai nominal atau plafon.',19:'Formula/tabel kelompok. Jika nominal khusus individu, pertimbangkan nilai kontrak.',24:'Konfirmasi 40,000 per anak atau total; jumlah anak eligible menjadi input bila per anak.',26:'Pajak dihitung otomatis sesuai metode perusahaan; parameter dan basis perlu ditetapkan.',30:'Koreksi transaksi payroll, berbeda dari perubahan nominal master kontrak.',31:'Upload nominal bonus approved.',32:'Setup awal memakai upload nominal THR approved, mengikuti keputusan implementasi.',34:'Kontrak jika tetap bulanan; jika berbasis pencapaian gunakan formula payroll.',35:'Nominal individu; jika tarif seragam per skill, gunakan parameter komponen gaji.',39:'Upload hasil settlement approved; formula sumber belum diotomatisasi pada setup awal.',40:'Upload hasil settlement approved; formula sumber belum diotomatisasi pada setup awal.',41:'Upload hasil settlement approved; formula sumber belum diotomatisasi pada setup awal.',42:'Upload hasil settlement approved; formula sumber belum diotomatisasi pada setup awal.',45:'Mekanisme pengali komponen; hindari pembayaran nilai penuh dan prorate sekaligus.',48:'Formula program insentif pajak berdasarkan eligibility dan periode berlaku.',49:'Formula selisih terhadap nilai yang telah diproses; perlukan referensi periode asal.',50:'Pajak dihitung otomatis. Nilai manfaat natura dapat diinput/upload sebagai basis; pastikan definisi agar tidak dihitung dua kali.',51:'Konfirmasi pemicu biaya 9,000 dan pihak penanggung.',52:'Upload nominal approved. Jika substansinya dividen, arahkan ke proses finance.',53:'Nominal individu; jika tarif seragam bagi seluruh UO, gunakan parameter komponen gaji.'};
function label(r,n){let t=r[3]||r[2]||r[1]||'';t=r[1]?t.replace(/^\d+(?:\.\d+)*[. ]*/, ''):t.replace(/^[a-z]\.\s*/, '');if([8,9,10,11].includes(n))t='Transport '+t;if([39,40,41,42].includes(n))t='Pesangon - '+t;return t;}
const data=raw.slice(4).map((r,i)=>{const n=i+1;const setup=groups.has(n)?'Judul kelompok':contracts.has(n)?'Kontrak':uploads.has(n)?'Upload':'Formula Otomatis';return[n,label(r,n),r[4]||'—',r[8]||'—',r[6]??'—',r[7]||'—',setup,groups.has(n)?'Judul kelompok; tidak menghasilkan nilai.':notes[n]||(setup==='Kontrak'?'Nominal individu dibaca dari kontrak.':setup==='Upload'?'Upload nilai transaksi approved.':'Sistem menghitung dari parameter, eligibility dan data pemicu; rule rinci perlu ditetapkan.')];});
const counts=Object.fromEntries(['Formula Otomatis','Upload','Kontrak','Judul kelompok'].map(x=>[x,data.filter(r=>r[6]===x).length]));
if(JSON.stringify(Object.values(counts))!==JSON.stringify([26,15,9,3]))throw Error(JSON.stringify(counts));
const wb=Workbook.create();const s=wb.worksheets.add('Setup Komponen');const src=wb.worksheets.add('Data Sumber');
s.getRange('A2').values=[['HOGY — Setup Komponen Gaji']];
s.getRange('A3').values=[['28 Oktober 2026 • Klasifikasi implementasi: formula otomatis, upload, dan kontrak.']];
s.getRange('A5:D5').values=[['Formula Otomatis','Upload','Kontrak','Judul kelompok']];
for(let i=0;i<4;i++)s.getCell(5,i).formulas=[[`=COUNTIFS($G$13:$G$65,${String.fromCharCode(65+i)}5)`]];
s.getRange('A8').values=[['53 nomor = 50 komponen detail + 3 judul kelompok. Sembilan baris kontrak menjadi delapan jenis field.']];
s.getRange('A9').values=[['Formula otomatis dapat memakai upload data dasar. Upload adalah nilai/kejadian approved; kontrak menyimpan nominal individu.']];
s.getRange('A10').values=[['Kolom metode sumber dipertahankan. Setup adalah rancangan implementasi dan dapat berbeda dari metode sumber.']];
s.getRange('A12:H12').values=[['No.','Komponen','Upah','Kriteria Posisi / Jabatan','Nilai','Fix Value / Formula Sumber','Setup','Catatan Implementasi']];
s.getRange('A13:H65').values=data;
s.tables.add('A12:H65',true,'SetupKomponenPayroll');
s.getRange('G13:G65').dataValidation={rule:{type:'list',values:['Formula Otomatis','Upload','Kontrak','Judul kelompok']}};
for(const [t,c] of [['Formula Otomatis','#E2EFDA'],['Upload','#FCE4D6'],['Kontrak','#DCEAF7'],['Judul kelompok','#E7E6E6']])s.getRange('G13:G65').conditionalFormats.add('containsText',{text:t,format:{fill:c}});
src.getRange('A1:J57').values=raw;
src.getRange('L2').values=[['Sumber: Salary Componen (Penjelasan).xlsx, Sheet1!A1:J57']];
src.getRange('L3').values=[['Salinan nilai sumber; file asli tidak diubah. Formula nomor sumber disalin sebagai hasil nilai.']];
src.getRange('L4').values=[['Kolom Upah dipertahankan tanpa mengasumsikan maknanya sebagai dasar pajak.']];
for(const [sh,r] of [[s,'A1:H65'],[src,'A1:L57']]){sh.showGridLines=false;sh.getRange(r).format.font={name:'Arial',size:10,color:'#203040'};sh.getRange(r).format.verticalAlignment='center';}
function header(sh,r){sh.getRange(r).format={fill:'#203864',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',rowHeight:34};}
header(s,'A12:H12');header(s,'A5:D5');header(src,'A4:J4');
s.getRange('A2').format.font={size:15,bold:true};s.getRange('A6:D6').format.font={size:15,bold:true};s.getRange('A6:D6').format.rowHeight=26;
const widths=[7,34,12,28,27,25,25,66];widths.forEach((w,i)=>s.getRangeByIndexes(0,i,65,1).format.columnWidth=w);
s.getRange('A13:H65').format.wrapText=true;s.getRange('A13:H65').format.rowHeight=62;s.getRange('E13:E65').setNumberFormat('#,##0');
s.freezePanes.freezeRows(12);s.freezePanes.freezeColumns(2);s.tabColor='#203864';
src.getRange('A1:A57').format.columnWidth=7;src.getRange('B1:D57').format.columnWidth=29;src.getRange('E1:E57').format.columnWidth=10;src.getRange('F1:J57').format.columnWidth=30;src.getRange('L1:L57').format.columnWidth=105;src.getRange('A5:J57').format.wrapText=true;src.getRange('A5:J57').format.rowHeight=46;src.getRange('G5:G57').setNumberFormat('#,##0');src.freezePanes.freezeRows(4);
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'Setup Komponen'!A5:D6",include:'values,formulas',tableMaxRows:2,tableMaxCols:4,maxChars:1000})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:15},maxChars:700})).ndjson);
for(const [name,range,file] of [['Setup Komponen','A12:G18','matrix'],['Setup Komponen','E59:H65','tax'],['Data Sumber','A4:J9','source']]){const b=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(dir+'/'+file+'.png',new Uint8Array(await b.arrayBuffer()));}
await(await SpreadsheetFile.exportXlsx(wb)).save(dir+'/HOGY_Setup_Formula_Upload_Kontrak.xlsx');
console.log('Exported, counts '+JSON.stringify(counts));
