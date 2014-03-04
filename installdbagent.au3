#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.0.0
 Author:         lushilong

 Script Function:
    AutoIt script.
#ce ----------------------------------------------------------------------------


#NoTrayIcon
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
    $selectclusterip = "Select Cluster IP"
    $clusteripinput = "Please select cluster service ip address"
    $clusterokb = "OK"
    $orcldirstep = "Oracle directory"
    $readinstep = "Ready to install DBackup Agent"
    $netstep = "&Next >"
    $install = "&Install"
    $finish = "&Finish"
    $finishcontects = "Completed the DBackup Agent Setup Wizard"
    $serviper = "the server address is error"
Else
    $setupWinTitle = "鼎甲迪备客户端 安装程序"
    $welcomestep = "欢迎使用 鼎甲迪备客户端 安装向导"
    $licensestep = "请仔细阅读以下许可协议"
    $folderstep = "目标文件夹"
    $servaddstep = "填写服务器地址"
    $selectclusterip = "选择集群IP"
    $clusteripinput = "请选择集群服务IP"
    $clusterokb = "确定"
    $orcldirstep = "Oracle安装目录"
    $readinstep = "已准备好安装 鼎甲迪备客户端"
    $netstep = "下一步(&N) >"
    $install = "安装(&I)"
    $finish = "完成(&F)"
    $finishcontects = "已完成 鼎甲迪备客户端 安装向导"
    $serviper = "服务器地址错误"
EndIf

$setinstdir = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "path", "NA")
$setserverip = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "server_ip", "NA")
$setusehttps = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "netprotocol", "NA")
$setserverport = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "serverport", "NA")
$select32bit = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "32bit_version", "NA")
$inputclusterip = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "clusterip", "NA")

; Run Dbackup Agent
Run($startupFile)

; if 64bit system them select the 64bit Version
if $setsystype == "x64" Then
    ;MsgBox(0, "Debug001", $setsystype)
    While 1
        
        If WinExists("Scutech DBackup Agent Setup", "Please select the Version to install") Then
            If $select32bit == "yes" Then
                ControlClick("Scutech DBackup Agent Setup", "32bit Version", "Button2")
            EndIf
            ControlClick("Scutech DBackup Agent Setup", "OK", "Button4")
            ExitLoop
            
        ElseIf WinExists("鼎甲迪备客户端安装程序", "请选择要安装的版本") Then
            If $select32bit == "yes" Then
                ControlClick("鼎甲迪备客户端安装程序", "安装32位版本", "Button2")
            EndIf
            ControlClick("鼎甲迪备客户端安装程序", "确定", "Button4")
            ExitLoop
            
        Else
            Sleep(1000)
            
        EndIf
        
    WEnd
    
EndIf

WinWaitActive($setupWinTitle, $welcomestep)
If WinExists($setupWinTitle, $welcomestep) Then
    WinActive($setupWinTitle, $welcomestep)
EndIf

$i = 0 ;for cluster ip
While 1
    
    ;In the Welcome Step
    If WinExists($setupWinTitle, $welcomestep) Then
        WinActive($setupWinTitle, $welcomestep)
        ControlClick($setupWinTitle, $netstep, "Button1")
    
    ElseIf WinExists($setupWinTitle, $licensestep) Then        ;In the License Step
        WinActive($setupWinTitle, $licensestep)
        ControlClick($setupWinTitle, $netstep, "Button1")

    ElseIf WinExists($setupWinTitle, $folderstep) Then        ;In the Destination Folder Step
        WinActive($setupWinTitle, $folderstep)
        if $setinstdir <> "NA" Then
            ControlFocus($setupWinTitle, $folderstep, "RichEdit20W1")
            ControlSend($setupWinTitle, $folderstep, "RichEdit20W1", $setinstdir)
        EndIf
        ControlClick($setupWinTitle, $netstep, "Button1")

    ElseIf WinExists($setupWinTitle, $servaddstep) Then        ;In the Input server address Step
        WinActive($setupWinTitle, $servaddstep)
        if $setusehttps == "https" Then
            ControlCommand($setupWinTitle, $servaddstep, "ComboBox1", "SelectString", "https")
        EndIf
        ;type Dbackup Server IP Address
        $getcurrentip = ControlGetText($setupWinTitle, $servaddstep, "RichEdit20W1")
        If $getcurrentip <> $setserverip Then
            ControlFocus($setupWinTitle, $servaddstep, "RichEdit20W1")
            ControlSend($setupWinTitle, $servaddstep, "RichEdit20W1", $setserverip)
        EndIf
        ; set the server port
        if $setserverport <> "NA" Then
            ControlFocus($setupWinTitle, $servaddstep, "RichEdit20W2")
            ControlSend($setupWinTitle, $servaddstep, "RichEdit20W2", $setserverport)
        EndIf
        ; Select Cluster IP
        If $inputclusterip <> "NA" And $i == 0 Then
            ControlClick($setupWinTitle, $selectclusterip, "Button4")
            While 1
                If WinExists($setupWinTitle, $clusteripinput) Then
                    ControlFocus($setupWinTitle, $clusteripinput, "RichEdit20W1")
                    ControlSend($setupWinTitle, $clusteripinput, "RichEdit20W1", $inputclusterip)
                    ControlClick($setupWinTitle, $clusterokb, "Button1")
                    Sleep(1000)
                    If Not WinExists($setupWinTitle, $clusteripinput) Then
                        $i = 1
                        ExitLoop
                    EndIf
                EndIf
            WEnd
        EndIf
        
        ControlClick($setupWinTitle, $netstep, "Button1")
        If WinExists($setupWinTitle, $serviper) Then
            ExitLoop
        EndIf
    
    ElseIf WinExists($setupWinTitle, $orcldirstep) Then        ;In the Oracle directory Step
        WinActive($setupWinTitle, $orcldirstep)
        ControlClick($setupWinTitle, $netstep, "Button1")

    ElseIf WinExists($setupWinTitle, $readinstep) Then        ;In the Ready to install DBackup Agent Step
        WinActive($setupWinTitle, $readinstep)
        ControlClick($setupWinTitle, $install, "Button1")

    ElseIf WinExists($setupWinTitle, $finishcontects) Then        ;In the Completed the DBackup Agent Setup Wizard Step
        WinActive($setupWinTitle, $finishcontects)
        ControlClick($setupWinTitle, $finish, "Button1")
        Sleep(3000)
        If Not WinExists($setupWinTitle) Then
            ExitLoop
        EndIf
    
    Else
        Sleep(1000)
    
    EndIf

WEnd
