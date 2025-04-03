import os
import json
from src.gengraphlib.logs import KeyGraph as ja
from progress.bar import Bar

def read_json(filepath: str):

 #   try:
        all_keys: dict[str, int] = {}

        bar = Bar("Processing", max=125145)
        with open( filepath ) as file:

            for line in file:
                obj = json.loads(line)
                for key, values_set in obj.items():
                    if key not in ja.log_to_json:
                        if key not in all_keys:
                            all_keys[key] = 1
                        else:
                            all_keys[key] += 1
                    else:
                        json_name = ja.log_to_json[key]
                        if json_name and ja.capture_flags[key]:
                            ja.values_bykeys_set[json_name ].append( values_set )

                bar.next()

        bar.finish()

        flipped_keys: dict[int, str] = {}

        for key, values_set in all_keys.items():
            flipped_keys[values_set] = key

        sorted_keys: dict[str,int] = {}
        for key, values_set in sorted(flipped_keys.items()):
            sorted_keys[values_set] = key

        data_str  = json.dumps(sorted_keys, indent=4)
        print(data_str)
        open( "/home/richard/data/jctl-logs/keys/missedkeys.json", "w" ).write( data_str )

        for key, values_set in ja.values_bykeys_set.items():
            if not os.path.exists(f"/home/richard/data/jctl-logs/keys/{key}"):
                os.mkdir(f"/home/richard/data/jctl-logs/keys/{key}")

            with open(f'/home/richard/data/jctl-logs/keys/{key}/{key}.json', "w") as keyfile:
                for value_line in values_set:
                    value_line_json = json.dumps(value_line, indent=4)
                    keyfile.write(value_line_json)
                    keyfile.write("\n")

"""
        for key, value in ja.capture_flags:
            if value:
                os.mkdir(f'/home/richard/data/jctl-logs/keys/{key}')
                with open(f'/home/richard/data/jctl-logs/keys/{key}/keys.json', 'w+') as keyfile:
                    keyline = ja.log_to_json[key]
                    key_str = json.dumps(keyline, indent=4)
                    keyfile.write(key_str)
"""



#    except Exception as e:
#        print(f"Exception: {e}")

if __name__ == "__main__":
    os.curdir = "/home/richard/data/jctl-logs/"
    read_json("/home/richard/data/jctl-logs/boots/2025-03-25T17:30:40/jctl-0.json")
