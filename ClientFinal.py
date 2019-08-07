import tkinter as tk
import socket
import threading
import time





class chat():
        
    def __init__(self):
        self.host = '130.71.242.119'
        self.port = 5000
        self.server = (self.host, 5000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setblocking(0)
        self.shutdown = False
        self.tLock = threading.Lock()
        self.name =''  
        #create window
        self.window=tk.Tk()
        canvas=tk.Canvas(self.window,width=400,height=500)
        self.window.title('Chin Chat 1.0')
        self.window.resizable(width='FALSE',height='FALSE')
        canvas.pack()
        #Create Chat Window
        self.chatlog=tk.Text(self.window,bd=0,bg="white",height=8,width=50,font="Arial")
        self.chatlog.configure(state=tk.DISABLED)
        #Bind Scrollbar to chat window
        scrollbar = tk.Scrollbar(self.window,command=self.chatlog.yview)
        self.chatlog['yscrollcommand'] = scrollbar.set
                    #Create Send Button
        sendbutton=tk.Button(self.window,font=30, text="Send", width="12", height=5,
                            bd=0, bg='lightblue', activebackground='blue',
                            command=self.ClickAction)

        self.entrybox=tk.Text(self.window,bd=0,bg='white',width='29',height='5',font='Arial')
        self.entrybox.bind('<Return>',self.DisableEntry)
        self.entrybox.bind('<KeyRelease-Return>',self.PressAction)
        self.entrybox.place(x=128, y=401, height=90, width=265)
        scrollbar.place(x=376,y=6, height=386)
        self.chatlog.place(x=6,y=6, height=386, width=370)
        sendbutton.place(x=6, y=401, height=90)

        self.lbl=tk.Label(self.window,text="Type your name followed by enter.")
        self.lbl.pack()

        
        self.e=tk.Entry(self.window)
        self.e.pack()
        self.e.bind('<Return>',self.get_name)

        self.changename=tk.Button(self.window,text='Click to change name',command =self.change_name)
        self.changename.pack()
        
        self.entrytext=""
        self.rectext=""
        
    def change_name(self):
        self.e.configure(state='normal')
                                  
        
    def get_name(self, event):
        #self.e.configure(state='normal')
        self.name = self.e.get()
        self.e.configure(state='disabled')
        

        
    def update_entry_text(self):
        self.entrybox=tk.Text(self.window,bd=0,bg='white',width='29',height='5',font='Arial')
        
        self.entrybox.place(x=128, y=401, height=90, width=265)
        self.window.update_idletasks()
        self.window.after(1000,self.update_entry_text)
        
    def DisableEntry(self,event):
        self.entrybox.configure(state=tk.DISABLED)

    def ClickAction(self):
        #write message to chat window
        #self.update_text()
        self.entrytext = self.entrybox.get("0.0",tk.END)
        #Scroll to the bottom of chat window
        self.chatlog.yview(tk.END)
       # Erase previous message in entry box
        self.send(self.entrytext)
        self.entrybox.delete("0.0",tk.END)
        #send message
        
    def PressAction(self,event):
        self.entrybox.configure(state=tk.NORMAL)
        self.ClickAction()
    def DisableEntry(self,event):
        self.entrybox.configure(state=tk.DISABLED)
        
        

    def send(self,message):
        if message != 'q':
            
            if message != '':
                message= self.name+ ": " + message
                message= message.encode()
                self.s.sendto(message, self.server)
                message= message.decode()
            self.tLock.acquire()
            self.tLock.release()
            time.sleep(0.2)
        if message == 'q':
            message = (self.name + " Has left the Chatroom :C")
            message=message.encode()
            self.s.sendto(message,self.server)
            time.sleep(0.2)
    def receving(self, name, sock):        
        while not self.shutdown:

            self.tLock.acquire()
            try:                
                while True:
                    data, addr = sock.recvfrom(1024)
                    self.rectext=data.decode()

                    if self.rectext !="":
                        self.chatlog.configure(state='normal')
                        if self.chatlog.index('end') != None:
                            linenumber=float(self.chatlog.index('end'))-1
                            self.chatlog.insert(tk.END, self.rectext)
                            self.chatlog.configure(state='disabled')
                            self.chatlog.yview(tk.END)
                    print(self.rectext)
                    update_rec(self.rectext)
                    recieve(data)
            except:
                pass
            finally:
                self.tLock.release()
        

     
    def main(self):
        

        rT = threading.Thread(target = self.receving, args = ("RecvThead", self.s ))
        rT.start()
        
        self.window.mainloop()
        self.shutdown = True
        rT.join()
        self.s.close()
        
        
        

        

chat().main()

