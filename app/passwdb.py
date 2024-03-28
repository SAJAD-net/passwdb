#!/usr/bin/env python3

from base64 import b64encode, urlsafe_b64encode
import readline
import os.path
import sys
import hashlib
import pathlib
import re
from time import sleep
import sqlite3
from getpass import getpass
import pyperclip
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from termcolor import colored
from colorama import Fore, init
init()

# Finds the home path in linux
if os.name == "posix":
    home = pathlib.Path.home()
    nhome = re.findall(r"\w*", str(home))
    home = "/"+nhome[1]+"/"+nhome[3]

# Finds the home path in windows
else:
    home = str(pathlib.Path.home())

first_location = os.getcwd()

# Gets an input to return
def back():
    input(Fore.LIGHTBLUE_EX+" [Enter] to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)


def passwdb(sname, mpassword):
    logo()
    incm = ["[0]- write", "[1]- read", "[2]- delete"]
    for option in incm:
        print(Fore.YELLOW+" ➜"+Fore.LIGHTBLUE_EX+" "+str(option), "\n")
        sleep(0.2)

    choice = input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()
    if choice == "0":
        logo()

        name = input(Fore.LIGHTBLUE_EX+" name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()
        password = getpass(Fore.LIGHTBLUE_EX+" password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()

        write_password(sname, name, password, mpassword)

    elif choice == "1":
        read_password(sname, mpassword)

    elif choice == "2":
        delete_password(sname, mpassword)

    else:
        os.chdir(first_location)
        sys.exit()


# Checks if $HOME/.passwdb directory exists, otherwise, creates it
def create_home_dir():
    if not os.path.exists(f"{home}/.passwdb"):
        os.mkdir(f"{home}/.passwdb")
        os.mkdir(f"{home}/.passwdb/.data")

    os.chdir(f"{home}/.passwdb/.data")


# Prints the passwdb logo
def logo():
    os.system("clear") if os.name == "posix" else os.system("cls")
    logo_str = """
         ██████╗  █████╗ ███████╗███████╗██╗    ██╗██████╗ ██████╗
         ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗██╔══██╗
         ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║  ██║██████╔╝
         ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║  ██║██╔══██╗
         ██║     ██║  ██║███████║███████║╚███╔███╔╝██████╔╝██████╔╝
         ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═════╝ ╚═════╝ """
    print(colored(text=logo_str, color='yellow'))
    print("\t"*4, colored(text="passwdb v0.8", color='yellow', attrs=['blink']))


# This function stores passwords in the database
def write_password(sname, name, password, mpassword):
    logo()

    hashed = encrypt_password(sname, mpassword, password)
    db = sqlite3.connect(f".{sname}.db")

    try:
        db.execute("CREATE TABLE passwsh (name varchar(20), hash varchar(64))")
        db.execute(f"INSERT INTO passwsh VALUES('{name}', '{hashed}')")

    except sqlite3.OperationalError:
        db.execute(f"INSERT INTO passwsh VALUES('{name}', '{hashed}')")

    finally:
        print(Fore.LIGHTBLUE_EX+" Query 1, OK")
        db.commit()
        db.close()
        back()
        passwdb(sname, mpassword)


# Checks whether the database is is_empty or not
def is_empty(sname):
    db = sqlite3.connect(f".{sname}.db")
    cursor = db.cursor()
    cursor.execute('''SELECT COUNT(*) from passwsh''')
    result = cursor.fetchall()[0][0]
    cursor.close()
    db.close()
    if result == 0:
        return True

    return False


# Reads databsae data
def read_password(sname, mpassword):
    logo()

    print(Fore.LIGHTBLUE_EX+" Enter the password name or type 'all' to get a list of all the passwords")
    choice = input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()

    if not os.path.exists(f"{home}/.passwdb/.data/.{sname}.db"):
        print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+" No password in the database")
        back()
        passwdb(sname, mpassword)

    flash = f"{Fore.YELLOW}➜{Fore.LIGHTCYAN_EX}"
    if choice == "all":
        try:
            db = sqlite3.connect(f".{sname}.db")
            result = db.execute("SELECT * FROM passwsh")

            if is_empty(sname):
                print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+" there is no password in the database")
                db.close()
                back()
                passwdb(sname, mpassword)

            for name, _ in result.fetchall():
                print(Fore.LIGHTCYAN_EX+f"\tname {flash} {name}")

            print(Fore.LIGHTBLUE_EX+" Query 1, OK")

        except Exception as e:
            print(Fore.LIGHTRED_EX+"➜ "+Fore.LIGHTBLUE_EX+str(e))

        finally:
            db.close()
            back()
            passwdb(sname, mpassword)

    elif choice == "quit":
        os.chdir(first_location)
        sys.exit()

    else:
        try:
            db = sqlite3.connect(f".{sname}.db")
            result = db.execute(f"SELECT * FROM passwsh WHERE name='{choice}'")
            name, hashed = result.fetchone()

            password = decrypt_password(sname, mpassword, hashed)
            pyperclip.copy(password)
            print(Fore.LIGHTCYAN_EX+f"\tname {flash} {name}\n\tpassword {flash} copied !\n")

        except:
            print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTRED_EX+" Password doesn't exist!")

        finally:
            db.close()
            back()
            passwdb(sname, mpassword)


