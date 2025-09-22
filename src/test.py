import eventlet
import gevent
import socketio
import stats
import threading
import time
import unicorn_mini_driver

WINDOW_SECONDS = 1
s = stats.Stats(10, WINDOW_SECONDS)

global last_timer_time
global last_timer_cleared
last_timer_time = 0
last_timer_timeout = 5
last_timer_cleared = True

#u = unicorn_driver.UnicornDriver()
u = unicorn_mini_driver.UnicornMiniDriver()

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})
    
@sio.event
def connect(sid, environ):
    print(f"Got remote io connection from {sid}")


@sio.event
def set_timer(sid, data):
    print(f"Got timer data len {len(data)}")
    global last_timer_time
    global last_timer_cleared
    last_timer_time = time.time()
    last_timer_cleared = False

    u.display_raw(data)

def serve_app(sio, app):
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('192.168.1.1', 5000)), app)

wst = threading.Thread(target=serve_app, args=(sio,app))
wst.daemon = True
wst.start()
print("Daemon started")

while True:
    if not last_timer_cleared and time.time() - last_timer_time > last_timer_timeout:
        u.clear_display()
        u.enable_network_display()
        last_timer_cleared = True
    
    (net_sent, net_recv) = s.get_network("eth1")

    in_MBs = round(float(net_recv)/1024.0/float(WINDOW_SECONDS))
    out_MBs = round(float(net_sent)/1024.0/float(WINDOW_SECONDS))
    in_mbit = in_MBs*8
    out_mbit = out_MBs*8


    u.set_network(out_mbit, in_mbit)

    cpu_speed = s.get_cpu()
    u.set_cpu(cpu_speed)

    if not u.is_network_display_disabled():
        u.refresh()

    gevent.sleep(.1)
