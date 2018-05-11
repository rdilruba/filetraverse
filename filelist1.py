import os

import sys

import datetime

import subprocess

from collections import deque

import re

import hashlib

import argparse

# we parse the arguments here

parser = argparse.ArgumentParser()

parser.add_argument('-before', action='store', dest='before_date')

parser.add_argument('-after', action='store', dest='after_date')

parser.add_argument('-match', action='store', dest='pattern')

parser.add_argument('-bigger', action='store', dest='big_size')

parser.add_argument('-smaller', action='store', dest='small_size')

parser.add_argument('-delete', action='store_true', dest='delete')

parser.add_argument('-zip', action='store', dest='zipfile')

parser.add_argument('-duplcont', action='store_true', dest='duplcont')

parser.add_argument('-duplname', action='store_true', dest='duplname')

parser.add_argument('-stats', action='store_true', dest='stats')

parser.add_argument('-nofilelist', action='store_true', dest='nofilelist', default= False)

parser.add_argument('rest', nargs=argparse.REMAINDER)

results = parser.parse_args()

# finds the modification time of the file in given path
# takes filepath as string
# returns the modification time

def mod_time(filepath):

        st = os.stat(filepath)

        modtime = os.path.getmtime(filepath)

        modtime = st.st_mtime


	return datetime.datetime.fromtimestamp(modtime).strftime('%Y%m%dT%H%M%S')

# finds the size of the file in given path
# takes filepath as string
# returns the size

def fisize(filepath):

	st = os.stat(filepath)

        filesize = st.st_size

        filesize = os.path.getsize(filepath)

   	return filesize

#gives error message if some unwanted combinations are given 

if results.delete:
		if results.zipfile is not None:
			print('both zip and delete  options are not allowed at the same time.')
		if results.duplcont :
			print('both duplcont and delete  options are not allowed at the same time.')
		if results.duplname :
			print('both duplname and delete  options are not allowed at the same time.')
		

# prints all file paths in given or current directory if no option is given

elif len(sys.argv) == 1 or (len(sys.argv) == len(results.rest) +1 ):
	
	# if a directory is given uses it, uses current directory otherwise.

	if results.rest:

		qlist = deque(results.rest)

	else:
	
		qlist = deque([ '.' ])

	#recursively traverses the directories and finds paths of files. Then prints the paths.

	while qlist:
	
        	currentdir = qlist.popleft()

        	dircontents = os.listdir(currentdir)

        	for name in dircontents:

        		currentitem = currentdir + '/' + name

           		if os.path.isdir(currentitem):
               	
				qlist.append(currentitem)

          		else:

                		print(currentitem)

# checks all options in given or current directory

