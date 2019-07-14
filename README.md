# autorainmeter

An AutoHotKey script to automatically cycle through Rainmeter layouts

## Setup

### Config

The only necessary change for it to run properly is that you must fix the `LayoutPath` key in the `config.ini`
with your own username instead of the placeholder. Other than that, everything is already set up with defaults.
If you want to change the timer, or hotkeys please note that the duration is in milliseconds. If you're not
familiar with AutoHotKey hotkey syntax, you can find the mappings [here](https://www.autohotkey.com/docs/KeyList.htm).

## Usage

* Your preview hotkey (default: `ctrl-l`) will open a message box telling you the next layout on deck and supply the option to re-randomize a new next layout.
* Your blank hotkey (default: `ctrl-b`) will activate a blank layout (default: `$Blank`).
* The script will run indefinitely in the background and simply cycle to a random valid layout from your folder when the user-defined timer
(default: `60m`) is up.

Note: There can not be any spaces in the individual layout names for this script to work.

## Alternative

In the `legacy-input` branch the program uses a different method to configure the script, relying on a Python script to
complete a skeleton of the AHK script here. if you have plenty of layouts with spaces, you may prefer to simply use
the other branch rather than change all your names. It also does things like allow you to put in `TimerDuration` in
a normal format, and use a file browser to input `LayoutPath`.

## Contributions

[/u/sidola](https://www.reddit.com/user/sidola) from [/r/autohotkey](https://www.reddit.com/r/autohotkey) helped develop the script.

Please let me know if there are any bugs or feature requests!