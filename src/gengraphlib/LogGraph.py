import json
import os
from typing import Self
from progress.bar import Bar
import asyncio as aio

from JsonLogGraph import KeyGraphRootBase, StrKeyDef, IntKeyDef, BoolKeyDef, TmstKeyDef
from LogDirManager import LogDirManagerBase, ManagerCmd
from fileparse.PipedBases import PipeFromStdoutBase
from logs.BootLogDir import BootLogDirBase, BootRecordBase
from src.gengraphlib.logs.BootLogDir import BootRecCmd


class PipedToGraph(PipeFromStdoutBase):
    def __init__( self: Self, output_filepath: str ) -> None:
        super(PipedToGraph, self).__init__("PipedToKeys", output_filepath )

    async def process_line( self: Self, line: str ) -> bool:
        try:
            print(line)
            return True

        except Exception as exc:
            print(f'[PipedToFile: {self.name}] Exception: {exc}')
            self.started = False
            self.error = -3
            return False

    def __getitem__(self, item) -> tuple[bytes,bytes] | None:
        return self.proc_result

    def run_export( self: Self) -> None:
        self.run_command( "" )

class GraphBootRec(BootRecordBase):

    def __init__(self: Self, root_dir: str, boot_rec: BootRecordBase) -> None:
        super(GraphBootRec, self).__init__( root_dir, boot_rec )

class GraphLogDir( BootLogDirBase ):
    def __init__(self: Self, root_dir: str, boot_rec: GraphBootRec) -> None:
        super( GraphLogDir, self ).__init__( root_dir, boot_rec )
        self.keys_filepath = os.path.join( self.dir_path, "dirkeys.json" )
        self.journalPipe = PipedToGraph(self.keys_filepath)

    def export_topipe( self: Self ) -> bool:
        try:
            boot_id = self.boot_rec.id
            if self._dir_exists():
                # list[str] = [f"journalctl -b {boot_id} -o json","| python3 KeyMaps.py", f"> {self.keys_filepath}"]
                journalctl_cmd: str = f"journalctl -b {boot_id} -o json > {self.keys_filepath}"
                self.journalPipe.run_command( journalctl_cmd )

            return True

        except Exception as ext:
            print(f'[export_log] Exception: {ext}')
            return False

    def exec_cmd( self: Self, cmd: BootRecCmd ) -> bool:
        return False

class GraphLogDirManager( LogDirManagerBase ):

    def __init__( self: Self, root_dir: str ) -> None:
        super( GraphLogDirManager, self ).__init__( root_dir )

    def process_dir(self: Self, boot_rec: GraphBootRec) -> bool:
        #boot_rec.bootlog_dir.log_fromquery()
        return True


