from base64 import decode
from concurrent.futures import process
import time
import http.server#BaseHTTPServer
import os, subprocess
import cpustat
import platform
import psutil

HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000

cpuinfo = cpustat.GetCpuLoad()

def uptime2():  
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds

def get_running_process():
    cmd = ["ps", "aux"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    o, e = proc.communicate()


    resp = []
    aux = ""

    for i in o.decode():
        if i.lower() in ["root", "command"]:
            resp += [aux]
            aux = ""

        aux += i

    return resp

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(bytes("<html><head><title>T1 - Sistemas Operacionais</title></head>", 'utf-8'))
        s.wfile.write(bytes("<body><p>T1 - Author: Guilherme Hiago Costa dos Santos</p>", 'utf-8'))

        datahora = os.popen('date').read()
        s.wfile.write(bytes("<p>Data e Hora: %s</p>" % datahora, 'utf-8'))
        s.wfile.write(bytes("<p>CPU uptime: %s in seconds</p>" % uptime2(), 'utf-8'))
        s.wfile.write(bytes("<p>CPU frequency: %s</p>" % str(psutil.cpu_freq()), 'utf-8'))
        s.wfile.write(bytes("<p>CPU model: %s</p>" % platform.processor(), 'utf-8'))
        s.wfile.write(bytes("<p>CPU: %s</p>" % cpuinfo.getcputime(), 'utf-8'))
        s.wfile.write(bytes("<p>Running Process: </p>", 'utf-8'))

        process_list = get_running_process()

        print(process_list)

        for i in process_list:
            s.wfile.write(bytes("<p>%s</p>" % i, 'utf-8'))


        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        #s.wfile.write(bytes("<p>You accessed path: %s</p>" % s.path, 'utf-8'))
        s.wfile.write(bytes("</body></html>", 'utf-8)'))

if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

