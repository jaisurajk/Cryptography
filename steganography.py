# author: Jaisuraj Kaleeswaran
# date: March 18, 2023
# file: steganography.py encodes and decodes a message in an image
# input: text and/or binary text
# output: binary text of the input text and/or text of the input binary text

import cv2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    def __init__(self):
        self.text = ''  #Both the text and binary start as empty strings
        self.binary = ''
        self.delimiter = '#' # delimeters are indicated by '#' sign
        self.codec = None
        
    # convert text to binary
    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(self.delimiter + message)
        
        # check if it is possible to encode the message
        num_bytes = ceil(len(binary) // 8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes)
            self.text = message
            self.binary = binary
            
           # The nditer operand per pixel in the image is being read
            for i in np.nditer(image, op_flags = ['readwrite']):
                if len(binary) >= 1:
                    
                    # Subtract 1 if the bit is even and first binary bit equals 0
                    if i % 2 == 0 and binary[0] == '0':
                        i[...] = i - 1
                        
                    # Add 1 if the bit is odd and first binary bit equals 0
                    elif i % 2 == 1 and binary[0] == '1':
                        i[...] = i + 1
                else:
                    # break out of the for loop
                    break 
                # shrink the binary by removing the first bit
                binary = binary[1:]  
            cv2.imwrite(fileout, image) #image is the missing parameter
            
    # convert binary to text         
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging      
        flag = True
        
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            binary_data = ''
            for i in np.nditer(image):
                if i % 2 == 0:
                    binary_data += '1'
                else:
                    binary_data += '0'
            self.text = self.codec.decode(binary_data)
            self.binary = self.codec.encode(self.delimiter + self.text)            
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          
    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

#driver code for the steganography class
if __name__ == '__main__':
    
    s = Steganography()
    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    s.decode('fractal.png', 'binary')
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')