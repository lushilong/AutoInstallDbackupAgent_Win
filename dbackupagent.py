#
# -*- coding: utf-8 -*-
#

import os, sys, re, locale, shutil,time
import ConfigParser
import _winreg
from ftplib import FTP
import socket

cfg = ConfigParser.ConfigParser()
cfg.read("Config.ini")
set_ftp_server_ip = cfg.get("FtpInfo", "ftp_server_ip")
set_ftp_user_name = cfg.get("FtpInfo", "ftp_user_name")
set_ftp_user_passwd = cfg.get("FtpInfo", "ftp_user_passwd")
set_ftp_dir_path = cfg.get("FtpInfo", "ftp_dir_path")


# This function is raising exceptions
def RaisingException(someerror):

    print someerror + '\n'
    raw_input('Press "ENTER" to continue......')
    sys.exit(0)


# This function try to connect the FTP
def ConnectFtp():

    try:
        ftp = FTP(set_ftp_server_ip)
    except:
        RaisingException("Cna not connect to Ftp Server !!!")
    try:
        ftp.login(set_ftp_user_name, set_ftp_user_passwd)
    except:
        ftp.quit()
        RaisingException("Can not login to Ftp Server !!!")
    try:
        ftp.cwd(set_ftp_dir_path)
    except:
        ftp.quit()
        RaisingException("Can not open Ftp directory !!!")
    return ftp


# This function get the last version package
def GetLastVsersion(name):

    searchftp = ConnectFtp()
    package_list = searchftp.nlst()
    pattern = r'dbackup-%s_([0-9]{1,2}).([0-9]{1,2}).([0-9]{3,6}).([0-9]{1,2}).exe' % name 
    handle = re.compile(pattern)
    package_version = 0
    last_version_package = ''
    for i in package_list:
        match_package = handle.match(i)
        if match_package != None:
            getversion = int(match_package.group(3))
            if package_version < getversion:
                package_version = getversion
                last_version_package = i
    if package_version == 0:
        return 0
    else:
        return last_version_package
    searchftp.quit()


# define function download last version of Dbackup Agent Package from Ftp
def DownPackage(packagename):

    print "Downloading " + packagename + "...",
    downloadftp = ConnectFtp() 
    localfile = "dbagentpackage\\" + packagename
    try:
        downloadftp.retrbinary('RETR ' + packagename, open(localfile, 'wb').write)
        print "OK."
    except:
        RaisingException("Fail.")
    time.sleep(1)
    downloadftp.quit()


# detect the Windows is whether 64-bit system
def Is64Windows():

    return 'PROGRAMFILES(X86)' in os.environ


# define function auto get the ProductCode
def GetPackageInfo(pname):
    # 32-bit system or 64-bit system and 64-bit programs 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    # 64-bit system and 32-bit programs 'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    regkey = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
    if Is64Windows():
        arch_keys = [_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY]
    else:
        arch_keys = {0}
    for arch_key in arch_keys:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, regkey, 0, _winreg.KEY_ALL_ACCESS | arch_key)
        for i in xrange(0, _winreg.QueryInfoKey(key)[0]):
            skey_name = _winreg.EnumKey(key, i)
            skey = _winreg.OpenKey(key, skey_name)
            try:
                value = _winreg.QueryValueEx(skey, 'DisplayName')[0]
                if value == pname:
                    uninst_str = _winreg.QueryValueEx(skey, 'UninstallString')[0]
                    prod_code = re.findall(r'{[^}]*}', uninst_str)
                    prod_vers = _winreg.QueryValueEx(skey, 'DisplayVersion')[0]
                    return prod_code[0],prod_vers
            except:
                pass
            finally:
                _winreg.CloseKey(skey)
    return 0,0


# define function Auto Uninstall programs
def UninstallPackage(productcode, uninname):

    uninstallcommend = "MsiExec.exe /X" + str(productcode) + " /quiet"
    print "Uninstalling " + uninname + "...",
    if os.system(uninstallcommend) == 0:
        print "OK."
    else:
        RaisingException("Fail.")


