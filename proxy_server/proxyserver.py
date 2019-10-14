import socket,sys
import thread,threading
import os
import time

read_buffer = 4096
cache = {1:None,2:None,3:None}

def proxy_server(webserver,port,conn,data,addr,fname):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect((webserver,port)) # establishing connection
    # print(data)
    s.send(data)

    fname = fname.replace("/","_")

    ap = "./Cache/"
    cfile = ap+fname            # file name

    cf = open(cfile,'wb+')      # opening file

    while 1:
        reply = s.recv(read_buffer)

        if (len(reply)>0):
            cf.write(reply)     # writing the data into the file

            conn.send(reply)    # sending the data to the client

            # dar = float(len(reply))
            # dar = float(dar/1024)
            # dar = "%.3s" % (str(dar))
            # dar = "%s KB" % (dar)
            # 'Data transferred'

            # # print ("Successfully sent data")
            # print "[*] Request Complete: %s => %s <=" % (str(addr[0]),str(dar))

        else:
            break
        
    
    cf.close()              # closing the file
    
    s.close()               # closing socket

    conn.close()            # closing connection to 

def routing(data):
    t1 = data.split("\n")
    
    t2 = t1[1].split(" ")
    t3 = t2[1].replace("\n","")
    t4 = t3.replace("\r","")

    print(t4)

    data = data.replace(t4,"",1)    # modifying get request format
    data = data.replace("http://","",1)

    print(data)

    return data

def conn_string(conn,data,addr,fname):
    first_line = data.split("\n")[0]
    url = first_line.split(" ")[1]

    http_pos = url.find("://")  # storing position of the http address in the data

    if (http_pos == -1):
        temp = url
    else:
        temp = url[(http_pos+3):]
    
    port_pos = temp.find(":")

    webserver_pos = temp.find("/")

    if (webserver_pos == -1):
        webserver_pos = len(temp)

    webserver = ""
    port = -1

    if (port_pos == -1 or webserver_pos < port_pos):
        port = 80
        webserver = temp[:webserver_pos]

    else:
        port = int((temp[(port_pos+1):])[:webserver_pos - port_pos -1]) # port number
        webserver = temp[:port_pos]

    data = routing(data)    # parshing so as to modify get request
    
    proxy_server(webserver,port,conn,data,addr,fname)   # start a new thread for each request

def in_cache(fname):
    avail = cache.values()  #values of the cache dictionary

    if fname in avail:
        return 1
    
    else:
        return 0

def get_fname(data):
    t1 = data.split("\n")
    
    t2 = t1[0].split(" ")
    t3 = t2[1].replace("\n","")
    t4 = t3.replace("\r","")

    return t4

def put_in_cache(fname):    # storing the data in cache file
    old = cache[3]
    
    cache[3] = cache[2]
    cache[2] = cache[1]
    cache[1] = fname

    if (old):
        old = old.replace("/","_")
        path = "./Cache/"

        path = path+old
        os.remove(path)

def cache_retr(fname,conn):
    lst = os.listdir("./Cache") 

    fname = fname.replace("/","_")

    for i in range(len(lst)):
        if lst[i] == fname:
            ap = "./Cache/"
            cfile = ap+fname

            cf = open(cfile,'r')

            resp = cf.read()

            conn.send(resp)
            # print(cf.read())

            cf.close()

def modified_file(fname,data,conn):
    ap = "./Cache/"

    fname = fname.replace("/","_")

    cfile = ap+fname

    last_mtime = time.strptime(time.ctime(os.path.getmtime(cfile)), "%a %b %d %H:%M:%S %Y")
    header = time.strftime("%a %b %d %H:%M:%S %Y", last_mtime)

    h = "If-Modified-Since: "

    data = data[:-2]

    # data.append(header)
    data = data + h + header + '\r\n\r\n'

    print(repr(data))

    # print("conn val is below")
    # print(conn)

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect(('127.0.0.1',20000))
    # print(data)
    s.send(data)

    reply = s.recv(read_buffer)

    # print("status num is below")
    print(reply)

    stat = reply.split(" ")
    stat_msg = stat[1]

    # print(stat_msg)

    if (int(stat_msg) == 304):
        return 0
    
    elif (int(stat_msg) == 200):
        return 1

def start():
    try:
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'Cache')
        
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(("", 12345))               
        print("sock bound")                      
        s.listen(10)
        print("socket listing")

        print("Proxy Server Running at port 12345")

    except Exception, e:
        print("error initializing socket")
        s.close()
        sys.exit(2)

    while 1:
        try:

            conn,addr = s.accept()
            print("connection accepted")
            data = conn.recv(read_buffer)

            # conn_string(conn,data,addr)

            temp = routing(data)

            fname = get_fname(temp)

            cache_hit = 0

            if (in_cache(fname)):
                cache_hit = 1

            print("value of hit is ",cache_hit)
            print(cache)

            mod_stat = 0

            if (cache_hit):
                mod_stat = modified_file(fname,temp,conn)

            if (cache_hit and not mod_stat):
                # print("working bro")
                thread.start_new_thread(cache_retr,(fname,conn))

            else:
                put_in_cache(fname)
                thread.start_new_thread(conn_string,(conn,data,addr,fname))

            print(threading.activeCount(),threading.enumerate())

        except KeyboardInterrupt:
            s.close()
            print("Exiting Proxy Server due to Keyboard Interrupt")
            sys.exit(2)

    s.close()

start()