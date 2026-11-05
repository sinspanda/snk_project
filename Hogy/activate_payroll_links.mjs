import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
const require=createRequire('C:/Users/SAYID/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const {SpreadsheetFile,FileBlob}=require('@oai/artifact-tool');
const dir='E:/Panda/Hogy/outputs/payroll-analysis-20261102';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(`${dir}/HOGY_Analisis_Formula_Komponen_Gaji.xlsx`));
const sh=wb.worksheets.getItem('Analisis Komponen');
const before=await wb.render({sheetName:sh.name,range:'K6:M9',scale:1});await fs.writeFile(`${dir}/links-before.png`,new Uint8Array(await before.arrayBuffer()));
let count=0;
for(let row=7;row<=59;row++)for(const col of ['K','M']){
 const cell=sh.getRange(`${col}${row}`);const label=cell.values[0][0];
 const m=String(label).match(/^(Rules HI 2025|Setup Asal)!([A-Z]+\d+(?::[A-Z]+\d+)?)/);
 if(!m)continue;
 cell.formulas=[[`=HYPERLINK("#'${m[1]}'!${m[2]}","${label.replaceAll('"','""')}")`]];
 cell.format.font.color='#0563C1';count++;
}
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:'Analisis Komponen!K7:M8',include:'values,formulas',maxChars:2000})).ndjson);
const after=await wb.render({sheetName:sh.name,range:'K6:M9',scale:1});await fs.writeFile(`${dir}/links-after.png`,new Uint8Array(await after.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(wb)).save(`${dir}/HOGY_Analisis_Formula_Komponen_Gaji_v2.xlsx`);
console.log('Hyperlink formulas: '+count);
