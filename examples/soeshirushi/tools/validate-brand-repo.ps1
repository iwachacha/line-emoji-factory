param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Path,

    [string]$ReleaseId = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$factoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$toolPath = Join-Path $factoryRoot "tools/validate-brand-repo.py"
$arguments = @($toolPath, $Path)

if ($ReleaseId) {
    $arguments += @("--release-id", $ReleaseId)
}

& python @arguments
exit $LASTEXITCODE
