#!/usr/bin/env python

"""
Authors: Nick Russo & Matthew Rich
Purpose: Demonstrate using SSH via paramiko to get information from
the network and write it to a file for future reference.
"""

import time
import paramiko


def send_cmd(conn, command):
    """
    Given an open connection and a command, issue the command and wait
    1 second for the command to be processed.
    """
    conn.send(command + "\n")
    time.sleep(1.0)


def get_output(conn):
    """
    Given an open connection, read all the data from the buffer and
    decode the byte string as UTF-8.
    """
    return conn.recv(65535).decode("utf-8")


def main():
    """
    Execution starts here.
    """

    # Define host inventory in line.
    # sandbox-iosxe-latest-1.cisco.com is a Cisco IOS-XE CSR1000v
    host_dict = {
        "sandbox-iosxe-latest-1.cisco.com": "show running-config",
    }

    # For each host in the inventory dict, extract key and value
    for hostname, cmd in host_dict.items():
        # Paramiko can be SSH client or server; use client here
        conn_params = paramiko.SSHClient()

        # We don't need paramiko to refuse connections due to missing SSH keys
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(
            hostname=hostname,
            port=22,
            username="developer",
            password="C1sco12345",
            look_for_keys=False,
            allow_agent=False,
        )

        # Get an interactive shell and wait a bit for the prompt to appear
        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"Logged into {get_output(conn).strip()} successfully")

        # Iterate over the list of commands, sending each one in series
        # The final command in the list is the OS-specific VRF "show" command
        commands = [
            "terminal length 0",
            "show version | include Software,",
            cmd,
        ]
        concat_output = ""
        for command in commands:
            # Send command, get output, and append to output string
            send_cmd(conn, command)
            concat_output += get_output(conn)

        # Close session when we are done
        conn.close()

        # Open a new text file per host and write the output
        print(f"Writing {hostname} facts to file")
        with open(f"{hostname}_facts.txt", "w") as handle:
            handle.write(concat_output)


if __name__ == "__main__":
    main()