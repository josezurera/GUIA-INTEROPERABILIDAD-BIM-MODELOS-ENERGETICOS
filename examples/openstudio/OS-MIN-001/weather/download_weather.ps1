$ErrorActionPreference = 'Stop'

$fileName = 'ESP_MD_Madrid-Barajas-Suarez.AP.082210_TMYx.2009-2023'
$url = "https://climate.onebuilding.org/WMO_Region_6_Europe/ESP_Spain/MD_Madrid/$fileName.zip"
$zipPath = Join-Path $PSScriptRoot "$fileName.zip"
$epwPath = Join-Path $PSScriptRoot "$fileName.epw"
$expectedZip = '565aec437eefc483fb8d3c5aacb60d1128be79c5b8847e18bb69a4b9c4ec1385'
$expectedEpw = '2137be4961ebe634fe6f09f392ec3a320dfefcff34b4152c155334574bf8ba16'

Invoke-WebRequest -Uri $url -OutFile $zipPath
$zipHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
if ($zipHash -ne $expectedZip) { throw "Checksum ZIP no válido: $zipHash" }

Expand-Archive -LiteralPath $zipPath -DestinationPath $PSScriptRoot -Force
$epwHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $epwPath).Hash.ToLowerInvariant()
if ($epwHash -ne $expectedEpw) { throw "Checksum EPW no válido: $epwHash" }

Get-ChildItem -LiteralPath $PSScriptRoot -File |
  Where-Object { $_.BaseName -eq $fileName -and $_.Extension -ne '.epw' } |
  Remove-Item -Force
Write-Output "EPW verificado: $epwPath"
