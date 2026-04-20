$nodePath = "D:\CODE\node-v22.22.2-win-x64\node.exe"
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path -LiteralPath $nodePath)) {
  Write-Error "Khong tim thay node.exe tai $nodePath"
  exit 1
}

Set-Location -LiteralPath $projectDir
& $nodePath ".\server.js"
