#!/usr/bin/python3

import readline
import os,sys
import hashlib
import pathlib, re
from time import sleep
import sqlite3
from getpass import getpass
import pyperclip
from cryptography.fernet import Fernet
from termcolor import colored
from colorama import Fore,init
init()

#Finds the $HOME path
home=pathlib.Path.home()
nhome=re.findall(r"\w*",str(home))
home="/"+nhome[1]+"/"+nhome[3]

#Gets an input to return
def back():
    input(Fore.LIGHTBLUE_EX+" press [Enter] to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)


def passwdb(sname):
    pwd=os.getcwd()
    logo() 
    
    incm=["[0]- write","[1]- read","[2]- delete"]
    for e in incm:
        print(Fore.YELLOW+" ➜"+Fore.LIGHTBLUE_EX+" "+e,"\n")
        sleep(0.2)
    
    com=(input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX))  
   
    if com == "0":
        logo()

        name=input(Fore.LIGHTBLUE_EX+" username "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()
        passwd = getpass(Fore.LIGHTBLUE_EX+" [MASTER] password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)	
        #print(Fore.LIGHTBLUE_EX+" ok, please wait ...")
        
        hasher(sname,name,passwd)

    elif com == "1":
        sqliteR(sname)
    elif com == "2":
        sqliteD(sname)
    else:
        os.chdir(pwd)
        sys.exit()


#Checks if $HOME/.passwdb exists and if not, builds it
def homeC():
    if not os.path.exists(f"{home}/.passwdb"):
        os.mkdir(f"{home}/.passwdb")
        os.mkdir(f"{home}/.passwdb/.data")   

#Prints the Passwdb logo 
def logo():
    os.system("clear") if os.name == "posix" else os.system("cls")
    logo = """
         ██████╗  █████╗ ███████╗███████╗██╗    ██╗██████╗ ██████╗ 
         ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗██╔══██╗
         ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║  ██║██████╔╝
         ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║  ██║██╔══██╗
         ██║     ██║  ██║███████║███████║╚███╔███╔╝██████╔╝██████╔╝
         ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═════╝ ╚═════╝ """
    print(colored(text=logo, color='yellow'))
    print("\t"*4,colored(text="passwdb v0.8", color='yellow', attrs=['blink']))

#This function stores passwords in the database
def sqliteW(sname,name,passwd,_hash):
    logo()
    pwd=os.getcwd()

    try:
        dname=sname
        os.chdir(f"{home}/.passwdb/.data")
        db=sqlite3.connect(f".{dname}.db")
        db.execute("CREATE TABLE hashs (name varchar(20),password INT,hashs varchar(32))")
        db.execute(f"INSERT INTO hashs VALUES('{name}', '{passwd}', '{_hash}')")
    except sqlite3.OperationalError:
        db.execute(f"INSERT INTO hashs VALUES('{name}', '{passwd}', '{_hash}')")
    finally:
        print(Fore.LIGHTBLUE_EX+" Query 1,OK")
        back()
        db.commit()
        db.close()
        passwdb(sname)
        
#Checks whether the database is empty or not
def empty(sname):
    db = sqlite3.connect(f".{sname}.db")
    cursor = db.cursor()
    cursor.execute('''SELECT COUNT(*) from hashs ''')
    result=cursor.fetchall()
    db.close()
    if result[0][0] == 0:
        return True 
    else:
         return False

#Reads databsae data
def sqliteR(sname):
    logo()
    pwd=os.getcwd()

    print(Fore.LIGHTBLUE_EX+" enter the password name or type the all word")
    cms=input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
    dname=sname
    flash = f"{Fore.YELLOW}➜{Fore.LIGHTCYAN_EX}"
    if cms == "all":
        try:
            os.chdir(f"{home}/.passwdb/.data")
            db=sqlite3.connect(f".{dname}.db") 
            hashs=db.execute("SELECT * FROM hashs")
            if empty(sname):    
                print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+" there are no passwords in the database")
            else:
                for name,passwd,phash in hashs:
                    print(Fore.LIGHTCYAN_EX+f"\tname {flash} {name}\n\tpassword {flash} {passwd}\n\tmd5 {flash} {phash}\n")
            
            print(Fore.LIGHTBLUE_EX+" Query 1, OK")
        except Exception as e:
            print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+e)
        finally:
            back()
            db.close()
            passwdb(sname)

    elif cms == "quit":
        os.chdir(pwd)
        sys.exit()
    else:
        try:
            os.chdir(f"{home}/.passwdb/.data")
            db=sqlite3.connect(f".{dname}.db") 
            hashs=db.execute(f"SELECT *  FROM hashs WHERE name='{cms}'")
            for name,passwd,phash in hashs:
                print(Fore.LIGHTCYAN_EX+f"\tname {flash} {name}\n\tpassword {flash} {passwd}\n\tmd5 {flash} {phash}")
        except Exception as e:
            print(Fore.LIGHTRED_EX+"➜ "+Fore.LIGHTBLUE_EX+e)
        finally:
            db.close()
            back()
            passwdb(sname)

