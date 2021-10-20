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
+-- slack_secret.txt\
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

In your code to connect to RDS instance of your choise,\
```python
rds_connection=rds.RDS() 
#check isinstance(rds_connection,rds.RDS)
```

### S3
S3 authentication is handles by the module s3_functions.py. When you call the get_bucket() function, it reads the s3_credentials.txt file and use that details to 
establish a connection with S3 storage. To create the s3_credentials.txt file, goto AWS console and users. Create a new user with IAM access to S3 storage. 
Please give them the minimun necessary privillages. Do not share the credentails among users. S3_credentials.txt has the following fealds. \
```
User name,Password,Access key ID,Secret access key,Console login link
```
Note that with IAM access, you will get an access token, not a password. password field must be left blank\

### slack
The code in monitor.py monitors the heartbeat of all deployments and send a message if a deployment is offline. Place the slack app's secret url 
in slack_secret.txt file. slack_secret.txt file has the following format. \
```
url
#@@ffoo/$%$t/long_secret_url*4*$%&2
```

## Heartbeat and Monitoring program
All the deployments upload a row into the RDS table sch_data.heart_beat every 30 mins (this frequency of uploading is configurable in code).
The table sch_data.heart_beat has the following columns\
```
dep_id (deployment id), ts (timestamp of the local machine) , p_key (primary key), updated_ts (timestamp of the database when the row was updated)

```
A monitoring program running in an EC2 instance monitors this table and detects when a deployment did not upload heartbeat in 2 hours (this, also is configurable in code). Monitoring program can also detect new deployments when they start uploading a heartbeat. When some out-of-the-ordinary is detected, the program uses the code in slack.py to message a slack channel (as defined by the secret slack url in the file slack_secret.txt)\
Tutorial on how to send slack channel messages with HTTPS : \
https://api.slack.com/messaging/webhooks\

### Running monitoring program in a remote machine (e.g AWS EC2)
1. download the key file (.pem) from AWS that can be used to connect to the instance
2. ssh -i /path/to/pem/file.pem user@instance_url
3. goto project directory
4. use screen to start a background process. Read more about screen :\
https://www.tecmint.com/keep-remote-ssh-sessions-running-after-disconnection/ \

### Tips on screen 
starting a background process with screen :\
```
$ screen
```
Then run any command on the screen environment. Then press Ctrl+a immiediately followed by d to detach screen from terminal. 
So when we close the terminal (or close the ssh session) the process will keep running. \

list all processes running in screen  : \
```
$ screen -ls
```
close a session :\
```
$ screen -XS <session-id> quit
```










