import getpass
import sys
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\helpers')
from colors import bcolors

def get_user_info():
    host_name = input("Please enter the host ip: ")
    username = input("Please enter the username on the machine: ")
    pw = getpass.getpass("Please enter the password: ")
    gitRepo = input("Please enter github repo link: ")
    print(bcolors.WARNING + "Connecting to machine '{0}', with username '{1}'.".format(host_name, username) + bcolors.ENDC)
    return host_name, username, pw, gitRepo

def check_web_type():
    print(f"{bcolors.WARNING}Please select what kind of website you're building: {bcolors.ENDC}")
    print(bcolors.OKGREEN + "[J]ekyll, [S]tatic HTML/CSS, [L]aravel")
    user_input = input(bcolors.OKGREEN + "-->")
    while True:
        if user_input.lower() not in ('j', 's', 'l'):
            print(f"{bcolors.WARNING}Please enter valid input.{bcolors.ENDC}")
            user_input = input(bcolors.OKGREEN + "-->")
        else:
            break
    return user_input

def check_continue():
    _user = input(f"{bcolors.WARNING}Are you sure you want to continue? (Clean /var/www/html/ and install repo)? [Y/n]{bcolors.ENDC}")
    if _user.lower() == 'y':
        return True
    else:
        return False

