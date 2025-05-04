import pyarrow as par
import pyarrow.parquet as parquet

ModelResults: type = dict[ str, par.Array ]

class ArrowResults:
    models: dict[ str, ModelResults ] = {}

    @classmethod
    def store_results( cls, model_id: str, name: str, par_array: par.Array ) -> None:
        if model_id not in ArrowResults.models:
            ArrowResults.models[ model_id ] = ModelResults()

        ArrowResults.models[ model_id ][ name ] = par_array

    @classmethod
    def write_arrowtable( cls, model_id: str, filepath: str ) -> None:
        try:
            model_results = ArrowResults.models[ model_id ]
            if model_results:
                column_names: list[str] = []
                arrow_arrays: list[par.Array] = []
                for name, array in model_results.items():
                    column_names.append( name )
                    arrow_arrays.append( array )

                arrow_table = par.Table( arrays=arrow_arrays, names=column_names)
                parquet.write_table(table=arrow_table, where=filepath)
            else:
                breakpoint()

        except KeyError as keyerr:
            breakpoint()
            print(f"DataTableModel.save_arrowtable( {filepath} ): Excption - {keyerr}")

        except Exception as ext:
            breakpoint()
            print(f"DataTableModel.save_arrowtable( {filepath} ): Excption - {ext}")

    @classmethod
    def get_modelresults( cls, model_id: str ) -> ModelResults | None:
        return ArrowResults.models[ model_id ]

