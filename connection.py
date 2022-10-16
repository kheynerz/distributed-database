from array import array
import psycopg2
from operator import itemgetter

def getScript(n: int) -> str:
    f = open("scripts.sql", "r")
    for _ in range(n):
        next(f)
    return f.readline().split('\n')[0]

def execute(params : dict, command: str) -> array:
    host, database, port, user, password = itemgetter('host', 'database', 'port', 'user', 'password')(params)
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
        cur.execute(command)
        # commit the changes
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return [None, error]
    finally:
        if conn is not None:
            conn.close()
            return [result, None] if result else [True, None]            

def command_table(nombre: str,attributes : dict) -> str:
    if len(attributes) == 0: return ""

    args = ""
    for key in attributes.keys():
        args += f"{key} {attributes[key]},"
    
    sql = f"CREATE TABLE {nombre} ({args[0:-1]});"
    return sql


#Postgresql Connection
param = {"host" : "localhost", "database" : "postgres", 'port': 5433, "user" : "postgres", "password" : "1234"}
#result = execute(param, getScript(0))
result = execute(param, command_table('test2',{'nombre': 'varchar', 'edad': 'integer'}))
print(result)