# Deleting password from the database
def delete_password(sname, mpassword):
    logo()

    print(Fore.LIGHTBLUE_EX+" Enter the password name or 'all' to wipe all the passwords")
    cms = input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()

    if cms == "all":
        logo()

        choice = input(Fore.LIGHTBLUE_EX+" Are you sure ? [Y/n] "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).upper()
        if choice == "Y":
            db = sqlite3.connect(f".{sname}.db")
            db.execute("DELETE FROM passwsh")
            db.commit()
            db.close()

            print(Fore.LIGHTBLUE_EX+" Query 1, OK")

            back()
            passwdb(sname, mpassword)

        else:
            print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTRED_EX+" Cancelled")
            back()
            passwdb(sname, mpassword)

    elif cms == "quit":
        os.chdir(first_location)
        sys.exit()

    else:
        logo()

        choice = input(Fore.LIGHTBLUE_EX+" Are you sure ? [Y/n] "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).upper()
        if choice == "Y":
            try:
                db = sqlite3.connect(f".{sname}.db")
                db.execute(f"DELETE FROM passwsh WHERE name='{cms}'")
                print(Fore.LIGHTBLUE_EX+" Query 1, OK")

            except:
                print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTRED_EX+" Password doesn't exist!")

            finally:
                db.commit()
                db.close()
                back()
                passwdb(sname, mpassword)
 
        else:
            print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTRED_EX+" Cancelled")
            back()
            passwdb(sname, mpassword)


# Encrypt passwords
def encrypt_password(sname, mpassword, password):
    # Encrypts the password and then calls the write_password function
    hashed = generate_key(sname, mpassword).encrypt(password.encode()).decode()
    return hashed


# Decrypt passwords
def decrypt_password(sname, mpassword, hashed):
    # Decrypts the password and then calls the write_password function
    password = generate_key(sname, mpassword).decrypt(hashed.encode()).decode()
    return password


def generate_key(sname, mpassword):
    # GENERATES A KEY FROM PASSWORD
    try:
        db = sqlite3.connect(".account.db")
        result = db.execute(f"SELECT Salt FROM accounts WHERE Username='{sname}'")
        salt = result.fetchone()[0]
        db.close()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=480000,
        )

        key = urlsafe_b64encode(kdf.derive(mpassword.encode()))
        return Fernet(key)

    except Exception as e:
        print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+str(e))


# Hash the master password
def mpassword_hash(mpassword):
    sha256 = hashlib.sha256()
    sha256.update(mpassword.encode("utf-8"))
    return sha256.hexdigest()


# Creating account
def account():
    logo()

    username = input(Fore.LIGHTBLUE_EX+" Username "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()
    mpassword = getpass(Fore.LIGHTBLUE_EX+" [MASTER] password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()

    hashed = mpassword_hash(mpassword)

    texist = False

    if os.path.exists(f"{home}/.passwdb/.data/.account.db"):
        try:
            db = sqlite3.connect(".account.db")

            result = db.execute(f"SELECT * from accounts WHERE Username='{username}'")
            if result.fetchone():
                print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+" Username already exists !")
                db.close()
                back()
                login()

            db.close()
            texist = True

        except:
            db.close()

    try:
        db = sqlite3.connect(".account.db")
        if not texist:
            db.execute("CREATE TABLE accounts (Username varchar(20), Hash varchar(64), Salt varchar(32))")

        salt = b64encode(os.urandom(16)).decode('utf-8')
        db.execute(f"INSERT INTO accounts VALUES('{username}', '{hashed}', '{salt}')")
        db.commit()
        db.close()

        print(Fore.LIGHTBLUE_EX+" Query 1, OK")
        back()
        login()

    except Exception as e:
        print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+str(e))
        db.close()
        back()
        login()


# Checks the authenticity of the username/password.
def login():
    logo()

    print(Fore.LIGHTBLUE_EX+" WELCOME TO PASSWDB ! :)\n")

    incm = ["[0]- login ", "[1]- account"]
    for opt in incm:
        print(Fore.YELLOW+" ➜"+Fore.LIGHTBLUE_EX+" "+str(opt),"\n")

    choice = input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)

    if choice == "0":
        logo()

        username = input(Fore.LIGHTBLUE_EX+" Username "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX+"")
        mpassword = getpass(Fore.LIGHTBLUE_EX + "[MASTER] password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        hashed = mpassword_hash(mpassword)

        try:
            db = sqlite3.connect(".account.db")
            result = db.execute(f"SELECT * FROM accounts WHERE Username='{username}' AND Hash='{hashed}'")
            if result.fetchone():
                db.close()
                passwdb(username, mpassword)

            print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" Username or password is wrong ! ")
            db.close()
            back()
            main()

        except:
            print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" Account doesn't exist !")
            db.close()
            back()
            main()

    elif choice == "1":
        account()

    else:
        os.chdir(first_location)
        sys.exit()


# Calls the create_home_dir and login functions
def main():
    create_home_dir()
    login()


main()
