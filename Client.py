# -*- coding:utf-8 -*-

import socket
import socketserver
import datetime


class MyTCPHandler(socketserver.BaseRequestHandler):  # 服务类，监听绑定等等
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):  # 请求处理类，所有请求的交互都是在handle里执行的
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()  # 每一个请求都会实例化MyTCPHandler(socketserver.BaseRequestHandler):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " recive:")
        print(self.data)
        # just send back the same data, but upper-cased
        flag = CamraControl.chgJob(self.data.decode('utf-8'))
        if flag:
            self.request.sendall(self.data)  # 返回机器人.
        else:
            self.request.sendall(b'0')  # 错误返回0
        # CamraControl.close()


class CamraControl:
    client = socket.socket()

    @staticmethod
    def login(IP, port):
        CamraControl.client.connect((IP, port))
        msgRev = ""
        while msgRev != "User Logged In":
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(msgRev)
            if msgRev == "User:":
                CamraControl.client.sendall(b"admin\r\n\r\n")
                print(b"admin\r\n\r\n")
                msgRev = ""
            elif msgRev == "Password":
                CamraControl.client.sendall(b" \r\n")
                print(b" \r\n")
                msgRev = ""
            elif 'User' in msgRev:
                msgRev = "User:"
            elif 'User Logged In' in msgRev:
                msgRev = 'User Logged In'
            else:
                msgRev = CamraControl.client.recv(1024).strip().decode('utf-8')
                print(msgRev)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(">>>登录成功")

    @staticmethod
    def currentJob():
        CamraControl.client.sendall(b'GJ\r\n')
        msgRev = CamraControl.client.recv(1024)
        msgRev = msgRev.strip().decode('utf-8')
        temp = msgRev.split("\r\n")
        if temp[0] == '1':
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('>>>当前任务：', temp[1])
            return temp[1]
        else:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('>>>获取数据失败')
        # print(temp)

    @staticmethod
    def chgJob(jobName):
        f = False
        CamraControl.client.sendall(b'SO0\r\n')
        msgRev = CamraControl.client.recv(1024).strip().decode('utf-8')
        if msgRev == '1':
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('>>>切换到离线模式')

        CamraControl.client.sendall(str.encode('LF' + jobName + '\r\n'))
        msgRev = CamraControl.client.recv(1024).strip().decode('utf-8')
        if msgRev == '1':
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('>>>切换到任务：' + jobName)
            f = True

        CamraControl.client.sendall(b'SO1\r\n')
        msgRev = CamraControl.client.recv(1024).strip().decode('utf-8')
        if msgRev == '1':
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('>>>切换到在线模式')
        else:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('>>>相机处于手动模式')
        return f

    @staticmethod
    def close():
        CamraControl.client.close()


if __name__ == '__main__':
    print('*************************************************************')
    print('*              上海君屹工业自动化股份有限公司               *')
    print('*                         2018-10                           *')
    print('*  Camra IP Address:192.168.125.10                          *')
    print('*  Local Port Numnber:60000                                 *')
    print('*************************************************************')

    try:
        CamraControl.login('192.168.125.10', 23)
    except:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('>>>连接失败，检查相机连接状态，然后重新启动程序')
    HOST, PORT = "localhost", 60000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
