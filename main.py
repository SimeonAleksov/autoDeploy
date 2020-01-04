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

if __name__ == "__main__":
    welcome_banner()
    host_name, username, pw, gitRepo = get_user_info()
    client = SSH(host_name, username, pw)
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
            client.execute('sudo -i')
            # print(linux_cmd.update_rep())
            print(client.execute('sudo apt-get update'))
            client.execute('/etc/init.d/httpd status')
            client.execute(linux_cmd.update_rep())
            client.execute(linux_cmd.install_apache())
            # client.execute(linux_cmd.clear_apache_html())
            # _clone, dir_name, copy_web = linux_cmd.handle_repos()
            # client.execute(_clone)
            # client.execute(copy_web)
            client.execute(linux_cmd.reload_apache())
            # server_ip = client.execute(linux_cmd.get_server_ip())
            print(f"{bcolors.OKGREEN} Installing website successful. You can check it here ")