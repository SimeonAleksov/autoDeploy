import sys
from threading import Thread
import time
import paramiko
sys.path.append("c:\\Users\\Samoil\\Desktop\\auto\\cmd")
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\helpers')
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\connections')
from linux_commands import *
from ssh_client import SSH
from loading import *
from user_input import *
from colors import bcolors

if __name__ == "__main__":
    welcome_banner()
    host_name, username, pw, gitRepo = get_user_info()
    client = SSH(host_name, username, pw, paramiko.SSHClient())
    threads = []
    t = Thread(target=loading())
    threads.append(t)
    t1 = Thread(target=client.connect())
    threads.append(t1)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    if client.is_alive():
        web_type = check_web_type()
        if check_continue():
            installing()
            linux_cmd = Linux(gitRepo)
            commands = []
            commands.append(linux_cmd.update_rep())
            commands.append(linux_cmd.install_apache())
            commands.append(linux_cmd.clear_apache_html())
            clone, copy = linux_cmd.handle_repos()
            commands.append(clone)
            commands.append(copy)
            commands.append(linux_cmd.reload_apache())
            sys.exit()
            for cmd in commands:
                status_code, output = client.execute(cmd)
                time.sleep(5)
                if status_code == 0:
                    print(cmd)
                else:
                    print(f"Error {status_code}")
            _, output = client.execute(linux_cmd.get_server_ip())
            print(f"{bcolors.OKGREEN} Installing website successful. You can check it here {output.decode('utf-8')}")
