import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['KEYS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['KEYS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Creating and returning a Spark session
    
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark



def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    song_df = spark.read.json(song_data)
    
    

    # extract columns to create songs table
    songs_table = song_df.select(["song_id", "title", "artist_id", "year", "duration"]).distinct()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy("year", "artist_id").parquet(output_data+'songs_table/')
        
   
    # extract columns to create artists table
    artists_table = df.select(["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]).distinct()
    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data+'artists_table/')


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = input_data + "log_data/*/*/*.json"

    # read log data file
    log_df = spark.read.json(log_data)
    
    # filter by actions for song plays
    log_df = log_df.where(page="Nextpage")

    # extract columns for users table    
    users_table = log_df.select(["userId", "firstName", "lastName", "gender", "level"]).distinct()
    
    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(output_data + 'users_table/')

    # create timestamp column from original timestamp column
    #get_timestamp = udf()
    #df = 
    
    # create datetime column from original timestamp column
    #get_datetime = udf()
    #df = 
    
    log_df = log_df.withColumn('timestamp',((log_df.ts.cast('float')/1000).cast('timestamp') ))
    
    
    # extract columns to create time table
    time_table = log_df.select(F.col('timestamp').alias('start_time'),\
                          F.hour('timestamp').alias('hour'),\
                          F.dayofmonth('timestamp').alias('day'),\
                          F.weekofyear('timestamp').alias('week'),\
                           F.month('timestamp').alias('month'),\
                           F.year('timestamp').alias('year'),\
                           F.date_format(F.col('timestamp'),'E').alias('weekday')\
                          )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy('year','month').parquet(output_data + 'time_table/')

    # read in song data to use for songplays table
    song_data = input_data + 'song_data/*/*/*/*.json'
    song_df = spark.read.json(song_data)
    song_df.createOrReplaceTempView("song_data_table")
    log_df.createOrReplaceTempView("log_data_table")

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = songplays_table = spark.sql("""
                                SELECT monotonically_increasing_id() as songplay_id,
                                to_timestamp(lt.ts/1000) as start_time,
                                month(to_timestamp(lt.ts/1000)) as month,
                                year(to_timestamp(lt.ts/1000)) as year,
                                lt.userId as user_id,
                                lt.level as level,
                                st.song_id as song_id,
                                st.artist_id as artist_id,
                                lt.sessionId as session_id,
                                lt.location as location,
                                lt.userAgent as user_agent
                                FROM log_data_table lt
                                JOIN song_data_table st on lt.artist = st.artist_name and lt.song = st.title
                            """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').partitionBy('year','month').parquet(output_data +'songplays_table/')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
