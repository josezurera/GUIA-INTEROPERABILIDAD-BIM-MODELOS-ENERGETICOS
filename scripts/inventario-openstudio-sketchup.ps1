$ErrorActionPreference = 'Stop'

$executables = @(
  'C:\Program Files\SketchUp\SketchUp 2025\SketchUp\SketchUp.exe',
  'C:\openstudioapplication-1.11.1\bin\OpenStudioApp.exe',
  'C:\openstudioapplication-1.11.1\bin\openstudio.exe'
)

foreach ($path in $executables) {
  if (Test-Path -LiteralPath $path) {
    $item = Get-Item -LiteralPath $path
    [pscustomobject]@{
      product = $item.VersionInfo.ProductName
      version = $item.VersionInfo.ProductVersion
      path = $path
      status = 'confirmado'
    }
  }
}

$pluginRoots = Get-ChildItem -LiteralPath "$env:APPDATA\SketchUp" -Directory -ErrorAction SilentlyContinue |
  ForEach-Object { Join-Path $_.FullName 'SketchUp\Plugins' } |
  Where-Object { Test-Path -LiteralPath $_ }

$openStudioPlugins = foreach ($root in $pluginRoots) {
  Get-ChildItem -LiteralPath $root -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match 'OpenStudio' } |
    Select-Object @{Name = 'product'; Expression = { 'OpenStudio SketchUp Plug-in' }},
      @{Name = 'version'; Expression = { 'pendiente de consultar en SketchUp' }},
      @{Name = 'path'; Expression = { $_.FullName }},
      @{Name = 'status'; Expression = { 'archivo localizado' }}
}

if (-not $openStudioPlugins) {
  [pscustomobject]@{
    product = 'OpenStudio SketchUp Plug-in'
    version = 'pendiente'
    path = 'no localizado en las carpetas de Plugins'
    status = 'requiere comprobar el Administrador de extensiones'
  }
} else {
  $openStudioPlugins
}
