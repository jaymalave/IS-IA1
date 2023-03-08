import sqlite3
import json
import hashlib
from cryptography.fernet import Fernet


conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# cursor.execute('CREATE TABLE IF NOT EXISTS PW(ACCOUNT TEXT, PASSWORD TEXT)')

def write_key():
   key = Fernet.generate_key()
   print(key)
   with open("key.key", "wb") as key_file:
        key_file.write(key)

   

def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

key = load_key()
fer = Fernet(key)

def add():

    acc = input("Enter the account: ")
    pw = input("Enter the password: ")

    encryptedpw = fer.encrypt(pw.encode()).decode()
    

    cursor.execute('INSERT INTO PW(ACCOUNT, PASSWORD) VALUES (?, ?)', (  acc  ,  encryptedpw   ))

    conn.commit()
    
    print("success")

def view():
    
    for row in cursor.execute('SELECT * FROM PW;'):
     account = row[0]
     password = row[1]
     decpas = fer.decrypt(password.encode()).decode()
     print(account, "|", decpas)


def close():
    conn.close()


def main():

    task = input("Press r to view the passwords and w to add a new one: ")

    if task == 'r':
        view()
    elif task == 'w':
        add()
    else:
     print("Invalid request")

    close()




masterpassword = input("Enter the master-password: ")

if hashlib.sha512(masterpassword.encode()).hexdigest() == '0022c89227de3975a820e5b49ed326e1f28354634e11ade0c2f7d0738855b5e50eaea2a270030cdc8e13858a458c250d0d117ac0d2cc2714d7e6342d6d102cb8':
    main()
else:
    print("Invalid Credentials")

