# -*- coding: UTF-8 -*-
# An anagram is a word or phrase formed by rearranging the 
# letters of a different word or phrase, 
# typically using all the original letters exactly once.

# by Matteo Carrara
# Un rekt a: birbantelli, zazinte, il tocio
# :P
	
import threading
from sys import argv, stdout
import sys
import time
import json
import os
from queue import Queue

CALC_DICT_FREQ_THREADS = 8
FREQ_EXPORT_FILE = "./dict-freq.json"
dict_f = "italiano.txt"
lower_alpha = list(map(chr, range(97, 123)))
accenti_ita = ['à','á','è','é','ì','í','ó','ò','ù','ú']
lower_alpha = lower_alpha + accenti_ita

logo = """ 
   __ _ _ __   __ _  __ _ _ __ __ _ _ __ ___  _   _ ___ 
  / _` | '_ \ / _` |/ _` | '__/ _` | '_ ` _ \| | | / __|
 | (_| | | | | (_| | (_| | | | (_| | | | | | | |_| \__ \\
  \__,_|_| |_|\__,_|\__, |_|  \__,_|_| |_| |_|\__,_|___/
                     __/ |                              
                    |___/        
		    
By matteo carrara
Windows edition

"""




def calc_dict_freq(corr_words, queue):
	#print("INSIDE THREAD", threading.current_thread().name)
	#print("LEN of input:", len(corr_words))
	i = 0
	freq_words = []
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

	#print("THREAD", threading.current_thread().name, "RETURN SIZE", len(freq_words))
	#print("THREAD LEFT", threading.current_thread().name)
	queue.put(freq_words)


def recursive_add(list_base, good_words, ANAGRAM_LEN, int_k, INPUT_FR, depth=0):
	#print("FN DEPTH = ", depth)
	#print("Entering recursive add with base:")
	for w in list_base:
		#print("-", w[1])
		pass
		
	DELTA_SRC = 0
	LIST_BASE_LEN = 0
	
	for w in list_base:
		LIST_BASE_LEN = LIST_BASE_LEN + len(w[1])
	
	DELTA_SRC = ANAGRAM_LEN - LIST_BASE_LEN
	#print("Base len", LIST_BASE_LEN, "Anagram len", ANAGRAM_LEN, "DELTA", DELTA_SRC)
	
	if(DELTA_SRC < 1):
		#print("***** VALID ANAGRAM FOUND, returning")
		out = ""
		wl = []
		for w in list_base:
			out = out+ " " + w[1] + " "
			wl.append(w[1])
		#print(out)
		wl_sort = sorted(wl, key=len, reverse=True)
		return wl_sort
	
	#print("Building freq list for input")
	p = {}
	for w in lower_alpha:
		p[w] = 0
		
	for w in list_base:
		for ch in w[0].keys():
			p[ch] = p[ch] + w[0][ch]

	#print("List built")
	#print(p)
	

	out = []

	if(LIST_BASE_LEN < ANAGRAM_LEN/2):
		print("**********LEAVING EARLY***************")
		return out
	
	# Cycle from 1 to DELTA_SRC
	for my_idx in range(1, DELTA_SRC+1):
		tmp = DELTA_SRC - my_idx + 1
		my_idx = tmp

		if (my_idx < DELTA_SRC/2):
			#print("Skipping: DELTA_SRC = ", DELTA_SRC, "IDX = ", my_idx)
			#print("***************BASE LEN", LIST_BASE_LEN)
			s = ""
			for w in list_base:
				s = s + w[1]
				pass
			#print(">>>>>>>>", s)
			#break
			pass
			# FIXME!!!!
		
		#print("Searching words for lenght", my_idx)
		if my_idx in int_k:
			for test in good_words[str(my_idx)]:
				#print("testing", test[1], "-depth", depth)
							
				good_add = True
				for ch in INPUT_FR.keys():
					if test[0][ch]+p[ch] > INPUT_FR[ch]:
						#print("Failed on char", ch)
						good_add = False
						break
					else:
						pass
						
				if(good_add == True):
					#print("Word is good to add", test[1])
					#print("MAKING A RECURSIVE CALL -from depth", depth)
					nl = list_base
					nl = nl + [test]
					tmpout = recursive_add(nl, good_words, ANAGRAM_LEN, int_k, INPUT_FR, depth+1)
					if(len(tmpout)!= 0):
						if(not (tmpout in out)):
							out.append(tmpout)
					#print("**GOT RETURN at depth", depth, "-", out)
	
	return out


def clear_screen():
	os.system("cls")


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


