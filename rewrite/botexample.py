import controller

# Adding command handling modules manually
#from motor.motor import DummyMotor
#controller.add(DummyMotor())

# Importing an full configured collection of command handling modules
from configexample import config
controller.add(config)

controller.run(33583635)
