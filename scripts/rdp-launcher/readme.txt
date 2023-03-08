Remote Desktop Session Launcher

1) Right click rdp-launcher.ps1 and run with Powershell.
2) Select the machine you want to go in.
3) Press Launch button to open RDP session.

Happy hunting!

print("[windows:children]\nwindows_server\nwindows_client\n\n[windows:vars]\nansible_user=administrator\nansible_password=Admin1Admin1\n\n[windows_server]\n" + windows_server + "\n[windows_client]\n" + windows_client + "\n[linux:children]\nlinux_server\nlinux_client\n\n[linux:vars]\nansible_user=root\nansible_password=Admin1Admin1\n\n[linux_server]\n" + linux_server + "\n[linux_client]\n" + linux_client)