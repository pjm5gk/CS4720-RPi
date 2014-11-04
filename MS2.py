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
        led.all_off()
        # led.fillRGB(255,0,0)
        led.update()
        requests.post("http://cs4720.cs.virginia.edu/pregistration/?pokemon=Chikorita&ip=" + check_output(['hostname','-I']))


    def GET(self):
        return "Hello World!"

    def POST(self):

        result = urllib2.unquote(web.data())
        result = json.loads(result)

        ip = check_output(['hostname', '-I'])
        lightsData = result["lights"]
        print lightsData
        
        print "We got a hit"
        propagate = bool(result["propagate"])
        led.all_off()
        index = 0
        previousColored = 0
        previousRed = 0
        previousGreen = 0
        previousBlue = 0
        previousIntensity = 0
        for i in lightsData: # loop through all lights
            print i["lightId"]
            if result["propagate"] is True or result["propagate"] is "True": #propagate is true, see Note 4 on RPi milestone 2 instructions
                print i
                while previousColored + 1 < i["lightId"]:
                    led.set(previousColored, Color(previousRed,previousGreen,previousBlue,previousIntensity))
                    print previousColored,":",previousRed,",",previousGreen,",",previousBlue,",",previousIntensity
                    previousColored += 1
                previousRed = i["red"]
                previousGreen = i["green"]
                previousBlue = i["blue"]
                previousIntensity = i["intensity"]
                led.set(i["lightId"], Color(previousRed,previousGreen,previousBlue,previousIntensity))
                previousColored = i["lightId"]
                print previousColored,":",previousRed,",",previousGreen,",",previousBlue,",",previousIntensity
            else:
                led.set(i["lightId"], Color(i["red"],i["green"],i["blue"],i["intensity"]))
        if result["propagate"] is "True":
            while previousColored < led.lastIndex:
                print previousColored
                led.set(previousColored, Color(previousRed,previousGreen,previousBlue,previousIntensity))
        led.update()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()