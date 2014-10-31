import urllib2
import re
import commands

found_ips = []
ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', commands.getoutput("/sbin/ifconfig"))
for ip in ips:
	if ip.startswith("255") or ip.startswith("127") or ip.endswith("255"):
		continue
	found_ips.append(ip)
urllib2.urlopen("http://cs4720.cs.virginia.edu/ipregistration/?pokemon=Chikorita&ip=" + found_ips[0])