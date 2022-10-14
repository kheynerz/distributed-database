import psycopg2
from operator import itemgetter

def execute(params, query):
    host, database, port, user, password = itemgetter('host', 'database', 'port', 'user', 'password')(params)
    """ Connect to the PostgreSQL database server """
    conn = result = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect( host=host,
                                database=database,
                                user=user,
                                port=port,
                                password=password)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        cur.execute(query)

        # display the PostgreSQL database server version
        result = cur.fetchall() 

	# close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return [None, error]
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return [result, None]            

#Postgresql Connection
params = {"host" : "localhost", "database" : "covid19", 'port': 5433, "user" : "admin", "password" : "1234"}
result = execute(params, 'SELECT * from aplicaciones')
print(result)