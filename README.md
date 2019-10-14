# Proxy-Server
A HTTPS proxy server with cache

A proxy server with a limited cache ability has been implemented
Proxy server runs at http://127.0.0.1:12345
Main server runs ar http://127.0.0.1:20000

Run the server using the command
```
python2 server.py
```

Run the proxy server using command
```
python2 proxyserver.py
```

The files 1.txt, 2.binary and trial.txt are present in the server directory curl requests were made to access the files

Eg: ```curl -x http://127.0.0.1:12345 http://127.0.0.1:20000/1.txt``` to access the file 1.txt from the server, and this will result in a cached file in a cache directory in the server directory. The next access is going to be faster.

Browser can also be used to communicate with the server.

Multiple requests can be handled by the proxy server simultaneously using threads.
