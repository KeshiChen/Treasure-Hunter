
# -*- coding: UTF-8 -*-
# 文件名：testclient.py

from socket import *               # 导入 socket 模块

s = socket(AF_INET, SOCK_STREAM)         # 创建 socket 对象
host = "localhost" # 获取本地主机名
port = 12345                # 设置端口好
view = [[None] * 5 for _ in range(5)]
s.connect((host, port))
def get_view(data):
        view = [[' ']*5 for _ in range(5)]
        n = 0
        for i in range(5):
            for j in range(5):
                if not (i == 2 and j == 2):
                    try:
                        view[i][j] = data[n]
                        n += 1
                    except IndexError:
                        pass
        return view

def print_view(view):
    print('\n+-----+')
    for i in range(5):
        print('|',end='')
        for j in range(5):
            if i == 2 and j == 2:
                print('^',end='')
            else:
                print(view[i][j],end='')
        print('|')
    print('+-----+')
while True:
    rec = s.recv(24, MSG_WAITALL).decode("UTF-8")
    if rec == 'won':
        print("Game won.")
        exit()
    elif rec == 'lost':
        print("Game lost.")
        exit()
    elif rec == 'exc':
        print("Exceeded max moves.")
        exit()
    else:
        view = get_view(rec)
        print_view(view)
    i = input("action = ")
    s.send(i.encode("UTF-8"))
    #print_view(get_view(s.recv(24, MSG_WAITALL).decode("UTF-8")))
