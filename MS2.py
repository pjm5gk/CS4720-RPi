import web # link to download on the RPi milestone page
import requests # this needs to be downloaded as well
import json
import socket
import urllib2
import fcntl
import struct
from subprocess import check_output
from operator import itemgetter, attrgetter, methodcaller
import os

urls = (
    '/rpi', 'rpi' # for navigation to http://our ip address/rpi
)


class rpi:


    # def get_ip_address(ifname):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     return socket.inet_ntoa(fcntl.ioctl(
    #         s.fileno(),
    #         0x8915,  # SIOCGIFADDR
    #         struct.pack('256s', ifname[:15])
    #     )[20:24])

    def GET(self):
        return "Hello World!"

    def POST(self):
        ip = check_output(['hostname', '-I'])
        # ip = get_ip_address('wlan0')
        # gw = os.popen("ip -4 route show default").read().split()
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.connect((gw[2], 0))
        # ipaddr = s.getsockname()[0]
        # gateway = gw[2]
        # host = socket.gethostname()
        # print ("IP:", ipaddr, " GW:", gateway, " Host:", host)
        
        lightIDValue = None
        redValue = None
        blueValue = None
        greenValue = None
        intensityValue = None
        propagateValue = None
        leftmostRed = None
        leftmostBlue = None
        leftmostGreen = None
        web.header = {"Content-type": "application/json"}
        data = {
                "lights": [
                {
                    "lightID": lightIDValue,
                    "red": redValue,
                    "blue": blueValue,
                    "green": greenValue,
                    "intensity": intensityValue
                }
                ],  "propagate": propagateValue
        }
        result = requests.post('http://' + ip + '/rpi', data=json.dumps(data), headers=web.header) # I don't know our IP address so it needs to be added here
        sorted(result, key=attrgetter(["lights"]["lightID"])) # sort by lightID, not quite sure if this line will work
        for i in xrange(len(result)): # loop through all lights
            if result[i].lights["lightID"] > 1:
                for x in range(0, i): # loop through all preceding lights and set to black
                    result[i].lights["red"] = 0
                    result[i].lights["blue"] = 0
                    result[i].lights["green"] = 0
            if result[i].propagate is False or result[i].propagate is None:
                for r in result: # loop through all lights and set ones with missing IDs to black
                    if r.lights["lightID"] is None:
                        r.lights["red"] = 0
                        r.lights["blue"] = 0
                        r.lights["green"] = 0
            else: # propagate is true, see Note 4 on RPi milestone 2 instructions
                if i is 0: # if leftmost, set color to propagate to black
                    leftmostRed = 0
                    leftmostBlue = 0
                    leftmostGreen = 0
                else: # if not leftmost, set color to propagate to color of leftmost
                    leftmostRed = result[0].lights["red"]
                    leftmostBlue = result[0].lights["blue"]
                    leftmostGreen = result[0].lights["green"]
                for r in result: # propagate color if lightID is missing
                    if r.lights["lightID"] is None:
                        r.lights["red"] = leftmostRed
                        r.lights["blue"] = leftmostBlue
                        r.lights["green"] = leftmostGreen
            # not quite sure what code actually changes the light colors
            # also not sure if colors should be changed only right here, or after both the lightID > 1 conditional ...
            # and at this point as well (based on propagate truth value)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()