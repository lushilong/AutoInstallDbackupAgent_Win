AutoInstallDbackupAgent_Win
===========================

首先要打开“Config.ini”文件设置参数


[InsConfig] --- 安装Agent

path          --- Agent和Standby安装路径，如果为空则使用默认
server_ip     --- DBackup Server的路径，一定要写正确
netprotocol   --- 使用“http”还是“https”，一定要写正确
serverport    --- DBackup Server的端口号，如果为空则使用默认
32bit_version --- 64位系统安装32位Agent则设置为“yes”，为空则使用默认
clusterip     --- 集群IP，有则自动输入；为空则不输入集群IP
32bitstandby  --- 输入“yes”则使用32位版本，如果为空则使用默认


[FtpInfo] --- 设置FTP

ftp_server_ip   --- 下载Agent包的FTP的IP地址
tp_user_name    --- FTP的用户名
ftp_user_passwd --- FTP的密码
ftp_dir_path    --- FTP服务器中Agent包的路径

[info] --- 该节下的参数不用设置，程序自动修改
