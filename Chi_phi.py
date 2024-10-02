import os
from openai import OpenAI
from dotenv import load_dotenv
import re  # Thêm thư viện re để loại bỏ ký tự Markdown

load_dotenv()

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Lỗi: Không tìm thấy file {file_path}"

def remove_markdown_formatting(text):
    """Loại bỏ các ký tự đặc biệt của Markdown như *, _, #, v.v."""
    # Loại bỏ các dấu * dùng để làm đậm hoặc in nghiêng
    text = re.sub(r'[\*\_]', '', text)
    # Loại bỏ tiêu đề markdown (# tiêu đề)
    text = re.sub(r'#+ ', '', text)
    return text

def generate_video_script(prompt, client, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            temperature=0.7,
            model=model,
            messages=[
                {"role": "system", "content": """Bạn là một chuyên gia sáng tạo nội dung video YouTube. 
                Nhiệm vụ của bạn là tạo ra chi tiết trong từng mục nhỏ ."""},
                {"role": "user", "content": f"""
        Dựa trên thông tin sau đây:

        {prompt}

        Hãy viết ra chi tiết chi phí của các mục cụ thể Thiết bị quay, chi phí quảng bá như nào và quảng bá ở đâu, càng chi tiết càng tốt để người dùng có thể hiểu đươc và thực hiện:

        Chi phí dự kiến (Chi tiết từng mục, chi phí của từng thiết bị quay phim)
        - Chi phí sản xuất:
        + Thiết bị quay phim:
        + Chi phí thuê diễn viên/nhiếp ảnh (nếu có):
        + Chi phí chỉnh sửa video:
        - Chi phí đi lại:
        - Chi phí ăn uống:
        - Chi phí vui chơi:
        - Chi phí thăm quan:
        - Chi phí quảng bá:
        - Dự phòng:

        """}
            ]
        )
        # Loại bỏ ký tự Markdown khỏi kết quả
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

    # Đọc nội dung yêu cầu từ file
    user_info = read_file("video_idea_1.txt")
    video_guide = read_file("Hướng dẫn tạo video")
    
    prompt = f"""
Thông tin người dùng:
{user_info}

Hướng dẫn tạo video:
{video_guide}
    """
    
    print("Đang dự đoán chi phí video...")
    
    # Gọi hàm tạo kịch bản video
    script = generate_video_script(prompt, client)
    
    # Tạo file kết quả
    create_file("chiphi.txt", script)
    print("Chi phí dự tính video đã được lưu vào file 'Chiphi.txt'")

if __name__ == "__main__":
    main()
