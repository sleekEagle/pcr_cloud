/*list all users*/
SELECT * FROM mysql.user;

/*drop user*/
drop user 'user0'@'%';

/*
create a user with SHA256 password authentication
guide : 
https://dev.mysql.com/doc/refman/8.0/en/caching-sha2-pluggable-authentication.html
*/

/*
criteria :
use https://passwordsgenerator.net/ to generate a password
length 16 characters (more than this did not work)
include symbols, numbers, lowercase, uppercase, similar characters,
exclude ambiguous characters (single quotes did not work)
generate on your device
*/
CREATE USER 'username'@'%' IDENTIFIED WITH caching_sha2_password BY '';

/*grant permissions to the user*/
GRANT SELECT,INSERT ON * . * TO 'user1'@'%';
GRANT SELECT ON * . * TO 'user2'@'%';
FLUSH PRIVILEGES;

/*show permissions granted for a user*/
show grants for 'user23'@'%';





