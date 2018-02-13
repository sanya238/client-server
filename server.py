import asyncio

#Словарь для хранения метрик
database=dict()
#Обработка команды put
def put (stroka):
    if len(stroka)==4:
        temp_k=[stroka[2],stroka[3]]
        if stroka[1] in database:
            database[stroka[1]].append(temp_k)
        else:
            temp_list=[temp_k]
            database[stroka[1]]=temp_list
        respond = "ok\n\n"
    else:
        respond = "error\nwrong command\n\n"
    return respond
#Обработка команды get
def get (stroka):
    print (stroka[1],len(stroka))
    if len(stroka) == 2:
        respond="ok\n"
        if stroka[1]=="*":
            for key in database:
                temp_list= database[key]
                for keyin in temp_list:
                    val,timestamp = keyin
                    respond = respond + str(key)+" "+ str(val)+" "+str(timestamp)+"\n"
        else:
            if stroka[1] in database:
                temp_list= database[stroka[1]]
                for keyin in temp_list:
                    val,timestamp = keyin
                    respond = respond + str(stroka[1])+" "+ str(val)+" "+str(timestamp)+"\n"
            else:
                respond = "ok\n"
        respond+="\n"
    else:
        respond = "error\nwrong command\n\n"
    return respond

#запуск корутины при подключении. Так как в одном сеансе возможно несколько команд,соединение разрывается по инициативе клиента
async def handle_echo(reader, writer):
   try:
        while not reader.at_eof():
            data = await reader.read(1024)
            message = data.decode()
            com_str=message.replace('\n','').split()
            print(message)
#Проверка команды
            if len(com_str)>0 and com_str[0]=="put":
                resp=put(com_str)
            elif len(com_str)>0 and com_str[0]=="get":
                resp=get(com_str)
            else:
                resp="error\nwrong command\n\n"
            writer.write(resp.encode())
            print(resp)
            print (database)
   finally:
        writer.close()
#Запуск сервера

def run_server(host,port):
    print (host,port)
    port=int(port)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(
        handle_echo,
        host, port, loop=loop
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

#Для теста
if  __name__ ==  "__main__" :
    run_server("127.0.0.1",8881)