import subprocess

WPA_FILE_TEMPLATE = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={{
            ssid=\"beepx\"
            psk=\"yellow123\"
            key_mgmt=WPA-PSK
    }}

network={{
            ssid=\"{name}\"
            psk=\"{password}\"
            key_mgmt=WPA-PSK
    }}
"""


def isInternetConnected():
    try:
        urllib2.urlopen('https://www.google.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

def ipInfoUpdate(socketIO):
    socketIO.emit('ip_information',
                  {'ip': subprocess.check_output(["hostname", "-I"]), 'robot_id': robotID})


def configWifiLogin(secretKey):

    url = 'https://%s/get_wifi_login/%s' % (server, secretKey)
    try:
        print "GET", url
        response = urllib2.urlopen(url).read()
        responseJson = json.loads(response)
        print "get wifi login response:", response

        with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'r') as originalWPAFile:
            originalWPAText = originalWPAFile.read()

        wpaText = WPA_FILE_TEMPLATE.format(name=responseJson['wifi_name'], password=responseJson['wifi_password'])


        print "original(" + originalWPAText + ")"
        print "new(" + wpaText + ")"

        if originalWPAText != wpaText:

            wpaFile = open("/etc/wpa_supplicant/wpa_supplicant.conf", 'w')

            print wpaText
            print
            wpaFile.write(wpaText)
            wpaFile.close()

            tts.say("Updated wifi settings. I will automatically reset in 10 seconds.")
            time.sleep(8)
            tts.say("Reseting")
            time.sleep(2)
            os.system("reboot")


    except:
        print "exception while configuring setting wifi", url
        traceback.print_exc()
