import argparse
import PHTML_DOC_html_generation

parser = argparse.ArgumentParser()
open_type = parser.add_mutually_exclusive_group(required=True)
open_type.add_argument('-all', '--all_files', action='store_true',
                       help="Search and parse all files in given path and subdirectories of path")
open_type.add_argument('-dir', '--directory', action='store_true',
                       help="Search and parse all files in given path directory")
open_type.add_argument('-file', '--file', action='store_true', help="Search and parse one file at given path")
parser.add_argument('path', help='Path to directory  with subdirectories|directory|file')
parser.add_argument('project_name', help='User`s name for project')
parser.add_argument('destination_folder',
                    help='Path to folder where html files will be saved, if folder not exists, creates it')
parser.add_argument('version', help='User`s version num of project')
parser.add_argument('del_html',
                    help='If True: deletes all html files in destination folder, if False: just add html files '
                         'to html files that already exist in destination folder')
args = parser.parse_args()
if args.all_files:
    PHTML_DOC_html_generation.document_all_files(args.path, args.destination_folder, args.project_name, args.version,
                                                 args.del_html)
elif args.file:
    PHTML_DOC_html_generation.document_one_file(args.path, args.destination_folder, args.project_name, args.version,
                                                args.del_html)
elif args.directory:
    PHTML_DOC_html_generation.document_files_from_dir(args.path, args.destination_folder, args.project_name,
                                                      args.version, args.del_html)
