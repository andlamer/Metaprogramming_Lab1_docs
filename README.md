metaLab1
Usage: cd to folder with lab files python PHTML_DOC_Interface.py -h -- for help

usage: PHTML_DOC_Interface.py [-h] (-all | -dir | -file) path project_name destination_folder version del_html

positional arguments: 
	path Path to directory with subdirectories|directory|file 
	project_name User's name for project 
	destination_folder Path to folder where html files will be saved, if folder not exists, creates it 
	version User's version num of project 
	del_html If True: deletes all html files in destination folder, if False: just add html files to html files that already exist in destination folder

optional arguments: -h, --help show this help message and exit 
-all, --all_files Search and parse all files in given path and subdirectories of path 
-dir, --directory Search and parse all files in given path directory 
-file, --file Search and parse one file at given path