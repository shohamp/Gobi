import re
import os
from fabric.api import run

_IP_A_PATTERNS = [
    r"^\d+:\s+(?P<device>\w+):\s+<.*?> mtu (?P<mtu>\d+)",
    r"^\s+link/\w+ (?P<ether>[^\s]*)( brd (?P<brd>[^\s]*))?",
    r"^\s+inet (?P<inet>[^\s/]*)(?P<netmask>[^\s]*)( brd (?P<brd>[^\s]*))?"
]


def _get_ifconfig():
    """
    This function was mostly copied from python-ifcfg package:
    https://github.com/ftao/python-ifcfg/blob/master/ifcfg/parser.py
    """
    interfaces = {}
    all_keys = []
    cur = None

    output = run("ip a")
    for line in output.split(os.linesep):
        for pattern in _IP_A_PATTERNS:
            m = re.match(pattern, line)
            if m:
                groupdict = m.groupdict()
                # Special treatment to trigger which interface we're
                # setting for if 'device' is in the line. Presumably the
                # device of the interface is within the first line of the
                # device block.
                if 'device' in groupdict:
                    cur = groupdict['device']
                    if not cur in interfaces:
                        interfaces[cur] = {}

                for key in groupdict:
                    if key not in all_keys:
                        all_keys.append(key)
                    if key not in interfaces[cur]:
                        interfaces[cur][key] = groupdict[key]

    # standardize
    for key in all_keys:
        for device, device_dict in interfaces.items():
            if key not in device_dict:
                interfaces[device][key] = None
            if type(device_dict[key]) == str:
                interfaces[device][key] = device_dict[key].lower()

    return interfaces


def get_interfaces():
    interfaces = _get_ifconfig()
    return interfaces.keys()


def get_ip(iface_name):
    interfaces = _get_ifconfig()
    return interfaces[iface_name]["inet"]
