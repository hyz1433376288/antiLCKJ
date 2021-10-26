# encoding:utf-8

import requests
import base64
import random
import tkinter
from PIL import ImageGrab


def snap():
    win = tkinter.Tk()

    # width = win.winfo_screenwidth()
    # height = win.winfo_screenheight()

    start_x = 200
    start_y = 70
    width = start_x + 560
    height = 1000
    print(width, height)

    img = ImageGrab.grab(bbox=(start_x, start_y, width, height))

    img.save('phone_screen.jpg')


def get_screen_info():
    '''
    通用文字识别
    '''

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    # f = open('full_screen_img.jpg', 'rb')
    f = open('phone_screen.jpg', 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = 'PASTE HERE'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if not response:
        return []
    print('response.json()')   

    # print(response.json())
    msg = response.json()
    words = []
    for each in msg['words_result']:
        words.append(each['words'])
    print(words)
    return words

# print(get_screen_info())

def exist_substr(des_str, substr_list):
    for s in substr_list:
        if des_str in s:
            return True
    return False


from pymouse import *

from pykeyboard import *
import time
import pyautogui

# ================================
def login(account, password):
    m = PyMouse()
    k = PyKeyboard()
    m.click(294+random.randint(-10, 10), 417)
    m.click(294+random.randint(-10, 10), 417)

    time.sleep(2)
    k.type_string(account)
    m.click(282+random.randint(-10, 10), 506)
    m.click(282+random.randint(-10, 10), 506)

    time.sleep(2)
    k.type_string(password)
    time.sleep(2)

    print('点击登陆')
    m.click(480+random.randint(-10, 10), 590+random.randint(-10, 10))
def entrance():
    time.sleep(2)
    pyautogui.doubleClick(x=320+random.randint(-10, 10), y=560+random.randint(-10, 10))
def take_photo():
    m = PyMouse()
    m.click(483, 961)
    time.sleep(2)
    m.click(665, 949)
    print('√')
    time.sleep(2)


def scroll():
    pyautogui.moveTo(480+random.randint(-10,10), 1000)
    pyautogui.dragTo(480+random.randint(-10,10), 809, 1, button='left')


def confirm():
    pyautogui.click(x=600+random.randint(-10,10), y=700)


def select_course():
    pyautogui.click(x=480+random.randint(-10,10), y=950)

# ==========================================
def log(f, info):
    f.write('\n'+time.asctime( time.localtime(time.time()))+'   '+info)
if __name__ == '__main__':
    with open('lckj.log', 'a') as f:
        consecutive = 0 # 连续拍照的次数
        while True:
            snap()
            time.sleep(1)
            # 防止proxy Error
            try:
                words = get_screen_info()
            except Exception:
                print('proxy error')
                log(f, 'proxy error')
                time.sleep(10)
                continue
            # 当多次拍照的时候，直接关闭
            if consecutive >= 20:
                break

            if len(words) == 0:
                continue

                    # 突袭
            if exist_substr('登录', words) :
                time.sleep(4)
                login('15865136859', '123456')
                log(f,'登陆')
            elif exist_substr('主页', words) and exist_substr('我的培训', words):
                log(f,'进入主页')
                entrance()
                
            elif exist_substr('轻触拍照', words):
                log(f,'轻触拍照')
                # 拍照 然后点击√ 然后点击完成
                consecutive += 1
                print('轻触拍照 连续' + str(consecutive)+'次')

                take_photo()
                time.sleep(2)
            elif exist_substr('抓拍', words) and exist_substr('提示', words):
                log(f,'抓拍确认')
                print('抓拍')

                # 点击确定 然后开始拍照
                confirm()
                #等待调用相机，时间可能较长
                time.sleep(8)
                snap()

            elif exist_substr('看完', words) or exist_substr('退回', words):
                log(f,'看完返回')
                pyautogui.click(x=600+random.randint(-10,10), y=630)
                time.sleep(4)

            elif exist_substr('列表', words):
                if not exist_substr('未完成', words):
                    log(f,'列表 未完成 继续下滑')
                    print('继续下滑')
                    time.sleep(0.5)
                    scroll()
                else:
                    log(f, '列表 选择未完成课程观看')
                    print('列表')
                    # 选择课程进行观看
                    select_course()
                    time.sleep(8)
                    snap()
                # 理想：人脸识别成功，继续播放
            elif exist_substr('成', words) and len(words) <= 2:
                log(f, '拍照了，点击完成')
                print('拍照了，点击完成')
                pyautogui.click(x=715, y=109)
                time.sleep(8)
            elif exist_substr('详情', words) and exist_substr('留言', words):
                log(f, '详情 无异常 继续观看')
                consecutive = 0
                print('详情 ')    
                time.sleep(10)
                print("..")
                # 无异常，继续观看

