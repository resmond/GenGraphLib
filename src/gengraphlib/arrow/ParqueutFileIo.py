from typing import Any

import pyarrow.parquet as parquet
import pyarrow as par

from ..columns import Column

def build_arrowschema( columns: dict[ str, Column ] ) -> par.schema:
    fieldtypes = list[tuple[str, par.DataType]]()
    for key, column in columns:
        fieldtypes.append(column.get_arrowfield())
    return par.schema(fields=fieldtypes)

def write_parquet( columns: dict[ str, Column ], filepath: str ) -> bool:

    try:
        dataarrays_map = dict[str, list[Any]]()
        fieldtypes = list[ tuple[str, par.DataType] ]()
        for key, column in columns.items():
            arrowdata = column.get_arrowdata()
            if arrowdata:
                datatype, dataarray, use_dict = arrowdata
                fieldtypes.append( ( key, datatype ) )
                dataarrays_map[key] = dataarray

        arrow_schema = par.schema( fields=fieldtypes )

        with parquet.ParquetWriter( where=filepath, schema=arrow_schema ) as writer:
            batch = par.record_batch( data=dataarrays_map, schema=arrow_schema )
            writer.write(batch)

        return True

    except IOError as ioexc:
        print(f'write_parquet( {filepath} ): IOError: {ioexc}' )
        return False

    except KeyError as exc:
        print(f'write_parquet( {filepath} ): IOError: {exc}' )
        return True

def read_parquet( columns: dict[ str, Column ], filepath: str ) -> par.Table | None:
    try:
        schema: par.Schema = build_arrowschema( columns )

        table: par.Table | None = None

        with parquet.ParquetReader( where=filepath, schema=schema ) as reader:
            table = reader.read_all()

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
