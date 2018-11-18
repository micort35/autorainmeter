#!/usr/bin/env python
import os
import string
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

#get path, hotkey preferences, and timer
def get_input():
    #frame creation
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

    #inner functions for button usage and event handling
    def browse():
        browser = tk.Tk()
        browser.withdraw()
        initialdir = 'C:\\Users\\{}\\AppData\\Roaming\\Rainmeter'
        user = os.environ.get('USERNAME')
        initialdir = initialdir.format(user)
        dir = tk.filedialog.askdirectory(parent=browser, initialdir=initialdir, title='Please select a directory')
        if len(path.get()) > 0:
            path.delete(0, tk.END)
            path.insert(0, dir)
        else:
            path.insert(0, dir)
        browser.destroy()

    def save():
        #get variables and ensure there the strings aren't empty
        fp = path.get()
        hotkeys = hotkey.get()
        duration = timer.get()
        if fp is '' or hotkeys is '' or duration is '':
            print('You must fill in all boxes!')
            return

        #process hotkeys if valid input
        hotkeys = hotkeys.split(',')
        if len(hotkeys) is not 2:
            print('Incorrect number of hotkeys!')
            return
        prev = hotkeys[0]
        blank = hotkeys[-1]

        #process duration if valid input
        duration = duration.split(':')
        if len(duration) is not 3:
            print('Please keep duration to hours, minutes, and seconds!')
            return
        try:
            duration = (int(duration[0]) * 3600000) + (int(duration[1]) * 60000) + (int(duration[-1]) * 1000)
        except ValueError:
            print('Input for duration restricted to whole numbers and colons!')
            return
        duration = str(duration)

        #write vars to storage and
        file = open('vars.txt', 'w')
        file.write(fp + '\n' + prev + '\n' + blank + '\n' + duration)
        file.close
        root.destroy()

    def on_close():
        if tk.messagebox.askokcancel('Quit', 'Are you sure you want to quit?'):
            root.destroy()
            sys.exit()

    #widget creation
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

    #initialization of window
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
    #attempt to read in variables from storage
    try:
        with open('vars.txt', 'r') as var_file:
            vars = var_file.read().splitlines()
            suites = os.listdir(vars[0])
            var_file.close()
    except FileNotFoundError:
        print('No variables to write in! Run without options to enter variables before running.')
        return

    #populate AHK skeleton with new settings
    with open('skeleton.ahk', 'r', encoding='UTF8') as ahk_file_r, \
    open('LayoutChanger.ahk', 'w', encoding='UTF8') as ahk_file_w:
        breakpoints = ['; Clear Layout\n', '; Get Next Theme\n', '; Start the theme changer on a specified interval\n', '; Themes start\n']
        cmd = None
        curr = None
        #read through file until EOF
        while curr is not '':
            #copy non-critical sections
            while curr not in breakpoints:
                if curr is '':
                    return
                curr = ahk_file_r.readline()
                ahk_file_w.write(curr)
            #check for current critical section and write proper lines
            point = breakpoints.pop()
            if point is '; Themes start\n':
                while len(suites) > 0:
                    suite = suites.pop()
                    #get next suite incase invalid
                    while suite[0] is '$':
                        if len(suites) is 0:
                            break
                        suite = suites.pop()
                    #check for invalid final suite
                    if suite[0] is '$':
                        break
                    cmd = 'G_THEME_ARRAY.insert("{}")\n'
                    cmd = cmd.format(suite)
                    ahk_file_w.write(cmd)

            elif point is '; Start the theme changer on a specified interval\n':
                cmd = 'SetTimer, Timer_ChangeTheme, {}\n'
                cmd = cmd.format(vars[3])
                ahk_file_w.write(cmd)

            elif point is '; Get Next Theme\n':
                cmd = '{}::'
                cmd = cmd.format(vars[1])
                ahk_file_w.write(cmd)

            elif point is '; Clear Layout\n':
                cmd = '{}::'
                cmd = cmd.format(vars[2])
                ahk_file_w.write(cmd)  

def list_vars():
    try:
        with open('vars.txt', 'r') as file:
            print(file.read())
            file.close()
    except FileNotFoundError:
        print('No variables to read! Enter variables by running without any options.')
        return

def get_and_set():
    get_input()
    write_AHK()

def main():
    #check for refresh or list option
    if len(sys.argv) > 1:
        if '-r' in sys.argv:
            write_AHK()
        if '-l' in sys.argv:
            list_vars()
    else:
        get_and_set()

if __name__ == '__main__':
    main()