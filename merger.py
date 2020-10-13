import json

def merger(data):

    merged_json = []

    for json_list in data:
        if 'dataset' in json.loads(json_list):
            for value in json.loads(json_list)['dataset']['record']:
                merged_json.append(value)
        else:
            for value in json.loads(json_list):
                merged_json.append(value)

    return merged_json