#Removes the passwords from database		
def sqliteD(sname):
    logo()
    pwd=os.getcwd()

    inec=["[0]- one", "[1]- all"]
    for i in inec:
        print(Fore.YELLOW+"➜"+Fore.LIGHTBLUE_EX+" "+i,"\n")
        sleep(0.2)

    ind=input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
    dname=sname

    if ind == "0":
        logo()
        name=input(Fore.LIGHTBLUE_EX+" enter name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        passwd=input(Fore.LIGHTBLUE_EX+" enter password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        es=input(Fore.LIGHTBLUE_EX+" do you want to delete it ? [Y/n] "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).upper()
        if es == "Y":
            os.chdir(f"{home}/.passwdb/.data")
            db=sqlite3.connect(f".{dname}.db") 
            try:
                db.execute("DELETE FROM hashs WHERE name='%s' AND password='%s' "%(name,passwd))
                db.commit()
                db.close()
                print(Fore.LIGHTBLUE_EX+" Query 1, OK")
            except:
                print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTRED_EX+" This password isn't exists !")
            finally:    
                back()
                passwdb(sname)
        else:
            back()
            passwdb(sname)
    elif ind == "1":
        logo()
        es=input(Fore.LIGHTBLUE_EX+" do you want to delete it ? [y/n] "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).upper()
        if es == "Y":
            os.chdir(f"{home}/.passwdb/.data")
            db=sqlite3.connect(f".{dname}.db") 
            db.execute("DELETE FROM hashs")
            db.commit()
            db.close()

            print(Fore.LIGHTBLUE_EX+" Query 1, OK")
            back()
            passwdb(sname)
        else:
            back()
            passwdb(sname)
    elif ind == "quit":
        os.chdir(pwd)
        sys.exit()
    else:
        print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTRED_EX+" not found !")
        back()
        passwdb(sname)
		
#This function hashes passwords
def hasher(sname,name,passwd):
    ##Hashes the password and then calls the sqliteW function

    hsh=hashlib.md5()
    hsh.update(passwd.encode("utf-8"))
    _hash=hsh.hexdigest()

    sqliteW(sname,name,passwd,_hash)

#Builds accounts
def account():
    logo()
    pwd=os.getcwd()
    
    name=input(Fore.LIGHTBLUE_EX+" enter name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
    passwd = getpass(Fore.LIGHTBLUE_EX+" enter password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
    print(Fore.LIGHTBLUE_EX+" ok !, please wait ...")
    sleep(3)
    
    hsh=hashlib.md5()
    hsh.update(passwd.encode("utf-8"))
    _hash=hsh.hexdigest()
    fe = False
    os.chdir(f"{home}/.passwdb/.data")
    if os.path.exists(f"{home}/.passwdb/.data/.li.db"):
        try:
            ex=sqlite3.connect(".li.db")
            xe = ex.execute("SELECT * from li")    
            fe = True
            for n, p, h in xe:
                if n == name:            
                    print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+" this account already exists !")
                    back()
                    ex.close()
                    login()           
        except:
            return 
    try:
        db=sqlite3.connect(".li.db")
        if fe == False:
            db.execute("CREATE TABLE li (name varchar(20),password INT,hashs varchar(32))")
        db.execute("INSERT INTO li VALUES('%s','%s','%s')"%(name,passwd,_hash))
        db.commit()
        db.close()
        print(Fore.LIGHTBLUE_EX+" Query 1,OK")
        back()
        login()
    except Exception as e:
        print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+e)
        back()
        login()


#Checks the authenticity of the username/password user for user login
def login():
    logo()
    pwd=os.getcwd()
    
    print(Fore.LIGHTBLUE_EX+" WELCOME TO PASSWDB ! :)\n")
    incm=["[0]- login ","[1]- account"] 
    for e in incm:
        print(Fore.YELLOW+" ➜"+Fore.LIGHTBLUE_EX+" "+e,"\n")
    com=(input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX))
    
    if com == "0":
        logo()
        
        name=input(Fore.LIGHTBLUE_EX+" enter name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX+"")
        passwd = getpass(Fore.LIGHTBLUE_EX+" enter password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        print(Fore.LIGHTBLUE_EX+" ok !, please wait ...")


        try:
            os.chdir(f"{home}/.passwdb/.data")
            db=sqlite3.connect(".li.db")
            ac=db.execute("SELECT * FROM li")
            sname=name
        except:
            print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" account is not exists !")
            back()
            main()

        for pname,ppasswd,phash in ac:
            nname=pname
            npasswd=ppasswd
            nhash=phash
        if name == nname:
            if passwd == npasswd:
                passwdb(sname)
            else:
                print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" name or password is wrong ! ")
                back()
                main()
        else:
            print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" name or password is wrong ! ")
            back()
            main()

    elif com == "1":
        account()
    else:
        os.chdir(pwd)
        sys.exit()

#Calls the homeC and login function 
def main():
    homeC()
    login()
	
if __name__ == "__main__":
    main() # Runs as the first function

