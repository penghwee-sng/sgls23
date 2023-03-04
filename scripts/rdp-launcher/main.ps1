Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$Form1 = New-Object system.Windows.Forms.Form
$Form1.ClientSize = '400,150'
$Form1.text = "RDP Launcher"
$Form1.BackColor = "#ffffff"
$List = New-Object system.Windows.Forms.ComboBox
$List.text = ""
$List.width = 260
$List.autosize = $true
# Add the items in the dropdown list

[array]$result = (Get-Content inventory.txt)
$result | ForEach-Object {[void] $List.Items.Add($_.Split(" ")[0])}
# Select the default value
$List.SelectedIndex = 0
$List.location = New-Object System.Drawing.Point(70,30)
$List.Font = 'Microsoft Sans Serif,14'
$List.add_SelectedIndexChanged({
$selected = $List.SelectedItem
write-host $selected
#$Description.text = “Selected index: $selected”
})

$Form1.Controls.Add($List)
# Add a Button which can be used to generate an action from our textboxes
$Button = New-Object System.Windows.Forms.Button
$Button.Location = New-Object System.Drawing.Size(150,80)
$Button.Size = New-Object System.Drawing.Size(100,40)
$Button.Text = "Launch"
# Declare the action to occur when button clicked
$Button.Add_Click( { launch_rdp } )
# Initialize the button inside the Form
$Form1.Controls.Add($Button)
# Create a Function to make use of textboxes
function launch_rdp {
    $selected_host = $result[$List.SelectedIndex]
    $ip = $selected_host.Split(" ")[1]
    $user = $selected_host.Split(" ")[2]
    $password = $selected_host.Split(" ")[3]
    cmdkey /generic:$ip /user:$user /pass:$password
    mstsc /v:$ip
}
# Display the form
[void]$Form1.ShowDialog()