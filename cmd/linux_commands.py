import sys
# print(sys.path)
class Linux(object):
    def __init__(self, git_link):
        self.git_link = git_link

    def get_server_ip(self):
        return "ip route get 1 | awk '{print $NF; exit}'"

    def update_rep(self):
        return "sudo apt-get update"

    def check_if_exists(self, file):
        return "test -e {0} && echo True || echo False".format(file)

    # If we're using apache, we need to install the server, 
    # TODO Need to check if already has apache installed
    def install_apache(self):
        return "sudo apt-get install apache2"
    def clear_apache_html(self):
        return "sudo rm -rf /var/www/html/*"

# After installing the web site contents, the server needs to reload
    def reload_apache(self):
        return "sudo /etc/init.d/apache2 reload"
        
    def get_repo_name(self):
        return self.git_link.rsplit('/', 1)[1]

    # Handling our repo, copying it straight to our apache html 
    def handle_repos(self):
        global dir_name
        _clone = "sudo git clone " + self.git_link
        dir_name = self.get_repo_name()
        copy_web = "sudo cp -r %s/. /var/www/html" %dir_name
        cmds = []
        cmds.append(_clone)
        cmds.append(copy_web)
        return cmds