# filetraverse

filelist that traverses directories and reports path names of files that satisfies some search criteria. The program is implemented in Python3. It is invoked as follows on the console:
	python filelist.py [options] [directory-list]
The arguments in [ ] are optional. If they are not given, the default action will be carried out. If no directory list is given, the default is the current directory. If no option arguments are given, pathnames of all files will be printed by the program.
-before datetime
This option prints the files last modified before a date (YYYYMMDD) or a date time (YYYYMMDDTHHMMSS). You must use this option in the following form:
-before YYYYMMDD or –before YYYYMMDDTHHMMSS
-after datetime
This option prints the files last modified after a date (YYYYMMDD) or a date time (YYYMMDDTHHMMSS). You must use this option in the following form:
-after YYYYMMDD or –before YYYYMMDDTHHMMSS
-match <pattern>
The match option prints the files which has a name matched with the given pattern. Pattern is a Python regular expression as ‘.\wt’. You can invoke this option like that:
-match ‘.\wt’
-bigger <int>
The bigger option prints the files having sizes greater than or equal to <int> bytes. <int> can also be given as kilobytes, megabytes and gigabytes, for example as, 2K, 3M, 7G.
-bigger 3K
-smaller <int>
The smaller option prints the files having sizes less than or equal to <int> bytes. <int> can also be given as kilobytes, megabytes and gigabytes, for example as, 2K, 3M, 7G.
-smaller 3K


-delete
The delete option deletes the files in given directory recursively. –duplname or –duplcont or –zip cannot use with –delete. If –duplcont and –duplname and -zip options are given with –delete, it gives an error message. It does not take any additional arguments, as:
-delete
-zip <zipfile>
This option packs files in <zipfile> as a zip. It creates zip file in current directory. Using with –delete option gives an error message. You should use in following form:
-zip myzipfile
-duplcont
This option prints the files whose contents are the same. It prints in sorted order with separated with a sequence of ----- characters. It does not take any additional arguments. Using with –delete option gives an error message. You should use in following form:
-duplcont 
-duplname
This option prints the files whose names are the same. It prints in sorted order with separated with a sequence of ----- characters. It does not take any additional arguments. Using with –delete option gives an error message. You should use in following form:
-duplname
-stats
It traverses the remaining files and prints the statistics. The statistics include total number of files visited, total size of files visited in bytes, total number of files listed, total size of files listed in bytes. Using with –delete option gives an error message. If –duplcont option is given, it also prints, total number of unique files listed, total size of unique files in bytes. If –duplname option is given, it also prints total number of files with unique names. It does not take any additional arguments. It is in form like:
-stats
-nofilelist
 When this option is given, nothing is printed on the screen except the statistics. 


