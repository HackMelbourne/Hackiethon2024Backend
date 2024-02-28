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
                return coords
            else:
                raise("DIFFERENT LENGTHS OF COORDINATES")          
    return None

def get_moves(jsonFile):
    if not jsonFile:
        return None
    if(os.path.isfile(jsonFile)):
        # files exists, so can read
        with open(jsonFile, 'r') as f:
            data = json.load(f)
            moveData = data['state']
            return moveData           


def get_info(jsonFile, infoType):
    if not jsonFile:
        return None
    if(os.path.isfile(jsonFile)):
        # files exists, so can read
        with open(jsonFile, 'r') as f:
            data = json.load(f)
            moveData = data[infoType]
            return moveData 
    