import xmltodict
import csv
import json
import yaml
import io

def xml_utility(file):
    to_json = xmltodict.parse(file)
    return to_json

def yaml_utility(file):
    to_json = yaml.safe_load(file)
    return to_json

def csv_utility(file):
    to_json = csv.DictReader(io.StringIO(file))
    return list(to_json)

def json_converter(index, file, func):
    to_json = func(file)
    json_file = json.dumps(to_json)
    return json_file