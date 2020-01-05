import paramiko
import sys
import re
import time
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\helpers')
from colors import bcolors

class SSH(object):
    def __init__(self, host, user, pw, ssh):
        self.host = host
        self.user = user
        self.pw = pw
        self.ssh = ssh
    def send_sudo_pw(self):
        channel = ssh.invoke_shell()
        channel.send(f"{self.pw}\n")
    def connect(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host, port=22, username=self.user, password=self.pw)
            print(bcolors.OKGREEN + "Connection established successfully!" + bcolors.ENDC)
        except Exception as e:
            print(bcolors.FAIL + "Connection failed, try again." + bcolors.ENDC)
    def execute(self, command):
        stdIn, stdOut, _ = self.ssh.exec_command(command, get_pty=True)
        stdIn.write(self.pw + '\n')
        stdIn.flush()
        exit_status = stdOut.channel.recv_exit_status()
        return exit_status, stdOut.read()
    def is_alive(self):
        if self.ssh.get_transport() is not None:
            self.ssh.get_transport().is_active()
            return True
        else:
            return False

    @property
    def get_ssh(self):
        return self.ssh

# client = SSH('83.212.126.194', 'user', 'root123', paramiko.SSHClient())
# client.connect()
# print(client.execute('mkdir test2')