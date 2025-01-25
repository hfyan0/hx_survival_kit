Add-Type -AssemblyName System.Windows.Forms

$cnt = 1
while ($true)
{
  # $pos = [System.Windows.Forms.Cursor]::Position

  # $x = ($pos.X % 500) + 1
  # $y = ($pos.Y % 500) + 1

  # $ran_move = Get-Random -Minimum -5 -Maximum 5
  # $x = $pos.X + $ran_move
  # $y = $pos.Y + $ran_move

  if (($cnt % 2) -eq 0) {
    $x = 250
    $y = 250
  } else {
    $x = 500
    $y = 500
  }
  [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($x, $y)
  $cnt = ($cnt + 1) % 500

  Start-Sleep -Seconds 20
  echo $cnt, $x, $y
}