if __name__ == '__main__':

    print "Checking the network connection... ",
    try:
        socket.gethostbyname("www.baidu.com")
        print "OK."
    except:
        RaisingException("Fail.")
    get_lang = locale.getdefaultlocale()[0]
    if get_lang == 'zh_CN':
        agentname = u'鼎甲迪备客户端'
        standbyname = u'鼎甲迪备数据同步'
    else:
        agentname = 'DBackup Agent'
        standbyname = 'Scutech DBackup Standby'
    agent_code, agent_version = GetPackageInfo(agentname)
    standby_code, standby_version = GetPackageInfo(standbyname)
    newest_agent = GetLastVsersion("agent")
    newest_standby = GetLastVsersion("standby")
    if newest_agent == 0 and newest_standby == 0:
        RaisingException("Can not match any packages !!!")
    else:
        newest_agent_version = (re.findall(r'(?<=_).{11,12}?(?=\.)', newest_agent))[0]
        if newest_standby == 0:
            newest_standby_version = 0
        else:
            newest_standby_version = (re.findall(r'(?<=_).{9,10}?(?=\.)', newest_standby))[0]
    print "Aready installed DBackup Agent:[%s] and DBackup Standby:[%s]" % \
        (agent_version, standby_version)
    print "Newest version is Dbackup Agent:[%s] and DBackup Standby:[%s]" % \
        (newest_agent_version, newest_standby_version)
    print "You can do:"
    print "Press '1' --Just remove old and install newest Agent"
    print "Press '2' --Install newest Agent and Standby"
    print "Press '3' --Just Download Agent and Standby"
    print "Press '4' --Uninstall all"
    print "Press '0' --exit"
    while True:
        try:
            get_input = int(raw_input("Please choose one: "))
            if get_input in [0, 1, 2, 3, 4]:
                break
            else:
                continue
        except BaseException:
            print "Please entry a number !"

    if get_input == 0:
        sys.exit(0)
    if get_input != 4:
        if os.path.exists('dbagentpackage'):
            shutil.rmtree('dbagentpackage')
        os.mkdir('dbagentpackage')
        cfg.set("info", "syslang", get_lang)
        cfg.set("info", "dbagentname", newest_agent)
        cfg.set("info", "dbstandbyname", newest_standby)
        if Is64Windows():
            cfg.set("info", "systype", "x64")
        else:
            cfg.set("info", "systype", "x86")
        cfg.write(open("Config.ini", "w"))
    if get_input in [1,2,3]:
        DownPackage(newest_agent)
        if get_input in [1,2]:
            if agent_code != 0:
                UninstallPackage(agent_code, "DBackup Agent")
            print "Installing DBackup Agent...",
            if os.system('InstallDbAgent.exe') == 0:
                if get_input == 1:
                    RaisingException("OK.")
                else:
                    print "OK."
            else:
                RaisingException("Fail.")
        if get_input in [2,3] and newest_standby_version != 0:
            DownPackage(newest_standby)
            if get_input == 2:
                if standby_code != 0:
                    UninstallPackage(standby_code, "DBackup Standby")
                print "Install DBackup Standby...",
                if os.system('InstallDbStandby.exe') == 0:
                    RaisingException("OK.")
                else:
                    RaisingException("Fail.")
            elif get_input == 3:
                RaisingException("Packages has downloaded.")
        else:
            RaisingException("Can not match any Standby packages !!!")
    elif get_input == 4:
        if standby_code == 0:
            print "DBackup Standby hasn't install."
        else:
            UninstallPackage(standby_code, "DBackup Standby")
        if agent_code == 0:
            RaisingException("DBackup Agent hasn't install.")
        else:
            UninstallPackage(agent_code, "DBackup Agent")
        print
        raw_input('Press "ENTER" to continue......')
        sys.exit(0)
    else:
        RaisingException("Something Error")
