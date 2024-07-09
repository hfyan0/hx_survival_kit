Add-Type -AssemblyName System.Windows.Forms

# Set the interval in seconds for moving the mouse cursor
$interval = 2

# Function to move the mouse cursor
function Move-MouseCursor {
    param (
        [int]$x,
        [int]$y
    )

    $api = Add-Type -MemberDefinition @"
    [DllImport("user32.dll")]
    public static extern void SetCursorPos(int x, int y);
"@ -Name "Win32API" -PassThru

    $api::SetCursorPos($x, $y)
}

# Main loop
while ($true) {
    # Get the current mouse position
    $currentPos = [System.Windows.Forms.Cursor]::Position

    # Move the mouse cursor to a new position
    Move-MouseCursor -x ($currentPos.X + 10) -y ($currentPos.Y + 10)

    # Wait for the specified interval
    Start-Sleep -Seconds $interval
}
