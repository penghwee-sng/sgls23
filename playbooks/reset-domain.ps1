$username = "beg\administrator"
$password = ConvertTo-SecureString "P@ssw0rdP@ssw0rd" -AsPlainText -Force

$cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $username, $password
Reset-ComputerMachinePassword -Server DC1 -Credential $cred
