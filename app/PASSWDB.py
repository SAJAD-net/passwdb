#!/usr/bin/python3

##THIS IS THE IMPORTING OS LIBRARY
import os,sys
from colorama import Fore,init
init()
from getpass import getpass
##THIS IS THE FUNCTOIN SHOW THE BANNER
def banner():
    print(Fore.RED+f"""
 ██████╗  █████╗ ███████╗███████╗██╗    ██╗██████╗ ██████╗ 
 ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗██╔══██╗
 ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║  ██║██████╔╝
 ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║  ██║██╔══██╗
 ██║     ██║  ██║███████║███████║╚███╔███╔╝██████╔╝██████╔╝
 ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═════╝ ╚═════╝ 
""")
    print(Fore.LIGHTBLUE_EX+"\t"*4,"PASSWDB V1.0\n","\t"*4,"Programmer :: ", Fore.RED+"SAJAD-CHEHRAZI\n")
print("""** WELCOME TO PASSWDB \n
    			## For 'EXIT', Enter 'quit' !\n""")
##THIS IS THE FUNCTOIN FOR SAVE A PASSW0RD AND HASHs ON DATABASE
def sqliteW(sname,name,passwd,hash):
	os.system("clear") if os.name=="posix" else os.system("cls")
	banner()
	import sqlite3
	try:
		dname=sname
		db=sqlite3.connect(".%s"%(dname))
		db.execute("CREATE TABLE hashs (name varchar(20),password INT,hashs varchar(256))")
		db.execute("INSERT INTO hashs VALUES('%s','%s','%s')"%(name,passwd,hash))
		db.commit()
		print(Fore.LIGHTCYAN_EX+"➜"+Fore.LIGHTBLUE_EX+" "+"Query 1,OK")
		db.close()
		input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		main(sname)
	except Exception as e:
		db=sqlite3.connect(".%s"%(dname))
		db.execute("INSERT INTO hashs VALUES('%s','%s','%s')"%(name,passwd,hash))
		db.commit()
		db.close()
		print(Fore.LIGHTCYAN_EX+"➜"+Fore.LIGHTBLUE_EX+" "+"Query 1, OK")
		input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		main(sname)
