$json = Get-Content C:\ghost\clubgabbay_captures_1996-1999.json | ConvertFrom-Json
$seen = @{}
$items = @()
foreach ($row in $json) {
    if ($row[0] -eq "timestamp") { continue }
    $ts = $row[0]; $url = $row[1]; $status = $row[2]
    if ($status -ne "200") { continue }
    if (-not $seen.ContainsKey($url)) { $seen[$url] = $true; $items += ,@($ts, $url) }
}
New-Item -ItemType Directory -Force -Path C:\ghost\gabbay-mirror | Out-Null
$log = "C:\ghost\gabbay-mirror\download.log"
Add-Content $log "START $(Get-Date -Format o) items=$($items.Count)"
$i = 0
foreach ($item in $items) {
    $ts = $item[0]; $url = $item[1]
    $i++
    $clean = $url -replace '^https?://', '' -replace ':80', ''
    $hostpart = ($clean -split '/')[0] -replace 'www\.', ''
    $pathpart = $clean -replace '^[^/]+', ''
    if ($pathpart -eq '' -or $pathpart -eq '/') { $pathpart = '/index.html' }
    $fname = ($hostpart + $pathpart) -replace '/', '_' -replace '[?&=]', '_'
    $out = "C:\ghost\gabbay-mirror\$fname"
    if (Test-Path $out) { Add-Content $log "SKIP $i/$($items.Count) $url (exists)"; continue }
    $wb = "https://web.archive.org/web/${ts}id_/$url"
    try {
        Invoke-WebRequest -Uri $wb -OutFile $out -TimeoutSec 60 -ErrorAction Stop
        Add-Content $log "OK $i/$($items.Count) $url"
    } catch {
        Add-Content $log "FAIL $i/$($items.Count) $url : $($_.Exception.Message)"
    }
}
Add-Content $log "DONE $(Get-Date -Format o) items=$($items.Count)"
