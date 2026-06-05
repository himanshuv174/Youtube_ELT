from airflow.providers.postgres.hooks.postgres import PostgresHook
from pyscopg2.extras import RealDictCursor


table = "yt_api"





def get_conn_cursor():      # To get the connection from the postgres DB, using postgress hook and cursor for connection
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt",database="elt_db")
    conn = hook.get_conn()
    cur = conn.cursor(cursfor_factory=RealDictCursor)
    return conn,cur

#cur.executez(select * from ....)   By the help of cursor we can make the DB Queries run


def close_conn_cursor(conn,cur):      # Closing the cursor and the connection of the DB to free resources
    cur.close()           
    conn.close()


def create_schema(schema):
    conn,cur = get_conn_cursor()    #getting the connection and cursor

    schema_sql = f"CREATE SCHEMA IF NOT EXIST {schema};"      #writing the DB query for Create schema
    
    cur.execute(schema_sql)     #this will execute the DB command
    conn.commit()               #this will commit the changes in the DB
    close_conn_cursor(conn,cur)    #After the operation closing the connection


def create_table(schema):

    conn,cur = get_conn_cursor()    #getting the connection and cursor

    if schema == 'staging':                                    #Based on schema Creating the table with the column names and their types
        table_sql = f"""                                       
                    CREATE TABLE IF NOT EXISTS {schema}.{table}(           
                        "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                        "Video_Title" TEXT NOT NULL,
                        "Upload_Date" TIMESTAMP NOT NULL,
                        "Duration" VARCHAR(20) NOT NULL,
                        "Video_Views" INT,
                        "Likes_Count" INT,
                        "Comments_Count" INT   
                    );
                """
    else:
        table_sql = f"""
                    CREATE TABLE IF NOT EXISTS {schema}.{table} (
                      "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                      "Video_Title" TEXT NOT NULL,
                      "Upload_Date" TIMESTAMP NOT NULL,
                      "Duration" TIME NOT NULL,
                      "Video_Type" VARCHAR(10) NOT NULL,
                      "Video_Views" INT,
                      "Likes_Count" INT,
                      "Comments_Count" INT    
                    ); 
                """

    cur.execute(table_sql)     #this will execute the DB command
    conn.commit()               #this will commit the changes in the DB
    close_conn_cursor(conn,cur)    #After the operation closing the connection


def get_video_ids(cur,schema):
    cur.execute(f"""SELECT "Video_ID" FROM {schema}.{table};""")
    ids = cur.fetchall()     #This will give the list of dictionaries where the key is always the Video_ID and the value will be the Video_id value.

    video_ids = [row["Video_ID"] for row in ids]   #this will extract all the video iids from the dictionary

    return video_ids

