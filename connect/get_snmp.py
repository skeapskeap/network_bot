# https://habr.com/ru/post/333614/
# https://habr.com/ru/post/340050/

from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget
from pysnmp.hlapi import ContextData, ObjectType, ObjectIdentity
from settings import SNMP_PORT, SWITCH_USERNAME, SWITCH_PASSWORD
from settings import SW_COMMUNITY, UPS_COMMUNITY
from .snmp_oid import PORT_STATE, PORT_DUPLEX, PORT_SPEED, MODEL_NAME
from .snmp_oid import RX_BYTES, TX_BYTES, ALIG_ERR, FCS_ERR
from .snmp_oid import UPS_MODEL, LOCATION
from .snmp_oid import INPUT_VOLTAGE, BATTERY_CHARGE, RUNTIME
from time import sleep
import socket
import telnetlib


def snmp_getcmd(community, ip, port, OID):
    return getCmd(SnmpEngine(),
                  CommunityData(community),
                  UdpTransportTarget((ip, port), timeout=0.5, retries=0),
                  ContextData(),
                  ObjectType(ObjectIdentity(OID)))


def snmp_get(*args):  # args = [community, ip, port, OID]
    errorIndication, errorStatus, errorIndex, varBinds = next(snmp_getcmd(*args))
    if errorIndication:
        return False
    for name, val in varBinds:
        return val.prettyPrint()


def snmp_reachable(ip, community):
    switch_model = snmp_get(community, ip, SNMP_PORT, MODEL_NAME)
    if switch_model:
        return switch_model
    else:
        return False


def choose_cmd(ip, port, cmd):
    if cmd == 'sh_port':
        return sh_port(ip, port)
    elif cmd == 'sh_mac':
        return sh_mac(ip, port)
    elif cmd == 'cab_diag':
        return cab_diag(ip, port)
    else:
        return 'Unknown command'


def sh_port(ip, port):
    if not snmp_reachable(ip, SW_COMMUNITY):
        return 'host timed out'
    args = SW_COMMUNITY, ip, SNMP_PORT
    if snmp_get(*args, (PORT_STATE + port)) == '2':
        status = f'port {port}: state down'
        return status
    else:
        if snmp_get(*args, (PORT_DUPLEX + port)) == '3':
            duplex = 'full'
        else:
            duplex = 'half'
        try:
            speed = int(int(snmp_get(*args, (PORT_SPEED + port)))/1000000)
            status = f'port {port}: state up, {speed} {duplex}'
            return status
        except ValueError:
            return False


def get_port_stats(ip, port):
    if not snmp_reachable(ip, SW_COMMUNITY):
        return False
    args = SW_COMMUNITY, ip, SNMP_PORT
    rx_bytes = int(snmp_get(*args, (RX_BYTES + port)))
    tx_bytes = int(snmp_get(*args, (TX_BYTES + port)))
    alig_err = int(snmp_get(*args, (ALIG_ERR + port)))
    fcs_err = int(snmp_get(*args, (FCS_ERR + port)))
    crc_err = alig_err + fcs_err
    return rx_bytes, tx_bytes, crc_err


def ups_info(ip):
    if not snmp_reachable(ip, UPS_COMMUNITY):
        return False
    args = UPS_COMMUNITY, ip, SNMP_PORT
    model = snmp_get(*args, UPS_MODEL)
    loc = snmp_get(*args, LOCATION)
    voltage = int(snmp_get(*args, INPUT_VOLTAGE))
    charge = int(snmp_get(*args, BATTERY_CHARGE))
    runtime = int(snmp_get(*args, RUNTIME))
    reply = {'model': model,
             'location': loc,
             'voltage': voltage,
             'charge': charge,
             'runtime': runtime}
    return reply


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
