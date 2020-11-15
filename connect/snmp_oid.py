PORT_STATE = '1.3.6.1.2.1.2.2.1.8.'       # 1=up, 2=down
PORT_DUPLEX = '.1.3.6.1.2.1.10.7.2.1.19.'  # 3=full, 2=half
PORT_SPEED = '.1.3.6.1.2.1.2.2.1.5.'       # /1000000
RX_BYTES = '.1.3.6.1.2.1.31.1.1.1.6.'  # http://xcme.blogspot.com/2014/10/oid-snmp.html
TX_BYTES = '.1.3.6.1.2.1.31.1.1.1.10.'
ALIG_ERR = '.1.3.6.1.2.1.10.7.2.1.2.'  # dot3StatsAlignmentErrors
FCS_ERR = '.1.3.6.1.2.1.10.7.2.1.3.'  # dot3StatsFCSErrors
# CRC = alig + fcs
MODEL_NAME = '.1.3.6.1.2.1.1.1.0'
UPS_MODEL = '.1.3.6.1.4.1.318.1.1.1.1.1.1.0'
LOCATION = '.1.3.6.1.2.1.1.6.0'
POWER_STATE = '.1.3.6.1.4.1.318.1.1.1.4.1.1.0'
BATTERY_CHARGE = '.1.3.6.1.4.1.318.1.1.1.2.2.1.0'
RUNTIME = '.1.3.6.1.4.1.318.1.1.1.2.2.3.0'
INPUT_VOLTAGE = '.1.3.6.1.4.1.318.1.1.1.3.2.1.0'
# snmpwalk -v 2c -c <community> <IP> 1.3.6.1.2.1.17.7.1.2.2.1.2.1850 маки по влану
# SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.1850.244.140.235.232.146.251 = INTEGER: 10 - это 10 порт
# snmpwalk -v 2c -c <community> <IP> 1.3.6.1.2.1.17.7.1.4.5.1.1.9 - port_vlanid, возвращает нетегированный влан на порту
# vlan on port http://xcme.blogspot.com/2014/10/vlan-snmp.html
# OID = port_status + '1'
