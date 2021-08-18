# pcr cloud

## How to re-create tables in case the RDS is deleted
use the schema in file schema.sql to re-create all the tables. 
Before this delete all existing tables. 

## When launching with a new machine or when the machine's IP address is changed
1. goto AWS console
2. goto pcr-data RDS DB instance
3. select the active VPC security group
4. select the security group ID
5. edit inbout rules
6. add rule with the new laptop's IP address

## Things to do when creating a new deployment to get access to s3
1. goto AWS console
2. goto IAM
3. goto users
4. create a new user (Add user)
5. access type = programatic access
6. add user to group 'deployments'
7. create user
8. add these credentials to the s3_credentials.txt file in project home directory


## Connecting to RDS using this code
You must have the RDS_credentials.txt file which contains the username, password, port and hostname of RDS instance runing on AWS. You can obtain this 
by loggin into aws console as root and navigating to the RDS instance. \
1. place RDS_credentials.txt file in current directory\
+-- RDS_credentials.txt\
+-- dir1\
&emsp;|   +--dir2\
&emsp; &emsp; |   +--dir3 (clone this git repo here)\
&emsp; &emsp; &emsp; &emsp; |  +--pcr_cloud\
&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; |  +--rds.py\
&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; +--other files\
              
2. in pythonn code import rds
3. To make connection with cloud RDS MYSQL databse, use 
rds.connect_cloud()
4. with the rds module you can perform tasks such as getting all rows in a particular table and getting the last entry of a table


## Structure of Tables in the RDS cloud
### ema_data
suid - INT\
primekey - VARCHAR(150)\
variablename - VARCHAR(150)\
answer - BLOB\
dirty - INT\
language - INT\
mode - INT\
version - INT\
completed - INT\
synced - INT\
ts - DATETIME\
dep_id - INT\
cloud_pkey - INT - primery key\

### reward_data
empathid - VARCHAR(45)\
TimeSent - VARCHAR(20)\
TimeReceived - VARCHAR(20)\
Response - VARCHAR(20)\
dep_id - INT\
p_key - INT - primery key\
ConnectionError - INT\
Question - VARCHAR(5000)\
QuestionName - VARCHAR(500)\
QuestionType - VARCHAR(200)\
Reactive - INT\
SentTimes - INT\
speakerID - VARCHAR(500)\
suid - VARCHAR(20)\

### ema_storing_data
time - DATETIME\
event_vct - LONGTEXT\
stats_vct - LONGTEXT\
action - INT\
reward - FLOAT\
action_vct - LONGTEXT\
message_name - LONGTEXT\
uploaded - INT\
dep_id - INT\
p_key - BIGINT - primary key\


## Authentication
### RDS
RDS authentication is handled in rds.py module. When you call connect_cloud(), It reads authentication file RDS_credentials.txt.
This contains details needed to connect to the RDS instance in AWS. These details include endpoint, port, database name, username and password for a particular user.


