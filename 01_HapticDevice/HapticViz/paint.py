from tkinter import *
from tkinter.colorchooser import askcolor
import paho.mqtt.client as mqtt
import json

C_WIDTH=1200
C_HEIGHT=1200

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'



    def __init__(self):

        self.contact=False

        self.root = Tk()
        #self.root.geometry("1500x500")

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=C_WIDTH, height=C_HEIGHT)
        self.c.grid(row=1, columnspan=5)

        self.setup()

        if True:
            print("Starting mqtt..")
            #MQTT
            self.i=0
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message

            self.client.connect("192.169.1.3", 1883, 60)

            self.client.loop_start()
        self.root.mainloop()



    def setup(self):
        self.old_x = None
        self.old_y = None
        self.choose_size_button.set(1)
        self.line_width = self.choose_size_button.get()
  
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        #self.screen_width = self.root.winfo_screenwidth()
        #self.screen_height = self.root.winfo_screenheight()

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

        # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("Force_n")
        self.client.subscribe("Pos_m")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        #print(msg.topic+" "+str(msg.payload))

        if msg.topic=="Force_n":
            j=json.loads(str(msg.payload,'utf-8'))
            if j['F_n']>0.1:
                self.contact=True
            else:
                self.contact=False

        if msg.topic=="Pos_m":
            j=json.loads(str(msg.payload,'utf-8'))
            print(j['Py'])
            event= lambda : None
            scale=3500
            event.x=j['Py']*scale+C_WIDTH/2
            event.y=j['Pz']*-scale+C_HEIGHT/ 2
            print (str(event.x) + ' ' +str(event.y) )

            if self.contact:
                self.choose_size_button.set(6)
                self.paint(event)
            else:
                self.choose_size_button.set(1)
                self.paint(event)



        

        #self.c.create


if __name__ == '__main__':
        Paint()