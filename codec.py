# author: Jaisuraj Kaleeswaran
# date: March 18, 2023
# file: codec.py encodes and decodes messages in images
# input: the image file
# output: a message encoded in an image

# import numpy as np
from collections import Counter

class Codec():
   # constructor  
   def __init__(self):
       self.delimiter = '#' # delimeters are indicated by '#' sign
       self.name = 'binary'

   # convert text to binary
   def encode(self, text):
       bin_form = []
       if type(text) == str:
           for i in text:
               bin_form.append(format(ord(i), "08b"))
           return ''.join(bin_form)
       print('Format error')  #If the text isn't a string, print format error

   # convert binary to text
   def decode(self, b):
       text = ''
       binary = []
       for i in range(0, len(b), 8):
           byte = b[i: i+8]
           if byte == self.encode(self.delimiter):
               break
           binary.append(byte)
       for byte in binary:
           text += chr(int(byte, 2))
       return text


class CaesarCypher(Codec):
   # constructor   
   def __init__(self):
       self.delimiter = '#'
       self.name = 'caesar'
       self.chars = 256      # total number of characters

   # convert text to binary
   def encode(self, text):
       if type(text) == str:
           # shift the character by 3
           bin_form = []
           for i in text:
               bin_form.append(format((ord(i)+3) % 256, "08b"))
           return ''.join(bin_form)
       print('Format error')  #If the text isn't a string, print format error

   # convert binary to text
   def decode(self, data):
       text = ''
       if type(data) == str:
           for i in range(0, len(data), 8):
               byte = data[i: i+8]
               if byte == self.encode(self.delimiter):
                   break
               # shift the character back 3
               text += chr(int(byte, 2) - 3)
       return text

# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
   def __init__(self, freq, symbol, left = None, right = None):
       self.freq = freq
       self.symbol = symbol
       self.code = ''
       self.left = left
       self.right = right

class HuffmanCodes(Codec):   
   def __init__(self):
       self.nodes = None
       self.data = {}  #the data object is stored as a dictionary
       self.name = 'huffman'
       self.delimiter = '#'

   #Create a Huffman Tree
   def make_tree(self, data):
        # make nodes
        nodes = [Node(freq, ch) for ch, freq in data.items()]

        # Make the nodes form into a tree
        while len(nodes) >= 2:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key = lambda x: x.freq)

            # assign codes
            nodes[0].code = '0'
            nodes[1].code = '1'

            # combine the nodes into a tree
            tree = Node(nodes[1].freq+nodes[0].freq, nodes[1].symbol+nodes[0].symbol,
                        nodes[1], nodes[0])

            # remove the two nodes and add their parent to the list of nodes
            for i in range(2):
                nodes.remove(nodes[0])
            nodes.append(tree)
        self.nodes = nodes  #Make self.nodes equal to nodes
        return self.nodes   #Return self.nodes
  
   # traverse a Huffman tree
   def traverse_tree(self, node, val):
       next_val = val + node.code
       if (node.left):
           self.traverse_tree(node.left, next_val)
       if (node.right):
           self.traverse_tree(node.right, next_val)
       if (not node.left and not node.right):
           self.data[node.symbol] = next_val

   # convert text to binary
   def encode(self, text):
        # make a tree
       self.make_tree(Counter(text)) 
       # traverse the tree
       self.traverse_tree(self.nodes[0], '') 
       bin_form = []
       for i in text:
           bin_form.append(self.data[i])
       return ''.join(bin_form)

   # convert binary to text
   def decode(self, data):
       temp = ''
       text = ''
       for i in data:  # for each bit in the binary data
           temp += i  # add the bit to the temporary string
           
           # for each character and its binary code in the dictionary data
           for ch, bin in self.data.items():  
               
               # if the temporary string is the delimiter
               if temp == bin:               # if the temporary string is in the dictionary data
                   temp = ''                     # make the temporary string empty
                   text += ch                  # add the character to the text
               elif temp == self.data[self.delimiter]:
                   break  # break out of the second for loop
               else:
                   # otherwise, continue to the next characters in the text
                   continue                     
       return text  # return the text

# driver code for the codec classes
if __name__ == '__main__':
   text = 'hello'
   print('Original:', text)


   c = Codec()
   binary = c.encode(text + c.delimiter)
   print('Binary:', binary)
   data = c.decode(binary)
   print('Text:', data)


   cc = CaesarCypher()
   binary = cc.encode(text + cc.delimiter)
   print('Binary:', binary)
   data = cc.decode(binary)
   print('Text:', data)


   h = HuffmanCodes()
   binary = h.encode(text + h.delimiter)
   print('Binary:', binary)
   data = h.decode(binary)
   print('Text:', data)