#サーバ起動
gnome-terminal -- sh startServer.sh
sleep 10
#ブラウザ起動
gnome-terminal -- sh startBrowser.sh
sleep 60
#Greeting起動
gnome-terminal -- sh startGreeting.sh
sleep 300
#ブラウザを最前面に移動
browser_window_id=$(xdotool search --name --onlyvisible "chromium")
xdotool windowactivate $browser_window_id
sleep 5
#Unityを最大表示
xdotool key z

