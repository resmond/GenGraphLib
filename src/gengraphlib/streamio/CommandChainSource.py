from typing import Self

import asyncio as aio
import asyncio.subprocess as asub
import simsimd as simd

from src.gengraphlib.streamio import ChainSourceBase, ChainableResult, StreamType

class CommandChainSource[ T: ChainableResult ]( ChainSourceBase ):

    def __init__(self: Self, cmd: str, stream_type: StreamType = StreamType.LfTextLine, buffer_size: int = 4096  ):
        super( CommandChainSource, self ).__init__(stream_type, buffer_size)
        self.nlbk_memview: memoryview | None = None
        self.cmd: str = cmd

        match stream_type:
            case StreamType.LfTextLine:
                self.nlbk_memview = memoryview( b'\n' )
            case StreamType.CrLfTextLine:
                self.nlbk_memview = memoryview( b'\r\n' )

        #self.exec_process: asub.Process | None = None

    async def _new_result( self: Self ) -> T | None:
        if self.cmd is not None:

            try:
                chain_result = ChainableResult()

                exec_process: asub.Process = await aio.create_subprocess_shell(
                    cmd=self.cmd,
                    stdout=aio.subprocess.PIPE,
                )

                if exec_process is not None:
                    try:

                        buffer = await self.exec_process.stdout.read( self.buffer_size )

                        if len(buffer) > 0:

                            mem_view = memoryview(buffer)
                            found_at = simd.intersection(mem_view, self.nlbk_memview)
                            if found_at > 0:
                                print(f"found_at: {found_at} - ] {buffer} [")

                            chain_result.buffer = buffer

                            return chain_result
                        else:
                            self.started = False

                    except Exception as innerexc:
                        print(f"CmdStreamBinary.stream_binary: {innerexc}")


            except Exception as exc:
                print(f"CmdStreamBase.run_command: {exc}")

        else:
            print("CmdStreamBase.run_command: No command")


    #async def split( self, buffer: bytes ) -> AsyncGenerator[ bytes, None ]:


if __name__ == "__main__":
    teststr =   "found_at = simd.intersection(mem_view, self.nlbk_memview)" + \
                "found_at = simd.intersection(mem_view, self.nlbk_memview)" + \
                "a;lskdjfsdl fj sdlkfjsd;lkfjds;lkfljsdklfj\nskldjfdsldddd" + \
                "found_at = simd.intersection(mem_view, self.nlbk_memview)" + \
                "a;lskdjfsdl fj sdlkfjsd;lkfjds;lkfljsdklfj\nskldjfdsldddd" + \
                "found_at = simd.intersection(mem_view, self.nlbk_memview)" + \
                "a;lskdjfsdl fj sdlkfjsd;lkfjds;lkfljsdklfj\nskldjfdsldddd" + \
                "found_at = simd.intersection(mem_view, self.nlbk_memview)"

    test_memview = memoryview( teststr.encode() )
    test_nlbk_memview = memoryview( b"\n" )

    test_found_at = simd.intersection( test_memview, test_nlbk_memview )

    print( test_found_at )
