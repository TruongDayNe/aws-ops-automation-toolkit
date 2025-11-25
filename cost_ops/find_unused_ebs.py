import boto3

def find_unused_ebs():

    ec2 = boto3.client('ec2', region_name='ap-southeast-1') # Thay region 
    
    # Lọc các volume có trạng thái 'available'
    response = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    
    print("--- REPORT: UNUSED EBS VOLUMES (WASTED COST) ---")
    if not response['Volumes']:
        print("Great! No unused volumes found.")
        return

    for volume in response['Volumes']:
        v_id = volume['VolumeId']
        size = volume['Size']
        v_type = volume['VolumeType']
        # Tính nhẩm chi phí (Ví dụ gp3 ~ $0.08/GB)
        # est_cost = size * 0.08 # Điều chỉnh theo loại volume và region
        
        print(f"Found Wasted Volume: {v_id} | Size: {size}GB ({v_type})")
        # Uncomment dòng dưới để XÓA tự động (Cẩn thận!)
        # ec2.delete_volume(VolumeId=v_id)

if __name__ == "__main__":
    find_unused_ebs()