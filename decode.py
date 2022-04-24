## metadata

# source ./MNAE1/bin/activate
# python3 -m pip install <module>
# run file as admin: sudo python3 decode.py

### flanging system: send characters with a time or character offset based on shared sinusoidal functions

## sinusoidal functions

import geocoder
g = geocoder.ip('me')
print(g.latlng) # could be any location, just using this for a geo example

# delay between characters

delayPeriod = abs(g.latlng[0]) + abs(g.latlng[1]) # dont use this - this is private key -- instead create a shared public key which is the distance from the senders private location to the recievers private location

import math

def undelay(t):
    return math.sin(delayPeriod * t) * 160 # average words typed per minute

# offset between characters

offsetPeriod = abs(g.latlng[0]) + abs(g.latlng[1]) # dont use this - this is private key -- instead create a shared public key which is the distance from the senders private location to the recievers private location

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
encodedAlphabet = []

def char_position(char):
    return ord(char.lower()) - 96

def offset(char):
    if char == ' ':
        return ' '
    else:
        return alphabet[ round( math.sin( offsetPeriod * char_position(char)) * 13 ) ]

for i in range(len(alphabet) - 1):
    encodedAlphabet.append(offset(alphabet[i]))
    
print(encodedAlphabet)

## i/o

# get input

message = input()

# decode message

decodedMessage = [''] * len(message)
for i in range(len(message)):
    decodedMessage[i] = message[ round( undelay(i) ) ]
decodedMessage = ''.join(decodedMessage[:-160])
print(decodedMessage)

# split into words

# options function -- breaks when has 2 equal chars in a row: appends to options even when not meant to

def optionsGenerator(word):
    optionsPerChar = []
    for i in range(len(word)):
        temp = []
        for j in range(len(encodedAlphabet)):
            if word[i] == encodedAlphabet[j]:
                temp.append(alphabet[j])
        optionsPerChar.append(temp)
    options = []
    for i in range(len(optionsPerChar)):
        for j in range(len(optionsPerChar[i])):
            if (i == 0):
                options.append(optionsPerChar[i][j])
            else:
                for k in range(len(options)):
                    if (len(options[k]) == i): options.append(options[k] + optionsPerChar[i][j])
    return filter(lambda x: len(x) == len(word), options)

wordArray = decodedMessage.split(' ')
for i in range(len(wordArray)):
    print(wordArray[i])
    print('\n')
    print( list( dict.fromkeys( optionsGenerator(wordArray[i]) ) ) ) # all possible words for that word in the message