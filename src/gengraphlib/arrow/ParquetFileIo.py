import os

import pyarrow.parquet as parquet
import pyarrow as par

from loguru import logger

# def build_arrowschema( columns: dict[ str, Column ] ) -> par.schema:
#     fieldtypes = list[tuple[str, par.DataType]]()
#     for key, column in columns.items():
#         fieldtypes.append(column.get_arrowfield())
#     return par.schema(fields=fieldtypes)

default_dir:      str = '/home/richard/data/jctl-logs/boots/25-04-27:22-28/'
default_filename: str = 'logevents.parquet'

def get_filepath( filepath: str | None = None, filename: str | None = None ) -> str:
    if not filepath and not filename:
        return os.path.join( default_dir, default_filename )
    else:
        if filename:
            return os.path.join( default_dir, filename )
        else:
            return filepath

def write_pararrays( par_arrays: dict[ str, par.Array ], **kwargs ) -> bool:
    filepath = get_filepath(**kwargs)
    logger.info(f"Writting parquet file - {filepath}")
    try:
        if filepath and filepath != "":
            if len(par_arrays) > 0:
                column_names: list[str] = []
                arrow_arrays: list[par.Array] = []
                for name, array in par_arrays.items():
                    column_names.append(name)
                    arrow_arrays.append(array)

                arrow_table = par.Table(arrays=arrow_arrays, names=column_names)
                parquet.write_table(table=arrow_table, where=filepath)
                return True
            else:
                logger.error("par_arrays is missing or empty")
                return False
        else:
            logger.error("Missing filepath")
            return False

    except IOError as ioexc:
        logger.error(f"write_parquet( {filepath} ): IOError: {ioexc}")
        return False

    except KeyError as exc:
        logger.error(f"write_parquet( {filepath} ): IOError: {exc}")
        return False

def read_parquet( **kwargs ) -> par.Table | None:
    filepath = get_filepath(**kwargs)
    try:
        logger.info(f"reading parquet file - {filepath}")

        table: par.Table = parquet.read_table(filepath)
        return table

    except IOError as ioexc:
        logger.error(f'read_parqueut( {filepath} ): IOError: {ioexc}' )
        return None

    except KeyError as exc:
        logger.error(f'read_parqueut( {filepath} ): IOError: {exc}' )
        return None

#reader =  parquet.ParquetReader( where=filepath, schema=schema )
#
# schema = par.schema([par.field("nums", self.store_type)])
# with par.OSFile(f"/home/richard/data/jctl-logs/boots/{self.name}.arrow", "wb") as sink:
#     with par.ipc.new_file(sink, schema=schema) as writer:
#         batch = par.record_batch(self.par_array, schema=schema)
#         writer.write(batch)

#dfpq=pol.scan_parquet( 'somefile.parquet' )

# data = [par.array( obj=[ next( self.stream_source ) ], type=par.int32() )]                 ]
# names = ['a' ]
# batch= par.record_batch( data=data, names=names )
