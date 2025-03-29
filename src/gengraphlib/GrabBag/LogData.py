import subprocess

from typing import Self
from dataclasses import dataclass

#from json import JSONDecodeError
import datetime as dt
import io as io
import os as os
import json as js

from MyTextBuffer import MyBufferedFile

#BootLine = namedtuple("BootLine", ("idx", "id", "first", "last"))

@dataclass
class BootRecord:
    idx: int
    id: str
    first_dt: dt.datetime | None = None
    last_dt: dt.datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return BootRecord(idx=d["idx"], id=d["id"], first_dt=d["first_dt"], last_dt=d["last_dt"])

    def __repr__(self: Self ) -> str:
        return f'{{"idx":{self.idx}, "id":"{self.id}", "first_dt":"{self.first_dt}", "last_dt":"{self.last_dt}"}}'
    def __str__(self) -> str: return self.__repr__()

class LogDataRoot(object):

    def __init__(self: Self, root_dir: str) -> None:
        self.root_dir = root_dir
        self._load_boots: list[BootRecord] = list[BootRecord]()
        super().__init__()

    def parse_bootrefs( self: Self, boots_file_name: str ) -> bool:
        try:
            file_path = os.path.join(self.root_dir, boots_file_name)
            with (open( file_path ) as file):
                first_line: bool = True

                for line in file:

                    val_list: list[str] = line.split()
                    if not first_line:
                        idx: str = val_list[0]
                        id: str = val_list[1]
                        first: str = " ".join(val_list[3:5])
                        last: str = " ".join(val_list[7:9])
                        boot_line = BootRecord(int(idx), id, dt.datetime.fromisoformat(first), dt.datetime.fromisoformat(last))
                        self._load_boots.append(boot_line)
                    else:
                        first_line: bool = False

            self._load_boots.reverse()

            return True

        except Exception as e:
            print(f'[parse_bootrefs] Exception: {e}')
            return False

    def dump_bootrefs( self: Self, jline_file: str ) -> bool:
        try:
            file_path = os.path.join( self.root_dir, jline_file )
            with open( file_path, "w", newline='\n' ) as file:
#                file.writelines( self._load_boots )

                for boot_rec in self._load_boots:
                    file.write( boot_rec.__repr__() )
                    file.write('\n')

            return True 
        except Exception as e:
            print(f'[dump_bootrefs] Exception: {e}')
            return False

    def load_jfile( self: Self, jline_file: str ) -> bool:
        try:
            file_path = os.path.join( self.root_dir, jline_file )
            with io.open( file_path ) as file:
                for line in file:
                    self._parse_bootref( line )

            return True
        except Exception as e:
            print(f'[load_jfile] Exception: {e}')
            return False


    def _parse_bootref( self: Self, ref_line: str ) -> bool:
        try:
            ref_dict = js.loads( ref_line.strip() )
            first_dt: dt.datetime = dt.datetime.fromisoformat(ref_dict["first_dt"])
            last_dt: dt.datetime = dt.datetime.fromisoformat(ref_dict["last_dt"])
            boot_rec = BootRecord( idx=int(ref_dict["idx"]), id=ref_dict["id"],first_dt=first_dt, last_dt=last_dt )
            self._load_boots.append(boot_rec)
            return True
        except js.JSONDecodeError as e:
            print(f'[_parse_bootref] JSONDecodeError: {e}')
            print(f'[{e.colno}={ref_line[e.colno]}]: {ref_line}')
            return False

    def make_dir( self: Self, idx: int ) -> bool:
        try:
            boot_rec = self._load_boots[idx]
            dir_name = boot_rec.first_dt.isoformat()
            dir_path = os.path.join(self.root_dir, dir_name)
            os.makedirs( dir_path, exist_ok=True )
            return True

        except Exception as e:
            print(f'[make_dir] Exception: {e}')
            return False

    def export_log( self: Self, idx: int ) -> bool:
        try:
            boot_rec = self._load_boots[idx]
            dir_name = boot_rec.first_dt.isoformat()
            dir_path = os.path.join(self.root_dir, dir_name)

            journalctl_cmd = f"journalctl -b {idx} -o json"


            #with open( output_file_name, 'w' ) as file:

            output_file_name = os.path.join( dir_path, f"test-{idx}.json" )

            with MyBufferedFile(output_file_name) as file:
                result = subprocess.run(args=journalctl_cmd, shell=True, cwd=dir_path)

                st_err = result.stderr
                print(f'stderr: {st_err}')

            return True

        except Exception as e:
            print(f'[make_dir] Exception: {e}')
            return False


def load_bootlist( log_root: str ) -> bool:
    log_root = LogDataRoot(log_root)
    if log_root.parse_bootrefs( "bootlist.txt" ):
        log_root.dump_bootrefs("bootlist.jline")

    return True

def make_bootdirs( log_root: str ) -> bool:
    log_root = LogDataRoot(log_root)
    if log_root.load_jfile("bootlist.jline"):
        if log_root.make_dir( 0 ):
            log_root.export_log( 0 )
            
    return True

if __name__ == "__main__":
    parse = False
    if parse:
        load_bootlist( "/home/richard/data/jctl-logs/boots" )
    else:
        make_bootdirs( "/home/richard/data/jctl-logs/boots" )



