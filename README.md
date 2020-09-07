# Proxy-Server
A HTTPS proxy server with cache

A proxy server with a limited cache ability has been implemented
* Proxy server runs at http://127.0.0.1:12345
* Main server runs ar http://127.0.0.1:20000

#### How to use

Run the server using the command
```
python2 server.py
```

Run the proxy server using command
```
python2 proxyserver.py
```

The files 1.txt, 2.binary and trial.txt are present in the server directory
curl requests were made to access the files

Eg: ```curl -x http://127.0.0.1:12345 http://127.0.0.1:20000/1.txt``` to access the file 1.txt from the server, and this will result in a cached file in a cache directory in the server directory. The next access is going to be faster.

Browser can also be used to communicate with the server, with the above mentioned address of the proxy server (```http://127.0.0.1:12345```).

#### Cache

After making a request, on browser or from terminal, the files are temporarily stored in the cache directory in the proxy server. The next request for the same file will be faster because of this. Can be verified by timing the curl requests on terminal.

#### Multi-threading

Multiple requests can be handled by the proxy server simultaneously using multi-threading.

This can be seen by opening the server on multiple browsers or terminals.
