from typing import Self, Protocol

import os
import datetime as dt

from .BootLogInfo import BootLogInfo

class RepoInterface(Protocol):

    def get_sourcestream( self, repo_id: str, isbinary: bool, issource: bool ):
        pass



class BootLogDir:

    def __init__( self: Self, root_dir: str, log_rec: str ) -> None:
        super( BootLogDir, self ).__init__()
        val_list: list[str] = log_rec.split()
        self.root_dir = root_dir
        self.index: int = int( val_list[0 ] )
        self.id: str = val_list[1]
        self.first_dt: dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[3:5]))
        self.last_dt: dt.datetime = dt.datetime.fromisoformat(" ".join(val_list[7:9]))
        self.dir_name: str = self.shema_bootid()
        self.dir_path: str = os.path.join(self.root_dir, "boots", self.dir_name)
        self.keys_path: str = os.path.join( self.root_dir, "keys" )

    def boot_id( self: Self ) -> str:
        yymmdd: str = self.first_dt.strftime("%y-%m-%d")
        hhmm: str   = self.first_dt.strftime("%H-%M")
        return f"{yymmdd}:{hhmm}"

    def make_dir( self: Self ) -> bool:
        try:
            os.makedirs( self.dir_path, exist_ok=True )
            return True

        except Exception as e:
            print(f'[BootLogDirBase._dir_exists] Exception: {e}')
            return False


    def get_info( self: Self ) -> BootLogInfo:
        return BootLogInfo( schema_bootid=self.boot_id(), first_dt=self.first_dt, last_dt=self.last_dt, dir_name=self.dir_name, dir_path=self.dir_path, keys_path=self.keys_path )

    def __repr__( self: Self ) -> str:
        return f'{{idx:{self.index}, id:{self.id}, first_dt:{self.first_dt}, last_dt:{self.last_dt}, dir_name:{self.dir_name}, dir_path:{self.dir_path}, keys_filepath:{self.keys_path}}}'

    def __str__( self: Self ) -> str: return self.__repr__()




