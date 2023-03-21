rand=$RANDOM
if [ $((rand % 100)) -lt 20 ]; then
  cd /home/jetson/work/webGL_Greeting2/WebGL
elif [ $((rand % 100)) -lt 30 ]; then
  cd /home/jetson/work/webGL_Greeting3/WebGL
else
  cd /home/jetson/work/webGL_Greeting1/WebGL
fi
python3 startServer.py
