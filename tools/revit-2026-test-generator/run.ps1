param(
    [string]$OutputDirectory = "",
    [int]$TimeoutSeconds = 600,
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

function Approve-TemporaryAddinLoad {
    param([int]$ProcessId)

    $nameCondition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::NameProperty,
        "Cargar una vez")
    $processCondition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ProcessIdProperty,
        $ProcessId)
    $condition = New-Object System.Windows.Automation.AndCondition($nameCondition, $processCondition)
    try {
        $button = [System.Windows.Automation.AutomationElement]::RootElement.FindFirst(
            [System.Windows.Automation.TreeScope]::Descendants,
            $condition)
    }
    catch {
        return $false
    }
    if ($null -eq $button) {
        return $false
    }

    $pattern = $null
    if ($button.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$pattern)) {
        $pattern.Invoke()
    }
    else {
        $button.SetFocus()
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    }
    return $true
}

$toolDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$repositoryRoot = Resolve-Path (Join-Path $toolDirectory "..\..")
$revit = "C:\Program Files\Autodesk\Revit 2026\Revit.exe"
$template = "C:\ProgramData\Autodesk\RVT 2026\Templates\Spanish\DefaultESPESP.rte"
$addinDirectory = Join-Path $env:APPDATA "Autodesk\Revit\Addins\2026"
$addinManifest = Join-Path $addinDirectory "EemRevit2026TestGenerator.addin"
$assembly = Join-Path $toolDirectory "bin\Release\net8.0-windows\EemRevit2026TestGenerator.dll"

if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $repositoryRoot "tmp\revit-2026-mvd"
}
$OutputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)

if (-not (Test-Path -LiteralPath $revit)) {
    throw "No se encuentra Revit 2026 en $revit"
}
if (-not (Test-Path -LiteralPath $template)) {
    throw "No se encuentra la plantilla en $template"
}

if (-not $SkipBuild) {
    dotnet build (Join-Path $toolDirectory "EemRevit2026TestGenerator.csproj") -c Release
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo compilar el generador."
    }
}

New-Item -ItemType Directory -Force -Path $addinDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
Remove-Item -LiteralPath (Join-Path $OutputDirectory "DONE") -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $OutputDirectory "FAILED") -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $OutputDirectory "revit-generator.log") -Force -ErrorAction SilentlyContinue

$escapedAssembly = [System.Security.SecurityElement]::Escape($assembly)
$manifest = @"
<?xml version="1.0" encoding="utf-8" standalone="no"?>
<RevitAddIns>
  <AddIn Type="Application">
    <Name>EEM Revit 2026 Test Generator</Name>
    <Assembly>$escapedAssembly</Assembly>
    <AddInId>7EAE8D2D-858B-49F8-8E66-603279B48F6C</AddInId>
    <FullClassName>Eem.Revit2026TestGenerator.App</FullClassName>
    <VendorId>EEMG</VendorId>
    <VendorDescription>Guía de interoperabilidad BIM y modelos energéticos</VendorDescription>
  </AddIn>
</RevitAddIns>
"@
[System.IO.File]::WriteAllText($addinManifest, $manifest, [System.Text.UTF8Encoding]::new($false))

$env:EEM_REVIT_TEST_GENERATOR = "1"
$env:EEM_REVIT_TEST_OUTPUT = $OutputDirectory
$env:EEM_REVIT_TEST_TEMPLATE = $template

try {
    # Revit necesita crear su ventana principal para emitir el evento Idling.
    # La ejecución es visible durante el ensayo y el generador la cierra al terminar.
    $process = Start-Process -FilePath $revit -PassThru
    $securityDeadline = [DateTime]::UtcNow.AddSeconds(120)
    do {
        Start-Sleep -Milliseconds 200
        if (Approve-TemporaryAddinLoad -ProcessId $process.Id) {
            Write-Output "Carga temporal del complemento autorizada para esta ejecucion."
            break
        }
        if ($process.HasExited -or (Test-Path -LiteralPath (Join-Path $OutputDirectory "revit-generator.log"))) {
            break
        }
    } while ([DateTime]::UtcNow -lt $securityDeadline)

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        Start-Sleep -Seconds 2
        if (Test-Path -LiteralPath (Join-Path $OutputDirectory "FAILED")) {
            $failure = Get-Content -Raw -LiteralPath (Join-Path $OutputDirectory "FAILED")
            throw "El generador de Revit falló:`n$failure"
        }
        if (Test-Path -LiteralPath (Join-Path $OutputDirectory "DONE")) {
            break
        }
        if ($process.HasExited) {
            throw "Revit se cerró antes de terminar el generador."
        }
    } while ([DateTime]::UtcNow -lt $deadline)

    if (-not (Test-Path -LiteralPath (Join-Path $OutputDirectory "DONE"))) {
        throw "Tiempo de espera agotado. Consulte los diarios de Revit y revit-generator.log."
    }

    $process.WaitForExit(30000) | Out-Null
    Write-Output "Ensayo generado en $OutputDirectory"
}
finally {
    Remove-Item -LiteralPath $addinManifest -Force -ErrorAction SilentlyContinue
    Remove-Item Env:EEM_REVIT_TEST_GENERATOR -ErrorAction SilentlyContinue
    Remove-Item Env:EEM_REVIT_TEST_OUTPUT -ErrorAction SilentlyContinue
    Remove-Item Env:EEM_REVIT_TEST_TEMPLATE -ErrorAction SilentlyContinue
}
