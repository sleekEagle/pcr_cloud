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
You must have the RDS_credentials.txt and s3_credentials.txt files which contains the credential details for this user\
1. place the credential files in current directory\
+-- RDS_credentials.txt\
+-- s3_credentials.txt\
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
Place the two credential files (RDS_credentials.txt and s3_credentials.txt) in your directory structure as mentioned in the section "Connecting to RDS using this code" above.  
### RDS
RDS authentication is handled in rds.py module. When you call connect_cloud(), It reads authentication file RDS_credentials.txt.
This contains details needed to connect to the RDS instance in AWS. Refer to the mysql file user_operations.sql for a guide for various operations related to users (creating users, cranting them permissions,...etc.). Create a user and assign them a password as metntioned in user_operations.sql. Please use the password generator or similar one as mentioned there to create a password. RDS_credentials.txt file should contain following details\
```
endpoint,port,database_name,username,password
????.????.rds.amazonaws.com,port_number,database_name,user1,strongpassword1234
```

Do not share credentials among users. Always create new credentails file for each new user. Only grant them the neccessary privillages. \

### S3
S3 authentication is handles by the module s3_functions.py. When you call the get_bucket() function, it reads the s3_credentials.txt file and use that details to 
establish a connection with S3 storage. To create the s3_credentials.txt file, goto AWS console and users. Create a new user with IAM access to S3 storage. 
Please give them the minimun necessary privillages. Do not share the credentails among users. S3_credentials.txt has the following fealds. \
```
User name,Password,Access key ID,Secret access key,Console login link
```
Note that with IAM access, you will get an access token, not a password. password field must be left blank\