else:
	# if a directory is given uses it, uses current directory otherwise.

	if len(results.rest) != 0:

		qlist = deque(results.rest)

	else:

		qlist = deque(['.'])
		

	files = list()

	totalsize = 0

	#recursively traverses the directories and finds paths of files. Then adds them into a list called files.    

	while qlist:

		currentdir = qlist.popleft()

        	dircontents = os.listdir(currentdir)

        	for name in dircontents:

        	    currentitem = currentdir + '/' + name

        	    if os.path.isdir(currentitem):

        	        qlist.append(currentitem)

        	    else:

        	        files.append(currentitem)

			totalsize = totalsize + fisize(currentitem) # finds size of each file and adds them.

	totalnumber = len(files)
	
	duplnum = 0
		
	duplsize = 0
	duplnumber = 0


	# checks if the file is modified before the given time. If not removes them from the list.

	if results.before_date is not None:

		newlist= []
		for j in files:

			if(results.before_date < mod_time(j)):
				newlist.append(j)
		
		for k in newlist:
			files.remove(k)				

	# checks if the file is modified after the given time. If not removes them from the list.	

	if results.after_date is not None:

		newlist= []
		for j in files:

			if(results.after_date > mod_time(j)):
				newlist.append(j)
		
		for k in newlist:
			files.remove(k)		

        	
	# checks if the file name matches the given pattern. If not removes them from the list.

	if results.pattern is not None:

		newlist = []
		for j in files: 

			filename = ''

			i =len(j)-1

			while j[i] is not '/':   # finds file name from its path

				filename = j[i] + filename
				i = i - 1

			if(re.search(results.pattern, filename) is None):

		            	newlist.append(j)
		
		for k in newlist:
			files.remove(k)	


	# checks if the file size is greater than or equal to given size. If not removes them from the list.

	if results.big_size is not None:

		newlist = []

	
		if 'K' in results.big_size:	# converts Kilobytes to bytes

			bsize = int(results.big_size[:-1]) * 1024

		elif 'M' in results.big_size:	# converts Megabytes to bytes

			bsize = int(results.big_size[:-1]) * 1048576

		elif 'G' in results.big_size:	# converts Gigabytes to bytes

			bsize = int(results.big_size[:-1]) * 107374182
		else:
			bsize = int(results.big_size)

		for j in files:
	
			if(bsize > fisize(j)):

		        	newlist.append(j)
		
		for k in newlist:
			files.remove(k)	

	                    
	# checks if the file size is smaller than or equal to given size. If not removes them from the list.

	if results.small_size is not None:

		newlist = []

		if 'K' in results.small_size:	# converts Kilobytes to bytes

			bsize = int(results.small_size[:-1]) * 1024

		elif 'M' in results.small_size:	# converts Megabytes to bytes

			bsize = int(results.small_size[:-1]) * 1048576

		elif 'G' in results.small_size:	# converts Gigabytes to bytes

			bsize = int(results.small_size[:-1]) * 107374182
		else:
			bsize = int(results.small_size)

		for j in files:

			if(bsize < fisize(j)):

				newlist.append(j)
		
		for k in newlist:
			files.remove(k)	

	                    
	# removes all files in given path recursively.

	if results.delete:
	
		if files:
	
			command = 'rm '+ ' '.join(files)
	
	                os.system(command)


	# checks if the contents of files are the same by looking hash codes. If so, prints them together.

	if results.duplcont :

		diff = {}

		maplist = []

		for j in files:
	
	            	command = 'shasum ' + j

	            	output = os.popen(command).read()  # takes hash output of file and stores it in output

			maplist.append(output)

			hash = ''
			i =0

			while output[i] is not ' ':   # takes just the hash code part of output

				hash = hash + output[i]
				
				i = i + 1
			

			if diff.has_key(hash):	# looks for same hash codes

				diff[hash] = diff.get(hash) +1

			else:

				diff[hash] = 1
		
		
		for k in diff.keys(): # finds and prints files which have the same hash code

			if diff.get(k) > 1:
				
				for m in maplist:
					
					if k in m:
	
						for l in range(0, len(m)):
							if m[l] is '/':
								print(m[l:])
								duplsize = duplsize + fisize(m[l:-1]) # finds size of duplicate files
								duplnumber = duplnumber + 1 # finds number of duplicate files
								break

				print('--------')

  	

	# checks if the names of files are the same. If so, prints them together.                    

	if results.duplname:

		names = {}

		for j in files:

			filename = ''

			i =len(j)-1

			while j[i] is not '/':	# takes the file name from its path

				filename = j[i] + filename
				i = i - 1


			if names.has_key(filename): # finds files which have the same name

				names[filename] = names.get(filename) +1
				
				duplnum = duplnum + 1
				


			else:

				names[filename] = 1
		
		for k in names.keys():	# prints files which have the same name
		
			if names.get(k) > 1:
				
				for f in files:

					if k in f:

						print(f)

				print('--------')						
	                    

	# prints remaining files

	if results.nofilelist == False:

		for j in files:

			print(j)	



	# prints some statistics about files 	             
	
	if results.stats:

		leftnumber = len(files)
		leftsize = 0      

		for j in files:
			leftsize = leftsize + fisize(j)
		
		print("total number of files visited:{}".format(totalnumber))
		print("total size of files visited in bytes:{}".format(totalsize))
		print("total number of files listed:{}".format(leftnumber))
		print("total size of files listed in bytes:{}".format(leftsize))
		
		if results.duplcont :
				duplnumber = leftnumber - duplnumber
				duplsize = leftsize - duplsize
				print("total number of unique files listed:{}".format(duplnumber))	
	                    	print("total size of unique files listed in bytes:{}".format(duplsize))
		if results.duplname :
				duplnum = leftnumber - duplnum
	    			print("total number of files with unique names:{}".format(duplnum))
	

	# zips the files to given file name in current directory	

	if results.zipfile is not None:
	
		if files:
	
	                command = 'zip '+ results.zipfile + ' ' + ' '.join(files)

	                os.system(command)

	

		

          