param(
    [Parameter(Mandatory = $true)]
    [string]$BrandSlug,

    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [string]$BrandName = "",

    [ValidateSet("8", "16", "24", "32", "40")]
    [int]$InitialSetCount = 8,

    [ValidateSet("generic", "fixed_ip", "collaboration")]
    [string]$BrandType = "generic"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$toolPath = Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..")).Path "tools/init-brand-repo.ps1"
& $toolPath `
    -BrandSlug $BrandSlug `
    -Destination $Destination `
    -BrandName $BrandName `
    -InitialSetCount $InitialSetCount `
    -BrandType $BrandType
