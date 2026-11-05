$ErrorActionPreference = 'Stop'

$source = [System.IO.Path]::GetFullPath('E:\Panda\MITO\MITO SFA Mobile - Blueprint Draft V0.1.docx')
$qaDir = [System.IO.Path]::GetFullPath('E:\Panda\MITO\.tmp_blueprint\final_render_customer_user')
$workspace = [System.IO.Path]::GetFullPath('E:\Panda\MITO')

if (-not $qaDir.StartsWith($workspace + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe QA directory: $qaDir"
}

New-Item -ItemType Directory -Force -Path $qaDir | Out-Null
$inputCopy = Join-Path $qaDir 'input.docx'
$outputPdf = Join-Path $qaDir 'blueprint-qa.pdf'
$logFile = Join-Path $qaDir 'export.log'
Copy-Item -LiteralPath $source -Destination $inputCopy -Force

$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.Options.SaveNormalPrompt = $false
    $word.AutomationSecurity = 3
    $document = $word.Documents.OpenNoRepairDialog($inputCopy, $false, $true, $false)
    $document.ExportAsFixedFormat($outputPdf, 17)
    $document.Close(0)
    $document = $null
    "OK`n$outputPdf" | Set-Content -LiteralPath $logFile
}
catch {
    "ERROR`n$($_.Exception.ToString())" | Set-Content -LiteralPath $logFile
    throw
}
finally {
    if ($null -ne $document) {
        try { $document.Close(0) } catch { }
    }
    if ($null -ne $word) {
        try { $word.Quit(0) } catch { }
    }
}
