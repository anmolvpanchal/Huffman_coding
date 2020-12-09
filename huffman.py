import heapq
import os

class HuffmanCoding: #main class   
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode: # class for making heap and storing characters and its frequency
		def __init__(self, char, character_frequency):
			self.char = char
			self.character_frequency = character_frequency
			self.left = None
			self.right = None

		# defining less_than and equals function
		def __lt__(self, other):
			return self.character_frequency < other.character_frequency

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, self)):
				return False
			return self.character_frequency == other.character_frequency

	# functions required for compression:

	def frequency_dictionar_function(self, text): # counting the frequency of the character and storing to dictionary 
		frequency_dictionar = {}
		for character in text:
			if not character in frequency_dictionar:
				frequency_dictionar[character] = 0
			frequency_dictionar[character] += 1
		return frequency_dictionar

	def heap_function(self, frequency_dictionar):
		for key in frequency_dictionar:
			node = self.HeapNode(key, frequency_dictionar[key])
			heapq.heappush(self.heap, node)

	def merging_nodes_function(self): # merging two samllest nodes and pushing back it to the heap till there is only one element left  
		while(len(self.heap)>1):
			node_one = heapq.heappop(self.heap)
			node_two = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node_one.character_frequency + node_two.character_frequency)
			merged.left = node_one
			merged.right = node_two

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code): # making code and also keeping the reverse mapping for trace back 
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self): # make codes using code helper function 
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def encoded_text_function(self, text): # replace the characters by codes 
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def padding_function(self, encoded_text): # if length is not multiple of 8 add padding to it and store padding information 
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padding_information = "{0:08b}".format(extra_padding)
		encoded_text = padding_information + encoded_text
		return encoded_text


	def bytearray_function(self, padded_encoded_text): # creating byte array 
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self): # compression functon and create output binary file
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"

		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			frequency_dictionar = self.frequency_dictionar_function(text)
			self.heap_function(frequency_dictionar)
			self.merging_nodes_function()
			self.make_codes()

			encoded_text = self.encoded_text_function(text)
			padded_encoded_text = self.padding_function(encoded_text)

			output_bytes = self.bytearray_function(padded_encoded_text)
			output.write(bytes(output_bytes))
		

		print("Text file is Compressed ")


	# functions for decompression 


	def remove_padding_function(self, padded_encoded_text): # remove extra padding if added using the information 
		padding_information = padded_encoded_text[:8]
		extra_padding = int(padding_information, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decoding_text_function(self, encoded_text): #decode the encoded text using the revers mapping information and bring back the characters
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, input_path): # decompress the byte file and getting the txt 
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.remove_padding_function(bit_string)

			decompressed_text = self.decoding_text_function(encoded_text)
			
			output.write(decompressed_text)

		print("Decompressed bin file")
		