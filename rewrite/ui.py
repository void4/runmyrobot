import json
import requests
import getpass

def setCustomUI(robot_id, ui=None, username=None, password=None):
    if not ui:
        print("No custom UI.")
        return

    print("Creating custom UI")

    if username is None:
        username = raw_input("Input username for letsrobot.tv: ")
    if password is None:
        password = getpass.getpass("Input password for %s: " % username)

    print("Authenticating...")
    response = requests.request("POST", "https://letsrobot.tv/api/v1/authenticate", data=json.dumps({'username': username, 'password': password}), headers={'content-type': 'application/json'})
    print(response)
    cookies={'connect.sid' : response.cookies['connect.sid']}

    print("Requesting current configuration...")
    recv_robot = requests.request("GET", "https://letsrobot.tv/api/v1/accounts/", cookies=cookies)
    print(recv_robot)
    j = json.loads(recv_robot.content)
    index = [i for i,r in enumerate(j["robots"]) if r["robot_id"]==str(robot_id)][0]
    # Check if they are the same?
    j["robots"][index]["panels"] = json.dumps(ui)
    print(json.dumps({"robots":j["robots"]}, indent=4, sort_keys=True))
    print("Setting custom layout...")
    send_robot = requests.request("POST", "https://letsrobot.tv/api/v1/accounts/robots", data=json.dumps({"robots":j["robots"]}), cookies=cookies, headers={'content-type': 'application/json'})
    print(send_robot)
    #print(send_robot.content)
