import utility
import json

def convert_to_json(data):
    for indx, data_file in enumerate(data):
        if "xml" in data_file[1]:
            data[indx] = utility.json_converter(indx, data_file[0], utility.xml_utility)
        elif "yaml" in data_file[1]:
            data[indx] = utility.json_converter(indx, data_file[0], utility.yaml_utility)
        elif "csv" in data_file[1]:
            data[indx] = utility.json_converter(indx, data_file[0], utility.csv_utility)
        elif "json" in data_file[1]:
            data[indx] = data_file[0]

            if data[indx][len(data[indx]) - 3] == ',':
                tmp = list(data[indx])
                del tmp[len(data[indx]) - 3]
                data[indx] = ''.join(tmp)

    return data