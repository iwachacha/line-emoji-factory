param(
    [Parameter(Mandatory = $true)]
    [string]$BrandSlug,

    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [string]$BrandName = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$toolPath = Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..")).Path "tools/init-brand-repo.ps1"
& $toolPath -BrandSlug $BrandSlug -Destination $Destination -BrandName $BrandName
