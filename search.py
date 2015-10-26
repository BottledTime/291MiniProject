from main import *

def search(CONN_STRING):
    source = input("Source: ").upper()
    dest = input("Destination: ").upper()
    dep_date = input("Departure Date (DD/MM/YYYY): ")
    sql = """
    select flightno1, flightno2, src, dst, to_char(dep_time),
           to_char(arr_time), stops, 60 * layover, price, seats1, seats2
    from 
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1, 0 seats2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}')
    """.format(source, dest, dep_date)
    rs = sqlWithReturn(sql, CONN_STRING)
    if len(rs) != 0:
        i = 0
        for row in rs:
            print(i," ",row)
            i+=1
    else:
        sql = """
        select x.flightno1, x.flightno2, x.src, x.dst, to_char(x.dep_time),
               to_char(x.arr_time), x.stops, 24 * x.layover, x.price, x.seats1,
               x.seats2
        from airports a1, airports a2,
            (select flightno1, flightno2, src, dst, dep_time, arr_time,
            stops, layover, price, seats1, seats2
            from 
            (select flightno1, flightno2, src, dst, dep_time, arr_time,
            1 stops, layover, price, seats1, seats2
            from good_connections
            where to_char(dep_date,'DD/MM/YYYY')='{2}'
            union
            select flightno flightno1, '' flightno2, src, dst, dep_time,
            arr_time, 0 stops, 0 layover, price, seats seats1, null seats2
            from available_flights
            where to_char(dep_date,'DD/MM/YYYY')='{2}')) x
        where (lower(a1.city) like '%{0}%'
              or lower(a1.name) like '%{0}%')
              and a1.acode = x.src and a2.acode = x.dst
              and (lower(a2.city) like '%{1}%' or 
              lower(a2.name) like '%{1}%')   
        """.format(source.lower(), dest.lower(), dep_date)
        rs = sqlWithReturn(sql, CONN_STRING)
        if len(rs) != 0:
            i = 1
            for row in rs:
                print(i, " ", row)
                i+=1
        else:
            print("no results")
