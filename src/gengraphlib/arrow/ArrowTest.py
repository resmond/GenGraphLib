import pyarrow.parquet as parquet
import pyarrow as par
import os
import sys

from src.gengraphlib.common import KeyInfo, KeyType
from hold.columns.StrColumn import StrColumn

def arrow_test() -> None:

    try:
        boot_dir = "/home/richard/data/jctl-logs/boots/25-04-27:06-44"
        message  = KeyInfo(keytype=KeyType.KStr,pytype=str,partype=par.utf8(),key="message",alias="_MESSASE",groupids=["evt"])
        msg_col = StrColumn( message, boot_dir, True )
        par_msg: par.Array = msg_col.get_pararray()

        priority = KeyInfo(keytype=KeyType.KStr,pytype=str,partype=par.utf8(),key="priority",alias="_MESSASE",groupids=["evt"])
        pri_col = StrColumn( priority, boot_dir, True )
        par_pri: par.Array = pri_col.get_pararray()

        test_dir = "/home/richard/data/jctl-logs/boots/"

        msgpri_table = par.table( [par_msg, par_pri], ["message", "priority"]  )
        parquet.write_table(table=msgpri_table, where=f'{test_dir}msgpri.table' )
        print( f'write_table( {test_dir}msgpri.table ) - sizeof: {os.path.getsize(f'{test_dir}msgpri.table')}' )
        print( f'array: {sys.getsizeof(par_msg)} + {sys.getsizeof(par_pri)} ' )
        print( f'table: {sys.getsizeof(msgpri_table)}' )
        print()

        msg_table = par.table( [par_msg], ["message"]  )
        parquet.write_table(table=msg_table, where=f'{test_dir}msg.table' )
        print( f'write_table( {test_dir}msg.table ) - sizeof: {os.path.getsize(f'{test_dir}msg.table')}' )
        print( f'table: {sys.getsizeof(msg_table)}' )
        print()

        pri_table = par.table( [par_pri], ["priority"]  )
        parquet.write_table(table=pri_table, where=f'{test_dir}pri.table' )
        print( f'write_table( {test_dir}pri.table ) - sizeof: {os.path.getsize(f'{test_dir}pri.table')}' )
        print( f'table: {sys.getsizeof(msg_table)}' )

        print()

    except IOError as ioexc:
        print(f'write_parquet IOError: {ioexc}' )

    except KeyError as exc:
        print(f'write_parquet IOError: {exc}' )

    except Exception as ex:
        print(f'write_parquet IOError: {ex}' )

if __name__ == "__main__":
    arrow_test()