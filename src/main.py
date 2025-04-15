import asyncio as aio

from BootLogGraph import BootLogGraph

async def main() -> bool:
    print("main() start")

    log_graph = BootLogGraph( id="1", _log_root = "/home/richard/data/jctl-logs/" )
    await log_graph.exec( specific_ndx=-1 )
    log_graph.persist_data()

    print("main() complete")
    return True

if __name__ == "__main__":
    ret = aio.run( main() )
