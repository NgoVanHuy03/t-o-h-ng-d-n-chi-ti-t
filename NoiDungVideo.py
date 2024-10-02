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

def generate_enhanced_content(prompt, effects, shots, client, model="gpt-4-1106-preview"):
    try:
        response = client.chat.completions.create(
            temperature=0.7,
            model=model,
            messages=[
                {"role": "system", "content": """Bạn là một chuyên gia sáng tạo nội dung video YouTube. 
                Nhiệm vụ của bạn là tạo ra chi tiết trong từng mục nhỏ và chọn hiệu ứng, cảnh quay phù hợp cho từng phân đoạn."""},
                {"role": "user", "content": f"""
        Dựa trên thông tin sau đây:

        {prompt}

        Hiệu ứng có sẵn:
        {effects}

        Cảnh quay có sẵn:
        {shots}

        Hãy tạo nội dung chi tiết cho video, bao gồm cả việc chọn hiệu ứng và cảnh quay phù hợp cho từng phân đoạn.
        Với mỗi phân đoạn, hãy chọn ít nhất 1 hiệu ứng và 1 cảnh quay phù hợp nhất 
        Hướng dẫn cách sử dụng chúng 1 cách chi tiết
        Đặt hiệu ứng, cảnh quay, và nhạc nền phù hợp có lời hoặc không lời được chọn trong ngoặc vuông sau mỗi phân đoạn, 
        Giải thích ngắn gọn lý do chọn hiệu ứng, cảnh quay, và nhạc nền đó.


        Gợi ý 3-5 câu thoại cho mỗi phân đoạn

        Những phân đoạn nào sẽ nên ghép lời thoại
        """}
            ]
        )
        return remove_markdown_formatting(response.choices[0].message.content.strip())
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

    noi_dung_chinh = read_file("noidungchinh.txt")
    hieu_ung = read_file("HieuUng.txt")
    canh_quay = read_file("CanhQuay.txt")
    
    prompt = f"""
Nội dung chính:
{noi_dung_chinh} được kết hợp để ra được nội dung chi tiết cho video
    """
    
    print("Đang tạo nội dung chi tiết cho video...")
    
    enhanced_content = generate_enhanced_content(prompt, hieu_ung, canh_quay, client)
    
    create_file("NoiDungVideo.txt", enhanced_content)
    print("Nội dung chi tiết cho video đã được lưu vào file 'NoiDungVideo.txt'")

if __name__ == "__main__":
    main()