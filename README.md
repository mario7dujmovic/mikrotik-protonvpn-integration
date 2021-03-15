# mikrotik-protonvpn-integration
This application enables you to easily implement ProtonVPN on your MikroTik routers.

## getting started
### prerequisites:
- python 3.8, pip, pipenv, tkinter
- ability to display to screen (WSL2 has issues)

### setup
`pipenv --python 3.8`

`pipenv install -r requirements.txt`

### running the script 
`pipenv run python app/home.py`

### worth noting
- the system clock on your router has to be set up properly. the certificates won't work if your clock is set to 1970
- the ProtonVPN server is currently hardcoded into the application, but the goal (for the start) is to have a dropdown of free VPN servers. if you'd like to change the server you're connecting to, run the app as you normally would, and then log in into your router and run this command:
`/ip ipsec peer set address=your-awesome-protonvpn-server.com ProtonVPN`