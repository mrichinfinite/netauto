#!/usr/bin/env python

"""
Authors: Nick Russo & Matthew Rich
Purpose: Demonstrate SCP file transfer using Netmiko.
"""

import sys
from netmiko import Netmiko, file_transfer
from yaml import safe_load

def main(argv):
    '''
    Execution starts here.
    '''

    # Read the hosts file into structured data, my raise YAMLError
    with open("hosts_2.yml", "r") as handle:
        host_root = safe_load(handle)

    # Iterate over the list of hosts (list of dicts)
    for host in host_root["host_list"]:

        # Create netmiko SSH connection handler to access the device
        conn = Netmiko( 
            host="sandbox-iosxe-latest-1.cisco.com",
            port=22,
            username="developer",
            password="C1sco12345",
            device_type="cisco_ios",)

        '''Upload the file specified. The dict.get(key) function tries to
        retrieve the value at the specified key and returns None if it does
        not exist. Very useful in network automation!'''
        print(f'Uploading {argv[1]}')
        result = file_transfer(
            conn,
            source_file=argv[1],
            dest_file=argv[1],)

        # Print the resulting details
        print(f'Details: {result}\n')
        
        conn.disconnect()

if __name__ == "__main__":
    main(sys.argv)