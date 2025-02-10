# Assignment - Week 5
## Task 1: Install MySQL server
### 成功安裝並登入MySQL
![](./screenshot/Task1/登入成功.PNG)
## Task 2: Create database and table in your MySQL server
### Create a new database named website.
![](./screenshot/Task2/create%20database%20website.PNG)
### Create a new table named member, in the website database.
![](./screenshot/Task2/create%20table%20named%20member.PNG)
## Task 3: SQL CRUD
### INSERT a new row to the member table where name, username and password must be set to <u>test</u> INSERT additional 4 rows with arbitrary data.
![](./screenshot/Task3/create%20new%20row%20that%20contain%20test%20and%20other%204%20rows.PNG)
### SELECT all rows from the member table.
![](./screenshot/Task3/SELECT%20all%20rows%20from%20the%20member%20table..PNG)
### SELECT all rows from the member table, in descending order of time.
![](./screenshot/Task3/SELECT%20all%20rows%20from%20the%20member%20table,%20in%20descending%20order%20of%20time..PNG)
### SELECT total 3 rows, second to fourth, from the member table, in descending order of time.
![](./screenshot/Task3/SELECT%20total%203%20rows,%20second%20to%20fourth,%20from%20the%20member%20table,%20in%20descending%20order%20of%20time..PNG)
### SELECT rows where username equals to <u>test</u>.  
![](./screenshot/Task3/SELECT%20rows%20where%20username%20equals%20to%20test..PNG)
### SELECT rows where name includes the <u>es</u> keyword.
![](./screenshot/Task3/SELECT%20rows%20where%20name%20includes%20the%20es%20keyword..PNG)
### SELECT rows where both username and password equal to <u>test</u>.
![](./screenshot/Task3/SELECT%20rows%20where%20both%20username%20and%20password%20equal%20to%20test..PNG)
### UPDATE data in name column to <u>test2</u> where username equals to <u>test</u>.
![](./screenshot/Task3/UPDATE%20data%20in%20name%20column%20to%20test2%20where%20username%20equals%20to%20test..PNG)
## Task 4: SQL Aggregation Functions
### Change the follow_count of all the rows (optional).
![](./screenshot/Task4/change%20dataset%20before%20count.PNG)
### SELECT how many rows from the member table.
![](./screenshot/Task4/SELECT%20how%20many%20rows%20from%20the%20member%20table..PNG)
### SELECT the sum of follower_count of all the rows from the member table.
![](./screenshot/Task4/SELECT%20the%20sum%20of%20follower_count%20of%20all%20the%20rows%20from%20the%20member%20table..PNG)
### SELECT the average of follower_count of all the rows from the member table.
![](./screenshot/Task4/SELECT%20the%20average%20of%20follower_count%20of%20all%20the%20rows%20from%20the%20member%20table..PNG)
### SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
![](./screenshot/Task4/SELECT%20the%20average%20of%20follower_count%20of%20the%20first%202%20rows,%20in%20descending%20order%20of%20follower_count,%20from%20the%20member%20table..PNG)
## Task 5: SQL JOIN
### Create a new table named message, in the website database.
![](./screenshot/Task5/Create%20a%20new%20table%20named%20message,%20in%20the%20website%20database.PNG)
### SELECT all messages, including sender names. We have to JOIN the member table to get that.
![](./screenshot/Task5/SELECT%20all%20messages,%20including%20sender%20names.%20We%20have%20to%20JOIN%20the%20member%20table%20to%20get%20that..PNG)
### SELECT all messages, including sender names, where sender username equals to <u>test</u> We have to JOIN the member table to filter and get that.
![](./screenshot/Task5/SELECT%20all%20messages,%20including%20sender%20names,%20where%20sender%20username%20equals%20to%20test.%20We%20have%20to%20JOIN%20the%20member%20table%20to%20filter%20and%20get%20that..PNG)
### Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to <u>test</u>.
![](./screenshot/Task5/Use%20SELECT,%20SQL%20Aggregation%20Functions%20with%20JOIN%20statement,%20get%20the%20average%20like%20count%20of%20messages%20where%20sender%20username%20equals%20to%20test..PNG)
### Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
![](./screenshot/Task5/Use%20SELECT,%20SQL%20Aggregation%20Functions%20with%20JOIN%20statement,%20get%20the%20average%20like%20count%20of%20messages%20GROUP%20BY%20sender%20username..PNG)