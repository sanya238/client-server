import socket

class Client:
    def __init__(self,host,port, timeout=None):
        self.host=host
        self.port=port
        self.timeout=timeout
        self.sock=socket.create_connection((self.host,self.port),self.timeout)
#Записываем информацию на сервер
    def put(self, key,value,timestamp):

        self.stringput="put "+key+" "+str(value)+" "+str(timestamp)+"\n"
        self.sock.sendall(self.stringput.encode("utf8"))
        self.stringget = self.sock.recv(1024)
        self.stringget = self.stringget.decode("utf8")

#Получаем информацию с сервера
    def get(self,key):
        self.stringput="get"+" "+key+"\n"
        self.sock.sendall(self.stringput.encode("utf8"))

        self.stringget=self.sock.recv(1024)
        self.stringget=self.stringget.decode("utf8")
        self.result=self.stringget.splitlines()
        self.return_dict=dict()
        if self.stringget=="ok\n\n":
            return  self.return_dict
        elif self.result[0]=="ok":

            for line in self.result:
                if line == "ok":
                    continue
                temp=line.split()
                if len(temp)==3:
                    temp_k= (int (temp[2]),float(temp[1]))
                    if temp[0] in self.return_dict:
                        self.return_dict[temp[0]].append(temp_k)
                    else:
                        temp_list=[temp_k]
                        self.return_dict[temp[0]]=temp_list



            return self.return_dict

    def __del(self):
        self.sock.close()

class ClientError(Exception):
    def __init__(self,value):
        self.msg=value
    def __str__(self):
        return self.msg



