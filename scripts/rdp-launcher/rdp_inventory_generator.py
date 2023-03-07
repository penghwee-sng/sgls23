base_list = []
filter_list = []

with open('inventory.ini') as f:
    content = f.read()
    start_tag = '[windows_server]'
    end_tag = '[linux:children]'
    start_index = content.index(start_tag) + len(start_tag)
    end_index = content.index(end_tag)
    result = content[start_index:end_index].strip()
    base_list = result.split("\n")

for entry in base_list:
    if entry.strip() == "" or entry.strip() == "[windows_client]":
        continue
    filter_list.append(entry)
    #print(entry)

with open(r'scripts\rdp-launcher\inventory.txt', "w") as f:
    for entry in filter_list:
        ip_addr = [x.split("ansible_host=")[1] for x in entry.split() if "ansible_host=" in x]
        ip_addr = ip_addr[0] if ip_addr else ""  # use empty string as default
        password = [x.split("ansible_password=")[1] for x in entry.split() if "ansible_password=" in x]
        password = password[0].strip('"') if password else "Admin1Admin1"  # use "123" as default
        f.write(f"{entry.split()[0]} {ip_addr} administrator {password}\n")