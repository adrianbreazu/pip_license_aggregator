# pip_license_aggregator
I needed a script that will aggregate multiple requirement.txt files and search for the license type (combination library + version)

Input files should be the output of '''pip freeze ''' command

Input parameters:
-path  : provide the path to the requirements.txt files
-o : provide the path to the output file, else it will be place on the current working directory

Sample execution:
''' python3 create_license_list.py -path /path/to/requirements_file/ -o /path/to/output '''
