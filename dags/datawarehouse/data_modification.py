#this script will handle the operactions like Insert, Update, Delete.
import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cur,conn,schema,row):       #this function will take the cursor, connection, schema to differenciate between schemas, and a variable row.
    
    try:
        if schema == 'staging':     #This has the schema, table and table content of the staging schema only.
            video_id = 'video_id'

            cur.execute(                         #the value defined like this to store the actual value of the JSON.
                f"""INSERT INTO {schema}.{table}("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Views", "Likes_Count", "Comments_Count")
                VALUES (%(video_id)s, %(title)s, %(publishedAt)s, %(duration)s, %(viewCount)s, %(likeCount)s, %(commentCount)s);
                """,
                row,
            )
        else:
            video_id = "Video_ID"      #This has the schema, table and table content of the Core schema only. which is different from staging.

            cur.execute(
                f"""
                INSERT INTO {schema}.{table}("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Type", "Video_Views", "Likes_Count", "Comments_Count")
                VALUES (%(Video_ID)s, %(Video_Title)s, %(Upload_Date)s, %(Duration)s, %(Video_Type)s, %(Video_Views)s, %(Likes_Count)s, %(Comments_Count)s)
                """,
                row,
            )

        conn.commit()

        logger.info(f"Inserted row with the Video_ID: {row[video_id]}")

    except Exception as e:
        logger.error(f"Error inserting row with Video_ID: {row[video_id]}")
        raise e



def update_rows(cur,conn,schema,row):        #this function will take the cursor, connection, schema to differenciate between schemas, and a variable row.
    
    try:
        # staging
        if schema == "staging":
            video_id = "video_id"
            upload_date = "publishedAt"
            video_title = "title"
            video_views = "viewCount"
            likes_count = "likeCount"
            comments_count = "commentCount"
        # core
        else:
            video_id = "Video_ID"
            upload_date = "Upload_Date"
            video_title = "Video_Title"
            video_views = "Video_Views"
            likes_count = "Likes_Count"
            comments_count = "Comments_Count"

        cur.execute(
            f"""
            UPDATE {schema}.{table}
            SET "Video_Title" = %({video_title})s,
                "Video_Views" = %({video_views})s, 
                "Likes_Count" = %({likes_count})s, 
                "Comments_Count" = %({comments_count})s
            WHERE "Video_ID" = %({video_id})s AND "Upload_Date" = %({upload_date})s;
            """,
            row,
        )

        conn.commit()

        logger.info(f"Updated row with Video_ID: {row[video_id]}")
    
    except Exception as e:
        logger.error(f"Error updating the row with Video_ID: {row[video_id]}")
        raise e
    

def delete_rows(cur,conn,schema,ids_to_delete):             #this function will take the cursor, connection, schema to differenciate between schemas, and ids/list of ids need to be deleted.

    try:                                                   #Note we have changed the format of the string.We can move on to the SQL delete statement that takes the table in question, and using the Where clause,deletes the row or rows depending if the IDs to delete variable has one or more IDs.
        ids_to_delete = f"""({', '.join(f"'{id}'" for id in ids_to_delete)})"""

        cur.execute(
            f"""
            DELETE FROM {schema}.{table}
            WHERE "Video_ID" IN {ids_to_delete};
            """
        )

        conn.commit()

        logger.info(f"Deleted row with Video_ID: {ids_to_delete}")
    
    except Exception as e:
        logger.error(f"Error updating the row with Video_ID: {ids_to_delete} - {e}")
        raise e