class LogGraph( KeyGraphRootBase ):
    def __init__( self: Self, _log_root: str ) -> None:
        super( LogGraph, self ).__init__( _log_root )
        self.dir_manager: GraphLogDirManager = GraphLogDirManager( _log_root )
        self.add_keydefs([
            StrKeyDef( "sysUnit", "_SYSTEMD_UNIT" ),                                  # id?
            StrKeyDef( "usrUnit", "UNIT" ),                                           # id?
            StrKeyDef( "udSName", "_UDEV_SYSNAME" ),                                  # id?
            StrKeyDef( "udDvNd", "_UDEV_DEVNODE" ),                                   # id?
            StrKeyDef( "krSubSys", "_KERNEL_SUBSYSTEM" ),                             # id?
            IntKeyDef( "tID", "TID" ),                                                # id?
            StrKeyDef( "comm", "_COMM" ),
            StrKeyDef( "slID", "SYSLOG_IDENTIFIER" ),                                 # id?
            TmstKeyDef( "srTime", "_SOURCE_REALTIME_TIMESTAMP" ),
            StrKeyDef( "sysFac", "SYSLOG_FACILITY" ),
            BoolKeyDef( "lnBk", "_LINE_BREAK" ),
            StrKeyDef( "cmdLn", "_CMDLINE" ),
            StrKeyDef( "usrInvID", "USER_INVOCATION_ID" ),                            # id?
            StrKeyDef( "glbLogApi", "GLIB_OLD_LOG_API" ),
            StrKeyDef( "nmDev", "NM_DEVICE" ),                                        # id?
            StrKeyDef( "glbDom", "GLIB_DOMAIN" ),                                     # id?
            StrKeyDef( "nmLogLev", "NM_LOG_LEVEL" ),
            StrKeyDef( "jbRes", "JOB_RESULT" ),
            StrKeyDef( "smTime", "_SOURCE_MONOTONIC_TIMESTAMP" ),
            StrKeyDef( "jbID", "JOB_ID" ),                                            # id?
            StrKeyDef( "jbType", "JOB_TYPE" ),
            StrKeyDef( "invID", "INVOCATION_ID" ),                                    # id?
            StrKeyDef( "slTime", "SYSLOG_TIMESTAMP" ),
            StrKeyDef( "msgID", "MESSAGE_ID" ),                                       # id?
            StrKeyDef( "slPID", "SYSLOG_PID" ),                                       # id?
            StrKeyDef( "sysdUsrUnit", "_SYSTEMD_USER_UNIT" ),                         # id?
            StrKeyDef( "ssysdUwnUID", "_SYSTEMD_OWNER_UID" ),                         # id?
            StrKeyDef( "strmID", "_STREAM_ID" ),                                      # id?
            StrKeyDef( "audSes", "_AUDIT_SESSION" ),
            StrKeyDef( "cdFn", "CODE_FUNC" ),
            StrKeyDef( "cdLn", "CODE_LINE" ),
            StrKeyDef( "cdFl", "CODE_FILE" ),
            StrKeyDef( "sysdInvID", "_SYSTEMD_INVOCATION_ID" ),                       # id?
            StrKeyDef( "exe", "_EXE" ),                                               # id?
            StrKeyDef( "sysdSLc", "_SYSTEMD_SLICE" ),                                 # id?
            StrKeyDef( "slnxCtx", "_SELINUX_CONTEXT" ),                               # id?
            StrKeyDef( "uID", "_UID" ),                                               # id?
            StrKeyDef( "cur", "__CURSOR" )
        ])
        self.new_keygroup_with_keys("ids", [
            "sysUnit",
            "usrUnit",
            "udSName",
            "udDvNd",
            "krSubSys",
            "tID",
            "slID",
            "usrInvID",
            "nmDev",
            "glbDom",
            "jbID",
            "invID",
            "msgID",
            "slPID",
            "sysdUsrUnit",
            "ssysdUwnUID",
            "strmID",
            "exe",
            "sysdSLc",
            "sysdInvID",
            "slnxCtx",
            "uID"
        ])

    def read_json(self: Self, filepath: str):
        try:
            line_num: int = 0
            read_len: int = 0
            file_size: int = os.path.getsize(filepath)
            bar = Bar("Processing", max=file_size)
            with open(filepath) as file:
                for line in file:
                    read_len += len(line)
                    field_dict = json.loads(line)
                    self.process_fields(field_dict, line_num)
                    bar.next(read_len )
            bar.finish()
        except FileNotFoundError as ext:
            print(f'[JsonLogKeyGraph.read_json]FileNotFoundError: {ext} - {filepath}')

    async def exec_query( self: Self, exec_cmd: ManagerCmd, specific_ndx: int ) -> bool:
        await self.dir_manager.exec( exec_cmd, specific_ndx )
        return True

if __name__ == "__main__":
    print("[LogGraph] starting main")

#    try:
    log_root: str = "/home/richard/data/jctl-logs"
    key_graph = LogGraph( log_root )
    aio.run( key_graph.exec_query( ManagerCmd.Full, 1 ) )

#    except Exception as e:
#        print(f"[LodDirManager] Exception: {e}")

    print("[LogGraph] done")
