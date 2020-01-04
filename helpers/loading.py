import sys
import time
import pyfiglet
from tqdm import tqdm
sys.path.append('c:\\Users\\Samoil\\Desktop\\auto\\helpers')
from colors import bcolors
def loading():
    for _ in tqdm(range(100), desc=bcolors.OKBLUE + "Connecting" + bcolors.BOLD):
        time.sleep(0.05)
def installing():
    for _ in tqdm(range(100), desc=bcolors.OKGREEN + "Installing" + bcolors.BOLD):
        time.sleep(0.1)
def welcome_banner():
    print(pyfiglet.figlet_format("autoDeploy"))