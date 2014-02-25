#cs ----------------------------------------------------------------------------

 AutoIt Version: 3.3.0.0
 Author:         lushilong

 Script Function:
    AutoIt script.
#ce ----------------------------------------------------------------------------


;ENVIRONMENT SETTINGS
$setpackagedir = @ScriptDir & "\" & "dbagentpackage"
$packagename = IniRead(@ScriptDir  & "\" & "Config.ini", "info", "dbstandbyname", "NA")
$startupFile = $setpackagedir & "\" & $packagename
$setsyslang = IniRead(@ScriptDir  & "\" & "Config.ini", "info", "syslang", "NA")
$setsystype = IniRead(@ScriptDir  & "\" & "Config.ini", "info", "systype", "NA")
$setinstdir = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "path", "NA")
$setstantype = IniRead(@ScriptDir  & "\" & "Config.ini", "InsConfig", "32bitstandby", "NA")
;MsgBox(0, "Debug001", $setsyslang)

if $setsyslang == "en_US" Then
	$installtitle = "Scutech DBackup Standby Setup"
	$welcomestep = "Welcome to the Scutech DBackup Standby Setup Wizard"
	$licensestep = "Please read the following license agreement carefully"
	$folderstep = "Destination Folder"
	$readinsll = "Ready to install Scutech DBackup Standby"
	$completed = "Completed the Scutech DBackup Standby Setup Wizard"
	$netstep = "&Next >"
    $install = "&Install"
    $finish = "&Finish"
Else
	$installtitle = "鼎甲迪备零丢失 安装程序"
	$welcomestep = "欢迎使用 鼎甲迪备零丢失 安装向导"
	$licensestep = "请仔细阅读以下许可协议"
	$folderstep = "目标文件夹"
	$readinsll = "已准备好安装 鼎甲迪备零丢失"
	$completed = "已完成 鼎甲迪备零丢失 安装向导"
	$netstep = "下一步(&N) >"
    $install = "安装(&I)"
    $finish = "完成(&F)"
EndIf

; Run Dbackup Agent
Run($startupFile)

; Select type Version
if $setsystype == "x64" Then
	While 1
		If WinExists("Scutech DBackup Standby Setup", "Please select the Version to install") Then
			If $setstantype == "yes" Then
				ControlClick("Scutech DBackup Standby Setup", "32bit Version", "Button2")
			EndIf
			ControlClick("Scutech DBackup Standby Setup", "OK", "Button4")
			ExitLoop
			
		ElseIf WinExists("鼎甲迪备零丢失安装程序", "请选择要安装的版本") Then
			If $setstantype == "yes" Then
				ControlClick("鼎甲迪备零丢失安装程序", "安装32位版本", "Button2")
			EndIf
			ControlClick("鼎甲迪备零丢失安装程序", "确定", "Button4")
			ExitLoop
			
		EndIf
	WEnd
EndIf


WinWaitActive($installtitle, $welcomestep)

While 1
    
    ;In the Welcome Step
    If WinExists($installtitle, $welcomestep) Then
        WinActive($installtitle, $welcomestep)
        ControlClick($installtitle, $netstep, "Button1")
    
	ElseIf WinExists($installtitle, $licensestep) Then        ;In the License Step
        WinActive($installtitle, $licensestep)
        ControlClick($installtitle, $netstep, "Button1")
		
	ElseIf WinExists($installtitle, $folderstep) Then        ;In the Destination Folder Step
        WinActive($installtitle, $folderstep)
        if $setinstdir <> "NA" Then
            ControlFocus($installtitle, $folderstep, "RichEdit20W")
            ControlSend($installtitle, $folderstep, "RichEdit20W", $setinstdir)
        EndIf
        ControlClick($installtitle, $netstep, "Button1")

	ElseIf WinExists($installtitle, $readinsll) Then        ;In the Read Install Step
        WinActive($installtitle, $readinsll)
        ControlClick($installtitle, $install, "Button1")
		
	ElseIf WinExists($installtitle, $completed) Then        ;In the Completed Step
        WinActive($installtitle, $completed)
        ControlClick($installtitle, $finish, "Button1")
		Sleep(3000)
        If Not WinExists($installtitle) Then
            ExitLoop
        EndIf
	
	Else
        Sleep(1000)
    
    EndIf
WEnd
