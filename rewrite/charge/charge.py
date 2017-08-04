

def updateChargeApproximation():

    username = getpass.getuser()
    path = "/tmp/charge_state_%s.txt" % username

    # read charge value
    # assume it is zero if no file exists
    if os.path.isfile(path):
        file = open(path, 'r')
        chargeValue = float(file.read())
        file.close()
    else:
        chargeValue = 0

    chargePerSecond = 1.0 / secondsToCharge
    dischargePerSecond = 1.0 / secondsToDischarge

    if isCharging():
        chargeValue += 100.0 * chargePerSecond * chargeCheckInterval
    else:
        chargeValue -= 100.0 * dischargePerSecond * chargeCheckInterval

    if chargeValue > 100.0:
        chargeValue = 100.0
    if chargeValue < 0:
        chargeValue = 0.0

    # write new charge value
    file = open(path, 'w')
    file.write(str(chargeValue))
    file.close()

    print "charge value updated to", chargeValue
