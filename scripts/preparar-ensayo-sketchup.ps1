$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repositoryRoot 'examples\openstudio\OS-MIN-001\model.osm'
$testRoot = Join-Path $repositoryRoot 'tmp\bem-62-sketchup-roundtrip'
$inputDirectory = Join-Path $testRoot 'entrada'
$outputDirectory = Join-Path $testRoot 'salida'
$inputModel = Join-Path $inputDirectory 'OS-MIN-001_entrada.osm'
$outputModel = Join-Path $outputDirectory 'OS-MIN-001_sketchup.osm'

if (-not (Test-Path -LiteralPath $source)) {
  throw "No se encuentra el modelo de referencia: $source"
}

New-Item -ItemType Directory -Path $inputDirectory, $outputDirectory -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $inputModel -Force

[pscustomobject]@{
  modelo_referencia = $source
  abrir_en_sketchup = $inputModel
  guardar_como = $outputModel
  estado_salida = if (Test-Path -LiteralPath $outputModel) { 'existente' } else { 'pendiente' }
}
