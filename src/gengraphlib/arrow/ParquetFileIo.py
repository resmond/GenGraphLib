import pyarrow.parquet as parquet
import pyarrow as par

# def build_arrowschema( columns: dict[ str, Column ] ) -> par.schema:
#     fieldtypes = list[tuple[str, par.DataType]]()
#     for key, column in columns.items():
#         fieldtypes.append(column.get_arrowfield())
#     return par.schema(fields=fieldtypes)

def write_parquet( par_arrays: dict[ str, par.Array ], filepath: str ) -> bool:

    try:
        return True

    except IOError as ioexc:
        print(f'write_parquet( {filepath} ): IOError: {ioexc}' )
        return False

    except KeyError as exc:
        print(f'write_parquet( {filepath} ): IOError: {exc}' )
        return False

def read_parquet( filepath: str ) -> par.Table | None:
    try:
        #schema: par.Schema = build_arrowschema( columns )

        #reader =  parquet.ParquetReader( where=filepath, schema=schema )
        table: par.Table = parquet.read_table(filepath)

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