def sqliteR(sname):
	import sqlite3
	os.system("clear") if os.name=="posix" else os.system("cls")
	banner()
	print(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+""" ## Please Enter name of password or Enter the ('all') to show all record of database !
		For 'EXIT', Enter 'quit'""")
	cms=input(Fore.LIGHTGREEN_EX+"➜"+Fore.LIGHTBLACK_EX+" KALI@HASHER "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
	dname=sname
	if cms == "all":
		try:
			db=sqlite3.connect(".%s"%dname) 
			hashs=db.execute("SELECT * FROM hashs")
			for name,passwd,phash in hashs:
				print(Fore.LIGHTCYAN_EX+"""**/ This is the name => %s 
	/ This is the passwd => %s /**
	/ This is the Hash => %s /**"""%(name,passwd,phash))
			db.close()
			input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			main(sname)
		except:
			print(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" You have not password on database !")
			#input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			input("Press enter to back ")
			main(sname)
	elif cms == "quit":
		sys.exit()
	else:
		try:
			db=sqlite3.connect(".%s"%(dname)) 
			hashs=db.execute("SELECT *  FROM hashs WHERE name='%s'"%(cms))
			for name,passwd,phash in hashs:
				print(Fore.LIGHTCYAN_EX+"""**/ This is the name => %s 
	/ This is the passwd => %s /** 
	/ This is the Hash =>  %s /**"""%(name,passwd,phash))
			db.close()
			input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			main(sname)
		except:
			try:
				db.close()
			except:
				db.close()
			finally:
				db.close()
				print("Not Found --> '%s' !"%(cms))
				input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press Enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
				main(sname)
##THIS IS THE FUNCTION FOR DELETE RECORD OF DATABASE
def sqliteD(sname):
	os.system("clear") if os.name=="posix" else os.system("cls")
	banner()
	from time import sleep
	inec=["1-(Delete[one record])--> delete a one record of database",\
	"2-(Delete[all record])--> delete all record of database"]
	for i in inec:
		print(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" "+i,"\n")
		sleep(0.2)
	ind=input(Fore.LIGHTGREEN_EX+"➜"+Fore.LIGHTBLUE_EX+" Enter number of Section "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
	dname=sname
	if ind == "1":
		name=input("Enter name of record "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		print(Fore.LIGHTGREEN_EX+"OK ... ")
		passwd=input(Fore.LIGHTGREEN_EX+"➜"+Fore.LIGHTBLUE_EX+" Enter passwd of record "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		es=input(Fore.LIGHTGREEN_EX+"➜"+Fore.LIGHTBLUE_EX+" Do you want to delete it ? [Y/N] "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).upper()
		print(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" "+"Please wite ...")
		if es == "Y":
			import sqlite3
			db=sqlite3.connect(".%s"%(dname)) 
			db.execute("DELETE FROM hashs WHERE name='%s' AND password='%s' "%(name,passwd))
			db.commit()
			db.close()
			print(Fore.LIGHTCYAN_EX+"➜"+Fore.LIGHTBLUE_EX+" "+"Query 1, OK")
			input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			main(sname)
		else:
			main(sname)
	elif ind == "2":
		es=input(Fore.LIGHTGREEN_EX+"➜"+Fore.LIGHTBLUE_EX+" Do you want to delete it ? [Y/N] "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).upper()
		if es == "Y":
			import sqlite3
			db=sqlite3.connect(".%s"%(dname)) 
			db.execute("DELETE FROM hashs")
			db.commit()
			db.close()
			input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			main(sname)
		else:
			input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" I can't ot delete all records,Press Enter to back" +Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			main(sname)
	elif ind == "exit" or "quit":
		sys.exit()
	else:
		print(Fore.CYAN+"➜"+Fore.LIGHTRED_EX+" Not Found !")
		input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		main(sname)
##THIS IS THE HASHING FUNCTION 
def hash(sname,name,passwd):
	import hashlib
#	passwd=input("Enter your password => ~$ ").strip()
	hsh=hashlib.sha256()
	hsh.update(passwd.encode("utf-8"))
	hash=hsh.hexdigest()
	sqliteW(sname,name,passwd,hash)
#	print("This is the hash of passwd --> %s"%(hash))
##THIS IS THE MAIB FUNCTION 
def acount():
	os.system("clear") if os.name == "posxi" else os.system("cls")
	banner()
	print(Fore.LIGHTBLUE_EX+" WELCOME TO PASSWDB \n ! :)")
	name=input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" Enter Your Name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX+"")
	passwd=input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" Enter your password For Login "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
	print(Fore.LIGHTCYAN_EX+" ➜"+Fore.LIGHTBLUE_EX+" "+"OK !, Please wite ...")
	import hashlib
#	passwd=input("Enter your password => ~$ ").strip()
	hsh=hashlib.sha256()
	hsh.update(passwd.encode("utf-8"))
	hash=hsh.hexdigest()
	#dbname="."+name+""+'.db'
	#tname=name	
	import sqlite3
	db=sqlite3.connect(".li.db")
	try:
		db.execute("CREATE TABLE li (name varchar(20),password INT,hashs varchar(256))")
		db.execute("INSERT INTO li VALUES('%s','%s','%s')"%(name,passwd,hash))
		db.commit()
		print(Fore.LIGHTCYAN_EX+"➜"+Fore.LIGHTBLUE_EX+" "+" Query 1,OK")
		db.close()
	except Exception:
		db.execute("INSERT INTO li VALUES('%s','%s','%s')"%(name,passwd,hash))
		db.commit()
	except:
		print(Fore.LIGHTRED_EX+"➜"+Fore.LIGHTBLUE_EX+" "+" This account is already exists !")
	finally:
		input(Fore.CYAN+"➜"+Fore.LIGHTBLUE_EX+" Press enter to login session "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		login()
def login():
	from time import sleep 
	os.system("clear")
	banner()
	print(Fore.LIGHTBLUE_EX+" WELCOME TO PASSWDB ! :)\n")
	incm=["1-(login)--> login to a home ","2-(acount)--> make acount "]
	for e in incm:
		print(Fore.CYAN+" ➜"+Fore.LIGHTBLUE_EX+" "+e,"\n")
		sleep(0.2)
	print(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" (+)Fine, Enter number of Section !\n")
	com=(input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLACK_EX+" KALI@HASHER "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX))
	if com == "1":
		os.system("clear") if os.name == "posix" else os.system("cls")
		banner()
		name=input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" Enter Your Name "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX+"")
		passwd=input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" Enter your password "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		print(Fore.LIGHTCYAN_EX+" ➜"+Fore.LIGHTBLUE_EX+" "+"OK !, Please wite ...")
		import sqlite3
		try:
			db=sqlite3.connect(".li.db")
			ac=db.execute("SELECT * FROM li")
			sname=name
		except:
			print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" "+"account is not exists !")
			input(Fore.CYAN+" ➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			loginer()
		for pname,ppasswd,phash in ac:
			nname=pname
			npasswd=ppasswd
			nhash=phash
		if name == nname:
			if passwd == npasswd:
				main(sname)
			else:
				print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" name or password is wrong ! ")
				input(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
				loginer()
		else:
			print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" name or password is wrong ! ")
			input(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
			loginer()

	elif com == "2":
		acount()
	elif com == "exit" or "quit":
		sys.exit()
def loginer():
	os.system("clear")
	login()
def main(sname):
	from time import sleep 
	pwd=os.getcwd()
	os.system("clear")
	banner()
	incm=["1-(Write)--> write a passwd and create hash for it","2-(Read)--> Read the name, passwd and hash it on database",\
	"3-(Delete)--> delete one or all record of database"]
	for e in incm:
		print(Fore.CYAN+" ➜"+Fore.LIGHTBLUE_EX+" "+e,"\n")
		sleep(0.2)
	print(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" (+)Fine, Enter number of Section !\n")
	com=(input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLACK_EX+" KALI@HASHER "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX))
	if com == "1":
		name=input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" Enter name of passwd "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()
		passwd=input(Fore.LIGHTGREEN_EX+" ➜"+Fore.LIGHTBLUE_EX+" Enter your password => "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX).strip()
		print(Fore.CYAN+" ➜"+Fore.LIGHTBLUE_EX+" OK, Please wite ...")
		hash(sname,name,passwd)
	elif com == "2":
		sqliteR(sname)
	elif com == "3":
		sqliteD(sname)
	elif com =="exit" or "quit":
		os.chdir(pwd)
		sys.exit()
	else:
		print(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" This is no found !")
		input(Fore.LIGHTRED_EX+" ➜"+Fore.LIGHTBLUE_EX+" Press enter to back "+Fore.LIGHTRED_EX+"✗ "+Fore.LIGHTBLUE_EX)
		main(sname)
loginer()
sname=""
if __name__ == "__main__":main(sname)
if __name__ == "__acount__":acount()
if __name__ == "__login__":login()
if __name__ == "__loginer__":loginer()
