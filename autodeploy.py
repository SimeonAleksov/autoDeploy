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

    
connect()
