import socket
import time
import dns.resolver
import requests


class Proxy :

    def __init__(self):

        #monireIP = '192.168.1.33'
        #mahtabIP = '192.168.1.55'
        self.IP = ''
        self.UDP_IP = ''
        self.UDP_PORT = 0
        self.TCP_PORT = 80
        self.TCP_IP = ''
        self.realdata = ''
        # self.realdata1 = ''
        self.cacheSaveMsg = ''
        self.NR = 1
        #turn = 0
        self.index = 0
        self.dnsindex = 0
        self.httpCache = []
        self.DNSCache = []
        self.inCache = 0
        self.inDNSCache = 0
        self.udp_to_tcp = False
        self.tcp_to_udp = False
        self.turn = 0
        self.file = open("index2.txt", "w")
        self.ignoreList = ['\\', '\\n', '\n', 'n', '\'', '\\t', '\t', 't', 'xa0', 'xc2']

    def checksum(self, message):
        c = 0
        # print(message)
        # print("staaaaaaaart")
        self.file = open("index2.txt", "w")
        self.file.write('new\n')

        for x in message:
            if x not in self.ignoreList:
                # print(x + " - ", end='', flush=True)
                c = c + ord(x)
                self.file.write(x)
                # c = c + x
        self.file.close()
        csum = bin(c)
        csum = csum.split('b')
        return csum[1]



    def response_to_client(self,data):

        print("------------------>>>>>>>")
        # print(data)
        udp_port = 5017
        udp_port = 5020 + self.turn

        # newdata = str(data)
        # newdata = newdata.split('\'')
        # splitedData = newdata[1].split(' ')
        # response_type = splitedData[1]

        response_type = data.status_code
        print(response_type)
        r = data
        # print("header : ", data.headers['Location'])
        # print(data.location)
        # print(data.history[0].status_code)
        # print('here',response_type)
        NS = 0
        MF = 0  # More fragment
        data = data.text
        iteration = 2
        # print(data.status_code)
        if int(response_type) == 200:

            print('ok ^^ , code = 200 !')
            segment_size = 5000
            # print('len : ', len(data))

            if len(data) > segment_size:
                iteration = int(len(data) / segment_size) + 2
                # print('number of iteration : ', iteration)
                MF = 1
                # print("fragment happened")
            else:
                    MF = 0
            data = str(data)
            # file.write(data)
            # data = data.replace('\'', '\\\'')
            for i in range(1, iteration):
                print("iteration : ", i)
                if i == iteration - 1:
                    MF = 0
                start = (i - 1) * segment_size
                end = i * segment_size
                if end > len(data):
                    end = len(data)

                msg = str(NS) + '!@#$%^&*()_+' + str(MF) + '!@#$%^&*()_+' + data[start:end]
                msg = msg.replace('\\xa0', ' ')
                msg = msg.replace('\\xc2', '')
                # msg = ''.join([i if ord(i) < 128 else ' ' for i in msg])
                csum = self.checksum(msg)
                # msg = msg.replace('\\n', '\n')
                # msg = msg.replace('\\r', '\r')
                # msg = msg.replace('\\\\', '\\')

                newmsg = msg + '!@#$%^&*()_+' + str(csum) + '\r\n\r\n'
                MESSAGE = newmsg.encode('utf-8')

                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                # print('sent message :' ,MESSAGE)
                udp_port = 5020 + self.turn
                sock.sendto(MESSAGE, (self.UDP_IP, udp_port))
                sock.close()
                counter = 0
                while True:
                    # print('man injam!!')
                    counter += 1
                    # print("counter :", counter)
                    UDP_PORT = 5018
                    UDP_PORT = 5030 + self.turn
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP
                    print(self.UDP_IP)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind((self.UDP_IP, UDP_PORT))
                    sock.settimeout(1)
                    try:
                        data2, addr = sock.recvfrom(10000)
                        NR = data2.decode('utf-8')
                        print('ack : ', NR, NS)
                        sock.close()
                        print(int(NR) , int(not bool(NS)))
                        if int(NR) == int(not bool(NS)):
                            NS = int(NR)
                            print("sending segment finished ")
                            break
                        print("received data:", NR)

                    except socket.timeout:
                        sock.close()

                        print('timeout')
                        print('start to retransmit: ')
                        # break
                        UDP_PORT = 5018
                        UDP_PORT = 5020 + self.turn
                        sock = socket.socket(socket.AF_INET,  # Internet
                                             socket.SOCK_DGRAM)  # UDP
                        sock.sendto(MESSAGE, (self.UDP_IP, UDP_PORT))
                    sock.close()


            self.file.close()
        elif int(response_type) == 404:
            print('error not found , code = 404 !')

            msg = str(NS) + '!@#$%^&*()_+' + str(MF) + '!@#$%^&*()_+' + 'error not found !'
            # msg = msg.replace('\\xa0', ' ')
            # msg = msg.replace('\\xc2', '')
            # msg = ''.join([i if ord(i) < 128 else ' ' for i in msg])
            csum = self.checksum(msg)
            newmsg = msg + '!@#$%^&*()_+' + str(csum) + '\r\n\r\n'
            # MESSAGE = bytes(newmsg, 'utf-8')
            MESSAGE = newmsg.encode('utf-8')
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP

            sock.sendto(MESSAGE, (self.UDP_IP, udp_port))
            sock.close()
            counter = 0
            while True:
                counter += 1

                UDP_PORT = 5018

                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                print("-----------------" , self.inCache)
                # if self.inCache == 1 :
                print(UDP_PORT ,self.UDP_IP)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((self.UDP_IP, UDP_PORT))
                sock.settimeout(1)
                try:
                    data2, addr = sock.recvfrom(10000)
                    NR = data2.decode('utf-8')[2]
                    print('ack : ', NR, NS)
                    sock.shutdown(1)
                    sock.close()
                    print(int(NR), int(not bool(NS)))
                    if int(NR) == int(not bool(NS)):
                        NS = int(NR)
                        print("sending segment finished ")
                        break
                    print("received data:", NR)

                except socket.timeout:
                    sock.shutdown(1)
                    sock.close()
                    print('timeout')
                    print('start to retransmit: ')
                    # break
                    UDP_PORT = 5018
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP
                    sock.sendto(MESSAGE, (self.UDP_IP, UDP_PORT))
                    sock.close()


        elif int(response_type) == 400:
            print('bad req , code = 400 !')
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.sendto('bad request !'.encode('utf-8'), (self.UDP_IP, udp_port))
            sock.close()

        elif int(response_type) == 301 or int(response_type) == 302:
            print('moved and redirect  , code = 301 or 302 !')

            TCP_IP = r.url
            r = requests.get(TCP_IP, allow_redirects=True)
            print(r.text)
            self.response_to_client(r)

    def get_input(self):

        command = input('enter command : \n')
        # command = "proxy -s tcp:127.0.0.1:5016 -d udp"
        command = "proxy -s udp:127.0.0.1:5016 -d tcp"
        command = command.split(' ')

        if len(command) == 5:
            command2 = command[2].split(':')
            if command[0] == 'proxy' and command[1] == '-s' :
                if command2[0] == 'udp' and command[4] == 'tcp' :

                    self.udp_to_tcp = True
                elif command2[0] == 'tcp' and command[4] == 'udp' :
                    self.tcp_to_udp = True
                else :
                    print('wrong command')
                    return False

                self.UDP_IP =bytes (command2[1], 'utf-8')
                self.IP = bytes(command2[1], 'utf-8')
                self.UDP_PORT = int(command2[2])

            else :
                print('wrong command')
                return False
        return True

    def send_and_recieve_req(self):


        while True:

            correct_command = self.get_input()

            if self.udp_to_tcp and correct_command :
                while True:
                    # self.turn += 1
                    self.NR = 1
                    print(' waiting for client request (http mode)... ')
                    self.UDP_PORT = 5016
                    self.UDP_PORT = 5001 + self.turn
                    BUFFER_SIZE = 10000
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP
                    sock.bind((self.UDP_IP, self.UDP_PORT))
                    data, addr = sock.recvfrom(10000)  # buffer size is 10000 bytes
                    print('first data :', data)
                    sock.close()

                    if data:
                        data = data.decode('utf-8').split("!@#$%^&*()_+")
                        # TCP_IP = bytes(data[0][2:], 'utf-8')
                        TCP_IP = data[0]
                        TCP_PORT = int(data[1])
                        NS = int(data[2])
                        MF = int(data[3])
                        MESSAGE = data[0] + '!@#$%^&*()_+' + data[1] + '!@#$%^&*()_+' + data[2] + '!@#$%^&*()_+' + data[3] + '!@#$%^&*()_+' + data[4][:-4]
                        # cmsg = realdata1.split('\\')
                        # print(cmsg)
                        # cacheSaveMsg = realdata1.split('\\')[0]

                        print("received message:", MESSAGE)
                        print("tcpIP: ", TCP_IP)
                        print("tcpPORT", TCP_PORT)
                        print("N Next ", self.NR)
                        print(MESSAGE)
                        print('checksum', data[5], self.checksum(MESSAGE))
                        print(NS == int(not bool(self.NR)))
                        if NS == int(not bool(self.NR)) and (self.checksum(MESSAGE) == data[5]):
                            realdata1= ''
                            #print("heeeeeeeeeeeeereeeeeeeeeeeeee")
                            self.realdata = self.realdata + str(data[4][:-8])
                            realdata1 = realdata1 + str(data[0][2:]) + '!@#$%^&*()_+' + str(data[1]) + '!@#$%^&*()_+' + str(data[2]) + '!@#$%^&*()_+' + str(
                                data[3]) + '!@#$%^&*()_+' + str(data[4])

                            self.cacheSaveMsg = realdata1.split('\\')[0]

                            UDP_PORT = 5018
                            UDP_PORT = 5010 + self.turn
                            print("port:", UDP_PORT)
                            # ack = bytes(str(self.NR), 'utf-8')
                            ack = str(self.NR).encode('utf-8')
                            print("NR:", ack, self.NR, NS)

                            sock = socket.socket(socket.AF_INET,  # Internet
                                                 socket.SOCK_DGRAM)  # UDP

                            sock.sendto(ack, (self.UDP_IP, UDP_PORT))
                            sock.close()
                            self.NR = NS

                        if MF == 0:
                            break

                # realdata += '\r\n\r\n'
                # print("real data : ", realdata)


                for i in self.httpCache:
                    if self.cacheSaveMsg in i:
                        print('here  i use cache  :D', self.httpCache)
                        self.inCache = 1
                        self.response_to_client(i[1])



                if self.inCache == 0:  # if not in cache

                    print('it is not in cache  :( ', self.httpCache)
                    #----------------------------------------------------------------- socket
                    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # print(TCP_IP)
                    # s.connect((TCP_IP, TCP_PORT))
                    #
                    # # we just send " get request " :)
                    # s.send(bytes('GET / HTTP/1.0\r\n\r\n', 'utf-8'))
                    #
                    # data = s.recv(BUFFER_SIZE)
                    # s.close()

                    #------------------------------------------------------------------ requests

                    print(TCP_IP)
                    TCP_IP = 'http://' + TCP_IP
                    r = requests.get(TCP_IP,allow_redirects=False)
                    print('---------------->',r.text)


                    # save data in cache
                    if len(self.httpCache) < 10:
                        self.httpCache.append([self.cacheSaveMsg, r])
                    elif len(self.httpCache) == 10:
                        del self.httpCache[self.index]
                        self.httpCache.insert(self.index, [self.cacheSaveMsg, r])
                        self.index = self.index + 1
                        if self.index == 10:
                            self.index = 0

                    # print('index',index)
                    # print('new cache',httpCache)

                    self.response_to_client(r)
                    # self.response_to_client(data)

                self.inCache = 0


            elif self.tcp_to_udp and correct_command:

                print(' waiting for client request (DNS mode) ... ')

                # print(self.IP)

                noanswer = False

                TCP_IP = self.IP

                TCP_PORT = 5016

                BUFFER_SIZE = 10000  # Normally 10000, but we want fast response

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                s.bind((TCP_IP, TCP_PORT))

                s.listen(2)

                conn, addr = s.accept()

                print('Connection address:', addr)

                while 1:

                    if noanswer:
                        noanswer = False

                        break

                    data = conn.recv(BUFFER_SIZE)

                    if not data:

                        break

                    else:

                        print("received data:", data.decode('utf-8'))

                        data1 = data.decode('utf-8').split('!@#$%^&*()_+')

                        dns_type = str(data1[0][2:])

                        target = str(data1[1])

                        print('type: ', dns_type)

                        target = target.split('\\')[0]

                        print('target: ', target)

                        dnsIP = str(data1[2])

                        print('DNS Server: ', dnsIP)

                        myResolver = dns.resolver.Resolver()  # create a new instance named 'myResolver'

                        myResolver.timeout = 1

                        myResolver.lifetime = 1

                        for i in self.DNSCache:

                            if data in i:
                                print('here', self.DNSCache)

                                conn.send(i[1].encode('utf-8'))

                                self.inDNSCache = 1

                        if self.inDNSCache == 0:  # if not in cache


                            qm = dns.message.make_query(target, 'A')

                            counter = 0

                            AAflag = 0

                            while True:

                                try:

                                    qa = dns.query.udp(qm, dnsIP, timeout=4)

                                    print('inja :', qa.flags, dns.flags.AA)

                                    print('Authoritative : ', qa.flags & dns.flags.AA)

                                    if qa.flags & dns.flags.AA == 1024:

                                        AAflag = 1

                                    else:

                                        AAflag = 0

                                    break

                                except dns.exception.Timeout:

                                    print('time out')

                                    counter += 1

                                    if counter >= 10:
                                        break

                            result = ''

                            while True:

                                try:

                                    myResolver.nameservers = [dnsIP]

                                    myAnswers = myResolver.query(target,

                                                                 dns_type)  # Lookup the 'A' record(s) for google.com

                                    # print(myAnswers.flags , dns.flags.AA )

                                    break

                                except dns.exception.Timeout:

                                    print('time out')

                                except dns.resolver.NoAnswer:

                                    print('noanswer')

                                    result = 'no answer'

                                    conn.send(result.encode('utf-8'))  # echo

                                    conn.close()

                                    myAnswers = [result]

                                    noanswer = True

                                    break

                            result = ''

                            for rdata in myAnswers:  # for each response

                                if dns_type == 'CNAME':

                                    if rdata == 'no answer':

                                        result += str(rdata) + '@' + str(AAflag)

                                    else:

                                        result += str(rdata.target) + '@' + str(AAflag)

                                        print(rdata.target)  # print the data

                                else:

                                    result += str(rdata) + '@' + str(AAflag)

                                    print(rdata)

                            # print(myAnswers.authority)

                            # save data in cache

                            if len(self.DNSCache) < 10:

                                self.DNSCache.append([data, result])

                            elif len(self.httpCache) == 10:

                                del self.httpCache[self.dnsindex]

                                self.DNSCache.insert(self.dnsindex, [data, result])

                                self.dnsindex = self.dnsindex + 1

                                if self.dnsindex == 10:
                                    self.dnsindex = 0

                            if not noanswer:
                                conn.send(result.encode('utf-8'))  # echo

                            # conn.close()

                            self.inDNSCache = 0

                conn.close()

if __name__ == "__main__":
    proxy = Proxy()
    proxy.send_and_recieve_req()