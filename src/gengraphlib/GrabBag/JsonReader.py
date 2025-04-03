import os
import json
from src.gengraphlib import JsonLogGraph as ja

def read_json(filepath: str):

 #   try:

        bar = Bar("Processing", max=125145)
        with open( filepath ) as file:

            for line in file:
                field_dict = json.loads(line)


                bar.next()

        bar.finish()


        #data_str  = json.dumps(sorted_keys, indent=4)
        #print(data_str)
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
