Add-Type -AssemblyName System.Windows.Forms

$cnt = 1
while ($true)
{
  if (($cnt % 2) -eq 0) {
    $x = 400 + 10
    $y = 300
  } else {
    $x = 400 - 10
    $y = 300
  }
  [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($x, $y)
  $cnt = ($cnt + 1) % 500

  Start-Sleep -Seconds 20
  echo $cnt, $x, $y
}
