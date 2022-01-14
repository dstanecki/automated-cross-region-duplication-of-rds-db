# this Code will help to schedule the restoration of an RDS database from a cross-region database snapshot
# Daniel Stanecki
# Version -- 1.0

import boto3
import os
import sys
import time
import array as arr
from datetime import datetime, timezone
from time import gmtime, strftime

def restore_rds_all():
    region=os.environ['REGION'] #region we are restoring the DB snapshot in
    region2=os.environ['REGION2'] #region we are getting the snapshot from
    client = boto3.client('rds', region_name=region)
    client2 = boto3.client('rds', region_name=region2)
    
    response = client2.describe_db_snapshots( #returns array with two elements: DBSnapshots and Marker
        DBInstanceIdentifier='x', #pull all automated DBSnapshots associated with database 'x' 
        #DBSnapshotIdentifier='string',
        SnapshotType='automated' 
        #Filters=[
        #    {
        #       'Name': 'string',
         #       'Values': [
          #          'string',
           #     ]
            #},
        #],
        #MaxRecords=123,
        #Marker='string',
        #IncludeShared=True|False,
        #IncludePublic=True|False,
        #DbiResourceId='string'
    )
    
    def myFunc(e):
        return e['SnapshotCreateTime']
        
    x = response['DBSnapshots'] #x holds all DBSnapshots objects
    x.sort(key=myFunc, reverse=True) #sort from most recent to oldest DBSnapshots
    y = x[0] #y is a single DBSnapshots object
    print(y['SnapshotCreateTime'])  
    snapshotIdentifier = y['DBSnapshotIdentifier'] + '-' + os.environ['REGION2'] #cross-region snapshots have the original region appended in the identifier
    
    client.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier='y',
        DBSnapshotIdentifier=snapshotIdentifier,
        DBInstanceClass='db.t3.micro',
        Port=5432,
        #AvailabilityZone='string',
        #DBSubnetGroupName='string',
        MultiAZ=False,
        PubliclyAccessible=False,
        AutoMinorVersionUpgrade=False,
        #LicenseModel='string',
        #DBName='',
        Engine='postgres',
        #Iops=123,
        #OptionGroupName='string',
        Tags=[
            {
                'Key': 'DEV-TEST',
                'Value': 'Auto-Delete'
            },
        ],
        #StorageType='string',
        #TdeCredentialArn='string',
        #TdeCredentialPassword='string',
        #VpcSecurityGroupIds=[
            #'string',
            #],
        #Domain='string',
        CopyTagsToSnapshot=False,
        #DomainIAMRoleName='string',
        #EnableIAMDatabaseAuthentication=True|False,
        #EnableCloudwatchLogsExports=[
        #'string',
        #],
        #ProcessorFeatures=[
        #    {
         #       'Name': 'coreCount',
          #      'Value': '1'
           # },
        #],
        UseDefaultProcessorFeatures=True,
        #DBParameterGroupName='string',
        DeletionProtection=False,
        EnableCustomerOwnedIp=False,
        #CustomIamInstanceProfile='string',
        #BackupTarget='string'
    )

"""    
    client.restore_db_cluster_from_snapshot(
        AvailabilityZones=[
            'string',
        ],
        DBClusterIdentifier='string',
        SnapshotIdentifier='string',
        Engine='string',
        EngineVersion='string',
        Port=123,
        DBSubnetGroupName='string',
        DatabaseName='string',
        OptionGroupName='string',
        VpcSecurityGroupIds=[
            'string',
        ],
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        KmsKeyId='string',
        EnableIAMDatabaseAuthentication=True|False,
        BacktrackWindow=123,
        EnableCloudwatchLogsExports=[
            'string',
        ],
        EngineMode='string',
        ScalingConfiguration={
            'MinCapacity': 123,
            'MaxCapacity': 123,
            'AutoPause': True|False,
            'SecondsUntilAutoPause': 123,
            'TimeoutAction': 'string',
            'SecondsBeforeTimeout': 123
        },
        DBClusterParameterGroupName='string',
        DeletionProtection=True|False,
        CopyTagsToSnapshot=True|False,
        Domain='string',
        DomainIAMRoleName='string',
        DBClusterInstanceClass='string',
        StorageType='string',
        Iops=123,
        PubliclyAccessible=True|False
    )
    """
    
def lambda_handler(event, context):
    restore_rds_all()