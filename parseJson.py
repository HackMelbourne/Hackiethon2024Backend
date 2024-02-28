import json
import os

def get_coordinates(jsonFile):
    if not jsonFile:
        return None
    if(os.path.isfile(jsonFile)):
        # files exists, so can read
        with open(jsonFile, 'r') as f:
            data = json.load(f)
            x_data = data['xCoord']
            y_data = data['yCoord']
            if len(x_data) == len(y_data):
                coords = []
                coord_length = len(x_data)
                for i in range(coord_length):
                    coords.append((x_data[i], y_data[i]))
                        
            else:
                raise("DIFFERENT LENGTHS OF COORDINATES")
            
    return None

get_coordinates("jsonfiles\p1.json")
