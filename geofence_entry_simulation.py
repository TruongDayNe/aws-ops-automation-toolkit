import boto3
import time
from datetime import datetime

# ================= CẤU HÌNH =================
REGION = 'ap-northeast-1'      # Region của bạn (Check kỹ!)
TRACKER_NAME = 'WorkshopAssets' # Tên Tracker trong CloudFormation
DEVICE_ID = 'Vehicle-1'         # ID thiết bị giả lập

# Tọa độ mẫu (Bạn cần sửa lại cho khớp với Geofence bạn đã vẽ)
# Ví dụ: Geofence ở TP.HCM (Quận 1)
# Điểm 1: Ở xa (Ngoài Geofence)
POSITION_OUTSIDE = [108.150350, 16.076140] 
# Điểm 2: Đi vào trung tâm (Trong Geofence)
POSITION_INSIDE = [108.148642, 16.075313] 
# ============================================

client = boto3.client('location', region_name=REGION)

def update_position(lon, lat):
    print(f"🚚 Moving {DEVICE_ID} to [{lon}, {lat}]...")
    response = client.batch_update_device_position(
        TrackerName=TRACKER_NAME,
        Updates=[
            {
                'DeviceId': DEVICE_ID,
                'Position': [lon, lat],
                'SampleTime': datetime.utcnow()
            }
        ]
    )
    # Kiểm tra xem AWS có trả về sự kiện Geofence không (chỉ hiện trong response API)
    errors = response.get('Errors', [])
    if errors:
        print(f"❌ Error: {errors}")
    else:
        print("✅ Update Success.")

if __name__ == "__main__":
    print("--- BẮT ĐẦU MÔ PHỎNG ---")
    
    # Bước 1: Đặt thiết bị ở ngoài
    update_position(POSITION_OUTSIDE[0], POSITION_OUTSIDE[1])
    
    print("⏳ Đang đợi 5 giây để mô phỏng di chuyển...")
    time.sleep(5) 
    
    # Bước 2: Di chuyển thiết bị vào trong (Sẽ kích hoạt ENTER Event)
    update_position(POSITION_INSIDE[0], POSITION_INSIDE[1])
    
    print("--- KẾT THÚC ---")
    print("👉 Hãy kiểm tra terminal đang chạy 'aws logs tail' hoặc Email!")