#!/usr/bin/env python3

from napalm import get_network_driver
import json
from jinja2 import Environment, FileSystemLoader
import yaml

print('Imports - success')

def create_template(template, data):
	config_data = yaml.load(open(data))

	#This line uses the current directory and loads the jinja2 template
	env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
	template = env.get_template(template)

	#Return the template with data
	return template.render(config_data)

def configure_device(template_config):
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
	try:
		device.open()
		device.load_merge_candidate(config=template_config)

		print('\nDiff:')
		diff = device.compare_config()
		print(diff)

		if len(diff) and input('Do you want to commit [yn]: ') == 'y':
			print('\nCommit in progress...')
			device.commit_config()
			return 'Commited'
		else:
			print('\nNo Changes Required Closing...')
			device.discard_config()
			return 'Discarded'
	finally:
		device.close()
		print(f'Closed session to {hostname}')


config = create_template('loopback_template.j2', 'loopbacks_info.yml')
print(configure_device(config))
