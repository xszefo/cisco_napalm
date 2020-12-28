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

device.load_merge_candidate(filename='new_loopback.cfg')
print('\nDiff:')
diff = device.compare_config()
print(diff)

try:
	if len(diff) and input('Do you want to commit [yn]: ') == 'y':
		print('\nCommit in progress...')
		device.commit_config()
	else:
		print('\nNo Changes Required Closing...')
		device.discard_config()
finally:
	device.close()
