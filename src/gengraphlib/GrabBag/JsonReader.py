import os
import json
import JsonAnalysis as ja
from progress.bar import Bar

def read_json(filepath: str):

    try:
        all_keys: dict[str, int] = {}

        bar = Bar("Processing", max=125145)
        with open( filepath ) as file:

            for line in file:
                obj = json.loads(line)
                for key, value in obj.items():
                    if key not in all_keys:
                        all_keys[key] = 1
                    else:
                        all_keys[key] += 1

                    json_name = ja.log_to_json[key]
                    if json_name and ja.capture_flags[key]:
                        ja.print_dict[json_name].append(value)

                bar.next()

        bar.finish()

        flipped_keys: dict[int, str] = {}

        for key, value in all_keys.items():
            flipped_keys[value] = key

        sorted_keys: dict[str,int] = {}
        for key, value in sorted(flipped_keys.items()):
            sorted_keys[value] = key

        data_str  = json.dumps(sorted_keys, indent=4)
        print(data_str)
        open( "/home/richard/data/jctl-logs/keys/keys.json", "w+" ).write( data_str )

        for key, value in ja.print_dict.items():
            key_str = json.dumps(value, indent=4)

            with open(f'/home/richard/data/jctl-logs/keys/{key}.json', key_str) as keyfile:
                keyfile.write(key_str)

        for key, value in ja.capture_flags:
            if value:
                os.mkdir(f'/home/richard/data/jctl-logs/keys/{key}')
                with open(f'/home/richard/data/jctl-logs/keys/{key}/keys.json', 'w+') as keyfile:
                    keyline = ja.log_to_json[key]
                    key_str = json.dumps(keyline, indent=4)
                    keyfile.write(key_str)




    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    os.curdir = "/home/richard/data/jctl-logs/"
    read_json("/home/richard/data/jctl-logs/boots/2025-03-25T17:30:40/jctl-0.json")
