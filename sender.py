from tkinter import  *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import socket
import os
from time import sleep
import _thread

def fetchfile():
    global filename 
    filename = askopenfilename() 
    v.set(filename)
    pass   
def showfile():
    print(filename)
    pass 

def get_ip():
    sx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        sx.connect(('10.255.255.255', 1))
        IP = sx.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        sx.close()
    return IP

def addCheckBox():
    IP = get_ip()
    print(IP)
    ip = IP.split('.')
    ip.pop()
    network ='.'.join(ip)
    print(network)
    global alive 
    alive = []
    for host in range(8,9):
        try:
            s = socket.socket()
            s.settimeout(0.01)
            s.connect((network +'.'+str(host),12345))
            s.settimeout(None)
            s.send('name'.encode('utf-8'))
            s.send('\n'.encode('utf-8'))
            hostname = s.recv(100).decode("utf-8")
            s.recv(10) 
            print(hostname)
            alive.append({"ip":network +'.'+str(host),"hostname":hostname, "value":IntVar()})
            print("found"+(network +'.'+str(host)))
            
        except :#Exception as e:
            # print(str(e))
            pass
    # print(alive)
    i=1
    for server in alive:
        c = Checkbutton(rframe, text=server['ip']+'->'+server['hostname'], variable=server['value'])
        c.grid(row=i,column =0)
        i+=1
    pass


def sendtoreciever(ip,filename,master):
    s = socket.socket()
    s.connect((ip,12345))
    # print(s._closed)
    print(filename)
    statinfo = os.stat(filename)
    size = statinfo.st_size
    filen = filename.split('/')
    filen = filen[len(filen)-1]
    print(filen)
    f = open(filename,'rb')
    # print(s._closed)
    s.send("file".encode('utf-8'))
    s.send("\n".encode())
    s.send(filen.encode('utf-8'))
    s.send("\n".encode('utf-8'))
    s.send(str(size).encode('utf-8'))
    s.send("\n".encode('utf-8'))
    newwin = Toplevel(master)
    Label(newwin,text = filen+'\n'+ip).pack()
    percentage = StringVar()
    Label(newwin,textvariable = percentage).pack()
    newwin.geometry("+100+100")
    _thread.start_new_thread(sendshow,(s,f,percentage,size,newwin))
    newwin.mainloop()
    pass
    

def sendshow(s,f,percentage,size,newwin):
    i=0
    l = f.read(1024)
    i+=len(l)
    while(l):
        s.send(l)
        percentage.set(""+str(int(i*100/size))+"%")
        # print("transfered : %s perc" %(int((i*100)/size)))
        l = f.read(1024)
        i+=len(l)
    
    s.close()
    newwin.destroy()
    pass


def sendfile():
    global filename
    global alive
    if(filename is ''):
        messagebox.showinfo('File Error','Please Select File')
        return
    if(len(alive)==0):
        messagebox.showinfo('No Reciever','Please scan for recievers')
        return
    for rec in alive:
        if(rec['value'].get()==1):
            break
    else:
        messagebox.showinfo('No Reciever selected','Please select reciever')
    
    for rec in alive:
        if(rec['value'].get()==1):
            sendtoreciever(rec['ip'],filename,master)

    pass   

        
master = Tk()

filename =''
alive = []
fframe = Frame(master).grid(row=0,column=0)
v = StringVar(fframe,value = "select file")
Entry(fframe, state='disabled',textvariable = v,width = 100).grid(row=0, column=0)
Button(fframe,text = "Open", command= fetchfile).grid(row=0,column=1)
Button(fframe, text = "Scan for recievers", command = addCheckBox).grid(row=0,column=2)
Button(fframe, text = "Send file", command = sendfile).grid(row=0,column=3)
rframe = Frame(master).grid(row=1,column=0)

master.mainloop()