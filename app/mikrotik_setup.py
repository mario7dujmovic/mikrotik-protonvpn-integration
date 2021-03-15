import routeros_api as ros

class MikroTikSetup:
    def __init__(self, host, user, pw):
        self.host = host
        self.user = user
        self.pw = pw

    def connect_api(self):
        connection = ros.RouterOsApiPool(self.host, username=self.user, password=self.pw, plaintext_login=True)
        self.api = connection.get_api()

    def fetch_protonvpn_cert(self):
        self.api.get_binary_resource('/').call('tool/fetch',{ 'url': "https://protonvpn.com/download/ProtonVPN_ike_root.der" })

    def create_certificate(self):
        args = {
            'name': 'ProtonVPN',
            'file-name': 'ProtonVPN_ike_root.der',
            'passphrase': ''
        }
        self.api.get_binary_resource('/').call('certificate/import', args)

    def add_ipsec_mode_config(self):
        self.api.get_binary_resource('/').call('ip/ipsec/mode-config/add', {'connection-mark': 'ProtonVPN', 'name': 'ProtonVPN', 'responder': 'no'})

    def add_ipsec_policy_group(self):
        self.api.get_binary_resource('/').call('ip/ipsec/policy/group/add', {'name': 'ProtonVPN'})

    def add_ipsec_profile(self):
        self.api.get_binary_resource('/').call('ip/ipsec/profile/add', {'dh-group': 'modp4096,modp2048', 'enc-algorithm': 'aes-256', 'hash-algorithm': 'sha256', 'name': 'ProtonVPN'})

    def add_ipsec_peer(self):
        args = {
            'address': 'nl-free-04.protonvpn.com',
            'disabled': 'no',
            'exchange-mode': 'ike2',
            'name': 'ProtonVPN',
            'profile': 'ProtonVPN',
            'send-initial-contact': 'no'
        }
        self.api.get_binary_resource('/').call('ip/ipsec/peer/add',args)

    def get_ipsec_proposal(self):
        proposal = self.api.get_resource('/ip/ipsec/proposal')
        return proposal.get(default="yes")[0]['id']

    def set_ipsec_proposal(self):
        args = {
            'auth-algorithms': 'sha256',
            'enc-algorithms': 'aes-256-cbc',
            'pfs-group': 'modp2048',
            '.id': self.get_ipsec_proposal()
        }
        self.api.get_binary_resource('/').call('ip/ipsec/proposal/set',args)

    def add_ipsec_identity(self, username, password):
        args = {
            'auth-method': 'eap',
            'certificate': 'ProtonVPN',
            'eap-methods': 'eap-mschapv2',
            'generate-policy': 'port-override',
            'mode-config': 'ProtonVPN',
            'peer': 'ProtonVPN',
            'policy-template-group': 'ProtonVPN',
            'username': username,
            'password': password
        }
        self.api.get_binary_resource('/').call('ip/ipsec/identity/add',args)

    def add_ipsec_policy(self):
        args = {
            'dst-address': '0.0.0.0/0',
            'group': 'ProtonVPN',
            'src-address': '0.0.0.0/0',
            'template': 'yes'
        }
        self.api.get_binary_resource('/').call('ip/ipsec/policy/add',args)

    def add_fw_mangle_rule(self, args):
        self.api.get_binary_resource('/').call('ip/firewall/mangle/add', args)

    def add_fw_mangle_prerouting_rule(self):
        args = {
            'chain': 'prerouting',
            'action': 'mark-connection',
            'new-connection-mark': 'ProtonVPN',
            'dst-address': '0.0.0.0/0',
            'connection-mark': 'no-mark'
        }
        self.add_fw_mangle_rule(args)
    
    def add_fw_mangle_output_rule(self):
        args = {
            'chain': 'output',
            'action': 'mark-connection',
            'new-connection-mark': 'ProtonVPN',
            'dst-address': '0.0.0.0/0',
            'connection-mark': 'no-mark'
        }
        self.add_fw_mangle_rule(args)

    def set_ipsec_peer_activation(self):
        args = {
            'disabled': 'no',
            '.id': 'ProtonVPN'
        }
        self.api.get_binary_resource('/').call('ip/ipsec/peer/set',args)