#!/usr/bin/env python3

import subprocess
import sys
import re

def download_package(package_name):
	command = f"apt-rdepends {package_name} | grep -v '^ '"
	download_command = f"sudo apt-get download $({command})"
	print(f"Running command: {download_command}")
	result = subprocess.run(download_command, shell=True, stderr=subprocess.PIPE, text=True)
	
	print(result)
	# error check
	# ([\w.\-+]+) matches a single word where -, +, and . are not considered word boundaries as they normally would be
	errors = [error for error in re.findall(r"E: Can't select candidate version from package ([\w.\-+]+) as it has no candidate|E: Can't find a source to download version '[^']+' of '([\w.\-+]+):", result.stderr) if error]
	errors = [item for sublist in errors for item in sublist if item] # wow 
	if not errors:
		print("Download successful!")
		return
		
	# exclude errored pkgs
	for error_package in errors:
		print(f"Excluding package: {error_package}")
		command += f" | grep -vP '(^|\\s){re.escape(error_package)}(\\s|$)'"
		
	new_download_command = f"sudo apt-get download $({command})"
	print(f"New command to run: {new_download_command}")
	
if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python3 rdep.py <package name>")
		sys.exit(1)
		
	package_name = sys.argv[1]
	download_package(package_name)
