import os
import uasyncio
from nanoweb import HttpError, Nanoweb, send_file
from ubinascii import a2b_base64 as base64_decode
from machine import UART

CREDENTIALS = ('huahua', 'dandan')

async def send_response(request, code=200, message="OK"):
    await request.write("HTTP/1.1 %i %s\r\n" % (code, message))
    await request.write("Content-Type: application/json\r\n\r\n")
    await request.write('{"status": true}')

def authenticate(credentials):
    async def fail(request):
        await request.write("HTTP/1.1 401 Unauthorized\r\n")
        await request.write('WWW-Authenticate: Basic realm="Restricted"\r\n\r\n')
        await request.write("<h1>Unauthorized</h1>")

    def decorator(func):
        async def wrapper(request):
            header = request.headers.get('Authorization', None)
            if header is None:
                return await fail(request)

            # Authorization: Basic XXX
            kind, authorization = header.strip().split(' ', 1)
            if kind != "Basic":
                return await fail(request)

            authorization = base64_decode(authorization.strip()) \
                .decode('ascii') \
                .split(':')

            if list(credentials) != list(authorization):
                return await fail(request)

            return await func(request)
        return wrapper
    return decorator

@authenticate(credentials=CREDENTIALS)
async def api_status(request):
    """API status endpoint"""
    await request.write("HTTP/1.1 200 OK\r\n")
    await request.write("Content-Type: application/json\r\n\r\n")
    await request.write('{"status": "running"}')


@authenticate(credentials=CREDENTIALS)
async def api_ls(request):
    await request.write("HTTP/1.1 200 OK\r\n")
    await request.write("Content-Type: application/json\r\n\r\n")
    await request.write('{"files": [%s]}' % ', '.join(
        '"' + f + '"' for f in sorted(os.listdir('/'))
    ))

@authenticate(credentials=CREDENTIALS)
async def api_reboot(request):
    import machine
    machine.soft_reset()

@authenticate(credentials=CREDENTIALS)
async def api_download(request):
    await request.write("HTTP/1.1 200 OK\r\n")

    filename = request.url[len(request.route.rstrip("*")) - 1:].strip("/")

    await request.write("Content-Type: application/octet-stream\r\n")
    await request.write("Content-Disposition: attachment; filename=%s\r\n\r\n"
                        % filename)
    await send_file(request, filename)


@authenticate(credentials=CREDENTIALS)
async def api_upload(request):
    if request.method != "PUT":
        raise HttpError(request, 501, "Not Implemented")

    bytesleft = int(request.headers.get('Content-Length', 0))

    if not bytesleft:
        await request.write("HTTP/1.1 204 No Content\r\n\r\n")
        return

    output_file = request.url[len(request.route.rstrip("*")) - 1:].strip("\/")
    tmp_file = output_file + '.tmp'

    try:
        with open(tmp_file, 'wb') as o:
            while bytesleft > 0:
                chunk = await request.read(min(bytesleft, 64))
                o.write(chunk)
                bytesleft -= len(chunk)
            o.flush()
    except OSError as e:
        raise HttpError(request, 500, "Internal error")

    try:
        os.remove(output_file)
    except OSError as e:
        pass

    try:
        os.rename(tmp_file, output_file)
    except OSError as e:
        raise HttpError(request, 500, "Internal error")

    await send_response(request, 201, "Created")


@authenticate(credentials=CREDENTIALS)
async def api_delete(request):
    if request.method != "DELETE":
        raise HttpError(request, 501, "Not Implemented")

    filename = request.url[len(request.route.rstrip("*")) - 1:].strip("\/")

    try:
        os.remove(filename)
    except OSError as e:
        raise HttpError(request, 500, "Internal error")

    await send_response(request)


naw = Nanoweb()

para = {
    'dy':'',
    'dl':'',
    'gl':'',
    'dn':'',
    'pl':'',
    'ys':'',
}
# Declare route from a dict
naw.routes = {
    '/status.html': para,
    '/api/status': api_status,
    '/api/ls': api_ls,
    '/api/download/*': api_download,
    '/api/upload/*': api_upload,
    '/api/delete/*': api_delete,
    '/api/reboot': api_reboot,
}

# Declare route directly with decorator
@naw.route("/ping")
def ping(request):
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write("pong")



async def run_task(uart,period):
    import mylib
    global para
    global naw
    while True:
        buf = b'\x01\x04\x00\x00\x00\x0A\x70\x0D'
        uart.write(buf)
        await uasyncio.sleep_ms(100)
        readbuf = uart.read()
        dy,dl,gl,dn,pl,ys = mylib.CalcElecPara(readbuf)
        para['dy'] = str(dy)
        para['dl'] = str(dl)
        para['gl'] = str(gl)
        para['dn'] = str(dn)
        para['pl'] = str(pl)
        para['ys'] = str(ys)
        naw.routes['/status.html'] = para
        print(para)
        await uasyncio.sleep_ms(period-100)



uart = UART(0,9600)
uart.init(9600, bits=8, parity=None, stop=1, rxbuf=50)

loop = uasyncio.get_event_loop()
loop.create_task(naw.run())
loop.create_task(run_task(uart,1000))
loop.run_forever()
