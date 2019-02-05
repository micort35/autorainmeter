# autorainmeter

An autohotkey script to automatically cycle through Rainmeter layouts, with a Python script to configure the AHK script.

## Setup

Foremost, ensure your current Python version is 3.x, and that you have Autohotkey downloaded (all versions should work). Download skeleton.ahk and autorainmeter.py into the same directory, and do not rename them, unless you plan to go into the Python script and replace the file names there as well.

Running the script without arguments will use its default operation, creating a window to enter the path to your Rainmeter layouts folder, the hotkeys you want to use for previewing and blanking, as well as the layout duration.

Two files will then be created: vars.txt for variable storage, and LayoutChanger.ahk, the final product. You're free to move the generated AHK script, but vars.txt must stay with the Python script to run properly when using refresh or list.

The script can also be run with -r, or -l. -r will rewrite the AHK script using the current stored variables, useful if you've added new layouts but don't plan on changing the hotkeys or the layout duration. -l will list the stored variables in the terminal.

All error messages are printed out to the terminal.

Note: '$' is an escape character for layouts that you may not want to use for whatever reason. Any scripts such as '$Layout1' will not be entered into the list of layouts to cycle between. The script also ignores the '@Backup' layout.

## Usage

Your preview hotkey will open a message box telling you the next layout on deck and supply the option to re-randomize a new next layout.

Your blank hotkey will activate a blank layout (default: '$Blank'). Note that this does not cancel the timer and the script will still cycle to a non-blank layout when the timer is up. If you'd like to change the name of the blank layout, modify the skeleton.ahk or LayoutChanger.ahk under '; Clear Layout'.

Otherwise, the script will run in the background and simply cycle to a random valid layout from your folder when the user-defined timer is up, running until the script is exited.

## Contributions

/u/sidola from /r/autohotkey helped develop the AHK skeleton

Please let me know if there are any bugs or feature requests!