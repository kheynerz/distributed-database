import psycopg2
from operator import itemgetter

from nodos import getParams

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

def createServer(params : dict, serverName : str) -> list: 
    serverParams = getParams(serverName)
    name, host, database, port, user, password = itemgetter('name','host', 'database', 'port', 'user', 'password')(serverParams)
    name = '_'.join(name.lower().split())       

    sql = "DO $$ <<create_server>> BEGIN "
    sql += f"CREATE SERVER {name}_postgres_fdw FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '{host}', dbname '{database}', port '{port}'); "
    sql += f"CREATE USER MAPPING FOR {params['user']} SERVER {name}_postgres_fdw OPTIONS (user '{user}', password '{password}'); "
    sql += "EXCEPTION  WHEN duplicate_object THEN NULL; END create_server $$;"

    return(_execute(params, sql))



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

def createForeignTable(name, node, serverName):
    attributes = node['attributes']

    serverName = '_'.join(serverName.lower().split()) 
    sql =  f"create foreign table remote_{name}_{serverName} ("

    for a in attributes:
        atrName, atrType = itemgetter('name', 'type')(a)
        sql += f"{atrName} {atrType}, "

    sql = sql[0:-2] + f") server {serverName}_postgres_fdw OPTIONS (schema_name 'public', table_name '{name}');"
      
    return(_execute(getParams(node['name']), sql))


def generateTables(attributes : dict) -> bool:
    name, central, locals = itemgetter('name', 'central', 'locals')(attributes)

    #CREATE TABLE FOR CENTRAL NODE
    #createTable(name, central)

    view_sql = f"CREATE OR REPLACE VIEW view_{name} AS SELECT * from {name} "

    #CREATE TABLE FOR LOCALS
    for node in locals:
        serverName = '_'.join(node['name'].lower().split()) 
        view_sql += f"UNION SELECT * FROM remote_{name}_{serverName} "
        createTable(name, node)
        createForeignTable(name,node, central['name'])
        createForeignTable(name,central, node['name'])

    _execute(getParams(central['name']), view_sql)
    

#Postgresql Connection
#params = {"host" : "localhost", "database" : "postgres", 'port': 5435, "user" : "postgres", "password" : "1234"}
#result = execute(param, extensionCommand)
#result = execute(param, command_table('test2',{'nombre': 'varchar', 'edad': 'integer'}))


#param = {"host" : "localhost", "database" : "postgres", 'port': 5434, "user" : "postgres", "password" : "1234"}
#print(createServer(params))

"""

tabla = {
    "name": "personas",
    "central": 
        {
            "name": "INSTANCIA 1", 
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

"""


#print(getParams('INSTANCIA 1'))
#createExtension(getParams('INSTANCIA 1'))
#createExtension(getParams('INSTANCIA 2'))
#createExtension(getParams('INSTANCIA 3'))

#createServer(getParams('INSTANCIA 1'), 'INSTANCIA 2')
#createServer(getParams('INSTANCIA 1'), 'INSTANCIA 3')

#createServer(getParams('INSTANCIA 2'), 'INSTANCIA 1')
#createServer(getParams('INSTANCIA 3'), 'INSTANCIA 1')

#generateTables(tabla)


