param([string]$list)
$dir = "D:\Collage\Smt_5\Rancang_Kota\Claude outputs\Cangkot_Rev_26-30Okt\gambar"
Get-Content $list | ForEach-Object {
  if ($_ -match '^(.+?)\|(.+)$') {
    $f = Join-Path $dir $matches[1]; $u = $matches[2]
    $r = & curl.exe -sS -X POST -H "Content-Type: application/octet-stream" --data-binary "@$f" $u
    Write-Output ($matches[1] + " => " + $r)
  }
}
