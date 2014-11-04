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
        # led.fillRGB(255,0,0)
        led.update()
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
        
        # lightIDValue = None
        # redValue = None
        # blueValue = None
        # greenValue = None
        # intensityValue = None
        # propagateValue = None
        # leftmostRed = None
        # leftmostBlue = None
        # leftmostGreen = None

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
        lightsData = result["lights"]
        print lightsData
        # sorted(lightsData, key=attrgetter([u'lightId'])) # sort by lightID, not quite sure if this line will work
        # print lightsData

        print "We got a hit"
        propagate = bool(result["propagate"])
        led.all_off()
        index = 0
        previousColored = 0
        previousRed = 0
        previousGreen = 0
        previousBlue = 0
        previousIntensity = 0
        firstLightID = 0;
        firstLightID = lightsData[0]["lightID"];
        for i in lightsData: # first loop: set all colors without propagate
            if i["lightID"] < firstLightID:
                i["red"] = 0
                i["blue"] = 0
                i["green"] = 0
                i["intensity"] = 0


        for i in lightsData: # second loop: set colors based on propagate, set also on led strip
            if result["propagate"] is True:
                print i["lightID"];
                print i;
                if(i["lightID"] == "" or index == 0):
                    led.set(index, Color(0, 0, 0, 0))
                else:
                    led.set(index, Color(lightsData[0]["red"],lightsData[0]["green"],lightsData[0]["blue"],lightsData[0]["intensity"]))

            # if i["lightId"] > 1:
            #     # for x in range(0, index): # loop through all preceding lights and set to black
            #     #     i["red"] = 0
            #     #     i["blue"] = 0
            #     #     i["green"] = 0
            #     led.fill( Color(0, 0, 0, 1), previousColored,  index)
            #     led.set( i["lightID"], Color(i["red"], i["green"], i["blue"], i["intensity"]), )
            #     previousColored = index.copy()
            '''
            print i["lightId"]
            if result["propagate"] is True or result["propagate"] is "True": #propagate is true, see Note 4 on RPi milestone 2 instructions
                print i
                while previousColored + 1 < i["lightId"]:
                    led.set(previousColored, Color(previousRed,previousGreen,previousBlue,previousIntensity))
                    previousColored += 1
                previousRed = i["red"]
                previousGreen = i["green"]
                previousBlue = i["blue"]
                previousIntensity = i["intensity"]
                led.set(i["lightId"], Color(previousRed,previousGreen,previousBlue,previousIntensity))
                previousColored = i["lightId"]
                '''
                # if index is 0: # if leftmost, set color to propagate to black
                #     leftmostRed = 0
                #     leftmostBlue = 0
                #     leftmostGreen = 0
                # else: # if not leftmost, set color to propagate to color of leftmost
                #     leftmostRed = result["lights"][0]["red"]
                #     leftmostBlue = result["lights"][0]["blue"]
                #     leftmostGreen = result["lights"][0]["green"]
                # for r in result["lights"]: # propagate color if lightID is missing
                #     if r["lightId"] is None:
                #         r["red"] = leftmostRed
                #         r["blue"] = leftmostBlue
                #         r["green"] = leftmostGreen
            else:
                for i in lightsData:
                    if(i["lightID"] == ""):
                        led.set(index, Color(0, 0, 0, 0))
                    else:
                        led.set(index, Color(i["red"],i["green"],i["blue"],i["intensity"]))
            index += 1;
                # for r in result["lights"]: # loop through all lights and set ones with missing IDs to black
                #     if r["lightId"] is None:
                #         r["red"] = 0
                #         r["blue"] = 0
                #         r["green"] = 0

        #if result["propagate"] is "True":
         #   while previousColored < led.lastIndex:
          #      print previousColored
           #     led.set(previousColored, Color(previousRed,previousGreen,previousBlue,previousIntensity))
        led.update()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()