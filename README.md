# automated-duplication-of-rds-db-cross-region
This repository includes two Lambda scripts written in Python. One script automates the deletion of an RDS database instance 'y' and the other script automates the restoration of database 'y' from the latest automated snapshot of cross-region database instance 'x'. 

I scheduled an EventBridge rule to occur daily at the same time, which triggers the rdsDelete Lambda function. Then, using an RDS event subscription in conjunction with SNS, I set up a way to trigger the autoRestore function as soon as the original database instance finishes deletion. This way, downtime is minimized and the cross-region duplicate gets updated as often as you choose. 

You can read more about it here: https://www.danielstanecki.com/projects/2022/01/14/automated-duplication-of-rds-db-cross-region.html
