from typing import Self

import pyarrow.parquet as pq
import pyarrow as pa
import polars as pl

from collections.abc import Generator



field_list: list[tuple] = [
        ('a',pa.int32()),
        ('b',pa.utf8() )
    ]


pa_schema = pa.schema(field_list)

class ParqueutFileSink:

    def __init__( self: Self, stream_source: Generator[str, None], filepath: str ) -> None:
        self.stream_source: Generator[str, None] = stream_source
        self.filepath: str = filepath

    def loop_stream( self: Self ) -> None:

        with (pq.ParquetWriter(where='somefile.parquet', schema= pa_schema) as writer):
            while True:
                try:

                    ardatatype: pa.DataType
                    data = [
                        pa.array(obj=[next(self.stream_source)], type=pa.int32() )
                    ]
                    names = [
                        'a'
                    ]
                    batch= pa.record_batch(data=data, names=names)

                    writer.write(batch)
                except StopIteration:
                    break


dfpq=pl.scan_parquet('somefile.parquet')