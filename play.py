import subprocess

def play_sound(source):
    aplay = ['aplay','-q',source]
    wr = subprocess.Popen(aplay)
