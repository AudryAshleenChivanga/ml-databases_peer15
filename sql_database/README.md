to run the sqlSchema.sql you do the following

mysql < sqlSchema.sql
Data Cleaning:

Column names are renamed for consistency.

Missing values in Albumin_and_Globulin_Ratio are filled with the mean.

Gender is converted to binary (1 for Male, 0 for Female).

Diagnosis is converted to binary (1 for Liver disease, 0 for No disease).


Log in to MySQL as the root user:

bash
Copy
mysql -u root -p
Check if the user 'Ashleen'@'localhost' exists:

sql
Copy
SELECT user, host FROM mysql.user;
If the user does not exist, create it:

sql
Copy
CREATE USER 'Ashleen'@'localhost' IDENTIFIED BY 'your_password';
Grant the user access to the liver_disease_db database:

sql
Copy
GRANT ALL PRIVILEGES ON liver_disease_db.* TO 'Ashleen'@'localhost';
FLUSH PRIVILEGES;
Verify the permissions:

sql
Copy
SHOW GRANTS FOR 'Ashleen'@'localhost';



Solution 1: Grant Necessary Privileges
If you have access to a MySQL user with administrative privileges (e.g., root), log in to MySQL and grant the required privilege:

sql
Copy
Edit
GRANT PROCESS ON *.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
