import csv

with open(r'scripts\inventory-generator\Password List - Use This.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        fqdn = row['FQDN']
        updated_password = row['Changed to another password? Write it here. (use <> if it\'s not new password)']
        password = row['Changed to another password? Write it here. (use <> if it\'s not new password)'] if updated_password.strip() != "" and updated_password[0] != "<" else row['Password to change to']
        username = row['New username, or non-default username']

        with open('inventory.ini', 'r+') as inventory_file:
            lines = inventory_file.readlines()
            inventory_file.seek(0)
            for i, line in enumerate(lines):
                if fqdn in line:
                    new_line = line.strip()
                    comment_index = new_line.find('#')
                    if comment_index != -1:
                        comment = new_line[comment_index:]
                        new_line = new_line[:comment_index]
                    else:
                        comment = ''
                    
                    if username.strip() != "":
                        new_line += f'ansible_password={password} ansible_user={username} ' + comment + '\n'
                    else:
                        new_line += f'ansible_password={password} ' + comment + '\n'
                    lines[i] = new_line
                    break
            inventory_file.seek(0)
            inventory_file.writelines(lines)
            inventory_file.truncate()