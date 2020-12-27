#!/usr/bin/env python3

from napalm import get_network_driver
import json

print('Imports - success')

hostname = 'ios-xe-mgmt.cisco.com'
username = 'developer'
password = 'C1sco12345'
port = '8181'

driver = get_network_driver("ios")

device = driver(hostname=hostname,
				username=username,
				password=password,
				optional_args={'port': port})

print(f'Connecting to {hostname}')
device.open()

output = device.get_interfaces()

device.close()

for interface, details in output.items():
	print(interface)
	print(details)
	print(50*"*")


print(json.dumps(output, sort_keys=True, indent=4))

