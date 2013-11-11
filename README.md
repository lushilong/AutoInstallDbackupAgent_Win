AutoInstallDbackupAgent_Win
===========================

首先要打开“Config.ini”文件设置参数

[AutoMode] --- 自动模式

setmode --- “0”半自动模式，手动选择升级还是卸载后再安装，如果没有安装则提示安装；
        --- “1”自动模式，自动升级现有的版本，如果没有安装则自动安装；
	--- “2”自动模式，自动卸载现有的版本后安装新的版本，如果没有安装则自动安装；


[InsConfig] --- 安装Agent

path        --- Agent安装路径，如果为空则使用默认；
server_ip   --- DBackup Server的路径，一定要写正确；
netprotocol --- 使用“http”还是“https”，一定要写正确；
serverport  --- DBackup Server的端口号，如果为空则使用默认；
32bit_version --- 64位系统安装32位则设置为“yes”，否则为空



[FtpInfo] --- 设置FTP

ftp_server_ip   --- 下载Agent包的FTP的IP地址
tp_user_name    --- FTP的用户名
ftp_user_passwd --- FTP的密码
ftp_dir_path    --- FTP服务器中Agent包的路径



[info] --- 该节下的参数不用设置，程序自动修改
