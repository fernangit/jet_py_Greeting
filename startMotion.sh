#ブラウザを最前面に移動
browser_window_id=$(xdotool search --name --onlyvisible "chromium")
xdotool windowactivate $browser_window_id
sleep 10
#Unityを最大表示
xdotool key z
#モーション呼び出し
cd /home/jetson/work/jet_py_Greeting
python3 /home/jetson/work/jet_py_Greeting/motion.py $1
