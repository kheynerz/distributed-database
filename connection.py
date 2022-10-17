from pickle import TRUE
import psycopg2
from operator import itemgetter

from nodos import getNodes, getParams

def _execute(params : dict, command: str) -> list:
    host, database, port, user, password = itemgetter('host', 'database', 'port', 'user', 'password')(params)
    conn = result = None
    
    try:
        # connect to the PostgreSQL server
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

def createExtension(params : dict) -> list:
    extensionCommand = "DO $$ <<create_extension>> DECLARE installed BOOL := false; BEGIN SELECT (COUNT(*) = 1) into installed FROM pg_extension WHERE extname = 'postgres_fdw'; IF NOT installed THEN CREATE EXTENSION postgres_fdw; END IF; END create_extension $$;"
    return(_execute(params, extensionCommand))

def createServer(params : dict) -> list: 
    central, _ = getNodes()
    name, host, database, port, user, password = itemgetter('name','host', 'database', 'port', 'user', 'password')(central)
    name = '_'.join(name.lower().split())       

    sql = "DO $$ <<create_server>> BEGIN "
    sql += f"CREATE SERVER {name}_postgres_fdw FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '{host}', dbname '{database}', port '{port}'); "
    sql += f"CREATE USER MAPPING FOR {params['user']} SERVER {name}_postgres_fdw OPTIONS (user '{user}', password '{password}'); "
    sql += "EXCEPTION  WHEN duplicate_object THEN NULL; END create_server $$;"

    return(_execute(params, sql))

def createTable(nombre: str, attributes : dict) -> str:
    if len(attributes) == 0: return ""

    args = ""
    for key in attributes.keys():
        args += f"{key} {attributes[key]},"
    
    sql = f"CREATE TABLE {nombre} ({args[0:-1]});"
    return sql


def createTable(name: str, node: dict) -> bool:
    #CREATE TABLE FOR CENTRAL
    sql = f"CREATE TABLE {name} ( "
    attributes = node['attributes']

    pksql = "primary key ("
    pkCount = 0

    for a in attributes:
        atrName, atrType, atrPK, atrNull = itemgetter('name', 'type', 'pk', 'null')(a)
        null = "NULL" if (atrNull) else "NOT NULL"
        sql += f"{atrName} {atrType} {null}, "
        if (atrPK):
            pksql += f"{atrName},"
            pkCount += 1

    sql = sql + pksql[0:-1] + "))" if pkCount > 0 else sql[0:-2] + ")"

    return(_execute(getParams(node['name']), sql))

def createForeignTable(name, origin, dest):
    #TODO
    pass


def generateTables(attributes : dict) -> bool:
    name, central, locals = itemgetter('name', 'central', 'locals')(attributes)

    #CREATE TABLE FOR CENTRAL NODE
    createTable(name, central)

    #CREATE TABLE FOR LOCALS
    for node in locals:
        createTable(name, node)
        createForeignTable(name,node, central)
        createForeignTable(name,central, node)

#Postgresql Connection
params = {"host" : "localhost", "database" : "postgres", 'port': 5435, "user" : "postgres", "password" : "1234"}
#result = execute(param, extensionCommand)
#result = execute(param, command_table('test2',{'nombre': 'varchar', 'edad': 'integer'}))
#createExtension(params)

#param = {"host" : "localhost", "database" : "postgres", 'port': 5434, "user" : "postgres", "password" : "1234"}
#print(createServer(params))


tabla = {
    "name": "personas",
    "central": 
        {
            "name": "Instancia 1", 
            "attributes": [
                {"name": "cedula", "type" : "varchar", "pk" : False, "null" : False },
                {"name": "nombre", "type" : "varchar", "pk" : False, "null" : False },
                {"name": "ape1", "type" : "varchar", "pk" : False, "null" : False },
                {"name": "ape2", "type" : "varchar", "pk" : False, "null" : True }
            ]
        },
    "locals": [
        {
            "name": "INSTANCIA 2", 
            "attributes":[
                {"name": "cedula", "type" : "varchar", "pk" : True, "null" : False },
                {"name": "nombre", "type" : "varchar", "pk" : False, "null" : False },
                {"name": "ape1", "type" : "varchar", "pk" : False, "null" : False },
                {"name": "ape2", "type" : "varchar", "pk" : False, "null" : True }
            ]
        },
    
        {
            "name": "INSTANCIA 3", 
            "attributes":[
                {"name": "cedula", "type" : "varchar", "pk" : True, "null" : False },
                {"name": "nombre", "type" : "varchar", "pk" : False, "null" : False },
                {"name": "ape1", "type" : "varchar", "pk" : False, "null" : False },
                {"name": "ape2", "type" : "varchar", "pk" : False, "null" : True }
            ]
        }
    ]
}


generateTables(tabla)