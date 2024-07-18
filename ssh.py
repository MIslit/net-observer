import paramiko

class SSH:
    def __init__(self, message):
        self.message = message

    async def get_routes(self, message):
        router_ip = "192.168.10.62"
        router_username = "root"
        router_password = "P@ssw0rd"
        port = 2222
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(router_ip, username=router_username, password=router_password, port=port, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})

        command = message.get_args()
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()

        await message.reply(output)