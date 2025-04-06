import asyncio as aio

from src.gengraphlib.LogGraph import LogGraph

async def main() -> bool:
    log_graph = LogGraph("/home/richard/data/jctl-logs")
    await log_graph.exec_query( specific_ndx=-5 )
    log_graph.dump_key_groups()
    log_graph.dump_key_values()
    print("main() complete")
    return True

if __name__ == "__main__":
    ret = aio.run( main() )
    print(f"done [{ret}]")
