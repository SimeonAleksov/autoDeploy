import paramiko
import sys
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\helpers')
from colors import bcolors

class SSH(object):
    def __init__(self, host, user, pw):
        self.host = host
        self.user = user
        self.pw = pw

    def connect(self):
        global ssh
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.host, port=22, username=self.user, password=self.pw)
            print(bcolors.OKGREEN + "Connection established successfully!" + bcolors.ENDC)
        except Exception as e:
            print(bcolors.FAIL + "Connection failed, try again." + bcolors.ENDC)
    def execute(self, command):
        (_, stdOut, _) = ssh.exec_command(command)
        output = stdOut.read()
        return output.decode('utf-8')
    def is_alive(self):
        if ssh.get_transport() is not None:
            ssh.get_transport().is_active()
            return True
        else:
            return False
# client = SSH('snf-49543.vm.okeanos-global.grnet.gr', 'debian', 'shinsroot')