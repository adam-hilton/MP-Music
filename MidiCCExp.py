import mido
import time

port = mido.open_output('pisound MIDI PS-1MJPEPE')

NewVal = 22
direction = 1
step = 1

try: 

    while True:
        NewVal += direction * step
        
        message = mido.Message('control_change', channel=4, control=1, value=NewVal, time=1)

        print(message)

        port.send(message)
        
        if NewVal >= 110 or NewVal <= 10:
            direction *= -1
                
        

        time.sleep(0.04)

except KeyboardInterrupt:
    print("Loop interrupted")
    port.close()
    if port.closed:
        print("port closed.")


# mido.Message('control_change', channel=6, control=1, value=122)


