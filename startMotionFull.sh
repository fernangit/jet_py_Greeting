#ブラウザを最前面に移動
browser_window_id=$(xdotool search --name --onlyvisible "chromium")
xdotool windowactivate $browser_window_id
sleep 10
#Unityを最大表示
xdotool key z
#モーション呼び出し
cd /home/jetson/work/jet_py_Greeting
python3 /home/jetson/work/jet_py_Greeting/motion.py 0
sleep 3
python3 /home/jetson/work/jet_py_Greeting/motion.py 1
sleep 3
python3 /home/jetson/work/jet_py_Greeting/motion.py 2
sleep 3
python3 /home/jetson/work/jet_py_Greeting/motion.py 3
sleep 3
python3 /home/jetson/work/jet_py_Greeting/motion.py 4
sleep 3
python3 /home/jetson/work/jet_py_Greeting/motion.py 5
sleep 3
python3 /home/jetson/work/jet_py_Greeting/motion.py 6
sleep 3
python3 /home/jetson/work/jet_py_Greeting/motion.py 7
