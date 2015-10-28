import main
import search

def roundTrip(email, CONN_STRING):
    source = input("Source: ").upper()
    dest = input("Destination: ").upper()
    dep_date = input("Departure Date (DD/MM/YYYY): ")
    ret_date = input("Return Date (DD/MM/YYYY): ")
    printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date)

def printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, sortBy="1"):
    sortByPrice = """
    select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
    from
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    order by price asc)) t1,
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    order by price asc)) t2
    order by price asc
    """.format(source, dest, dep_date, ret_date)
    sortByStops = """
    select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
    from
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    order by price asc)) t1,
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    order by price asc)) t2
    order by stops, price asc
    """.format(source, dest, dep_date, ret_date)
    if sortBy == "1":
        try:
            rs, desc = main.sqlWithReturnDesc(sortByPrice, CONN_STRING)
        except:
            print("no match found")
            return main.menu(email, CONN_STRING)
    else:
        try:
            rs, desc = main.sqlWithReturnDesc(sortByStops, CONN_STRING)
        except:
            print("no match found")
            return main.menu(email, CONN_STRING)
    if len(rs) != 0:
        i = 1
        for row in desc:
            print(row[0], end=" ")
        print("")
        for row in rs:
            print(str(i)+".",row)
            i+=1
    else:
        sortByPrice = """
        select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
        from airports a1, airports a2,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
        arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        order by price asc)) t1,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        order by price asc)) t2
        where (lower(a1.city) like '%{0}%'
              or lower(a1.name) like '%{0}%')
              and a1.acode = t1.src and a2.acode = t1.dst
              and (lower(a2.city) like '%{1}%' or
              lower(a2.name) like '%{1}%') and
              t1.src = t2.dst and t1.dst = t2.src
        order by price asc
        """.format(source.lower(), dest.lower(), dep_date, ret_date)
        sortByStops = """
        select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
        from airports a1, airports a2,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
        arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        order by price asc)) t1,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        order by price asc)) t2
        where (lower(a1.city) like '%{0}%'
              or lower(a1.name) like '%{0}%')
              and a1.acode = t1.src and a2.acode = t1.dst
              and (lower(a2.city) like '%{1}%' or
              lower(a2.name) like '%{1}%') and
              t1.src = t2.dst and t1.dst = t2.src
        order by price asc
        """.format(source.lower(), dest.lower(), dep_date, ret_date)
        if sortBy == "1":
            try:
                rs, desc = main.sqlWithReturnDesc(sortByPrice, CONN_STRING)
            except:
                print("There was an unexpected error while trying to find flights. Please try again.")
                return main.menu(email, CONN_STRING)
        else:
            try:
                rs, desc = main.sqlWithReturnDesc(sortByStops, CONN_STRING)
            except:
                print("There was an unexpected error while trying to find flights. Please try again.")
                return main.menu(email, CONN_STRING)
        if len(rs) != 0:
            i = 1
            for row in desc:
                print(row[0], end=" ")
            print("")
            for row in rs:
                print(str(i)+".", row)
                i+=1
        else:
            print("no results")
            return main.menu(email, CONN_STRING)
    print(str(len(rs)+1)+".", "Sort by number of connections")
    print(str(len(rs)+2)+".", "Make a booking")
    print(str(len(rs)+3)+".", "Go back to menu")
    option = input("Enter the number of an option: ")
    try:
        optNum = int(option)
        if optNum<0 or optNum>len(rs)+3:
            print("Not valid number")
        elif optNum == len(rs)+1:
            printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, "2")
        elif optNum == len(rs)+2:
            flightno = int(input("Enter the number before the flight you want to book: "))
            if sortBy == "1":
                rs = main.sqlWithReturn(sortByPrice, CONN_STRING)
            else:
                rs = main.sqlWithReturn(sortByStops, CONN_STRING)
            roundBooking(email, CONN_STRING, flightno, rs, dep_date, ret_date, source, dest)
        elif optNum == len(rs)+3:
            main.menu(email, CONN_STRING)
        else:
            print("Not valid number")
            return main.menu(email, CONN_STRING)
    except:
        print("Not valid number")
        return main.menu(email, CONN_STRING)

def roundBooking(email, CONN_STRING, flightno, rs, dep_date, ret_date, source, dest):
    row = rs[flightno-1]
    if row[-2] <= 0:
        print("tickets not exists, please choose another flight")
        printInfo(email, CONN_STRING, source, dest, dep_date, "1")
    try:
        sql = "select max(tno) from tickets"
        maxTno = main.sqlWithReturn(sql, CONN_STRING)[0][0]
        sql = "select name from passengers where email = '{0}'".format(email)
        name = main.sqlWithReturn(sql, CONN_STRING)[0][0]
        sql = "insert into tickets values({0}, '{1}', '{2}', '{3}')".format(maxTno+1, name, email, row[-1])
        main.sqlWithNoReturn(sql, CONN_STRING)
        sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[0], row[8], dep_date)
        main.sqlWithNoReturn(sql, CONN_STRING)
        sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[10], row[-5], ret_date)
        main.sqlWithNoReturn(sql, CONN_STRING)
        if row[1] is not None:
            sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[1], row[9], dep_date)
            main.sqlWithNoReturn(sql, CONN_STRING)
        if row[11] is not None:
            sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[11], row[-4], ret_date)
            main.sqlWithNoReturn(sql, CONN_STRING)
        print("success")
    except:
        print("There was an error during booking. Please try again")
        main.menu(email, CONN_STRING)
    printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date)
