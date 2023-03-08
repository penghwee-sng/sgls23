import json

data = {}
# Opening JSON file
with open(r'dump.json') as json_file:
    data = json.load(json_file)['data']['systems']
 
# Print the type of data variable
windows_server = ""
windows_client = ""
linux_server = ""
linux_client = ""
for system in data:
    # print(system['os'])
    system['zones'][0] = system['zones'][0].replace("_","-")
    if "windows_server" in system['os']:
        windows_server = windows_server + f"{system['zones'][0]}_{system['hostname_common']} ansible_host={system['network_interfaces'][0]['fqdn']} os={system['os']} fqdn={system['network_interfaces'][0]['fqdn']} # {system['network_interfaces'][0]['network_id']}\n"
    elif "windows" in system['os']:
        windows_client = windows_client + f"{system['zones'][0]}_{system['hostname_common']} ansible_host={system['network_interfaces'][0]['fqdn']} os={system['os']} fqdn={system['network_interfaces'][0]['fqdn']} # {system['network_interfaces'][0]['network_id']}\n"
    elif "desktop" in system['os']:
        linux_client = linux_client + f"{system['zones'][0]}_{system['hostname_common']} ansible_host={system['network_interfaces'][0]['fqdn']} os={system['os']} fqdn={system['network_interfaces'][0]['fqdn']} # {system['network_interfaces'][0]['network_id']}\n"
    else:
        linux_server = linux_server + f"{system['zones'][0]}_{system['hostname_common']} ansible_host={system['network_interfaces'][0]['fqdn']} os={system['os']} fqdn={system['network_interfaces'][0]['fqdn']} # {system['network_interfaces'][0]['network_id']}\n"

print("[windows:children]\nwindows_server\nwindows_client\n\n[windows:vars]\nansible_user=administrator\nansible_password=Admin1Admin1\n\n[windows_server]\n" + windows_server + "\n[windows_client]\n" + windows_client + "\n[linux:children]\nlinux_server\nlinux_client\n\n[linux:vars]\nansible_user=root\nansible_password=Admin1Admin1\n\n[linux_server]\n" + linux_server + "\n[linux_client]\n" + linux_client)
