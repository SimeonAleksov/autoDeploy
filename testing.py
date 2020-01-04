import paramiko
import pyfiglet
import time
from tqdm import tqdm
import getpass
from multiprocessing import Process
from threading import Thread
from ast import literal_eval
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))


sys.exit()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def loading():
    for _ in tqdm(range(100), desc=bcolors.OKBLUE + "Connecting" + bcolors.BOLD):
        time.sleep(0.05)
def installing():
    for _ in tqdm(range(100), desc=bcolors.OKGREEN + "Installing" + bcolors.BOLD):
        time.sleep(0.1)
def output():
    welcome_banner = pyfiglet.figlet_format("autoDeploy")
    print(welcome_banner)
# Basic attempt to connect to a server via ssh, will update for other choices later.
def get_user_info():
    host_name = input("Please enter the host ip: ")
    username = input("Please enter the username on the machine: ")
    pw = getpass.getpass("Please enter the password: ")
    gitRepo = input("Please enter github repo link: ")
    print(bcolors.WARNING + "Connecting to machine '{0}', with username '{1}'.".format(host_name, username) + bcolors.ENDC)
    return host_name, username, pw, gitRepo

# Function to check if our connection is alive. 
def is_alive():
    if ssh.get_transport() is not None:
         ssh.get_transport().is_active()
         return True
    else:
        return False

def connect(host=None, user=None, pw=None):
    global ssh
    # print('Attempting to connect')
    ssh = paramiko.SSHClient()
    # For now, we'll connect without key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # loading()
    try:
        ssh.connect(host, port=22, username=user, password=pw)
        # Really simple way to check if my connection is active, I'll find better solution later
        (_, stOut, _) = ssh.exec_command('whoami')
        print(bcolors.OKGREEN + "Connection established successfully!" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + "Connection failed, try again." + bcolors.ENDC)

def execute(command):
    (_, stdOut, _) = ssh.exec_command(command)
    output = stdOut.read()
    return output.decode('utf-8')

# After we connect to the machine, we need to update linux packages, repos
def update_rep():
    return "sudo apt-get update"


# If we're using apache, we need to install the server, 
# TODO Need to check if already has apache installed
def install_apache():
    return "sudo apt-get install apache2"


# For starters we'll be using this only for static web sites, will update for other stuff as well
# TODO: Next one is jekyll
def check_web_type():
    user_input = input("Do you want to deploy static html/css webpage? (Y/n)")
    if user_input.lower() == 'y':
        return True
    else:
        return False

# We're getting the repo/dir name from the url the users given us
def get_repo_name(gitUrl):
    return gitUrl.rsplit('/', 1)[1]

# Handling our repo, copying it straight to our apache html 
def handle_repos(gitlink):
    global dir_name
    _clone = "sudo git clone " + gitlink
    dir_name = get_repo_name(gitlink)
    copy_web = "cp -r %s/. /var/www/html" %dir_name
    return _clone, dir_name, copy_web

# Before we copy anything we need to clear our html directory
def clear_apache_html():
    return "sudo rm -rf /var/www/html/*"

# After installing the web site contents, the server needs to reload
def reload_apache():
    return "sudo /etc/init.d/apache2 reload"

# This is for jekyll, we need to install ruby.
def install_ruby():
    return "sudo apt-get install ruby-full build-essential zlib1g-dev"

# Finally, we'll installing jekyll
def install_jekyll():
    return "gem install jekyll bundler"

# Simple bash line to check if file exists, going to need it later to determine path for apache conf 
def check_if_exists(file):
    return "test -e {0} && echo True || echo False".format(file)

# If the user doesn't know where the apache conf is located it, we'll determine
# It's usually in some of these dirs
def find_apache_conf():
    valid_paths = {}
    # Oops.. forgot to use my function..
    first_location = "test -e /etc/apache2/httpd.conf && echo True || echo False"
    second_location = "test -e /etc/apache2/apache2.conf && echo True || echo False"
    third_location = "test -e /etc/httpd/httpd.conf && echo True || echo False"
    forth_location = "test -e /etc/httpd/conf/httpd.conf && echo True || echo False"
    for test in first_location, second_location, third_location, forth_location:
        (_, std1Out, _) = ssh.exec_command(test)
        finOutput = std1Out.read()
        valid_paths[test.split(' ')[2]] = finOutput.decode('utf-8')
    for key, value in valid_paths.items():
        if "".join(value.split()) == 'True':
            return key

# Simple bash line to find public IP
def get_server_ip():
    return "ip route get 1 | awk '{print $NF; exit}'"

# If we want to modify our apache conf to use our domain name, usage:
# dns_setup('simeonaleksov.codes', '/etc/apache2/apache2.conf')
# If we don't know the path to our apache conf, we can call our function to find it.
def dns_setup(dns_string, apache_conf_path):
    for line in dns_string.splitlines():
        ssh.exec_command("echo '{0}' >> {1}".format(line, apache_conf_path))

if __name__ == "__main__":
    output()
    host_name, username, pw, gitRepo = get_user_info()
    threads = []
    t = Thread(target=loading())
    threads.append(t)
    t1 = Thread(target=connect(host_name, username, pw))
    threads.append(t1)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    if is_alive():
        ssh.exec_command(update_rep())
        installing()
        # ssh.exec_command(install_apache)
        (stdIn, stOut, stdErr) = ssh.exec_command(check_if_exists("/var/www/html"))
        output = stOut.read()
        if output.decode('utf-8'):
            ssh.exec_command(clear_apache_html())
            clone, dir_name, copy_web  = handle_repos(gitRepo)
            ssh.exec_command(clone)
            ssh.exec_command(copy_web)
            (stdIn, stdOut, stdErr) = ssh.exec_command(get_server_ip())
            output1 = stdOut.read()
            installing()
            print(bcolors.OKGREEN + "Web site successfully installed. You can check your website on {0}".format(output1.decode('utf-8')))
        else:
            print("Apache server still not installed")
    else:
        print(bcolors.WARNING + "Connection is dead, please try again connecting again." + bcolors.ENDC)
        sys.exit()