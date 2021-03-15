import PySimpleGUI as sg
import routeros_api as ros
from mikrotik_setup import MikroTikSetup as mtik

sg.theme('SystemDefaultForReal')

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
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Ok':
        try:
            setupMikrotik = mtik(values[2], values[3], values[4])
            setupMikrotik.connect_api()
            setupMikrotik.fetch_protonvpn_cert()
            setupMikrotik.create_certificate()
            setupMikrotik.add_ipsec_mode_config()
            setupMikrotik.add_ipsec_policy_group()
            setupMikrotik.add_ipsec_profile()
            setupMikrotik.add_ipsec_peer()
            setupMikrotik.set_ipsec_proposal()
            setupMikrotik.add_ipsec_identity(values[0], values[1])
            setupMikrotik.add_ipsec_policy()
            setupMikrotik.add_fw_mangle_prerouting_rule()
            setupMikrotik.add_fw_mangle_output_rule()
        except ValueError:
            print("Things broke somewhere lol")
            
        break

window.close()