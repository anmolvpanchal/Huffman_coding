from huffman import HuffmanCoding

#input file path of your pc where the files are stored 
path = "C:/Users/Panchal/Desktop/huffman/sample.txt"

h = HuffmanCoding(path)

h.compress() # calling compress function 

h.decompress("C:/Users/Panchal/Desktop/huffman/sample.bin") # calling decompresse fuction