import base64
import os
from cryptography.exceptions import InvalidKey
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import pickle
import passwords

VIEW_ALL = 1
ADD = 2
CHANGE = 3
DELETE = 4
CHANGE_MASTER = 5
QUIT = 6

FILENAME = 'passwords.dat'

'''Database Encryption
____________________________________________________________________'''
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

'''Password Selection
__________________________________________________________________'''
def main():


    mypasswords = load_passwords()

    choice = 0

    while choice != QUIT:
        choice = get_menu_choice()

        if choice == VIEW_ALL:
            view_all(mypasswords)
        if choice == ADD:
            add(mypasswords)
        if choice == CHANGE:
            change(mypasswords)
        if choice == CHANGE_MASTER:
            write_key()
        if choice == DELETE:
            delete(mypasswords)

    save_passwords(mypasswords)

def load_passwords():
    try:
        input_file = open(FILENAME, 'rb')
        passwords_dct = pickle.load(input_file)
        input_file.close()
    except IOError:
        passwords_dct = {}
    return passwords_dct

def get_menu_choice():
    print('\nPassword Database')
    print('____________________________')
    print('1. View all passwords. ')
    print('2. Add a password. ')
    print('3. Change a password')
    print('4. Delete a password. ')
    print('5. Change master password. ')
    print('6. Quit the program. ')
    print()

    choice = 0

    while choice < VIEW_ALL or choice > QUIT:
        try:
            choice = int(input('Enter your choice: '))
        except ValueError:
            print('Please input a selection. ')
        return choice

def view_all(mypasswords):
    print('Here are all of the stored passwords')
    print('____________________________________')
    for key, password in mypasswords.items():
        print()
        print(f'Web Account: {password.get_web_account()}')
        print(f'Username: {password.get_username()}')
        print(f'Password: {f.decrypt(password.get_password().encode()).decode()}')


def add(mypasswords):
    account = input('Web Accounts: ')
    name = input('Username: ')
    pwd = f.encrypt(input('Password: ').encode()).decode()

    entry = passwords.Password(account,name,pwd)

    if name not in mypasswords:
        mypasswords[account] = entry
        print('\nPassword has been added. ')
    else:
        print('\nThat web account already exists. ')

def change(mypasswords):

    web_account = input('\nEnter web account name: ')

    if web_account in mypasswords:
        username = input('Enter a new username: ')
        password = f.encrypt(input('Enter a new password: ').encode()).decode()

        entry = passwords.Password(web_account,username,password)
        mypasswords[web_account] = entry
        print('Information Updated. ')
    else:
        print('Web account not found. ')

def delete(mypasswords):
    web_account = input('Enter web account name: ')
    if web_account in mypasswords:
        del mypasswords[web_account]
        print('Entry deleted. \n')
    else:
        print('Web account not found. ')

def save_passwords(mypasswords):
    output_file = open(FILENAME, 'wb')
    pickle.dump(mypasswords, output_file)
    output_file.close()

main()









