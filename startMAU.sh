#サーバ起動
cd /home/jetson/work
gnome-terminal -- sh startServer.sh
sleep 10
#ブラウザ起動
cd /home/jetson/work
gnome-terminal -- sh startBrowser.sh
sleep 60
#Greeting起動
cd /home/jetson/work
gnome-terminal -- sh startGreeting.sh
sleep 300
#ブラウザを最前面に移動
browser_window_id=$(xdotool search --name --onlyvisible "chromium")
xdotool windowactivate $browser_window_id
sleep 10
#Unityを最大表示
xdotool key z

