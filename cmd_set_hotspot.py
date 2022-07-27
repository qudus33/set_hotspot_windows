# This program is used to setup a hotspot using python.
# Option includes setting the name of the hotspot as well as the password to be used
# You can also view the details on whether to start the hotspot or stop it

import subprocess

def get_details():
    """ Get information for the ssid and the password """
    settings_confirmation = input("""
    Enter 'y' to create new hotspot settings.
    Enter 'n' to proceed with last hotspot settings.
    : """)
    if settings_confirmation == 'y':
        settings = open('settings.in', 'w')
        print("Setup your hotspot by providing a name and password\n")
        global ssid_name
        global hotspot_password
        ssid_name = input("Type the desired name for your hotspot: ")
        ssid_name = str(ssid_name)
        settings.write(ssid_name + '\n')
        hotspot_password = input("Type the password for the hotspot: ")
        hotspot_password = str(hotspot_password)
        settings.write(hotspot_password)
        settings.close()
    else:
        settings = open('settings.in', 'r')
        ssid_name = str(settings.readline())
        hotspot_password = str(settings.readline())
        settings.close()

def setup_hotspot():
    """ Setup the hotspot according to details gotteen. """
    print("Now configuring the hotspot")
    cmd_config = subprocess.run(f"netsh wlan set hostednetwork mode=allow ssid=\"{ssid_name}\" key=\"{hotspot_password}\"", shell=True)
    print(f"\nHotspot has been setup with ssid {ssid_name} and password {hotspot_password}")

def start_stop_show_hotspot():
    """ Start the hostspot session, show status and stop hotspot """
    while True:
        command = input("""
        1) Type 'start' to start hotspot.
        2) Type 'status' to view hotspot details.
        3) Type 'stop' to stop hotspot.
        4) Type 'exit' to quit.
        : """)
        if command == 'start':
            start_hotspot = subprocess.run("netsh wlan start hostednetwork", shell=True, capture_output=True)
            print(f"\nHostspot {ssid_name} started.")
        elif command == 'status':
            show_status = subprocess.run("netsh wlan show hostednetwork", shell=True, capture_output=True)
            print(show_status.stdout.decode())
        elif command == 'stop':
            stop_hotspot = subprocess.run("netsh wlan stop hostednetwork", shell=True, capture_output=True)
            print(f"\nHotspot {ssid_name} stopped.")
        elif command == 'exit':
            stop_hotspot = subprocess.run("netsh wlan stop hostednetwork", shell=True, capture_output=True)
            print("Exiting.....")
            break
        else:
            print("\nInput not found.")

subprocess.run("title SET HOTSPOT", shell=True, capture_output=True)
try:
    get_details()
    setup_hotspot()
    start_stop_show_hotspot()
except KeyboardInterrupt:
    print("Now exiting...")