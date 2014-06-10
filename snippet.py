
import re 
import sys


def argmin(pos, Dictlist):
	"""
	Args: 
		pos - current position 
		Dictlist - a dictionary containing lists of search key positions

	Returns:
		the list that has the increasing minimum element

	"""

	minVal = sys.maxsize
	arg = -1
	
	try: 
		for key in Dictlist: 
			if Dictlist[key][pos[key]] < minVal:
				minVal = Dictlist[key][pos[key]] 
				arg = key
	except:
		arg = -1
	return arg

def argmax(pos, Dictlist):
	"""
	Args: 
		pos - current position 
		Dictlist - a dictionary containing lists of search key positions

	Returns:
		the list that has the maximum current element position

	"""

	maxVal = -1
	arg = -1
	try:
		for key in Dictlist: 
			if Dictlist[key][pos[key]] > maxVal:
				maxVal = Dictlist[key][pos[key]] 
				arg = key
	except:
		arg = -1
	return arg


def get_tail_text(text, start, length):

	"""
	Makes the tail text for snippet print.
	Args:
		text - Text containing the snippet as well as rest of the text.
		start - Point that tail starts (snippet ends)
		length - Desired length
	Returns: 
		tail - Tail text.
	"""
	tail = ""
	for i in text[start:-1]: 
		if is_new_sentence(i) or len(tail) == length:
			break
		else: 
			tail = tail + i
	tail += "..."
	return tail 

def get_head_text(text, start, length):

	"""
	Makes the head text for snippet print.
	Args:
		text - Text containing the snippet as well as rest of the text.
		start - Point that tail starts backward (snippet starts)
		length - Desired length
	Returns: 
		head - Head text.
	"""
	head = ""
	walk_back = 0
	for i in text[start::-1]:
		if is_new_sentence(i) or walk_back >= length:
			break
		else: 
			walk_back += 1
		
	head = "..." + text[start - walk_back+1:start] 
	return head

def print_snippet(text, snippet_start, snippet_end):

	"""
	Prints the snippet in a beautiful way. 
	Args:
		text - Whole text containing the snippet
		snippet_start - Startin point for snippet i the text
		snippet_end - Ending point for snippet in the text

	"""
	WINDOW_SIZE = 50
	print 
	print text
	print 
	# Check if there in snippet to be printed
	if snippet_start == -1 or snippet_end == -1:
		print " No snippet available to print."
		return

	WINDOW_SIZE = max(WINDOW_SIZE, snippet_end - snippet_start)
	
	available_space = WINDOW_SIZE - (snippet_end - snippet_start)

	tail_text = get_tail_text(text, snippet_end, available_space/2)

	head_text = get_head_text(text, snippet_start, available_space/2)

	output_text = "{head} {highlight} {snippet} {endhighlight} {tail}".format(
			highlight = "[[HIGHLIGHT]]",
			endhighlight = "[[END HIGHLIGHT]]",
			snippet = text[snippet_start:snippet_end],
			head = head_text,
			tail = tail_text
			)

	print output_text



def is_new_sentence(in_char):

	"Checks if in_char is a sign of sentence termination. "

	punctuations = ['.', '\n', ';', '!', ',']

	if in_char in punctuations:
		return True
	return False


def find_snippet(context, query):
	"""
	Finds snippet in the given text. Returns (-1,-1) if nothing found.
	Args: 
		context - Input text/Document
		query - query containing the snippets 
	Returns: 
		snippet_start - starting point for the snippet in the text.
		snippet_end - ending point for the snippet in the text.

	"""

	search_keys = {}
	for key in query.split():
		search_keys[key] = []

	rx ='|'.join(search_keys)

	for m in re.finditer(r""+rx, context): 
	 	if m.group(0) in search_keys:
	 		search_keys[m.group(0)].append(m.start(0))

	# the current selected element of each list
	pos = {}
	# the current best solution position 
	sol = {}
	for key in search_keys:
		pos[key] = 0
		sol[key] = 0 

	# the score (window length) of current solution 
	currsol = sys.maxsize
	snippet_start = -1
	snippet_end = -1

	# for k in search_keys:
	# 	print k,search_keys[k]

	while True:

		# select the list that has the increasing minimum element 
		minList = argmin(pos, search_keys)
		
		# if you cant increase the minimum, stop
		if minList == -1:
			break  

		#calcuate the window size 
		minValue = search_keys[minList][pos[minList]]
		maxList = argmax(pos, search_keys)
		maxValue = search_keys[maxList][pos[maxList]]
		nextSol = maxValue - minValue
		
		# update the solution if required
		if nextSol < currsol:
			currsol = nextSol
			sol = pos.copy()
	
		pos[minList] += 1

	# get the best sol properties 
	minList = argmin(sol, search_keys)	
	maxList = argmax(sol, search_keys)

	minValue = search_keys[minList][sol[minList]]
	maxValue = search_keys[maxList][sol[maxList]]
	
	snippet_start = minValue
	snippet_end = maxValue + len(maxList)
	
	return snippet_start,snippet_end



if __name__ == "__main__":
	context = "I like fish. Little start's deep dish pizza sure is fantastic. Dog are great. deep something dish pizza"
	query = "deep dish pizza"
	snippet_start, snippet_end = find_snippet(context, query)
	print_snippet(context, snippet_start, snippet_end)