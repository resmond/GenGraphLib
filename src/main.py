import asyncio as aio

from src.gengraphlib.LogGraph import LogGraph, GraphCmd

async def main() -> bool:
    log_graph = LogGraph("/home/richard/data/jctl-logs")
    await log_graph.exec_query( GraphCmd.Full, -5 )
    log_graph.dump_missed_keys()
    print("main() complete")
    return True;

if __name__ == "__main__":
    ret = aio.run( main() )
    print(f"done [{ret}]")
