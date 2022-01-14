# automated-duplication-of-rds-db-cross-region
This repository includes two Lambda scripts written in Python. One script automates the deletion of an RDS database instance 'y' and the other script automates the restoration of database 'y' from the latest automated snapshot of cross-region database instance 'x'. 

I scheduled an EventBridge rule to occur daily at the same time, which triggers the rdsDelete Lambda function. Then, using an RDS event subscription in conjunction with SNS, I set up a way to trigger the second autoRestore function as soon as the original database instance finishes deletion. This way, downtime is minimized, and the cross-region duplicate stays up to date as often as you choose. 
