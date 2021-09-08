def CalcElecPara(arr):
    if(arr == None):
        return 0,0,0,0,0,0
    if(len(arr) < 21):
        return 0,0,0,0,0,0
    ret1 = ((arr[3]<<8)+arr[4])/10
    ret2 = ((arr[5]<<8)+arr[6]+(arr[7]<<24)+(arr[8]<<16))/1000
    ret3 = ((arr[9]<<8)+arr[10]+(arr[11]<<24)+(arr[12]<<16))/10
    ret4 = ((arr[13]<<8)+arr[14]+(arr[15]<<24)+(arr[16]<<16))/1000
    ret5 = ((arr[17]<<8)+arr[18])/10
    ret6 = ((arr[19]<<8)+arr[20])/100
    return ret1,ret2,ret3,ret4,ret5,ret6

def web_page(data):
    dy,dl,gl,dn,pl,ys = CalcElecPara(data)
    #dy,dl,gl,dn,pl,ys = 0,0,0,0,0,0
    html = """<!DOCTYPE HTML><html><head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; }
    h2 { font-size: 3.0rem; } p { font-size: 3.0rem; } .units { font-size: 1.2rem; } 
    .ds-labels{ font-size: 1.5rem; vertical-align:middle; padding-bottom: 15px; }
  </style></head>
  <body> <h2>电量统计</h2>
  <p>
    <span class="ds-labels">电压</span>""" + str(dy) + """V
  </p>
  <p>
    <span class="ds-labels">电流</span>""" + str(dl) + """A
  </p>
  <p>
    <span class="ds-labels">功率</span>""" + str(gl) + """W
  </p>
  <p>
    <span class="ds-labels">用电量</span>""" + str(dn) + """kwh
  </p>
  <p>
    <span class="ds-labels">频率</span>""" + str(pl) + """Hz
  </p>
  <p>
    <span class="ds-labels">功率因素</span>""" + str(ys) + """
  </p>
  </body></html>"""
    return html

def ReadPara(uart):
    import time
    buf = b'\x01\x04\x00\x00\x00\x0A\x70\x0D'
    uart.write(buf)
    time.sleep_ms(100)
    return uart.read()
    
def start_station(uart):
    import usocket as socket
    import gc
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while True:
      try:
        if gc.mem_free() < 12000:
          gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Content = %s' % request)
        readbuf = ReadPara(uart)
        response = web_page(readbuf)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        ret = conn.write(response)
        sendtime=0
        print(ret)
      except OSError as e:
        conn.close()
        print('Connection closed')
