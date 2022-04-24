## metadata

# source ./MNAE1/bin/activate
# python3 -m pip install <module>
# run file as admin: sudo python3 encode.py

### flanging system: send characters with a time or character offset based on shared sinusoidal functions

## sinusoidal functions

import geocoder
g = geocoder.ip('me')
print(g.latlng) # could be any location, just using this for a geo example

# delay between characters

delayPeriod = abs(g.latlng[0]) + abs(g.latlng[1]) # dont use this - this is private key -- instead create a shared public key which is the distance from the senders private location to the recievers private location

import math

def delay(t):
    return math.sin(delayPeriod * t) * 160 # average words typed per minute

# offset between characters

offsetPeriod = abs(g.latlng[0]) + abs(g.latlng[1]) # dont use this - this is private key -- instead create a shared public key which is the distance from the senders private location to the recievers private location

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

def char_position(char):
    return ord(char.lower()) - 96

def offset(char):
    if char == ' ':
        return ' '
    else:
        return alphabet[round( math.sin( offsetPeriod * char_position(char)) * 13 )]

## i/o

# initialize message and time

message = ''

# map key to character

from pynput import keyboard
from pynput.keyboard import Key
import random

def mapkey(key):
    global message
    
    if key == Key.enter:
        print('\n')
        tempArray = []
        for i in range(len(message) + 160):
            tempArray.append(alphabet[ random.randrange(0, 26) ])
        for i in range(len(message)):
            tempArray[ round( delay(i) ) ] = message[i]
        print( ''.join(tempArray) )
        message = ''
        
        return 'break'
    
    elif key == Key.backspace:
        message = message[:-1]
        
    elif key == Key.space:
        message += ' '
        
    else:
        message += offset(key.char)

# listen for keypresses

print('Enter message:')
print('\n')

with keyboard.Listener(
        on_press=mapkey) as listener:
    listener.join()
    
listener = keyboard.Listener(
    on_press=mapkey)

listener.start()