from netmiko import ConnectHandler

import re
import sys
import paramiko
fd = open(r'C:\Users\"insert User here"\\PythonOutput.txt','w') 
sys.stdout = fd 
platform = 'cisco_ios'
username = 'admin'
password = 'admin'

##Make this the directory of the IPlist.txt
ip_add_file = open(r'C:\Users\"insert User here"\\IPAddressList.txt','r') 

for host in ip_add_file:
    device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
    output = device.send_command('enable')
    showIP = device.send_command("show int status | in 174 | 176")
    
    #collection of interfaces for modification
    interfaces = [];
    for line in showIP.splitlines():
        print ("\n############################")
        print ("Host " +host)
        xx = line
        r1 = re.match(r"^Fa.*\/[0-9]|Gi.*\/[0-9]|Gigabitethernet.*\/[0-9]", str(xx))
        print(xx)
        print('Matched Interface ' +r1.group())
        if "174" or "176" in line: 
            interfaces.append(r1.group())
         
            
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
            
            # issue commands to te interface that has been matched
            config_commands = [
            'int '+intf,
            'switchport access vlan 178',
            'no shut']
            device.send_config_set(config_commands)
            print("Done!")
            
fd.close()