def main():
	clear_screen()
	print(logo)
	
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
		print("Loading dictionary...")
		
		i = 0
		# Example usage
		script_dir = os.path.dirname(os.path.abspath(__file__))
		bundled_file_path = os.path.join(script_dir, dict_f)
		with open(bundled_file_path, 'rb') as f:
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

		##################
		print("Calculating frequencies for dictionary...")
		print("USING", CALC_DICT_FREQ_THREADS, "THREADS")
		print("(Words with not allowed symbols will be skipped)")
		print("This operation MAY TAKE a few minutes. NO MESSAGES will be shown on the screen to improve performance.")
		
		dict_thread_pool = []
		queue_pool = []
		#print("Dict len", len(corr_words))
		#print("Threads", CALC_DICT_FREQ_THREADS)
		
		DEBUG_slice_sum = 0
		for i in range(CALC_DICT_FREQ_THREADS):
			slice_start = int(i*len(corr_words)/CALC_DICT_FREQ_THREADS)
			slice_end = int((i+1)*len(corr_words)/CALC_DICT_FREQ_THREADS)
			DEBUG_sl_el = slice_end - slice_start
			DEBUG_slice_sum = DEBUG_slice_sum + DEBUG_sl_el
			
			#print("Thread", i,": slice start", slice_start, "to end", slice_end)
			
			tmpq =  Queue()
			dict_thread_pool.append(threading.Thread(target=calc_dict_freq, args=(corr_words[slice_start:slice_end], tmpq), name="Thread-"+str(i)))
			queue_pool.append(tmpq)
		
		#print("DEBUG: sliced elemnts", DEBUG_slice_sum)
		#print("DICT SIZE", len(corr_words))
		start_time = time.time()
		for t in dict_thread_pool:
			t.start()

		for t in dict_thread_pool:
			t.join()
			
		#print("All thread left")

		for q in queue_pool:
			freq_words = freq_words + q.get()
			
		#print("Total freq words in MAIN", len(freq_words))
		end_time = time.time()
		print("Done")
		elapsed_time = end_time - start_time
		print(f"Elapsed time: {elapsed_time} seconds")
		
		#print("DEBUG: exiting")
		#exit(0)

		#####################
		

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
	
	#print("Starting to search for words")
	print("")
	
	while True:
		good_words = {}
		testing = 0
		delta = -1
		similar_idx = -1

		INPUT_LIMIT = 12
		src_str = input("Write something to find anagrams (max " + str(INPUT_LIMIT) + " char): ")
		print("LOOKING FOR ANAGRAMS OF <"+src_str+">...\n")

		src_str.replace(" ", "")
		
		if(len(src_str) > INPUT_LIMIT):
			print("String too long, try again")
			continue
		
		src_str = only_alpha(src_str).lower()
		INPUT_FR = calc_freq(src_str)
		
		print("Looking for whole-word anagrams...")
		for w in freq_words:
			is_good = True
	
			for letter in INPUT_FR.keys():
				if w[0][letter] > INPUT_FR[letter]:
					is_good = False
					#print("Failed: letter -", letter, "- is -",w[0][letter], "- where max is -", INPUT_FR[letter], "-")
					break
		
			if(is_good):
				if(len(w[1]) > 0):
					#print("Test passed",  w[1])
					#good_words_idx.append([testing, len(w[1])])
					if(str(len(w[1])) in good_words.keys()):
						good_words[str(len(w[1]))].append(w)
					else:
						good_words[str(len(w[1]))] = [w]
					if(len(w[1]) == len(src_str)) and(w[1] != src_str):
						print("WORD FOUND: ", w[1])
	
			testing = testing +1
		
		print("\nTrying to find words to form a sentence...")
		#print("Available lenght:")
		k = list(good_words.keys())
		int_k = []
		
		for elem in k:
			int_k.append(int(elem))

		int_k.sort()
		int_k.reverse()
		
		#print(int_k)
		
		ANAGRAM_LEN = len(src_str)
		#print("SOURCE -", src_str, "- len", ANAGRAM_LEN)
		
		run = 0
		LIMIT = 6
		results = []
		for l in int_k:
			run = run +1
			if (run == LIMIT):
				#print("DEBUG execution STOPPED (run =", LIMIT,")")
				#break
				pass
			
			DELTA_SRC = ANAGRAM_LEN - l
			#print("Words for lenght", l)
			#print("Delta from source",  DELTA_SRC)
			
			if(l < len(src_str)/2):
				break
			
			if DELTA_SRC < 1:
				continue
			
			
			for p in good_words[str(l)]:
				#print(p[1])
				#print("Looking for a word to add...")
				rl = recursive_add([p], good_words, ANAGRAM_LEN, int_k, INPUT_FR)
				#print("MAIN: function left")
				if(len(rl) != 0):
					#print("Got results")
					for elem in rl:
						#print(elem)
						if elem in results:
							print(">>>>>>>>>> FAILURE Already existing")
							pass
						else:
							results.append(elem)
							#print("Got result")
				
		s_res = sorted(results, key=len, reverse=True)
		print("Found ", len(s_res), "possible sets of words to form a sentence. (FIXME not shown for perfomance))")
			

	


	print("Done, exiting")
	

main()