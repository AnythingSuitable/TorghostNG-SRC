#
# Follow on GitHub : https://github.com/AnythingSuitable
#

from Configs import *
import fcntl
from json import loads
from os import geteuid, system, name, path
import socket
import struct
from subprocess import getoutput
import time


GUI_VERSION = 'GUI Version : 0.1'


def Get_Interface_List():

    Interface_List = []
    Interface_List_source = socket.if_nameindex()
    for _ in Interface_List_source:
        Interface_List.append(_[1])
    return Interface_List

def Get_MAC_Address(ifname):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(sock.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])

def Change_MAC_Address(interface):

    Interface_Down = getoutput(f'ifconfig {interface} down')

    if "ERROR" in Interface_Down:
        print("Someone's getting WRONG HERE........")
    else:
        system(f'macchanger -r {interface}')
        system(f'ifconfig {interface} up')
        print('DONE')

def Check_Update():

    Current_Version = float(GUI_VERSION.split(':')[1].strip())
    try:
        
        Latest_Version = getoutput('curl -s --max-time 60 https://raw.githubusercontent.com/AnythingSuitable/raw/main/Version.txt')
        Latest_Version = float(Latest_Version)

        if Current_Version == Latest_Version:
            Update_Available = False

        elif Current_Version < Latest_Version:
            Update_Available = True        

    except Exception as e:
        Current_Version, Latest_Version, Update_Available = float(0.0), float(0.0), False

    return Current_Version, Latest_Version, Update_Available


def DNS_Fix():

    if path.isfile(resolv_b) == True:
        pass
    else:
        #Take Backup of Original
        with open(resolv, 'r') as back_file:
            file_ = back_file.read()
            back_file.close()

        with open(resolv_b, 'wb') as file:
            file.write(file_.encode())
            file.close()

    with open(resolv, 'w') as Resolv_File:
        Resolv_File.write(FIX_DNS)
        Resolv_File.close()

def DNS_Restore():

    with open(resolv_b, 'r') as back_file:
            file_ = back_file.read()
            back_file.close()
    with open(resolv, 'wb') as file:
            file.write(file_.encode())
            file.close()

def check_tor(status):
    try:

        print("language.checking_tor")

        tor_status = loads(getoutput("curl -s --max-time 60 https://check.torproject.org/api/ip"))
        print('language.done')
        
        if tor_status['IsTor'] == False:
            if status == "failed":
                print('language.tor_failed')
                stop_connecting()
                
            elif status == "stopped":
                print('language.tor_disconnected')
            
        else:

            if 'LISTEN' in getoutput('netstat -atnp | grep privoxy'):
                print("language.tor_success.format('Privoxy')")
                
            else:
                print("language.tor_success.format('')")

        check_ip()

    except KeyboardInterrupt:
        print()
        exit()

def check_ip():
    try:

        print("language.checking_ip")

        ipv4_address = getoutput('curl -s --max-time 60 https://api.ipify.org')
        ipv6_address = getoutput('curl -s --max-time 60 https://api6.ipify.org')
        print("language.done")
        
        print("language.your_ip.format('IPv4') + color.BOLD + ipv4_address + color.END")
        
        if (ipv6_address != ipv4_address) and len(ipv6_address) > 0:
            print("language.your_ip.format('IPv6') + color.BOLD + ipv6_address + color.END")

    except KeyboardInterrupt:
        print()
        exit()

