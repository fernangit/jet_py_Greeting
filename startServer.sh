rand=$(od -vAn -N4 -tu4 < /dev/random)
echo "$rand"
if [ $((rand % 100)) -lt 20 ]; then
  echo 'webGL_Greeting2'
  cd /home/jetson/work/webGL_Greeting2/WebGL
elif [ $((rand % 100)) -lt 30 ]; then
  echo 'webGL_Greeting3'
  cd /home/jetson/work/webGL_Greeting3/WebGL
else
  echo 'webGL_Greeting1'
  cd /home/jetson/work/webGL_Greeting1/WebGL
fi
python3 startServer.py
