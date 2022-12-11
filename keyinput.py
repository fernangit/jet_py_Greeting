from pynput import keyboard

class MonKeyBoard:
    inputkey = ''
    def on_press(self,key):
        try:
            print('press: {}'.format(key.char))
            inputkey = key.char
            self.listener.stop()
            self.listener = None
        except AttributeError:
            print('spkey press: {}'.format(key))
    
    def on_release(self,key):
        print('release: {}'.format(key))
        if( key == keyboard.Key.esc):
            print("StopKey")
            self.listener.stop()
            self.listener = None
            
    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        
    def getstatus(self):
        if(self.listener == None):
            return False       
        return True
        
def keyin():
    monitor = MonKeyBoard()
    monitor.start()
    while(True):
        status = monitor.getstatus()
        #print(str(status))
        if(status == False):
            print("break")
            break
    return monitor.inputkey
