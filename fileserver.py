import socket
from tkinter import messagebox
from tkinter import Tk
import sys
import _thread

master = Tk()
master.withdraw()

def showmessage(filename,address):
    messagebox.showinfo("File Recieved",filename+"\n From : "+str(address))    

def makeserver():
    try:
        s = socket.socket()
        print("Socket Created")
        s.bind(("",12345))
        print("Socket Binded")
        s.listen(10)
        #print("waiting for command")
        while True:
            print("waiting for command\n\n")
            (sc,address) = s.accept()
            print(address)
            try:
                l =''
                command = ''
                while l is not '\n':
                    command += str(l)
                    l = sc.recv(1).decode('utf-8')
                    
                if(command =="name"):
                    print("DNS request\n\n")                
                    sc.send(socket.gethostname().encode("utf-8"))
                    sc.send('\n'.encode("utf-8"))
                    sc.close()
                    continue
                print("transfer Request")
                filename=''
                l=''
                while(l is not '\n'):
                    filename += str(l)
                    l=sc.recv(1).decode('utf-8')
                size=''
                l=''
                while(l is not '\n'):
                    size += str(l)
                    l=sc.recv(1).decode('utf-8')
                size=int(size)
                
                
                
            except Exception as e:
                print(str(e))
                sc.close()
                continue
            
            print(filename)
            print(size)
            #print("\n")
            try:
                f = open(filename,"wb")
            except Exception as e:
                print(str(e))
                continue
            #sc.recv(10)
            l = sc.recv(1024)
            while l :
                f.write(l)
                
                #print(l)
                l = sc.recv(1024)
            f.close()
            print("\n\nClosing file")
            #showmessage(filename,address)
            _thread.start_new_thread(showmessage,(filename,address))            
            sc.close()
            print("Closing client")
            
    except Exception as e:
        #sc.close()
        s.close()
        print(str(e))
    pass

_thread.start_new_thread(makeserver,())

master.mainloop()

