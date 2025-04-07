import asyncio as aio

from src.gengraphlib.BootLogGraph import BootLogGraph

async def main() -> bool:
    log_graph = BootLogGraph( "/home/richard/data/jctl-logs/" )
    await log_graph.exec_query( specific_ndx=-5 )
    log_graph.dump_trace_groups()
    log_graph.dump_key_values()
    print("main() complete")
    return True

if __name__ == "__main__":
    ret = aio.run( main() )
    print(f"done [{ret}]")
