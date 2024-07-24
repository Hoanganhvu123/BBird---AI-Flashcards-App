import flet as ft
from time import sleep
class Counter(ft.UserControl):
    def start(self):
        self.running = True
        self.update_timer()

    def stop(self):
        self.running = False

    def reset(self):
        self.seconds = 0
        mins, secs = divmod(self.seconds, 60)
        self.count.value = "{:02d}:{:02d}".format(mins, secs)
        self.update()

    def update_timer(self):
        while  self.running:
            mins, secs = divmod(self.seconds, 60)
            self.count.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            sleep(1)
            self.seconds += 1
    

    
    def build(self):
        self.seconds = 0
        self.count = ft.Text(value = "00:00",size=40)
        return self.count
    

