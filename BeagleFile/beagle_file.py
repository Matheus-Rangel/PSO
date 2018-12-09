import json
import time
import os
import shutil
import spur
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class BeagleHandler(FileSystemEventHandler):
    def __init__(self, remote_shell, local_shell, local_directory, remote_directory):
        super().__init__()
        self.remote_shell = remote_shell
        self.local_shell = local_shell
        self.local_directory = local_directory
        self.remote_directory = remote_directory

    def on_created(self, event):
        print(event)
        remote_path = self.format_path(os.path.join(self.remote_directory, os.path.relpath(event.src_path, self.local_directory)))
        if(event.is_directory):
            self.remote_shell.run(["mkdir", "-p", remote_path])
        else:
            self.remote_shell.run(["mkdir", "-p", os.path.dirname(remote_path)])
            with self.remote_shell.open(remote_path, "wb") as remote_file:
                with open(event.src_path, "rb") as local_file:
                    shutil.copyfileobj(local_file, remote_file)

    def on_deleted(self, event):
        print(event)
        remote_path = self.format_path(os.path.join(self.remote_directory, os.path.relpath(event.src_path, self.local_directory)))
        self.remote_shell.run(["rm", "-r", remote_path], allow_error=True)

    def on_modified(self, event):
        print(event)
        remote_path = self.format_path(os.path.join(self.remote_directory, os.path.relpath(event.src_path, self.local_directory)))
        self.remote_shell.run(["mkdir", "-p", os.path.dirname(remote_path)])
        with self.remote_shell.open(remote_path, "wb") as remote_file:
            with open(event.src_path, "rb") as local_file:
                shutil.copyfileobj(local_file, remote_file)

    def on_moved(self, event):
        print(event)
        remote_src_path = self.format_path(os.path.join(self.remote_directory, os.path.relpath(event.src_path, self.local_directory)))
        remote_dest_path = self.format_path(os.path.join(self.remote_directory, os.path.relpath(event.dest_path, self.local_directory)))
        if(event.is_directory):
            self.remote_shell.run(["mkdir", "-p", os.path.dirname(remote_dest_path)])
            self.remote_shell.run(["rm", "-r", remote_src_path])
        else:
            self.remote_shell.run(["mkdir", "-p", os.path.dirname(remote_dest_path)])
            self.remote_shell.run(["mv", remote_src_path, remote_dest_path])
    
    def format_path(self, any_path):
        chars = []
        for i in range(len(any_path)):
            char = any_path[i]
            if char == '\\':
                chars.append('/')
            else:
                chars.append(char)
        return ''.join(chars)

def load():
    config_file = open('config.json', 'r')
    config_dict = json.load(config_file)
    config_file.close()
    hostname = config_dict['hostname']
    username = config_dict['username']
    password = config_dict['password']
    local_directory = config_dict['local_directory']
    remote_directory = config_dict['remote_directory']
    return config_dict

def save(config_dict):
    config_file = open('config.json', 'w')
    json.dump(config_dict, config_file)
    config_file.close()

def main():
    opcao = input('Utilizar a ultima configuração? s/n ')
    if opcao == 's':
        try:
            config = load()
        except:
            print('Não foi possivel carregar a ultima configuração, por favor, inicie novamente o programa com novas configurações')
            return
    elif opcao == 'n':
        config = {}
        config['hostname'] = input('hostname:')
        config['username'] = input('username:')
        config['password'] = input('password:')
        config['local_directory'] = input('diretorio local:')
        config['remote_directory'] = input('diretorio remoto:')
        save(config)
    else:
        print('Opção invalida')
        return
    remote_shell = spur.SshShell(hostname=config['hostname'], username=config['username'], password=config['password'])
    local_shell = spur.LocalShell()
    observer = Observer()
    bh = BeagleHandler(remote_shell, local_shell,  config['local_directory'], config['remote_directory'])
    observer.schedule(bh, config['local_directory'], recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except spur.CouldNotChangeDirectoryError:
        print("Não foi possivel identificar os diretorios, por favor verifique se os diretorios existem")
    observer.join()

if __name__ == "__main__":
    main()