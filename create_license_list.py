import argparse
import os
import pprint
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-path', help="path to the directory")
parser.add_argument('-o', help="path to file output")
args = parser.parse_args()
SEPARATOR = "=="
OUTPUTFILE = "aggregated_ouptut.csv"
MAIN_URL = "https://pypi.org/project/"

def main():
    full_path = args.path
    output_path = args.o
    files = [] 
    for _file in os.listdir(full_path):
        files.append(os.path.join(full_path, _file))
    for item in files:
        parse_requirement_file(item)
    #print("And here's the output:")
    #pprint.pprint(library_dict)
    export_data(output_path)


def parse_requirement_file(file_path):
    print ("Parse file: {0}".format(file_path))
    with open(file_path, "r") as file_handler:
        for line in file_handler:
            try:
                library = line.splitlines()[0].split(SEPARATOR)[0]
                version = line.splitlines()[0].split(SEPARATOR) [1]
                if library in library_dict:
                    array_value = library_dict[library]
                    if not version in array_value:
                        array_value.append(version)
                        library_dict[library] = array_value
                else:
                    library_dict[library] = version.split("|") #fu.. just make an array, to lazy
            except IndexError:
                print ("Index error on file: {0}".format(file_path))


def export_data(path):
    if path == None:
        print("Man don't be lazy use -o and add output path")
        path = os.getcwd()
    
    with open(os.path.join(path, OUTPUTFILE), 'w') as file_handler:
        for key in library_dict:
            for item in library_dict[key]:
                license_type, license_url = scrap_for_license(key, item)
                file_handler.writelines("{0}|{1}|{2}|{3}\n".format(key,item, license_type, license_url))


#TODO make it more generic
def scrap_for_license(library, version):
    try:
        url = MAIN_URL + library + "/" + version + "/"
        print("Extract data from url: {0}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        value = str(soup.find('strong', text='License:').parent)
        value = value.replace('<p><strong>License:</strong> ', '')
        value = value.replace('</p>', '')
        #try to avoid spam detectors
        time.sleep(1)
        return value, url
    except Exception:
        return "Unable to find license !", ""


if __name__ == "__main__":
    library_dict = {}
    print ("-------- start --------")
    main()
    print ("-------- finished --------")