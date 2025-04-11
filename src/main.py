import asyncio as aio

from src.BootLogGraph import BootLogGraph


async def main() -> bool:
    log_graph = BootLogGraph( "/home/richard/data/jctl-logs/" )

    help(log_graph)

    await log_graph.exec_query( specific_ndx=0 )
    log_graph.dump_trace_groups()
    log_graph.dump_key_values()
    print("main() complete")
    return True

if __name__ == "__main__":
    print("main() start")
    ret = aio.run( main() )
    print(f"done [{ret}]")
