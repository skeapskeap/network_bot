# https://habr.com/ru/post/333614/
# https://habr.com/ru/post/340050/

from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget
from pysnmp.hlapi import ContextData, ObjectType, ObjectIdentity
from settings import COMMUNITY, SNMP_PORT, SWITCH_USERNAME, SWITCH_PASSWORD
import socket
from time import sleep
import telnetlib


PORT_STATE = '1.3.6.1.2.1.2.2.1.8.'       # 1=up, 2=down
PORT_DUPLEX = '.1.3.6.1.2.1.10.7.2.1.19.'  # 3=full, 2=half
PORT_SPEED = '.1.3.6.1.2.1.2.2.1.5.'       # /1000000
RX_BYTES = '.1.3.6.1.2.1.31.1.1.1.6.'  # http://xcme.blogspot.com/2014/10/oid-snmp.html
TX_BYTES = '.1.3.6.1.2.1.31.1.1.1.10.'
ALIG_ERR = '.1.3.6.1.2.1.10.7.2.1.2.'  # dot3StatsAlignmentErrors
FCS_ERR = '.1.3.6.1.2.1.10.7.2.1.3.'  # dot3StatsFCSErrors
# CRC = alig + fcs
MODEL_NAME = '.1.3.6.1.2.1.1.1.0'
# snmpwalk -v 2c -c <community> <IP> 1.3.6.1.2.1.17.7.1.2.2.1.2.1850 маки по влану
# SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.1850.244.140.235.232.146.251 = INTEGER: 10 - это 10 порт
# snmpwalk -v 2c -c <community> <IP> 1.3.6.1.2.1.17.7.1.4.5.1.1.9 - port_vlanid, возвращает нетегированный влан на порту
# vlan on port http://xcme.blogspot.com/2014/10/vlan-snmp.html
# OID = port_status + '1'


def snmp_getcmd(community, ip, port, OID):
    return getCmd(SnmpEngine(),
                  CommunityData(COMMUNITY),
                  UdpTransportTarget((ip, port), timeout=0.5, retries=0),
                  ContextData(),
                  ObjectType(ObjectIdentity(OID)))


def snmp_get(*args):  # args = [community, ip, port, OID]
    errorIndication, errorStatus, errorIndex, varBinds = next(snmp_getcmd(*args))
    if errorIndication:
        return False
    for name, val in varBinds:
        return val.prettyPrint()


def snmp_reachable(ip):
    if snmp_get(COMMUNITY, ip, SNMP_PORT, MODEL_NAME):
        return True
    else:
        return False


def choose_cmd(ip, port, cmd):
    if cmd == 'sh_port':
        return sh_port(ip, port)
    elif cmd == 'sh_mac':
        return sh_mac(ip, port)
    elif cmd == 'cab_diag':
        return cab_diag(ip, port)
    elif cmd == 'traffic':
        return port_stats(ip, port)
    else:
        return 'не понял, что делать?'


def sh_port(ip, port):
    if not snmp_reachable(ip):
        return 'host timed out'
    if snmp_get(COMMUNITY, ip, SNMP_PORT, (PORT_STATE + port)) == '2':
        status = f'port {port}: state down'
    else:
        if snmp_get(COMMUNITY, ip, SNMP_PORT, (PORT_DUPLEX + port)) == '3':
            duplex = 'full'
        else:
            duplex = 'half'
        speed = int(int(snmp_get(COMMUNITY, ip, SNMP_PORT, (PORT_SPEED + port)))/1000000)
        status = f'port {port}: state up, {speed} {duplex}'
    return status


def get_port_stats(ip, port):
    if not snmp_reachable(ip):
        return 'host timed out'
    rx_bytes = int(snmp_get(COMMUNITY, ip, SNMP_PORT, (RX_BYTES + port)))
    tx_bytes = int(snmp_get(COMMUNITY, ip, SNMP_PORT, (TX_BYTES + port)))
    alig_err = int(snmp_get(COMMUNITY, ip, SNMP_PORT, (ALIG_ERR + port)))
    fcs_err = int(snmp_get(COMMUNITY, ip, SNMP_PORT, (FCS_ERR + port)))
    crc_err = alig_err + fcs_err
    return rx_bytes, tx_bytes, crc_err


def telnet(func):
    def wrapper(ip, port):
        command = func(ip, port)
        username = f'{SWITCH_USERNAME}\n'.encode('ascii')
        password = f'{SWITCH_PASSWORD}\n'.encode('ascii')

        try:
            telnet = telnetlib.Telnet(ip, timeout=1)
        except socket.timeout:
            return 'host unreachable'
        sleep(0.5)
        telnet.read_very_eager()
        telnet.write(username)
        sleep(0.5)
        telnet.write(password)
        sleep(0.5)
        telnet.write(command.encode('utf-8'))

        skip_current_string = telnet.read_very_eager()
        output = telnet.read_until(b'#', timeout=5)
        output = output.decode('utf-8').split('\n')
        output = output[3:15]
        output = '\n'.join(output)
        return output
    return wrapper


@telnet
def sh_mac(ip, port):
    string = f'show fdb port {port}\n'
    return string


@telnet
def cab_diag(ip, port):
    string = f'cable_diag ports {port}\n'
    return string
