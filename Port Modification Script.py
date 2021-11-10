from netmiko import ConnectHandler

import sys
import paramiko
fd = open(r'C:\Users\Chris\\PythonOutput.txt','w') 
sys.stdout = fd 
platform = 'cisco_ios'
username = 'admin'
password = 'admin'

ip_add_file = open(r'C:\Users\Chris\\IPAddressList.txt','r') 

for host in ip_add_file:
    device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
    output = device.send_command('enable')
    showIP = device.send_command("show ip int br | inc 172.16")
    
    #collection of interfaces for modification
    interfaces = [];
    for line in showIP.splitlines():
        print ("\n############################")
        print ("Host " +host)
        print(line)
        if line[0:2] == 'Gi' or 'Gi':
            interfaces.append(line[0:16].strip())
            
    #showing interfaces collected

    print("\nFound these interfaces:")
    print(interfaces)
    
    #creating loop for interface change
    for intf in interfaces:
        output = device.send_command("sh int "+intf+" status");
        if "trunk" in output:
            print("\n" +intf)
            print("Skipping, port is a trunk.")
        else:
            print("\n" +intf)
            print("Modifying now ....Please Wait ")
            
            # issue commands
            config_commands = [
            'int '+intf,
            'desc PythonGuruFinal',
            'no shut']
            device.send_config_set(config_commands)
            print("Done!")
            
fd.close()
