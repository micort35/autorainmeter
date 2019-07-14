#!/usr/bin/env python
import os
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox


def get_input():
    """Get path, hotkey, and timer preferences"""

    # Create frame
    root = tk.Tk()
    root.title('autorainmeter')
    root.geometry('400x200')
    root.config(background='#a70000')
    root.resizable(height=False, width=False)
    root.rowconfigure(0, weight=2)
    root.rowconfigure(1, weight=2)
    root.rowconfigure(2, weight=2)
    root.rowconfigure(3, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)


    # Event handlers
    def browse():
        """Search for layout directory via local file explorer"""

        # Draw second search window and get username
        browser = tk.Tk()
        browser.withdraw()
        user = os.environ.get('USERNAME')

        # Open browser to get storage location
        initial_dir = f'C:\\Users\\{user}\\AppData\\Roaming\\Rainmeter'
        target_dir = tk.filedialog.askdirectory(parent=browser, initialdir=initial_dir,
                                                title='Please select a directory')

        # Update path field and destroy search window
        path.delete(0, tk.END)
        path.insert(0, target_dir)
        browser.destroy()


    def save():
        """Store config"""

        # Get variables if all entered
        fp = path.get()
        hotkeys = hotkey.get()
        duration = timer.get()
        if fp == '' or hotkeys == '' or duration == '':
            print('Error: Please complete all fields.')
            return

        # Assign individual hotkeys from string
        hotkeys = hotkeys.split(',')
        if len(hotkeys) != 2:
            print('Error: Incorrect number of hotkeys. Two neededed.')
            return
        prev = hotkeys[0]
        blank = hotkeys[-1]

        # Convert from hh:mm:ss format to ms
        duration = duration.split(':')
        if len(duration) != 3:
            print('Error: Please follow time format.')
            return
        try:
            duration = ((int(duration[0]) * 3600000) + (int(duration[1]) * 60000)
                        + (int(duration[-1]) * 1000))
        except ValueError:
            print('Error: Input for duration restricted to whole numbers and colons.')
            return
        duration = str(duration)

        # Store variables and destroy input GUI
        with open('out/config.txt', 'w') as out:
            out.write(fp + '\n' + prev + '\n' + blank + '\n' + duration)
        root.destroy()


    def on_close():
        """Confirm window close"""

        if tk.messagebox.askokcancel('Quit', 'Are you sure you want to quit?'):
            root.destroy()
            sys.exit()


    # Create widgets
    path_lbl = tk.Label(root, text='Rainmeter Suites Path')
    path = tk.Entry(root)
    browse = tk.Button(root, text='Browse', command=browse)
    hotkey_lbl = tk.Label(root, text='Hotkey Selection')
    hotkey_inst = 'preview,blank'
    hotkey = tk.Entry(root)
    hotkey.insert(0, hotkey_inst)
    timer_lbl = tk.Label(root, text='Layout Duration')
    timer_inst = 'hh:mm:ss'
    timer = tk.Entry(root)
    timer.insert(0, timer_inst)
    save = tk.Button(root, text='Save', command=save)

    # Structure and init window
    path_lbl.grid(row=0, column=0, ipadx=1)
    path.grid(row=0, column=1)
    browse.grid(row=0, column=2)
    hotkey_lbl.grid(row=1, column=0, ipadx=13)
    hotkey.grid(row=1, column=1)
    timer_lbl.grid(row=2, column=0, ipadx=15)
    timer.grid(row=2, column=1)
    save.grid(row=3, column=1)
    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()


def write_AHK():
    """Build AHK script from current config"""

    # Read in config options
    try:
        with open('out/config.txt', 'r') as config:
            config_options = config.read().splitlines()
            suites = os.listdir(config_options[0])
    except FileNotFoundError:
        print('Error: No config file found. Run without arguments to enter variables first.')
        return

    # Complete skeleton
    with open('src/skeleton.ahk', 'r', encoding='UTF8') as skeleton:
        breakpoints = ['; Clear Layout\n', '; Get Next Theme\n',
                       '; Start the theme changer on a specified interval\n', '; Themes start\n']
        lines = skeleton.readlines()

        # Search for critical sections
        for index, line in enumerate(lines):
            if line in breakpoints:
                breakpoints.pop()
                if len(breakpoints) == 3:
                    for number, suite in enumerate(suites):
                        # Ignore special layouts
                        if (suite.startswith('$') or suite.startswith('@')) is False:
                            lines.insert(index + number - 1, f'G_THEME_ARRAY.insert("{suite}")\n')
                elif len(breakpoints) == 2:
                    lines.insert(index + 1, f'SetTimer, Timer_ChangeTheme, {config_options[-1]}')
                elif len(breakpoints) == 1:
                    lines.insert(index + 1, f'{config_options[2]}::')
                elif not breakpoints:
                    lines.insert(index + 1, f'{config_options[1]}::')

        # Save configured script
        script = open('out/LayoutChanger.ahk', 'w', encoding='UTF8')
        script.writelines(lines)


def list_vars():
    """List current config options from storage"""

    try:
        with open('out/config.txt', 'r') as config:
            print(config.read())
    except FileNotFoundError:
        print('Error: No config file found. Run without arguments to enter variables first.')
        return


def get_and_set():
    """Complete operation: pull config options via GUI and build AHK script"""
    get_input()
    write_AHK()


def main():
    """Handler for CLI execution"""

    if len(sys.argv) > 1:
        if '-r' in sys.argv:
            write_AHK()
        if '-l' in sys.argv:
            list_vars()
    else:
        get_and_set()


if __name__ == '__main__':
    main()
