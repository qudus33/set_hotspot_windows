# This program is used to setup a hotspot using python.
# Option includes setting the name of the hotspot as well as the password to be used
# You can also view the details on whether to start the hotspot or stop it

import tkinter as tk
import subprocess
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    root = tk.Tk()
    root.title('Set Hotspot')
    root.geometry('350x320')

    myLabel = tk.Label(root, text='Setup your hotspot', )
    myLabel.grid()

    def get_details():
        New_window = tk.Toplevel()
        New_window.title('Create New hotspot')
        
        def submit():
            global get_ssid
            global get_password
            
            settings = open('settings.in', 'w')
            get_ssid = ssid.get()
            get_password = password.get()
            settings.write(get_ssid + '\n')
            settings.write(get_password)
        
            tk.Label(New_window, text=f'SSID = {get_ssid}', padx=10).grid(row=4, column=0)
            tk.Label(New_window, text=f'Password = {get_password}', padx=10).grid(row=5, column=0)
            settings.close()
            ssid.delete(0, "end")
            password.delete(0, "end")

        myLabel1 = tk.Label(New_window, text='Setup New Hotspot')
        myLabel1.grid()
        ssid = tk.Entry(New_window, width=30)
        ssid.insert(0, '')
        ssid_name = tk.Label(New_window, text='Enter SSID')
        password = tk.Entry(New_window, width=30)
        password.insert(0, '')
        password_name = tk.Label(New_window, text='Enter Password')
        button_submit = tk.Button(New_window, text='Submit', command=submit)
        button_exit = tk.Button(New_window, text='Exit', command=New_window.destroy)

        ssid_name.grid(row=1, column=0)
        ssid.grid(row=1, column=1)
        password_name.grid(row=2, column=0)
        password.grid(row=2, column=1)
        button_submit.grid(row=3, column=1, padx=20)
        button_exit.grid(row=3, column=2, padx=20)

    def start():
        global ssid_name
        global hotspot_password
        settings = open('settings.in', 'r')
        hotspot_settings = settings.read().split()
        ssid_name = hotspot_settings[0]
        hotspot_password = hotspot_settings[1]
        settings.close()
        
        subprocess.run(f"netsh wlan set hostednetwork mode=allow ssid=\"{ssid_name}\" key=\"{hotspot_password}\"", shell=True, capture_output=True)
        
        start = subprocess.run("netsh wlan start hostednetwork", shell=True, capture_output=True)
        tk.Label(root, text=start.stdout.decode()).grid(row=5)

    def stop():
        stop = subprocess.run("netsh wlan stop hostednetwork", shell=True, capture_output=True)
        tk.Label(root, text=stop.stdout.decode()).grid(row=5)

        

    def status():
        new_window = tk.Toplevel()
        new_window.title('Status')
        show_status = subprocess.run("netsh wlan show hostednetwork", shell=True, capture_output=True)
        tk.Label(new_window, text=show_status.stdout.decode()).grid(row=0, column=0)
        
        button_exit = tk.Button(new_window, text='Exit', command=new_window.destroy, padx=20, pady=20)
        button_exit.grid(row=1, column=0)


    settings = open('settings.in', 'r')
    ssid_name = str(settings.readline())
    hotspot_password = str(settings.readline())
    settings.close()

    button_start = tk.Button(root, text='Start', padx=40, pady=20, command=start)
    button_stop = tk.Button(root, text='Stop', padx=40, pady=20, command=stop)
    button_status = tk.Button(root, text='Status', padx=40, pady=20, command=status)
    button_new = tk.Button(root, text='New', padx=40, pady=20, command=get_details)
    tk.Label(root, text=f"SSID: {ssid_name}").grid(row=3, column=0)
    tk.Label(root, text=f"Password: {hotspot_password}").grid(row=4, column=0)

    button_start.grid(row=1, column=0)
    button_stop.grid(row=1, column=1)
    button_status.grid(row=2, column=0)
    button_new.grid(row=2, column=1)

    root.mainloop()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)