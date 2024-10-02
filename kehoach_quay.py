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
                Nhiệm vụ của bạn là tạo ra một kịch bản video chi tiết trong từng mục nhỏ và đặt câu hỏi giúp người dùng dễ thực hiện hơn, chi tiết trong chi phí dựa trên thông tin được cung cấp."""},
                {"role": "user", "content": f"""
        Dựa trên thông tin sau đây:

        {prompt}

        Hãy tạo ra một kế hoạch quay video YouTube chi tiết trong 2 tuần, với mỗi tuần có thể có 1 video cho mỗi ý tưởng. Kế hoạch như sau:

        Kế hoạch phát triển sau ngày video thứ nhất
        Những Thiết bị đã được chuẩn bị và mua sắm nên không được tính vào chi phi

        Trong 4 tuần (mỗi tuần 1 video cho 2 ý tưởng)
        - Tuần 1: Lên kịch bản, chuẩn bị video 1, Quay video 1 và biên tập video 1
        - Tuần 2: Lên kịch bản, chuẩn bị video 2, Quay video 2 và biên tập video 2
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

    # Danh sách các file ý tưởng video (chỉ có 2 ý tưởng)
    video_files = ["video_idea_1.txt", "video_idea_2.txt"]
    video_plans = []

    for index, video_file in enumerate(video_files):
        # Đọc nội dung yêu cầu từ file
        user_info = read_file(video_file)
        video_guide = read_file("Hướng dẫn tạo video")
        
        prompt = f"""
Thông tin người dùng:
{user_info}

Hướng dẫn tạo video:
{video_guide}
        """
        
        print(f"Đang tạo kế hoạch cho video từ file '{video_file}'...")
        
        # Gọi hàm tạo kịch bản video
        script = generate_video_script(prompt, client)
        video_plans.append((video_file, script))
    
    # Tạo file kết quả cho từng kế hoạch
    for video_file, script in video_plans:
        plan_file_name = f"kehoach_{os.path.basename(video_file).replace('.txt', '')}.txt"
        create_file(plan_file_name, script)

    print("Tất cả kịch bản video đã được lưu vào các file tương ứng.")

if __name__ == "__main__":
    main()
