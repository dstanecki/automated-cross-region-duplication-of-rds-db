# This code will restore an RDS database instance from the latest snapshot across regions
# Daniel Stanecki
# Version -- 2.0

import boto3
import os
import sys
import time
import json
import array as arr
from datetime import datetime, timezone
from time import gmtime, strftime

def lambda_handler(event, context):
    
    print("request: " + json.dumps(event))
    
    if 'targetRegion' not in event or 'crossRegion' not in event or 'originDB' not in event or 'newDB' not in event or 'newDBClass' not in event: 
        return "Event JSON body is incomplete."
    else:
        client1 = boto3.client('rds', region_name=event['targetRegion'])
        client2 = boto3.client('rds', region_name=event['crossRegion'])
        response = client2.describe_db_snapshots( # Returns array with two elements: DBSnapshots and Marker
            DBInstanceIdentifier=event['originDB'], # Pull all automated DBSnapshots associated with the origin database in another region
            SnapshotType='automated'
        )
    
        if not response:
            return "There are no snapshots in your selected region."
        else:
            snapshots = response['DBSnapshots'] # Holds all DBSnapshots objects 
            snapshots.sort(key=lambda x: x['SnapshotCreateTime'], reverse=True) # Sort from most recent to oldest DBSnapshots
            newestSnapshot = snapshots[0] # Single DBSnapshots object
            # print(newestSnapshot['SnapshotCreateTime'])  
            snapshotIdentifier = newestSnapshot['DBSnapshotIdentifier'] + '-' + event['crossRegion'] # Cross-region snapshots have the original region appended to the identifier
    
            client1.restore_db_instance_from_db_snapshot(
                DBInstanceIdentifier=event['newDB'],
                DBSnapshotIdentifier=snapshotIdentifier,
                DBInstanceClass=event['newDBClass'],
                Port=5432,
                MultiAZ=False,
                PubliclyAccessible=False,
                AutoMinorVersionUpgrade=False,
                Engine='postgres',
                Tags=[
                    {
                        'Key': 'DEV-TEST',
                        'Value': 'Auto-Delete'
                    },
                ],
                CopyTagsToSnapshot=False,
                UseDefaultProcessorFeatures=True,
                DeletionProtection=False,
                EnableCustomerOwnedIp=False
            )
