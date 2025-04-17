import datetime as dt
#import dateutil as dutil



if __name__ == "__main__":
    test_datetime = dt.datetime.now()
    __REALTIME_TIMESTAMP=1742941840634450

    rtTime = dt.timedelta( microseconds=__REALTIME_TIMESTAMP )
    very_beginning = dt.datetime.fromisoformat("1970-01-01")
    test3 = very_beginning + rtTime

    print( f"now: {test_datetime}" )
    print( f"very_beginning: {very_beginning}" )
    print( f"test3{type(test3)}: {test3}" )




