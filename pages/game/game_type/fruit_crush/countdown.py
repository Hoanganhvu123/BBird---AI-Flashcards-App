import flet as ft
import time
import threading
class Countdown(ft.UserControl):
    def __init__(self,seconds,func):
        super().__init__()
        self.seconds=seconds
        self.func=func
    
    def start(self):
        self.running = True
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()
    
    def end(self):
        self.running=False
        self.func()
        #print("Se acabo el tiempo")

    def reset(self,s):
        self.seconds = s
        mins, secs = divmod(self.seconds, 60)
        self.countdown.value = "{:02d}:{:02d}".format(mins, secs)
        self.update()
    
    def update_timer(self):
        while  self.running:
            mins, secs = divmod(self.seconds, 60)
            self.countdown.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            time.sleep(1)
            self.seconds -= 1
            if self.seconds==-1:
                self.end()

    def build(self):
        mins,secs=divmod(self.seconds,60)
        self.countdown=ft.Text(value="{:02d}:{:02d}".format(mins,secs),size=30,weight=ft.FontWeight.BOLD)
        return self.countdown
    

#def main(page: ft.Page):
#    a=Countdown(10)
#    page.add(a,ft.ElevatedButton("start",on_click=a.start))
    #page.add(Countdown(10))

#ft.app(target=main)
    
