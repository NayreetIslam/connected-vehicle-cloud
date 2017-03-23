from sense_hat import SenseHat

sense = SenseHat()

def startSensing():
    while True:
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']
    
        x = abs(x)
        y = abs(y)
        z = abs(z)
    
        yield {
            "x": x,
            "y": y,
            "z": z,
        }

for i in startSensing():
    print(i)
