class Motor:
    def __init__(self):
        print("Initialized dummy motor")

    def run(self, command):
        print("Running dummy motor command")
        print(command)

    def updateChargeApproximation(self):
        pass

    def ui(self):
        pass

class DummyMotor(Motor):
    def run(self, command):
        print("Running dummy motor command")
        print(command)

    def ui(self):
        return """
{
"button_panel_label": "movement controls",
"buttons": [
    {
        "command": "L",
        "label": "left"
    }
]
}"""
