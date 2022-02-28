# Project: Data Lake

**Introduction**

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app

**Project Description**

Apply the knowledge of Spark and Data Lakes to build and ETL pipeline for a Data Lake hosted on Amazon S3

In this task, we have to build an ETL Pipeline that extracts their data from S3 and process them using Spark and then load back into S3 in a set of Fact and Dimension Tables. This will allow their analytics team to continue finding insights in what songs their users are listening. Will have to deploy this Spark process on a Cluster using AWS

**Project Datasets**

Song Data Path --> *s3://udacity-dend/song_data*

Log Data Path --> *s3://udacity-dend/log_data* 

Song Dataset

The first dataset is a subset of real data from the Million Song Dataset(https://labrosa.ee.columbia.edu/millionsong/). Each file is in JSON format and contains metadata about a song and the artist of that song. 

Log Dataset

The second dataset consists of log files in JSON format. The log files in the dataset with are partitioned by year and month.

**Schema for Song Play Analysis**

A Star Schema would be required for optimized queries on song play queries

**Fact Table**

**songplays** - records in event data associated with song plays i.e. records with page NextSong *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

**Dimension Tables**

**users** - users in the app *user_id, first_name, last_name, gender, level*

**songs** - songs in music database *song_id, title, artist_id, year, duration*

**artists** - artists in music database *artist_id, name, location, lattitude, longitude*

**time** - timestamps of records in songplays broken down into specific units *start_time, hour, day, week, month, year, weekday*

Project Template

Project Template include three files:

1. etl.py reads data from S3, processes that data using Spark and writes them back to S3

2. dl.cfg contains AWS Credentials

3. README.md provides discussion on your process and decisions

**ETL Pipeline**

- Load the credentials from dl.cfg
- Load the Song Data and Log Data which are in JSON Files
- After loading the JSON Files from S3 ,use Spark to  process them and then generate a set of Fact and Dimension Tables
- Load the output to S3 as parquet files


**Open the terminal and run the command "python etl.py"**
