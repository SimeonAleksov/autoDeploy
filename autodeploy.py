import paramiko
import pyfiglet
import time
from tqdm import tqdm
import getpass
from multiprocessing import Process
from threading import Thread

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
    for i in tqdm(range(100), desc=bcolors.OKBLUE + "Connecting" + bcolors.BOLD):
        time.sleep(0.05)
def setting_up_html():
    for i in tqdm(range(100), desc="Installing"):
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
    
def connect(host=None, user=None, pw=None):
    # print('Attempting to connect')
    ssh = paramiko.SSHClient()
    # For now, we'll connect without key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # loading()
    try:
        ssh.connect(host, port=22, username=user, password=pw)
        # Really simple way to check if my connection is active, I'll find better solution later
        (stdIn, stOut, stdErr) = ssh.exec_command('whoami')
        output = stOut.read()
        # print(output.decode('utf-8'))
        # print('Connected!')
        print(bcolors.OKGREEN + "Connection established successfully!" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + "Connection failed, try again." + bcolors.ENDC)


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
        return 1
    else:
        return 0

def get_repo_name(gitUrl):
    return gitUrl.rsplit('/', 1)[1]

def handle_repos(gitlink):
    _clone = "sudo git clone " + gitlink
    dir_name = get_repo_name(gitlink)
    copy_web = "cp -r %s/. /var/www/html" %dir_name
# Before we copy anything we need to clear our html directory
def clear_apache_html():
    return "sudo rm -rf /var/www/html/*"

# After installing the web site contents, the server needs to reload
def reload_apache():
    return "sudo /etc/init.d/apache2 reload"

# This is for jekyll, we need to install ruby.
def install_ruby():
    return "sudo apt-get install ruby-full build-essential zlib1g-dev"

# It's best to avoid installing Ruby Gems as the root user.
# We might not need this, but we'll check later. 
"""def setup_env():
    _gem = "echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc"
    _export_gem = "echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc"
    _export_path = "echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc"
    fin = "source ~/.bashrc"
    return _gem, _export_gem, _export_path, fin
"""
# Finally, we'll installing jekyll

def install_jekyll():
    return "gem install jekyll bundler"

# We need to build our site, and we need to run this in the github jekyll repo
def jekyll_build():
    return "jekyll build"

    
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