def Connect_Tor(id=None,privoxy=None):
    try:

        #print(icon.process + ' ' + language.start_help)
        
        # Disable IPv6
        if DISABLE_IPv6 == open(Sysctl).read():
            print('language.ipv6_already_disabled')
            
        else:
            print('language.disable_ipv6_info')

            system('sudo cp {0} {0}.backup'.format(Sysctl))
            print('language.disabling_ipv6')
            
            with open(Sysctl, mode='w') as file_sysctl:
                file_sysctl.write(DISABLE_IPv6)
                file_sysctl.close()

            print('language.done')

        getoutput('sudo sysctl -p')

        # Configure Torrc
        #check_dependencies('tor')

        if id != None: # Check for exit node
            torrconfig = TorrcConfig_exitnode %(id)
            print('language.id_tip')
        else:
            torrconfig = TorrcConfig


        if (path.isfile(Torrc)) and (torrconfig == open(Torrc).read()):
            print('TorghostNG Torrc')
            
        else:
            print("language.configuring.format('TorghostNG Torrc')")

            with open(Torrc, mode='w') as file_torrc:
                file_torrc.write(torrconfig)
                file_torrc.close()

            print('language.done')

        # Configure DNS resolv.conf
        if privoxy == None:
            system('systemctl stop privoxy')
            if resolvConfig == open(resolv).read():
                print("language.already_configured.format('DNS resolv.conf')")
                
            else:
                system("cp {0} {0}.backup".format(resolv))
                
                with open(resolv, mode='w') as resolv_file:
                    print("language.configuring.format('DNS resolv.conf')")
                    resolv_file.write(resolvConfig)
                    resolv_file.close()
                    print('language.done')

        # Stop tor service
        #check_dependencies('tor')

        print("language.stopping_tor")
        system('systemctl stop tor')
        system('fuser -k 9051/tcp > /dev/null 2>&1')

        print("language.done")

        # Configure and start Privoxy
        if privoxy == True:
            #check_dependencies('privoxy')

            system(set_proxy)
            
            if privoxy_conf == open(Privoxy).read():
                print("language.already_configured.format('Privoxy')")
                
            else:
                system('cp {0} {0}.backup'.format(Privoxy))
                
                with open(Privoxy, mode='w') as privoxy_file:
                    print("language.configuring.format('Privoxy')")
                    privoxy_file.write(privoxy_conf)
                    privoxy_file.close()
                    print("language.done")
                    
            system('systemctl start privoxy')

        # Start new tor service
        #check_dependencies ('tor')

        print("language.starting_tor")
        system('sudo -u {0} tor -f {1} > /dev/null'.format(TOR_USER, Torrc))
        print("language.done")

        # Show some info
        print("language.iptables_info")
        print("language.block_bittorrent")

        # Configure iptables
        print("language.setting_iptables")
        system(iptables_rules)

        print('language.done')
        
        #check_tor('failed') # Check tor connection

        print("language.dns_tip") # Show some info

    except KeyboardInterrupt:
        print()
        exit()
    except FileNotFoundError:
        system('touch {}'.format(Sysctl))
        start_connecting(id,privoxy)

def Disconnect_Tor():
    try:
        

        if 'LISTEN' in getoutput('netstat -atnp | grep privoxy'):
            print("language.restoring_configuration.format('Privoxy')")
            
            if path.isfile(Privoxy + '.backup')  == True:
                system('mv {0}.backup {0}'.format(Privoxy))
            
            system('systemctl stop privoxy')
            system(rm_proxy)

            print("language.done")

        # Restore DNS resolv.conf configuration
        if path.isfile(resolv + '.backup') == True:
            print("language.restoring_configuration.format('DNS resolv.conf')")

            system('mv {0}.backup {0}'.format(resolv))

            print("language.done")

        # Restore IPv6 configuration
        if path.isfile(Sysctl + '.backup') == True:
            print("language.restoring_configuration.format('IPv6')")

            system('mv {0}.backup {0}'.format(Sysctl))
            system('sudo sysctl -p')

            print("language.done")

        # Reset iptables configuration
        print("language.flushing_iptables")
        system(IpFlush)
        system('fuser -k 9051/tcp > /dev/null 2>&1')

        print("done")

        # Restart NetworkManager
        print("language.restarting_network")
        system('systemctl restart --now NetworkManager')
        print("language.done")
        
        print("language.dns_tip")

    except KeyboardInterrupt:
        print()
        exit()


def Renew_Tor_Circuit():
    try:

        print("language.changing_tor_circuit")

        tor_status = loads(getoutput("curl -s --max-time 60 https://check.torproject.org/api/ip"))
        
        if tor_status['IsTor'] == True:
            system('pidof tor | xargs sudo kill -HUP')

            print("language.done")
            #check_tor('stopped')
            
        else:
            print('NULL')
            
    except KeyboardInterrupt:
        print()
        exit()

def Check_Tor():
    try:
        tor_status = loads(getoutput("curl -s --max-time 60 https://check.torproject.org/api/ip"))

            
        if tor_status['IsTor'] == True:
            connected = "CONNECTED"
            
        else:
            connected = "DISCONNECTED"

    except Exception as e:
        connected = "ERROR"

    return connected