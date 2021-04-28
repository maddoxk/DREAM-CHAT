
██████╗ ██████╗ ███████╗ █████╗ ███╗   ███╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗████╗ ████║
██║  ██║██████╔╝█████╗  ███████║██╔████╔██║
██║  ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║
██████╔╝██║  ██║███████╗██║  ██║██║ ╚═╝ ██║
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
Dream-Chat is a simple chat room script in python. It uses AES encryption for secured data transfer over public network. It consist of two scripts a server and a client. Run the server.py in a system so that the client client.py can connect from remote systems with the correct password. You can connect multiple client.py to one single server from remote systems for a group chat. You can edit dream.conf and change password, host, port and view mode.

##########################################

SERVER.PY USAGE

 $ python server.py

##########################################

CLIENT.PY USAGE

 $ python client.py "host_ip" "port" "password" "nick_name"

##########################################
![image](https://user-images.githubusercontent.com/58894216/116343032-7c776880-a798-11eb-9e25-ec8e98e57795.png)
