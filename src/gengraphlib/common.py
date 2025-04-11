from collections.abc import Callable
import datetime as dt

KeyValTypes: type = type[str, int, bool, dt.datetime]
process_fields_fn = Callable[ [ dict[ str,KeyValTypes ], int, str], bool ]
