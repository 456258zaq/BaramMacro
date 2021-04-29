import win32gui
import win32con
import win32api
import win32ui
import time
from ctypes import windll
from PIL import Image
import cv2
import pyautogui as pag
import numpy as np
from matplotlib import pyplot as plt
import os
import multiprocessing as mp

_MAX_ITERATIONS = 10

class ImageSearch:

    def __init__(self,PlayerName,Name):
        self.Name = Name
        self.PlayerName = PlayerName
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.hwnd = None
        self.hwnd_child = None
        
    def MainFrame_image_search(self):
        self.hwnd = win32gui.FindWindow(None,"{}".format(self.PlayerName))
        self.hwnd_child = win32gui.FindWindowEx(self.hwnd,0,0,"ScreenBoardClassWindow")
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        self.axis_main = [left,top,right,bot]
        w = self.axis_main[2] -self.axis_main[0]
        h = self.axis_main[3] - self.axis_main[1]
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 0)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        if result == 1:
            im.save("{}\\img\\test_{}.jpg".format(self.dir_path,self.PlayerName))
        img1 = cv2.imread("{}\\img\\test_{}.jpg".format(self.dir_path,self.PlayerName),0)
        temp= cv2.imread("{}\\img\\{}.jpg".format(self.dir_path,self.Name),0)
        w,h = temp.shape[::-1]
        result = cv2.matchTemplate(img1,temp ,cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        top_left = maxLoc
        bottom_right = (top_left[0]+w,top_left[1]+h)
        cv2.rectangle(img1,top_left,bottom_right,255,2)
        self.X = round((top_left[0]+bottom_right[0])/2)
        self.Y = round((top_left[1]+bottom_right[1])/2)-20
        self.maxVal = maxVal
        print(self.maxVal,self.X,self.Y)
        return self.maxVal,self.X, self.Y


    def image_search_click(self,X,Y):
        lParam = win32api.MAKELONG(X,Y)
        win32gui.SendMessage(self.hwnd_child, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.1)
        win32gui.SendMessage(self.hwnd_child, win32con.WM_LBUTTONUP, None, lParam)


def go_to_home():
    """
    Dict_item = [
        PlayerName1 : "NoxPlayer",
    PlayerName2 : "NoxPlayer(1)",
    Noran : "Noran",
    gotowhere : "gotowhere",
    gotostore : "gotostore",
    deok : "ddeok",
    sangjeom : "sangjoem",
    repair : "repair",
    all_repair : "all_repair",
    close : "close",
    Doho : "Doho",
    gotowhere2 : "gotowhere2",
    DOHOCAH : "DOHOCAH",
    sinsu : "sinsu",
    jujack : "jujack",
    chungryoung : "chungryoung",
    health : "health",
    listtab : "list",
    deongeon : "deongeon",
    deongeon2 : "deongeon2",
    sanayteojeocsi : "sanayteojeocsi",
    ok : "ok",
    autokey : "autokey",
    DDara : "DDara",
    sohwan : "sohwan",
    surack : "surack",
    ]
    """
    Dict_item1 = [
    "Noran",
    "gotowhere"
    ]
    #"gotostore"]
    
    Dict_item2= [
        "ddeok",
    "sangjoem",
    "repair",
    "all_repair",
    "close",
    "gotowhere2",
    ]
    #"Doho"
    """
    "DOHOCAH",
    "sinsu",
    "jujack",
    "chungryoung",
    "health",
    "list",
    "deongeon",
    "deongeon2",
    "sanayteojeocsi",
    "ok",
    "autokey",
    "DDara",
    "sohwan",
    "surack",
    """

    time.sleep(4)
    for i in Dict_item1:
        check_Noran = ImageSearch("NoxPlayer",i)
        max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()
        while True:
            if max_val < 0.7:
                max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()  
                continue
            else:
                check_Noran.image_search_click(check_Noran_X,check_Noran_Y)
                break
        time.sleep(1)
        check_Noran2 = ImageSearch("NoxPlayer(1)",i)
        max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
        while True:
            if max_val < 0.7:
                max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
                continue
            else:
                check_Noran2.image_search_click(check_Noran2_X,check_Noran2_Y)
                break
        time.sleep(5)

    check_Noran = ImageSearch("NoxPlayer","gotostore")
    max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()
    while True:
        if max_val < 0.7:
            max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()  
            continue
        else:
            check_Noran.image_search_click(check_Noran_X+120,check_Noran_Y)
            break
    time.sleep(1)
    check_Noran2 = ImageSearch("NoxPlayer(1)","gotostore")
    max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
    while True:
        if max_val < 0.7:
            max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
            continue
        else:
            check_Noran2.image_search_click(check_Noran2_X+120,check_Noran2_Y)
            break
    time.sleep(30)
    
    for j in Dict_item2:
        check_Noran = ImageSearch("NoxPlayer",j)
        max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()
        while True:
            if max_val < 0.7:
                max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()  
                continue
            else:
                check_Noran.image_search_click(check_Noran_X,check_Noran_Y)
                break
        time.sleep(1)
        check_Noran2 = ImageSearch("NoxPlayer(1)",j)
        max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
        while True:
            if max_val < 0.7:
                max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
                continue
            else:
                check_Noran2.image_search_click(check_Noran2_X,check_Noran2_Y)
                break
        time.sleep(3)
    
    check_Noran = ImageSearch("NoxPlayer","Doho")
    max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()
    while True:
        if max_val < 0.7:
            max_val,check_Noran_X,check_Noran_Y = check_Noran.MainFrame_image_search()  
            continue
        else:
            check_Noran.image_search_click(check_Noran_X+124,check_Noran_Y-10)
            break
    time.sleep(1)

    check_Noran2 = ImageSearch("NoxPlayer(1)","Doho")
    max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
    while True:
        if max_val < 0.7:
            max_val,check_Noran2_X,check_Noran2_Y = check_Noran2.MainFrame_image_search()
            continue
        else:
            check_Noran2.image_search_click(check_Noran2_X+119,check_Noran2_Y)
            break
    time.sleep(50)

    func_gotostore = ImageSearch("NoxPlayer","DOHOCAH")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    while True:
        if max_val <0.7:
            max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
            continue
        else:
            func_gotostore.image_search_click(gotostore_X,gotostore_Y)
            break
        time.sleep(3)
    func_gotostore2 = ImageSearch("NoxPlayer(1)","DOHOCAH")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    while True:
        if max_val < 0.7:
            max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
            continue
        else:
            func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)
            break
        time.sleep(3)
    time.sleep(3)
    func_gotostore = ImageSearch("NoxPlayer","sinsu")
    max_val,mgotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(0.5)
    func_gotostore2 = ImageSearch("NoxPlayer(1)","sinsu")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)    
    time.sleep(3)

    func_gotostore = ImageSearch("NoxPlayer","Baeckho")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(0.5)
    func_gotostore2 = ImageSearch("NoxPlayer(1)","Baeckho")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)    
    time.sleep(2)

    for i in range(1,100):
        func_gotostore = ImageSearch("NoxPlayer","health")
        max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
        func_gotostore.image_search_click(gotostore_X,gotostore_Y+10)
        time.sleep(0.1)
        func_gotostore2 = ImageSearch("NoxPlayer(1)","health")
        max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
        func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y+10)   
    time.sleep(3)

    func_deok = ImageSearch("NoxPlayer","close")
    max_val,gotostore_X,gotostore_Y = func_deok.MainFrame_image_search()
    func_deok.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(0.5)
    func_deok2 = ImageSearch("NoxPlayer(1)","close")
    max_val,gotostore2_X,gotostore2_Y = func_deok2.MainFrame_image_search()
    func_deok2.image_search_click(gotostore2_X,gotostore2_Y)
    time.sleep(3)

    func_gotostore = ImageSearch("NoxPlayer","list")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(3)
    func_gotostore = ImageSearch("NoxPlayer","deongeon")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(3)

    func_gotostore = ImageSearch("NoxPlayer","deongeon2")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(3)
    func_gotostore = ImageSearch("NoxPlayer","sanayteojeocsi")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(2)

    func_gotostore = ImageSearch("NoxPlayer","ok")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(5)
    func_gotostore = ImageSearch("NoxPlayer","sohwan")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    while True:
        if max_val < 0.8:
            max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
            continue
        else:
            func_gotostore.image_search_click(gotostore_X,gotostore_Y)
            break
    time.sleep(2)
    func_gotostore2 = ImageSearch("NoxPlayer(1)","surack")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    while True:
        if max_val < 0.8:
            max_val,gotostore2_X,gotostore2_Y = func_gotostore.MainFrame_image_search()
            continue
        else:
            func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)
            break
    #func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)    
    time.sleep(6)
    func_gotostore2 = ImageSearch("NoxPlayer(1)","DDara")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    while True:
        if max_val < 0.8:
            max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
            continue
        else:
            func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)
            break
    #func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)    
    time.sleep(0.5)
    func_gotostore = ImageSearch("NoxPlayer","autokey")
    max_val,gotostore_X,gotostore_Y = func_gotostore.MainFrame_image_search()
    func_gotostore.image_search_click(gotostore_X,gotostore_Y)
    time.sleep(0.5)
    func_gotostore2 = ImageSearch("NoxPlayer(1)","autokey")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)
    time.sleep(5184)


def close_oneday_module1():
    print("시작합니다.")
    func_gotostore2 = ImageSearch("NoxPlayer(1)","onedayclose")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    #while True:
    if max_val < 0.8:
        max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
        print("정상동작중입니다._module1")
        print(max_val)
        time.sleep(5)
        #continue
    else:
        func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)
        #break

def close_oneday_module():
    func_gotostore2 = ImageSearch("NoxPlayer","onedayclose")
    max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
    #while True:
    if max_val < 0.8:
        max_val,gotostore2_X,gotostore2_Y = func_gotostore2.MainFrame_image_search()
        #print(max_val)
        time.sleep(5)
        print("정상동작중입니다_module.")
        #continue
    else:
        func_gotostore2.image_search_click(gotostore2_X,gotostore2_Y)
        #print("정상동작중입니다.")
        #break

if __name__ == "__main__":
    while True:
        mp.Process(target=close_oneday_module()).start()
        mp.Process(target=close_oneday_module1()).start()
        #mp.Process(target=go_to_home()).start()

