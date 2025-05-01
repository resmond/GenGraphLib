from typing import Any

import sys
import os
import pyarrow.parquet as parquet
import pyarrow as par

from ..columns import Column

def build_arrowschema( columns: dict[ str, Column ] ) -> par.schema:
    fieldtypes = list[tuple[str, par.DataType]]()
    for key, column in columns.items():
        fieldtypes.append(column.get_arrowfield())
    return par.schema(fields=fieldtypes)

def write_parquet( columns: dict[ str, Column ], filepath: str, print_info: bool = False ) -> bool:

    try:
        fieldtypes = list[ tuple[str, par.DataType] ]()


        # dataarrays_map = dict[str, list[Any]]()
        # for key, column in columns.items():
        #     arrowdata = column.get_arrowdata()
        #     if arrowdata:
        #         datatype, dataarray, use_dict = arrowdata
        #         fieldtypes.append( ( key, datatype ) )
        #         dataarrays_map[key] = dataarray

        dataarrays_map = dict[str, par.Array]()
        dataarrays = list[par.Array]()
        keyslist = list[str]()
        for key, column in columns.items():
            keyslist.append(key)
            field = column.get_arrowfield()
            fieldtypes.append( field )
            par_array = column.get_pararray()
            dataarrays.append( par_array )
            dataarrays_map[ key ] = par_array
            print(f'{key} ( {field} ) - {par_array}')

        arrow_schema = par.schema( fields=fieldtypes )

        if print_info or True:
            for datatype in fieldtypes:
                print( f'{datatype[0]}: {datatype[1]}' )
            for key, data in dataarrays_map.items():
                print( f'{key}: [{len(data)}] - {sys.getsizeof(data)}' )

        table = par.Table.from_arrays( arrays=dataarrays, names=keyslist  )
        print( f'table: {table} size: {sys.getsizeof(table)}' )  

        parquet.write_table(table=table, where=filepath)
        print( f'write_table( {filepath} ) - sizeof: {os.path.getsize(filepath)}' )


        # with parquet.ParquetWriter( where=filepath, schema=arrow_schema ) as writer:
        #     batch = par.record_batch( data=dataarrays_map, schema=arrow_schema )
        #     writer.write(batch)

        return True

    except IOError as ioexc:
        print(f'write_parquet( {filepath} ): IOError: {ioexc}' )
        return False

    except KeyError as exc:
        print(f'write_parquet( {filepath} ): IOError: {exc}' )
        return True

def read_parquet( columns: dict[ str, Column ], filepath: str ) -> par.Table | None:
    try:
        #schema: par.Schema = build_arrowschema( columns )

        table: par.Table | None = None

        #reader =  parquet.ParquetReader( where=filepath, schema=schema )
        table = parquet.read_table(filepath)

        return table

    except IOError as ioexc:
        print(f'read_parqueut( {filepath} ): IOError: {ioexc}' )
        return None

    except KeyError as exc:
        print(f'read_parqueut( {filepath} ): IOError: {exc}' )
        return None



#dfpq=pol.scan_parquet( 'somefile.parquet' )


# data = [par.array( obj=[ next( self.stream_source ) ], type=par.int32() )]                 ]
# names = ['a' ]
# batch= par.record_batch( data=data, names=names )
