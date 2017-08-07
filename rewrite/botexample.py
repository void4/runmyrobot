import controller

# Adding command handling modules manually
#from motor.motor import DummyMotor
#controller.add(DummyMotor())

# Importing and running a full configured collection of command handling modules
from configexample import config

controller.run(33583635, config)

# Alternative syntax
#controller.add(config)
#controller.run(33583635)
