# autorainmeter

An autohotkey script to automatically cycle through Rainmeter layouts, with a Python script to configure the AHK script.

## Setup

### Requirements

`Python: >= 3.6`

### Build

`python C:\Users\User\autorainmeter\src\autorainmeter.py {-r, -l}`

The script supports two optional arguments:
* `-r` will build the script from an existing config file
* `-l` will list the current variables to the command line
* No arguments will prompt for input, build the config file, and then the script.

Note: `$` and `@` are escape characters: layouts beginning with either will not be added to the library to shuffle from.

## Usage

* Your preview hotkey will open a message box telling you the next layout on deck and supply the option to re-randomize a new next layout.
* Your blank hotkey will activate a blank layout (default: `$Blank`).
* The script will run indefinitely in the background and simply cycle to a random valid layout from your folder when the user-defined timer is up.

## Contributions

[/u/sidola](https://www.reddit.com/user/sidola) from [/r/autohotkey](https://www.reddit.com/r/autohotkey) helped develop the AHK skeleton.

Please let me know if there are any bugs or feature requests!