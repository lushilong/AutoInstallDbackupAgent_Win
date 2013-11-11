# -*- coding: utf-8 -*-

import os, sys, re, locale, shutil, time
import ConfigParser
import _winreg
from ftplib import FTP
import win32api, win32con
import socket

cfg = ConfigParser.ConfigParser()
cfg.read("Config.ini")
set_ftp_server_ip = cfg.get("FtpInfo", "ftp_server_ip")
set_ftp_user_name = cfg.get("FtpInfo", "ftp_user_name")
set_ftp_user_passwd = cfg.get("FtpInfo", "ftp_user_passwd")
set_ftp_dir_path = cfg.get("FtpInfo", "ftp_dir_path")
set_mode = cfg.get("AutoMode", "setmode")



# This function get the last version package
def GetLastVsersion():

    try:
        socket.gethostbyname("baidu.com")
    except:
        return 1

    ftp = FTP(set_ftp_server_ip)
    try:
        ftp.login(set_ftp_user_name, set_ftp_user_passwd)
    except:
        return 0
    try:
        ftp.cwd(set_ftp_dir_path)
    except Error:
        return 0

    package_list = ftp.nlst()
    pattern = r'dbackup-agent_2.2.([0-9]{4,5}).([0-9]{2}).exe'
    handle = re.compile(pattern)
    package_version = 0
    last_version_package = ''
    for i in package_list:
        match_package = handle.match(i)

        if match_package != None:
            getversion = int(match_package.group(1))
            
            if package_version < getversion:
                package_version = getversion
                last_version_package = i

    if package_version == 0:
        return 0
    else:
        return last_version_package

    ftp.quit()


# define function download last version of Dbackup Agent Package from Ftp
def AutoDownPackage(package_name):

    try:
        socket.gethostbyname("baidu.com")
    except:
        return 1
    
    ftp = FTP(set_ftp_server_ip)
    try:
        ftp.login(set_ftp_user_name, set_ftp_user_passwd)
    except:
        return 0

    try:
        ftp.cwd(set_ftp_dir_path)
    except Error:
        return 0

    localfile = "dbagentpackage\\" + package_name
    ftp.retrbinary('RETR ' + package_name, open(localfile, 'wb').write)

    ftp.quit()


# detect the Windows is whether 64-bit system
def Is64Windows():
    return 'PROGRAMFILES(X86)' in os.environ


# define function auto get the ProductCode
def AutoGetProductInfo(productname, regkey):
    # 32-bit system or 64-bit system and 64-bit programs
    # UnInsKey = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    UnInsKey = regkey
    # 64-bit system and 32-bit programs
    # UnInsKey = 'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    # open reg key 
    Key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, UnInsKey)

    try:
        i = 0
        while 1:
            KeyName = _winreg.EnumKey(Key, i)
            i += 1
            Subkey = _winreg.OpenKey(Key, KeyName)
            try:
                Value, Type = _winreg.QueryValueEx(Subkey, 'DisplayName')
                if Value == productname:
                    # get the ProductCode
                    UnInsValue, UnInsType = _winreg.QueryValueEx(Subkey, 'UninstallString')
                    ProductCode = re.findall(r'{[^}]*}', UnInsValue)
                    ProductVersion, VersionType = _winreg.QueryValueEx(Subkey, 'DisplayVersion')
                    # ProductVersion = re.findall(r'([0-9]{4})', displayversion)
                    return ProductCode[0], ProductVersion
                _winreg.CloseKey(Subkey)
            except:
                _winreg.CloseKey(Subkey)
    
    except:
        return 0, 0                 
    
    finally:
        _winreg.CloseKey(Key)


# define function Auto Uninstall programs
def AutoUninstall(productcode):

    uninstallcommend = "MsiExec.exe /X" + str(productcode) + " /quiet"
    if os.system(uninstallcommend) == 0:
        return 0
    else:
        return 1

# define function to use update Dbackup Agent
def AutoUpdate(packagename):

    updatecommend = "dbagentpackage\\" + packagename + " /qn QUIET=1 ISUPDATE=1 ReinstallMode=amus" 
    if os.system(updatecommend) == 0:
        return 0
    else:
        return 1





