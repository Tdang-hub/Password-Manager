import base64
import os
from cryptography.exceptions import InvalidKey
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def load_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key

def write_key():
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1,
    )
    master_password = input('What do you want the master password to be? ')
    key = kdf.derive(master_password.encode())
    with open('key.key', 'wb') as keyfile:
        keyfile.write(key)

def create_salt():
    salt = os.urandom(16)
    with open('salt.key', 'wb') as keyfile:
        keyfile.write(salt)

def load_salt():
    file = open('salt.key','rb')
    salt = file.read()
    file.close()
    return salt

def auth():
    while True:
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1, )
        try:
            master_pwd = kdf.derive(input('What is the master password? ').encode())
            kdf = Scrypt(
                salt=salt,
                length=32,
                n=2 ** 14,
                r=8,
                p=1, )
            kdf.verify(master_pwd, verify_key)
            print('Correct Password. ')
            break
        except InvalidKey:
            print('Incorrect password. Try again. ')



def view():
    with open('passwords.txt', 'r') as fer:
        for line in fer.readlines():
            data = line.rstrip()
            act,user,passw = data.split('|')
            print('Web Account:', act, '| User:', user, '| Password:', f.decrypt(passw.encode()).decode())

def add():
    account = input('Web Accounts: ')
    name = input('Username: ')
    pwd = input('Password: ')

    with open('passwords.txt', 'a') as fer:
        fer.write(account + '|' + name + '|' + f.encrypt(pwd.encode()).decode() + '\n')
    print('Successfully Added Password. ')

if not os.path.exists('salt.key'):
    create_salt()

salt = load_salt()

kdf = Scrypt(
    salt=salt,
    length=32,
    n=2 ** 14,
    r=8,
    p=1,
)
if not os.path.exists('key.key'):
    write_key()
verify_key = kdf.derive(load_key())

auth()

f = Fernet(base64.urlsafe_b64encode(verify_key))

while True:
    mode = input('Would you like to add a new password or view existing password (view, add)? Press q to quit. ').lower()
    if mode == 'q':
        break
    if mode == 'view':
        view()
    elif mode == 'add':
        add()
    else:
        print('Invalid mode.')
        continue













