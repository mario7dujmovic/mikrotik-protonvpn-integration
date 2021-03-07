import routeros_api as ros

class MikroTikSetup:
    def __init__(self, host, user, pw):
        self.host = host
        self.user = user
        self.pw = pw

    def connect_to_api(self):
        connection = ros.RouterOsApiPool(self.host, username=self.user, password=self.pw, plaintext_login=True)
        self.api = connection.get_api()

    def get_protonvpn_cert(self):
        self.api.get_binary_resource('/').call('tool/fetch',{ 'url': "https://protonvpn.com/download/ProtonVPN_ike_root.der" })

    def set_ipsec_mode_config(self):
        self.api.get_binary_resource('/').call('ip/ipsec/mode-config/add', {'connection-mark': 'ProtonVPN1', 'name': 'ProtonVPN1', 'responder': 'no'})

    def set_ipsec_policy_group(self):
        self.api.get_binary_resource('/').call('ip/ipsec/policy/group/add', {'name': 'ProtonVPN'})

    def set_ipsec_profile(self):
        self.api.get_binary_resource('/').call('ip/ipsec/profile/add', {'dh-group': 'modp4096,modp2048', 'enc-algorithm': 'aes-256', 'hash-algorithm': 'sha256', 'name': 'ProtonVPN'})

    def set_ipsec_peer(self):
        args = {
            'address': 'nl-free-04.protonvpn.com',
            'disabled': 'yes',
            'exchange-mode': 'ike2',
            'name': 'ProtonVPN',
            'profile': 'ProtonVPN',
            'send-initial-contact': 'no'
        }
        self.api.get_binary_resource('/').call('ip/ipsec/peer/add',args)

    def set_ipsec_proposal(self):
        args = {

        }
        self.api.get_binary_resource('/').call('ip/ipsec/proposal/set',args)