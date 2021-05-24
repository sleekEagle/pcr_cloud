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

## Things to do when creating a new deployment
1. goto AWS console
2. goto IAM
3. goto users
4. create a new user (Add user)
5. access type = programatic access
6. add user to group 'deployments'
7. create user
8. add these credentials to the RDS_credentials.txt file in project home directory
9. 
