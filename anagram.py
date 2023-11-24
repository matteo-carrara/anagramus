# -*- coding: UTF-8 -*-
# An anagram is a word or phrase formed by rearranging the 
# letters of a different word or phrase, 
# typically using all the original letters exactly once.

# by Matteo Carrara
# Un rekt a: birbantelli, zazinte, il tocio
# :P
	
from sys import argv, stdout
import time
import json
import os

FREQ_EXPORT_FILE = "./dict-freq.json"
dict_f = "./italiano.txt"
lower_alpha = list(map(chr, range(97, 123)))
accenti_ita = ['à','á','è','é','ì','í','ó','ò','ù','ú']
lower_alpha = lower_alpha + accenti_ita

def calc_freq(in_s):
	out = {}
	for ch in lower_alpha:
		out[ch] = 0
	
	for ch in in_s:
		if ch in out.keys():
			out[ch] = out[ch] +1
		else:
			print("Char not allowed in calc_freq:", ch)
			exit(1)
	return out
	


def only_alpha(src_str):
	out = ""
	for ch in src_str:
		if(ch.isalpha()):
			out = out + ch
	return out


if len(argv) != 2:
	print("Usage:", argv[0], "\"word or phrase inside quotation marks\"")
	exit(1)

src_str = argv[1].replace(" ", "") #remove spaces
src_str = only_alpha(src_str).lower()

corr_words = []
freq_words = []

EXISTING_FREQ = False
USE_FREQ_FILE = False

if(USE_FREQ_FILE):
	if os.path.exists(FREQ_EXPORT_FILE):
		print("Trying to load frequencies from file...")
		EXISTING_FREQ = True
		try:
			with open(FREQ_EXPORT_FILE, 'r') as file:
				print("Starting loading from file")
				start_time = time.time()
				freq_words = json.load(file)
				end_time = time.time()
				print("Done")
				elapsed_time = end_time - start_time
				print(f"Elapsed time: {elapsed_time} seconds")
		except IOError:
			print("Error reading from the file.")
			exit(1)
		except json.JSONDecodeError:
			print("Error decoding JSON.")
			exit(1)
	else:
		print(f'The file {FREQ_EXPORT_FILE} does not exist.')


if(not EXISTING_FREQ) or (not USE_FREQ_FILE):
	start_time = time.time()
	print("Loading dictionary")
	i = 0
	with open(dict_f, 'rb') as f:
		for line_bytes in f:
			try:
				line = line_bytes.decode('utf-8')
				corr_words.append(line.lower().replace("\n", ""))
			except UnicodeDecodeError as e:
				print(f"\nError decoding line in file: {e}")
		
			i = i+1
			#stdout.write("\rProgress "+str("{:,.0f}".format(i)))
			#stdout.flush()

	end_time = time.time()
	print("Dict loaded, rows = ", len(corr_words))
	elapsed_time = end_time - start_time
	print(f"Elapsed time: {elapsed_time} seconds")


	print("Calculating frequencies for dictionary...")
	print("Words with not allowed symbols will be skipped")
	start_time = time.time()

	i = 0
	for word in corr_words:
		valid_word = True
		tmpfreq  = {}
		for ch in lower_alpha:
			tmpfreq[ch] = 0
	
		for ch in word:
			if not (ch in lower_alpha):
				#print("FAILURE: char >", ch, "> in word >", word, "> not allowed, skipped")
				valid_word = False
			else:
				tmpfreq[ch] = tmpfreq[ch] + 1
		if(valid_word):		
			freq_words.append([tmpfreq, word])
			#print("\nWORD -", word, "- FREQ -", tmpfreq, "-")
		i = i + 1
	
		#stdout.write("\rProgress "+str("{:,.0f}".format(i))+"/"+str("{:,.0f}".format(len(corr_words))))
		#stdout.flush()

	end_time = time.time()
	print("Done")
	elapsed_time = end_time - start_time
	print(f"Elapsed time: {elapsed_time} seconds")

	if (not os.path.exists(FREQ_EXPORT_FILE)) and USE_FREQ_FILE:
		start_time = time.time()
		print("Dumping frequencies to file...")
		try:
			with open(FREQ_EXPORT_FILE, 'w') as file:
				json.dump(freq_words, file)
		except IOError as e:
			# Code to execute if an IOError occurs
			print(f"Error writing to the file: {e}")
			exit(1)
    
		end_time = time.time()
		print("Done")
		elapsed_time = end_time - start_time
		print(f"Elapsed time: {elapsed_time} seconds")
	
print("Starting to search for words")

while True:
	good_words_idx = []
	INPUT_FR = calc_freq(src_str)
	testing = 0
	delta = -1
	similar_idx = -1

	for w in freq_words:
		is_good = True
	
		for letter in INPUT_FR.keys():
			if w[0][letter] > INPUT_FR[letter]:
				is_good = False
				#print("Failed: letter -", letter, "- is -",w[0][letter], "- where max is -", INPUT_FR[letter], "-")
				break
		
		if(is_good):
			#print("Test passed",  w[1])
			good_words_idx.append(testing)
			if(len(w[1]) == len(src_str)) and(w[1] != src_str):
				print("COMPLETE ANAGRAM FOUND!!!!!!", w[1])
	
		testing = testing +1
		
	src_str = input("Insert another word: ").replace(" ", "")
	src_str = only_alpha(src_str).lower()

print("Done, exiting")