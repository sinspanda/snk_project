import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = "E:/Downloads/Compare Imei Retur Aug (x_bi_sql_view.imei_retur_aug) (1).xlsx";
const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);

const summary = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 12000,
  tableMaxRows: 100,
  tableMaxCols: 12,
  tableMaxCellChars: 200,
});

const sheet = workbook.worksheets.getItem("Sheet1");
const used = sheet.getUsedRange(true);
const all = used.values;
const headers = all[0];
const rows = all.slice(1);
const idx = Object.fromEntries(headers.map((h, i) => [String(h), i]));
const dataRows = rows.filter(r => /^MSR-/.test(String(r[idx["Mass Return"]] ?? "")));
const counts = (col) => {
  const m = {};
  for (const row of dataRows) {
    const v = String(row[idx[col]] ?? "(blank)");
    m[v] = (m[v] || 0) + 1;
  }
  return Object.entries(m).sort((a,b) => b[1]-a[1]);
};
const cases = dataRows.filter(r =>
  String(r[idx["Status"]] ?? "").includes("INVOICE AWAL") ||
  String(r[idx["Status"]] ?? "").includes("RECEIPT") ||
  Number(r[idx["Imei Line Count"]] ?? 0) > 1
).slice(0, 30).map(r => ({
  massReturn:r[idx["Mass Return"]], imei:r[idx["Imei"]], originalInvoice:r[idx["Original Invoice"]],
  originalDelivery:r[idx["Original Delivery"]], receipt:r[idx["Return Receipt"]], returnInvoice:r[idx["Return Invoice"]],
  imeiLineCount:r[idx["Imei Line Count"]], journalStatus:r[idx["Journal Status"]], status:r[idx["Status"]]
}));

process.stdout.write(summary.ndjson + "\n" + JSON.stringify({rowCount:dataRows.length,status:counts("Status"),journalStatus:counts("Journal Status"),hppStatus:counts("Hpp Status"),gitStatus:counts("Git Status"),receiptBlank:dataRows.filter(r=>!r[idx["Return Receipt"]]).length,returnInvoiceBlank:dataRows.filter(r=>!r[idx["Return Invoice"]]).length,originalInvoiceBlank:dataRows.filter(r=>!r[idx["Original Invoice"]]).length,duplicateRows:dataRows.filter(r=>Number(r[idx["Imei Line Count"]]??0)>1).length,cases}));
