#!/usr/bin/env python

"""
Authors: Nick Russo & Matthew Rich
Purpose: Demonstrate using SSH via netmiko to configure network devices.
"""

import time
from netmiko import Netmiko
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader

def main():
    """
    Execution starts here.
    """
    # Read the hosts file into the structured data, may raise YAMLError
    with open("hosts_2.yml", "r") as handle:
        host_root = safe_load(handle)

    # Iterate over the list of hosts (list of dicts)
    for host in host_root["host_list"]:
        
        # Load the host-specific interfaces declarative state
        with open(f"interfaces_2.yml", "r") as handle:
            config = safe_load(handle)
        
        # Setup the jinja2 templating environment and render the template
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template(f"config_2.j2")
        new_config = template.render(data=config)
        
        # Create netmiko SSH connection handler to access the device
        conn = Netmiko( 
            host="sandbox-iosxe-latest-1.cisco.com",
            port=22,
            username="developer",
            password="C1sco12345",
            device_type="cisco_ios",
        )

        print(f"Logged into {conn.find_prompt()} successfully")

        '''Send the configuration string to the device. Netmiko 
        takes a list of strings, so use the .split() function.'''
        result = conn.send_config_set(new_config.split("\n"))
        
        '''Netmiko automatically collects the results; you can ignore them
        or process them further'''
        print(result)

        conn.disconnect()

if __name__ == "__main__":
    main()