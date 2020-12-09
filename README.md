# Huffman_coding
Hufffman code in python to compress and decompress file.  

We are creating one main class HuffmanCoding in which we are going to creat different functions which will be used for compression and decompressing file. 

Class heap node is created to make and manage the heap and keep trace of left and right child and keeping the character frequency.
Two methods are written in it which are less then and equal 

Steps for compression  
Build frequency dictionary for the characters we have and building a priority queue.
Making Huffman tree by selecting 2 min nodes and merging them and pushing back the new node to tree and repeating the same till we are left with one node. 
Assigning codes to characters (from root to top node)
Encode the input text by replacing character by code and also making a reverse mapping tree which will be helpful while decompressing the file.
If overall length of final encoded bit is not multiple of 8 add padding to the text and storing the padding information at the start of overall encoded bit stream. 
Writing the result in to the output binary file 

Steps for decompression 
Read binary file 
Read padding information and remove padding if added any bits.
Decode the bits read the bits and replace the valid Huffman code bits with the character values using the reverse mapping information.  
Save the decoded data to the output file named as filename_decompressed.

How to run the code 
There are two files Huffman and UseHuffman file we have to run the usehuffman file which uses huffam file from which we import the main HuffmanCoding class we just have to pass the path (Depends on the Individuals pc where they store the file) wanted to be compressed and decompressed as we are calling both the functions in UseHuffman file.

