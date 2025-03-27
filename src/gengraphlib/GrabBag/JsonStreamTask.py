import os
import json

def read_json():

    try:
        all_keys: dict[str, int] = {}

        with open( "../../../data/jctl-obj-6.json" ) as file:
            for line in file:
                obj = json.loads(line)
                for key, value in obj.items():
                    if key not in all_keys:
                        all_keys[key] = 0
                    else:
                        all_keys[key] += 1

        flipped_keys: dict[int, str] = {}

        for key, value in all_keys.items():
            flipped_keys[value] = key

        sorted_keys: dict[str,int] = {}
        for key, value in sorted(flipped_keys.items()):
            sorted_keys[value] = key

        data_str  = json.dumps(sorted_keys, indent=4)
        print(data_str)
        open( "../../../data/keys.json", "w" ).write( data_str )

    except Exception as e:
        print(f'Exception: {e}')

if __name__ == "__main__":
    os.curdir = os.path.dirname("~/proj/GenGraphLib/data")
    read_json()
