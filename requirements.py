from os import system

def fun():
    require = ['colorama', 'termcolor']
    for req in require:
        try:
            system(f"python3 -m pip install {req}")
            print(f"[0]- {req} successfully installed [ok]")
        except Exception as e:
            print(e,f"[1]- faild to install {req}")

fun()
