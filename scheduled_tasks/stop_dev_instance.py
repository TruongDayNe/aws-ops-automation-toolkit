import boto3

def stop_dev_instances():
    ec2 = boto3.client('ec2', region_name='ap-southeast-1')
    
    # Lọc: Chỉ lấy server có Tag 'Environment=Dev' VÀ đang chạy (Running)
    filters = [
        {'Name': 'tag:Environment', 'Values': ['Dev']},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ]
    
    instances = ec2.describe_instances(Filters=filters)
    
    ids_to_stop = []
    
    # Gom ID lại
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            ids_to_stop.append(instance['InstanceId'])
            
    if len(ids_to_stop) > 0:
        print(f"Stopping instances: {ids_to_stop}")
        ec2.stop_instances(InstanceIds=ids_to_stop)
    else:
        print("No running Dev instances found.")

if __name__ == "__main__":
    stop_dev_instances()