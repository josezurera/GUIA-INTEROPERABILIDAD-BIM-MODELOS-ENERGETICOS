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
  $loader = Join-Path $root 'openstudio.rb'
  $resources = Join-Path $root 'openstudio'
  if ((Test-Path -LiteralPath $loader) -or (Test-Path -LiteralPath $resources)) {
    $match = if (Test-Path -LiteralPath $loader) {
      Select-String -LiteralPath $loader -Pattern 'SKETCHUPPLUGIN_VERSION\s*=\s*"([^"]+)"' | Select-Object -First 1
    }
    [pscustomobject]@{
      product = 'OpenStudio SketchUp Plug-in'
      version = if ($match) { $match.Matches[0].Groups[1].Value } else { 'no identificada' }
      path = if (Test-Path -LiteralPath $loader) { $loader } else { $resources }
      status = 'archivo localizado'
    }
  }
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
