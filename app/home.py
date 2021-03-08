import PySimpleGUI as sg
import routeros_api as ros
from mikrotik_setup import MikroTikSetup as mtik

def print_users(router_api):
    return router_api.get_binary_resource('/').call('user/print', {})

sg.theme('SystemDefaultForReal')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Configure ProtonVPN on MikroTik', font='14')],
            [sg.Text('OpenVPN / IKEv2 username: '), sg.InputText()],
            [sg.Text('OpenVPN / IKEv2 password: '), sg.InputText()],
            [sg.Text('MikroTik IP address: '), sg.InputText()],
            [sg.Text('MikroTik User: '), sg.InputText()],
            [sg.Text('MikroTik Password: '), sg.InputText()],
            [sg.Button('Ok', bind_return_key=True), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Ok':
        # connection = ros.RouterOsApiPool(values[2], username=values[3], password=values[4], plaintext_login=True)
        # api = connection.get_api()
        # api.get_binary_resource('/').call('tool/fetch',{ 'url': "https://protonvpn.com/download/ProtonVPN_ike_root.der" })
        #users = api.get_resource('user')
        try:
            setupMikrotik = mtik(values[2], values[3], values[4])
            setupMikrotik.connect_to_api()
            #setupMikrotik.get_protonvpn_cert()
            #setupMikrotik.set_ipsec_mode_config()
            print(setupMikrotik.get_ipsec_proposal())
            # users.remove(id="testuser1")
            # users.add(name='testuser1', password='987654321', group='read')
            # users_list = print_users(api)
            print('users_list')
        except ValueError:
            print("Could not add a user, since it already exists.")

window.close()