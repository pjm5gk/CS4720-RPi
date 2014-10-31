import web # link to download on the RPi milestone page
import requests # this needs to be downloaded as well
import json
import socket
import urllib2
import fcntl
import struct
from subprocess import check_output
from operator import itemgetter, attrgetter, methodcaller
from bootstrap import *
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

    def __init__(self):
        self.led = LEDStrip(32)
        led.all_off()
        led.fillRGB(255,0,0)
        led.update()
        print "We got a hit"
        requests.post("http://cs4720.cs.virginia.edu/pregistration/?pokemon=Chikorita&ip=" + check_output(['hostname','-I']))


    def GET(self):
        return "Hello World!"

    def POST(self):

        result = urllib2.unquote(web.data())
        result = json.loads(result)

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
        # web.header = {"Content-type": "application/json"}
        # payload = {
        #         "lights": [
        #         {
        #             "lightID": lightIDValue,
        #             "red": redValue,
        #             "blue": blueValue,
        #             "green": greenValue,
        #             "intensity": intensityValue
        #         }
        #         ],  "propagate": propagateValue
        # }
        # result = requests.post('http://' + ip + '/rpi', data=json.dumps(payload), headers=web.header) # I don't know our IP address so it needs to be added here
        # print result

        # print result["lights"]["lightID"]
        # sorted(result, key=attrgetter(["lights"]["lightID"])) # sort by lightID, not quite sure if this line will work
        index = 0
        for i in result["lights"]: # loop through all lights
            index += 1
            if i["lightId"] > 1:
                for x in range(0, index): # loop through all preceding lights and set to black
                    i["red"] = 0
                    i["blue"] = 0
                    i["green"] = 0
            if result["propagate"] is False or result["propagate"] is None:
                for r in result["lights"]: # loop through all lights and set ones with missing IDs to black
                    if r["lightId"] is None:
                        r["red"] = 0
                        r["blue"] = 0
                        r["green"] = 0
            else: # propagate is true, see Note 4 on RPi milestone 2 instructions
                if index is 0: # if leftmost, set color to propagate to black
                    leftmostRed = 0
                    leftmostBlue = 0
                    leftmostGreen = 0
                else: # if not leftmost, set color to propagate to color of leftmost
                    leftmostRed = result["lights"][0]["red"]
                    leftmostBlue = result["lights"][0]["blue"]
                    leftmostGreen = result["lights"][0]["green"]
                for r in result["lights"]: # propagate color if lightID is missing
                    if r["lightId"] is None:
                        r["red"] = leftmostRed
                        r["blue"] = leftmostBlue
                        r["green"] = leftmostGreen
            # not quite sure what code actually changes the light colors
            # also not sure if colors should be changed only right here, or after both the lightID > 1 conditional ...
            # and at this point as well (based on propagate truth value)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()