# autoDeploy

For now, the script works only for static websites.


```sh
$: autodeploy.py
             _        ____             _
  __ _ _   _| |_ ___ |  _ \  ___ _ __ | | ___  _   _
 / _` | | | | __/ _ \| | | |/ _ \ '_ \| |/ _ \| | | |
| (_| | |_| | || (_) | |_| |  __/ |_) | | (_) | |_| |
 \__,_|\__,_|\__\___/|____/ \___| .__/|_|\___/ \__, |
                                |_|            |___/

Please enter the host ip: test
Please enter the username on the machine: test
Please enter the password:
Please enter github repo link: test
Connecting: 100%|████████████████████████████████████████████████████████████████████████████████| 100/100 [00:05<00:00, 18.06it/s]
Connection failed, try again.
$: python autodeploy.py
             _        ____             _
  __ _ _   _| |_ ___ |  _ \  ___ _ __ | | ___  _   _
 / _` | | | | __/ _ \| | | |/ _ \ '_ \| |/ _ \| | | |
| (_| | |_| | || (_) | |_| |  __/ |_) | | (_) | |_| |
 \__,_|\__,_|\__\___/|____/ \___| .__/|_|\___/ \__, |
                                |_|            |___/

Please enter the host ip: myActualServer
Please enter the username on the machine: debian
Please enter the password:
Please enter github repo link:
Connecting: 100%|████████████████████████████████████████████████████████████████████████████████| 100/100 [00:05<00:00, 18.06it/s]
Connection established successfully!
```
