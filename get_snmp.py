# https://habr.com/ru/post/333614/
# https://habr.com/ru/post/340050/

from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget
from pysnmp.hlapi import ContextData, ObjectType, ObjectIdentity
from settings import COMMUNITY, SNMP_PORT, SWITCH_USERNAME, SWITCH_PASSWORD
from time import sleep
import telnetlib


port_state = '1.3.6.1.2.1.2.2.1.8.'       # 1=up, 2=down
port_duplex = '.1.3.6.1.2.1.10.7.2.1.19.'  # 3=full, 2=half
port_speed = '.1.3.6.1.2.1.2.2.1.5.'       # /1000000
# model_name = '.1.3.6.1.2.1.1.1.0'
# snmpwalk -v 2c -c <community> <IP> 1.3.6.1.2.1.17.7.1.2.2.1.2.1850 маки по влану
# SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.1850.244.140.235.232.146.251 = INTEGER: 10 - это 10 порт
# snmpwalk -v 2c -c <community> <IP> 1.3.6.1.2.1.17.7.1.4.5.1.1.9 - port_vlanid, возвращает нетегированный влан на порту
# vlan on port http://xcme.blogspot.com/2014/10/vlan-snmp.html
# OID = port_status + '1'


def snmp_getcmd(community, ip, port, OID):
    return getCmd(SnmpEngine(),
                  CommunityData(COMMUNITY),
                  UdpTransportTarget((ip, port)),
                  ContextData(),
                  ObjectType(ObjectIdentity(OID)))


def snmp_get(*args):  # args = [community, ip, port, OID]
    errorIndication, errorStatus, errorIndex, varBinds = next(snmp_getcmd(*args))
    print(varBinds)
    for name, val in varBinds:
        return val.prettyPrint()


def choose_cmd(ip, port, cmd):
    if cmd == 'sh_port':
        return sh_port(ip, port, cmd)
    elif cmd == 'sh_mac':
        return sh_mac(ip, port)
    else:
        return 'не понял, что делать?'


def sh_port(ip, port, cmd):
    if snmp_get(COMMUNITY, ip, SNMP_PORT, (port_state + port)) == '2':
        status = f'port {port}: state down'
    else:
        if snmp_get(COMMUNITY, ip, SNMP_PORT, (port_duplex + port)) == '3':
            duplex = 'full'
        else:
            duplex = 'half'
        speed = int(int(snmp_get(COMMUNITY, ip, SNMP_PORT, (port_speed + port)))/1000000)
        status = f'port {port}: state up, {speed} {duplex}'
    return status


def sh_mac(ip, port):
    string = f'show fdb port {port}\n'
    username = f'{SWITCH_USERNAME}\n'.encode('ascii')
    password = f'{SWITCH_PASSWORD}\n'.encode('ascii')

    telnet = telnetlib.Telnet(ip)
    sleep(0.5)
    telnet.read_very_eager()
    telnet.write(username)
    sleep(0.5)
    telnet.write(password)
    sleep(0.5)
    telnet.write(string.encode('utf-8'))
    sleep(0.5)

    output = telnet.read_very_eager()
    output = output.decode('utf-8').split('\n')
    output = output[6:17]
    output = '\n'.join(output)
    return output