if __name__ == '__main__':

    if os.path.exists('dbagentpackage'):
        shutil.rmtree('dbagentpackage')
    os.mkdir('dbagentpackage')
    get_lang = locale.getdefaultlocale()[0]
    get_systype = Is64Windows()
    if get_lang == 'zh_CN':
        productname = u'鼎甲迪备客户端'
    else:
        productname = 'DBackup Agent'

    regkey = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    get_productcode, get_productversion = AutoGetProductInfo(productname, regkey)
    if get_systype and get_productversion == 0:
        regkey = 'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
        get_productcode, get_productversion = AutoGetProductInfo(productname, regkey)

    last_packagename = GetLastVsersion()
    if last_packagename == 1:
        win32api.MessageBox(0, "Can not connect Internet", "Error",win32con.MB_OK)
        sys.exit(0)
    elif last_packagename == 0:
        win32api.MessageBox(0, "Can not connect to FTP Server", "Error",win32con.MB_OK)
        sys.exit(0)

    newestversion = re.findall(r'(?<=_).{11,12}?(?=\.)', last_packagename)
    if not get_productversion == 0:
        i = int((re.findall(r'([0-9]{4,5})', get_productversion))[0])
        j = int((re.findall(r'([0-9]{4,5})', newestversion[0]))[0])
        if i >= j:
            win32api.MessageBox(0, "[ %s ] is already install, There hasn't newer version." % get_productversion,\
                                "Message",win32con.MB_OK)
            sys.exit(0)
   
    cfg.set("info", "syslang", get_lang)
    cfg.set("info", "dbagentname", last_packagename)
    if get_systype:
        cfg.set("info", "systype", "x64")
    else:
        cfg.set("info", "systype", "x86")

    cfg.write(open("Config.ini", "w"))

    if get_productversion == 0:
        print "The system has not install DBackup Agent!"
        if set_mode == "0":
            inputs = raw_input('Press "ENTER" to install newest Agent: ')
        else:
            print "After 5 secends, It will automatic installing newest Agent!"
            time.sleep(5)

        print "Downloading Agent Package......"
        download = AutoDownPackage(last_packagename)
        if download == 1:
            win32api.MessageBox(0, "Can not connect Internet", "Error",win32con.MB_OK)
            sys.exit(0)
        elif download == 0:
            win32api.MessageBox(0, "Can not connect to FTP Server", "Error",win32con.MB_OK)
            sys.exit(0)
        else:
            print "Download Agent Package Successful !!!"

        print "Installing DBackup Agent......"
        if os.system('InstallDbAgent.exe') == 0:
            print "Dbackup Agent install successful !!!"
        else:
            win32api.MessageBox(0, "False", "Error", win32con.MB_OK) 

    else:
        if set_mode == '0':
            print "There is aready install [ %s ]" % get_productversion
            print "So the newest version is [ %s ]" % newestversion[0]
            print "You can do:"
            print "Press '1' --will update Dbackup Agnet"
            print "Press '2' --will remove and install newest Dbackup Agent"
            print "Press '0' --exit"
            while 1:
                try:
                    get_input = int(raw_input("Please choose one: "))
                except BaseException:
                    print "Please entry a number !"
                if get_input in [0, 1, 2]:
                    break
                else:
                    continue

            if get_input == 0:
                sys.exit(0) 
            else:
                print "Downloading Agent Package......" 
                download = AutoDownPackage(last_packagename)
                if download == 1:
                    win32api.MessageBox(0, "Can not connect Internet", "Error",win32con.MB_OK)
                    sys.exit(0)
                elif download == 0:
                    win32api.MessageBox(0, "Can not connect to FTP Server", "Error",win32con.MB_OK)
                    sys.exit(0)
                else:
                    print "Download Agent Package Successful !!!"
                if get_input == 1:
                    print "Updating Dbackup Agent......."
                    if AutoUpdate(last_packagename) == 0:
                        print "Dbackup Agent update successful !!!"
                    else:
                        win32api.MessageBox(0, "False", "Error", win32con.MB_OK)
                elif get_input == 2:
                    print "Removing Dbackup Agent......"
                    if AutoUninstall(get_productcode) == 0:
                        print "Dbackup Agent remove successful !!!"
                        print "Installing Dbackup Agent......"
                    else:
                        win32api.MessageBox(0, "Dbackup Agent remove false!", "Error", win32con.MB_OK)
                    if os.system('InstallDbAgent.exe') == 0:
                        print "Dbackup Agent install successful !!!"
                    else:
                        win32api.MessageBox(0, "False", "Error", win32con.MB_OK)
                else:
                    win32api.MessageBox(0, "Ooh!! Something Error!", "Error", win32con.MB_OK)

        else:
            print "Downloading Agent Package......" 
            download = AutoDownPackage(last_packagename)
            if download == 1:
                win32api.MessageBox(0, "Can not connect Internet", "Error",win32con.MB_OK)
                sys.exit(0)
            elif download == 0:
                win32api.MessageBox(0, "Can not connect to FTP Server", "Error",win32con.MB_OK)
                sys.exit(0)
            else:
                print "Download Agent Package Successful !!!"
            if set_mode == '1':
                print "Updating Dbackup Agent......"
                if AutoUpdate(last_packagename) == 0:
                    print "Dbackup Agent update successful !!!"
                else:
                    win32api.MessageBox(0, "False", "Error", win32con.MB_OK) 

            elif set_mode == '2':
                print "Removing Dbackup Agent......"
                if AutoUninstall(get_productcode) == 0:
                    print "Dbackup Agent remove successful !!!"
                    print "Installing Dbackup Agent......"
                else:
                    win32api.MessageBox(0, "Dbackup Agent remove false!", "Error", win32con.MB_OK)
                if os.system('InstallDbAgent.exe') == 0:
                    print "Dbackup Agent install successful !!!"
                else:
                    win32api.MessageBox(0, "False", "Error", win32con.MB_OK)

            else:
                win32api.MessageBox(0, "The [ set_mode ] parameter false!", "Error",win32con.MB_OK)
    time.sleep(3)
