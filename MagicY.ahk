#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Recommended for catching common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

FileInstall, CalculateYVal.py,  %A_ScriptDir%\CalculateYVal.py, 1

FileSelectFile, SelectedFile, 3, , Please select your obj file, WaveFront Object (*.obj)

InputBox, UserInput, Model Scale, Please enter the scale of your model, , 250, 150

^y::
SendInput ^c
ClipWait
Sleep 100

RunWait, "%A_ScriptDir%\CalculateYVal.py" "%SelectedFile%" %UserInput% "%A_ScriptDir%\ypostemp.txt" %clipboard%

FileRead, ypos, %A_ScriptDir%\ypostemp.txt
FileDelete, %A_ScriptDir%\ypostemp.txt

Send {Left 10}{Right}{Right}%ypos%

return

	
#Persistent
return



