#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.0.0
 Author:         lushilong

 Script Function:
        AutoIt script.
#ce ----------------------------------------------------------------------------


;ENVIRONMENT SETTINGS
$setpackagedir = @ScriptDir & "\" & "dbagentpackage"
$setpackagename = IniRead(@ScriptDir  & "\" & "Config.ini", "info", "dbagentname", "NA")
$startupFile = $setpackagedir & "\" & $setpackagename
$setsystype = IniRead(@ScriptDir  & "\" & "Config.ini", "info", "systype", "NA")
$setsyslang = IniRead(@ScriptDir  & "\" & "Config.ini", "info", "syslang", "NA")
;MsgBox(0, "Debug001", $setsyslang)

if $setsyslang == "en_US" Then
        $setupWintitle = "DBackup Agent Setup"
        $welcomestep = "Welcome to the DBackup Agent Setup Wizard"
        $licensestep = "Please read the following license agreement carefully"
        $folderstep = "Destination Folder"
        $servaddstep = "Input server address"
        $orcldirstep = "Oracle directory"
        $readinstep = "Ready to install DBackup Agent"
        $netstep = "&Next >"
        $install = "&Install"
        $finish = "&Finish"
        $finishcontects = "Completed the DBackup Agent Setup Wizard"
Else
        $setupWinTitle = "鼎甲迪备客户端 安装程序"
        $welcomestep = "欢迎使用 鼎甲迪备客户端 安装向导"
        $licensestep = "请仔细阅读以下许可协议"
        $folderstep = "目标文件夹"
        $servaddstep = "填写服务器地址"
        $orcldirstep = "Oracle安装目录"
        $readinstep = "已准备好安装 鼎甲迪备客户端"
        $netstep = "下一步(&N) >"
        $install = "安装(&I)"
        $finish = "完成(&F)"
        $finishcontects = "已完成 鼎甲迪备客户端 安装向导"
EndIf

$setinstdir = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "path", "NA")
$setserverip = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "server_ip", "NA")
$setusehttps = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "netprotocol", "NA")
$setserverport = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "serverport", "NA")
$select32bit = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "32bit_version", "NA")


; Run Dbackup Agent
Run($startupFile)
Sleep(1000)

; if 64bit system them select the 64bit Version
if $setsystype == "x64" Then
        ;MsgBox(0, "Debug001", $setsystype)
        While 1
                
                if WinExists("DBackup Agent", "Please select the Version to install") Then
                        if $select32bit == "yes" Then
                                ControlClick("DBackup Agent", "32bit Version", "Button2")
                        EndIf
                        Sleep(1000)
                        ControlClick("DBackup Agent", "OK", "Button4")
                        ExitLoop
                ElseIf WinExists("鼎甲迪备客户端安装程序", "请选择要安装的版本") Then
                        if $select32bit == "yes" Then
                                ControlClick("鼎甲迪备客户端安装程序", "安装32位版本", "Button2")
                        EndIf
                        sleep(1000)
                        ControlClick("鼎甲迪备客户端安装程序", "确定", "Button4")
                        ExitLoop
                Else
                        Sleep(2000)
                EndIf
                
        WEnd
        
EndIf

;In the Welcome Step
WinWaitActive($setupWinTitle, $welcomestep)
Sleep(1000)
ControlClick($setupWinTitle, $netstep, "Button1")
Sleep(1000)

;In the License Step
WinWaitActive($setupWinTitle, $licensestep)
Sleep(1000)
ControlClick($setupWinTitle, $netstep, "Button1")
Sleep(1000)

;In the Destination Folder Step
WinWaitActive($setupWinTitle, $folderstep)
Sleep(1000)
if $setinstdir <> "NA" Then
        ControlFocus($setupWinTitle, $folderstep, "RichEdit20W1")
        Sleep(1000)
        ControlSend($setupWinTitle, $folderstep, "RichEdit20W1", $setinstdir)
        Sleep(1000)
EndIf
ControlClick($setupWinTitle, $netstep, "Button1")
Sleep(1000)

;In the Input server address Step
WinWaitActive($setupWinTitle, $servaddstep)
Sleep(1000)
if $setusehttps == "https" Then
        ControlCommand($setupWinTitle, $servaddstep, "ComboBox1", "SelectString", "https")
EndIf
;type Dbackup Server IP Address
ControlSend($setupWinTitle, $servaddstep, "RichEdit20W1", $setserverip)
Sleep(1000)
ControlFocus($setupWinTitle, $servaddstep, "RichEdit20W1")
sleep(1000)
; set the server port
if $setserverport <> "NA" Then
        ControlFocus($setupWinTitle, $servaddstep, "RichEdit20W2")
        sleep(1000)
        ControlSend($setupWinTitle, $servaddstep, "RichEdit20W2", $setserverport)
        Sleep(1000)
EndIf
ControlClick($setupWinTitle, $netstep, "Button1")
Sleep(1000)

;In the Oracle directory Step
WinWaitActive($setupWinTitle, $orcldirstep)
Sleep(1000)
ControlClick($setupWinTitle, $netstep, "Button1")
Sleep(1000)

;In the Ready to install DBackup Agent Step
WinWaitActive($setupWinTitle, $readinstep)
Sleep(1000)
ControlClick($setupWinTitle, $install, "Button1")
Sleep(1000)

;waiting for installer complete
;In the Completed the DBackup Agent Setup Wizard Step
WinWaitActive($setupWinTitle, $finishcontects)
Sleep(1000)
ControlClick($setupWinTitle, $finish, "Button1")
Sleep(1000)
