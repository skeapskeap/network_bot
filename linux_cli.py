import subprocess
import socket


def linux_cli(target: str, command: str) -> str:
    if valid_target(target):
        query = [command, target, '-c 4']
        try:
            result = subprocess.check_output(query, universal_newlines=True, stderr=subprocess.STDOUT)
        except FileNotFoundError as no_file:
            result = f'{no_file.filename}: {no_file.strerror}'
        except subprocess.CalledProcessError as proc_err:
            result = proc_err.output
        return result
    else:
        return 'incorrect host'


def valid_target(target:str) -> bool:
        try:
            target = socket.gethostbyname(target)     # если указан домен, проверяет резолвинг его в IP
            return True                               # если указан ip, проверяет его корректность
        except socket.error:
            return False


if __name__ == '__main__':
    print(linux_cli('8.8.8.8', 'ping'))