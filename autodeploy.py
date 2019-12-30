import paramiko

# Basic attempt to connect to a server via ssh, will update for other choices later.
def connect(host=None, user=None, pw=None):
    print('Attempting to connect')
    ssh = paramiko.SSHClient()
    # For now, we'll connect without key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=22, username=user, password=pw)
    # Really simple way to check if my connection is active, I'll find better solution later
    (stdIn, stOut, stdErr) = ssh.exec_command('whoami')
    output = stOut.read()
    print(output.decode('utf-8'))
    print('connected')

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


# I'm doing this because I need to copy the page content to the www/html, I'm doing this because I have no idea what your repo will be called,
# There's probably better way of doing this, but for now it be like this
def handle_repos(gitlink):
    create_dir = "sudo mkdir ignoreThis"
    change_dir = "cd ignoreThis"
    _clone = "sudo git clone " + gitlink
    _back = "cd .. "
    copy_web = "cp -r ignoreThis/*/. /var/www/html"
    return create_dir, change_dir, _clone, _back, copy_web

# Before we copy anything we need to clear our html directory
def clear_apache_html():
    return "sudo rm -rf /var/www/html/*"

# After installing the web site contents, the server needs to reload
def reload_apache():
    return "sudo /etc/init.d/apache2 reload"

connect()