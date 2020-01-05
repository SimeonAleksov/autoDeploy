import sys
from threading import Thread
sys.path.append("c:\\Users\\Samoil\\Desktop\\auto\\cmd")
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\helpers')
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\connections')
from linux_commands import *
from ssh_client import SSH
from loading import *
from user_input import *
from colors import bcolors
import time
import paramiko
if __name__ == "__main__":
    welcome_banner()
    host_name, username, pw, gitRepo = get_user_info()
    # client = SSH(host_name, username, pw, paramiko.SSHClient())
    client = SSH('83.212.126.194','user', 'root123', paramiko.SSHClient())
    threads = []
    # t = Thread(target=loading())
    # threads.append(t)
    t1 = Thread(target=client.connect())
    threads.append(t1)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    if client.is_alive():
        web_type = check_web_type()
        if check_continue():
            # installing()
            linux_cmd = Linux(gitRepo)
            commands = []
            commands.append(linux_cmd.update_rep())
            clone, copy = linux_cmd.handle_repos()
            commands.append(clone)
            commands.append(copy)
            commands.append(linux_cmd.reload_apache())
            print(commands)
            sys.exit()
            for cmd in commands:
                status_code, output = client.execute(cmd)
                time.sleep(5)
                if status_code == 0:
                    print(output.decode('utf-8'))
                    print('Success')
                else:
                    print(output.decode('utf-8'))
                    print(f"Error {status_code}")

            print(f"{bcolors.OKGREEN} Installing website successful. You can check it here ")