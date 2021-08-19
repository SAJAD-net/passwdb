#!/usr/bin/python3

import readline
import os,sys
from colorama import Fore,init
init()
from termcolor import colored
from getpass import getpass
from time import sleep
import pathlib, re
import sqlite3
import hashlib

home=pathlib.Path.home()
nhome=re.findall(r"\w*",str(home))
home="/"+nhome[1]+"/"+nhome[3]

#logo printer

def homeC():
    if not os.path.exists(f"{home}/.passwdb"):
        os.mkdir(f"{home}/.passwdb")
        os.mkdir(f"{home}/.passwdb/.data")   

def logo():
    logo = """
         ██████╗  █████╗ ███████╗███████╗██╗    ██╗██████╗ ██████╗ 
         ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗██╔══██╗
         ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║  ██║██████╔╝
         ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║  ██║██╔══██╗
         ██║     ██║  ██║███████║███████║╚███╔███╔╝██████╔╝██████╔╝
         ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═════╝ ╚═════╝ """
    print(colored(text=logo, color='yellow'))
    print("\t"*4,colored(text="passwdb v0.5", color='yellow', attrs=['blink']))

# this function saved the passwords and hashs on databases 
def sqliteW(sname,name,passwd,_hash):
    os.system("clear") if os.name=="posix" else os.system("cls")
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
        input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        db.commit()
        db.close()
        passwdb(sname)
        
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

# database reade    r		
def sqliteR(sname):
## readin the passwords from dateabase
    os.system("clear") if os.name=="posix" else os.system("cls")
    logo()
    pwd=os.getcwd()

    print(Fore.LIGHTBLUE_EX+" name of password or enter all")
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
            input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
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
            input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
            passwdb(sname)

# Password remover				
def sqliteD(sname):
    os.system("clear") if os.name=="posix" else os.system("cls")
    logo()
    pwd=os.getcwd()

    inec=["[0]- one", "[1]- all"]
    for i in inec:
        print(Fore.YELLOW+"➜"+Fore.LIGHTBLUE_EX+" "+i,"\n")
        sleep(0.2)

    ind=input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
    dname=sname

    if ind == "0":
        os.system("clear") if os.name=="posix" else os.system("cls")
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
                input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
                passwdb(sname)
        else:
            input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
            passwdb(sname)
    elif ind == "1":
        os.system("clear") if os.name=="posix" else os.system("cls")
        logo()
        es=input(Fore.LIGHTBLUE_EX+" do you want to delete it ? [y/n] "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).upper()
        if es == "Y":
            os.chdir(f"{home}/.passwdb/.data")
            db=sqlite3.connect(f".{dname}.db") 
            db.execute("DELETE FROM hashs")
            db.commit()
            db.close()

            print(Fore.LIGHTBLUE_EX+" Query 1, OK")
            input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
            passwdb(sname)
        else:
            input(Fore.LIGHTBLUE_EX+" press enter to return" +Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
            passwdb(sname)
    elif ind == "quit":
        os.chdir(pwd)
        sys.exit()
    else:
        print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTRED_EX+" not found !")
        input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        passwdb(sname)
		
# this function hashs the passwords
def hasher(sname,name,passwd):
    ## Hashes the password and then calls the sqliteW function

    hsh=hashlib.md5()
    hsh.update(passwd.encode("utf-8"))
    _hash=hsh.hexdigest()

    sqliteW(sname,name,passwd,_hash)

# account creator
def account():
    os.system("clear") if os.name == "posix" else os.system("cls")
    logo()
    pwd=os.getcwd()
    
    name=input(Fore.LIGHTBLUE_EX+" enter name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
    passwd = getpass(Fore.LIGHTBLUE_EX+" enter password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
    print(Fore.LIGHTBLUE_EX+" ok !, please wite ...")
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
                    input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
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
        input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        login()
    except Exception as e:
        print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+e)
        input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        login()


## login function
def login():
    os.system("clear") if os.name == "posix" else os.system("cls")
    pwd=os.getcwd()
    logo()
    
    print(Fore.LIGHTBLUE_EX+" WELCOME TO PASSWDB ! :)\n")
    incm=["[0]- login ","[1]- account"] 
    for e in incm:
        print(Fore.YELLOW+" ➜"+Fore.LIGHTBLUE_EX+" "+e,"\n")
    com=(input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX))
    
    if com == "0":
        os.system("clear") if os.name == "posix" else os.system("cls")
        logo()
        
        name=input(Fore.LIGHTBLUE_EX+" enter name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX+"")
        passwd = getpass(Fore.LIGHTBLUE_EX+" enter password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
        print(Fore.LIGHTBLUE_EX+" ok !, please wite ...")


        try:
            os.chdir(f"{home}/.passwdb/.data")
            db=sqlite3.connect(".li.db")
            ac=db.execute("SELECT * FROM li")
            sname=name
        except:
            print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" account is not exists !")
            input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
            loginer()

        for pname,ppasswd,phash in ac:
            nname=pname
            npasswd=ppasswd
            nhash=phash
        if name == nname:
            if passwd == npasswd:
                passwdb(sname)
            else:
                print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" name or password is wrong ! ")
                input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
                loginer()
        else:
            print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" name or password is wrong ! ")
            input(Fore.LIGHTBLUE_EX+" press enter to return "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
            loginer()

    elif com == "1":
        account()
    else:
        os.chdir(pwd)
        sys.exit()

def loginer():
    homeC()
    login()
	
def passwdb(sname): 
    
    pwd=os.getcwd()
    os.system("clear") if os.name == "posix" else os.system("cls")
    logo()
    
    incm=["[0]- write","[1]- read","[2]- delete"]
    for e in incm:
        print(Fore.YELLOW+" ➜"+Fore.LIGHTBLUE_EX+" "+e,"\n")
        sleep(0.2)
    
    com=(input(Fore.LIGHTBLUE_EX+" passwdb "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX))  
   
    if com == "0":
        os.system("clear") if os.name == "posix" else os.system("cls")
        logo()
        
        name=input(Fore.LIGHTBLUE_EX+" enter name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()
        passwd = getpass(Fore.LIGHTBLUE_EX+" enter password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)	
        print(Fore.LIGHTBLUE_EX+" ok, please wite ...")
        
        hasher(sname,name,passwd)

    elif com == "1":
        sqliteR(sname)
    elif com == "2":
        sqliteD(sname)
    else:
        os.chdir(pwd)
        sys.exit()

loginer() # Runs as the first function
sname=""

if __name__ == "__passwdb__":passwdb(sname)
if __name__ == "__account__":account()
if __name__ == "__login__":login()
if __name__ == "__loginer__":loginer()
