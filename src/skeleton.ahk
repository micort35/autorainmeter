#NoEnv                          ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input                  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%     ; Ensures a consistent starting directory.
#SingleInstance
#Persistent
 
; Theme Array
G_THEME_ARRAY := []
 
; Themes start

; Boolean Initialization
IsRunning := true

; Init variables
nextTheme := 0
prevTheme := 0
 
; Get a theme for the first run
nextTheme := GetNextTheme(prevTheme)
 
; Run timer once when we start
Gosub, Timer_ChangeTheme

; Start the theme changer on a specified interval


return ; AUTO EXEC ENDS ------------
 
; ------------ HOTKEYS -------------
 
; Get Next Theme

    nextThemeName := G_THEME_ARRAY[nextTheme]
    MsgBox, 5, Next Layout, Your next layout is %nextThemeName%.`nPress retry to randomize your layout again.
    ifMsgBox, Retry
    {
        nextTheme := GetNextTheme(prevTheme)
        return
    }
return

; Clear Layout

{
    if(IsRunning := 1) {
   	    Run, "C:\Program Files\Rainmeter\Rainmeter.exe\" !LoadLayout "$Blank"
	    IsRunning := 0
	    return
	} else{
	    Reload
	    IsRunning := 1
	}
}

; ------------ TIMERS --------------
 
; Theme Change Timer
Timer_ChangeTheme:
   ; Loop through our theme array and use the theme that matches the number
    for each, value in G_THEME_ARRAY {
        ; Index = Each, Output = Value
        if (nextTheme = each) {
            ; Run this theme
            Run, "C:\Program Files\Rainmeter\Rainmeter.exe" !LoadLayout "%value%"
 
            ; For testing
            TrayTip, Theme, %value%
 
            ; Remember this theme
            prevTheme := each
            break        
        }
    }
 
    ; Get a new theme for the next run
    nextTheme := GetNextTheme(prevTheme)
return
 
; ------------ FUNCTIONS ------------
 
GetNextTheme(prevTheme) {
    Global G_THEME_ARRAY ; Get our global theme array
    nextTheme := prevTheme
 
    ; Get a random number between 1 and the amount if values in the array
    while (nextTheme = prevTheme) {
        Random, nextTheme, 1, % G_THEME_ARRAY._MaxIndex()
    }
 
    ; Return our new random theme
    return nextTheme
}