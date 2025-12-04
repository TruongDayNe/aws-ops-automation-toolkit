import boto3

def find_workshop_resources():
    # Sử dụng Resource Groups Tagging API thay vì client của từng dịch vụ
    # Region nên khớp với nơi bạn deploy CloudFormation
    tagging_client = boto3.client('resourcegroupstaggingapi', region_name='ap-northeast-1') 
    
    print("--- SCANNING FOR RESOURCES WITH TAG: Type=Workshop ---")
    
    # Tìm kiếm tất cả resource có tag Key='Type' và Value='Workshop'
    try:
        response = tagging_client.get_resources(
            TagFilters=[
                {
                    'Key': 'Type',
                    'Values': ['Workshop']
                }
            ],
            ResourcesPerPage=50 # Lấy tối đa 50 resource mỗi lần
        )
        
        resources = response['ResourceTagMappingList']
        
        if not resources:
            print("No resources found with tag Type: Workshop.")
            return

        print(f"Found {len(resources)} resources:")
        
        for resource in resources:
            resource_arn = resource['ResourceARN']
            # Lấy tên dịch vụ từ ARN (ví dụ: arn:aws:geo:... -> geo)
            service = resource_arn.split(':')[2] 
            
            print(f" - [{service.upper()}] {resource_arn}")
            
            # --- KHU VỰC XỬ LÝ XÓA (CẨN THẬN) ---
            # Nếu bạn muốn xóa tự động, bạn phải khởi tạo client tương ứng với service
            # Ví dụ: Nếu service == 'geo', gọi location_client.delete_...
            # Phần này phức tạp vì mỗi service có lệnh delete khác nhau.
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_workshop_resources()