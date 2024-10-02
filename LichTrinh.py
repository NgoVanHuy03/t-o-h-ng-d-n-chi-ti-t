import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Lỗi: Không tìm thấy file {file_path}"

def remove_markdown_formatting(text):
    text = re.sub(r'[\*\_]', '', text)
    text = re.sub(r'#+ ', '', text)
    return text

def generate_video_script(prompt, client, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            temperature=0.7,
            model=model,
            messages=[
                {"role": "system", "content": """Bạn là một chuyên gia sáng tạo nội dung video YouTube và đạo diễn video du lịch. 
                Nhiệm vụ của bạn là tạo ra một lịch trình quay video chi tiết, bao gồm cách quay và thời gian cụ thể cho từng cảnh."""},
                {"role": "user", "content": prompt}
            ]
        )
        clean_text = remove_markdown_formatting(response.choices[0].message.content.strip())
        return clean_text
    except Exception as e:
        return f"Lỗi khi gọi API ChatGPT: {str(e)}"

def create_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File '{file_path}' đã được tạo và ghi nội dung.")
    except Exception as e:
        print(f"Lỗi khi tạo file '{file_path}': {e}")

def main():
    client = OpenAI()

    user_info = read_file("video_idea_1.txt")
    video_guide = read_file("Hướng dẫn tạo video")
    cost_info = read_file("chiphi.txt")
    sanxuat = read_file("BuocSanXuat.txt")
    
    prompt = f"""
Thông tin người dùng:
{user_info}

Hướng dẫn tạo video:
{video_guide}

Thông tin chi phí:
{cost_info}

Thông tin bước sản xuất:
{sanxuat}

Hãy tạo ra một lịch trình quay video chi tiết theo thông tin người dùng, bao gồm:

1. Thời gian cụ thể cho từng cảnh quay (ngày, giờ)
2. Địa điểm quay cho mỗi cảnh
3. Nội dung cần quay trong mỗi cảnh
4. Kỹ thuật quay cụ thể (góc máy, chuyển động camera, loại shot)
5. Thiết bị cần sử dụng cho mỗi cảnh (máy quay, gimbal, drone, v.v.)
6. Thời lượng dự kiến cho mỗi cảnh
7. Ghi chú về ánh sáng và âm thanh cần chú ý

Hãy chia lịch trình quay thành các ngày cụ thể, từ lúc khởi hành đến khi kết thúc chuyến đi. Đảm bảo rằng lịch trình quay phù hợp với các hoạt động và thời gian di chuyển.

Đối với mỗi địa điểm hoặc hoạt động chính, hãy đề xuất ít nhất 2-3 cảnh quay khác nhau để đảm bảo có đủ tư liệu cho quá trình biên tập sau này.

Cuối cùng, hãy đưa ra một số gợi ý về cách tối ưu hóa quá trình quay để đảm bảo chất lượng video tốt nhất trong khuôn khổ ngân sách và thời gian có sẵn.
    """
    
    print("Đang tạo lịch trình quay video...")
    
    schedule = generate_video_script(prompt, client)
    
    create_file("LichTrinh.txt", schedule)
    print("Lịch trình quay video chi tiết đã được lưu vào file 'LichTrinhQuayVideo.txt'")

if __name__ == "__main__":
    main()