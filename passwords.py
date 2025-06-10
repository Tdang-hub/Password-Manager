class Password:

    def __init__(self,web_account,username,password):
        self.__web_account = web_account
        self.__username = username
        self.__password = password

    def set_web_account(self,web_account):
        self.__web_account = web_account

    def set_username(self,username):
        self.__username = username

    def set_password(self,password):
        self.__password = password

    def get_web_account(self):
        return self.__web_account

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def __str__(self):
        return f'Web Account: {self.__web_account}\n' +\
            f'Username: {self.__username}\n' +\
            f'Password: {self.__password}\n'