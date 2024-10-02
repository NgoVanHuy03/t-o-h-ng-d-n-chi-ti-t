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

def generate_video_ideas(prompt, client, model="gpt-4"):
    try:
        response = client.chat.completions.create(
            temperature=0.7,
            model=model,
            messages=[
                {"role": "system", "content": """Bạn là một chuyên gia sáng tạo nội dung video YouTube. 
                Nhiệm vụ của bạn là tạo ra 20 ý tưởng video chi tiết trong từng mục nhỏ và kết hợp với thông tin người dùng."""},
                {"role": "user", "content": f"""
        Dựa trên thông tin sau đây:

        {prompt}

        Hãy viết ra 20 ý tưởng video chi tiết
        """}
            ]
        )
        # Loại bỏ ký tự Markdown khỏi kết quả
        clean_text = remove_markdown_formatting(response.choices[0].message.content.strip())
        
        # Tạo danh sách các ý tưởng, loại bỏ dòng trống
        ideas = [idea for idea in clean_text.split('\n') if idea.strip()]
        
        return ideas  # Trả về danh sách ý tưởng không có dòng trống
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

    # Đọc nội dung yêu cầu từ file user_info.txt
    user_info = read_file("user_info.txt")
    video_guide = read_file("Hướng dẫn tạo video.txt")

    prompt = f"""
Thông tin người dùng:
{user_info}

Hướng dẫn tạo video:
{video_guide}
    """

    print("Đang tạo ý tưởng video...")

    # Gọi hàm tạo 20 ý tưởng video
    ideas = generate_video_ideas(prompt, client)

    if isinstance(ideas, list):
        # Giới hạn số lượng ý tưởng thành 20
        ideas = ideas[:20]
        
        # Tạo 20 file cho mỗi ý tưởng
        for i, idea in enumerate(ideas, 1):
            file_content = f"Idea {i}:\n{idea}\n\nThông tin người dùng:\n{user_info}"
            file_name = f"video_idea_{i}.txt"
            create_file(file_name, file_content)
        print("20 ý tưởng video đã được lưu vào các file.")
    else:
        print("Lỗi trong việc tạo kịch bản video: ", ideas)

if __name__ == "__main__":
    main()
