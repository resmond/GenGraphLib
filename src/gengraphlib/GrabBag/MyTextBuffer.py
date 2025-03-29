from abc import ABC

from typing import Self, Any, TextIO, overload

import io

class MyBufferedWritter(io.BufferedWriter, ABC):

    def __init__(self, *args, **kwargs):
        raw_io = io.RawIOBase()
        super().__init__(raw=raw_io,*args, **kwargs)
        #self.buffer = buffer

    def write(self, data: Any) -> int:
        return super().write(data)

    def flush(self) -> None:
        pass

    def close(self) -> None:
        pass

    def isatty(self) -> bool:
        return False

    def fileno(self) -> int:
        return -1

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return False

    def writable(self) -> bool:
       return True

    def tell(self) -> int:
        return 0









class MyBufferedFile(TextIO):


    def isatty( self ):
        pass

    def read( self, n = -1, / ):
        pass

    def readable( self ):
        pass

    def readline( self, limit = -1, / ):
        pass

    def readlines( self, hint = -1, / ):
        pass

    def seekable( self ):
        pass

    def tell( self ):
        pass

    def __next__( self ):
        pass

    def __iter__( self ):
        pass


    def __init__(self: Self, file_path: str, *args, **kwargs) -> None:
        self.file = open(file_path, 'w')
        self.writter = MyBufferedWritter(*args, **kwargs)
        super().__init__()

    def __enter__( self ) -> TextIO:
        #x = super().__enter__()
        return self.file


    def __exit__( self, etype, evalue, etraceback, / ) -> None:
        super().__exit__(etype, evalue, etraceback)

    @overload
    def writable(self, *args, **kwargs) -> bool: # real signature unknown
        """ True if file was opened in a write mode. """
        write = super().writable()
        return write

    def writable( self ) -> bool:
        return True

    def write(self, buffer: Any, *args, **kwargs): # real signature unknown
        """
        Write buffer b to file, return number of bytes written.

        Only makes one system call, so not all of the data may be written.
        The number of bytes actually written is returned.  In non-blocking mode,
        returns None if the write would block.
        """
        #return len(buffer)
        pass

    def fileno(self) -> int:
        file_num = self.file.fileno()
        print(f"fileno: {file_num}")
        return -1

    def flush(self, *args, **kwargs) -> None:
        pass

    def close(self, *args, **kwargs):
        pass

    def seek(self, *args, **kwargs) -> None:
        pass

    def truncate(self, *args, **kwargs) -> None:
        pass

    def writelines(self, *args, **kwargs) -> None:
        pass


