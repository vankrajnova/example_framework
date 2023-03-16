import traceback
import paramiko


class PowerShellHelper:
    def __init__(self, config):
        self.config = config
        self._ssh = self.initialize_session(username=self.config.pwsh_login, password=self.config.pwsh_pwd)

    def initialize_session(self, username, password):
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.config.pwsh_ip,
                        port=22,
                        username=username,
                        password=password,
                        timeout=200,
                        look_for_keys=False)
        except ConnectionResetError:
            print(traceback.format_exc())
            return ssh
        return ssh

    def close(self):
        self._ssh.close()

    def _is_session_valid(self):
        try:
            if self._ssh.get_transport().authenticated:
                return True
        except Exception as e:
            print(f'Ошибка {e}:\n', traceback.format_exc())
            return False

    def _exec_command(self, ssh_cmnd):
        if self._is_session_valid():
            *x, stderr = self._ssh.exec_command(ssh_cmnd)
            return x

    def get_account_status(self, account_name) -> str:
        ssh_cmnd = f'Get-ADUser -Identity "{account_name}" -Properties Enabled | Select-Object -ExpandProperty Enabled'
        _, stdout = self._exec_command(ssh_cmnd)
        status = stdout.read().decode("cp866")
        return status.strip()

    def get_account_name_list(self) -> list:
        ssh_cmnd = f'Get-ADUser -Filter * | Select-Object -Expand SamAccountName'
        _, stdout = self._exec_command(ssh_cmnd)
        account_name_list = stdout.read().decode('cp866').replace('\r\n', ' ').split(' ')
        return account_name_list
