import os
from openai import OpenAI
from dotenv import load_dotenv
import re  # Thêm thư viện re để loại bỏ ký tự Markdown

load_dotenv()

def read_file(file_path):
    """Đọc nội dung từ tệp."""
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
    """Tạo kịch bản video bằng API GPT dựa trên thông tin từ prompt."""
    try:
        response = client.chat.completions.create(
            temperature=0.7,
            model=model,
            messages=[
                {"role": "system", "content": """Bạn là một chuyên gia sáng tạo nội dung video YouTube. 
                Nhiệm vụ của bạn là tạo ra chi tiết trong từng mục nhỏ và đặt câu hỏi giúp người dùng dễ thực hiện hơn, chi tiết trong chi phí dựa trên thông tin được cung cấp."""},
                {"role": "user", "content": prompt}  # Sử dụng prompt đã được tạo trong hàm main()
            ]
        )
        # Loại bỏ ký tự Markdown khỏi kết quả
        clean_text = remove_markdown_formatting(response.choices[0].message.content.strip())
        return clean_text
    except Exception as e:
        return f"Lỗi khi gọi API ChatGPT: {str(e)}"

def create_file(file_path, content):
    """Tạo và ghi nội dung vào tệp."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"File '{file_path}' đã được tạo và ghi nội dung.")
    except Exception as e:
        print(f"Lỗi khi tạo file '{file_path}': {e}")

def main():
    # Khởi tạo client OpenAI (chỉnh lại thông tin nếu cần)
    client = OpenAI()

    # Đọc nội dung yêu cầu từ file
    user_info = read_file("video_idea_1.txt")
    video_guide = read_file("Huong_dan_tao_video.txt")
    
    # Định dạng prompt với chuỗi nhiều dòng
    prompt = f"""
Thông tin người dùng:
{user_info}

Hướng dẫn tạo video:
{video_guide}

Hãy viết ra chi tiết từng bước sản xuất video càng chi tiết càng tốt để người dùng có thể hiểu được và thực hiện:

Các bước sản xuất:
a. Chuẩn bị trước quay: 
    - Lên kế hoạch chi tiết cho từng cảnh quay.
    - Các thiết bị cần chuẩn bị (máy ảnh, đèn chiếu sáng, micro).
    - Cách chuẩn bị ánh sáng phù hợp cho chủ đề đi phượt.
    - Các loại góc quay phù hợp cho việc quay cảnh ngoại cảnh (góc rộng, cận cảnh, flycam).
    - Thời điểm và vị trí quay thích hợp (buổi sáng, hoàng hôn, hoặc địa điểm nổi bật dọc hành trình Hà Nội - Sapa).
    - Tính toán chi phí cho việc thuê thiết bị hoặc sử dụng thiết bị cá nhân.
    
b. Quay video:
    - Hướng dẫn cách điều chỉnh máy quay (khẩu độ, tốc độ màn trập) để quay phong cảnh.
    - Kỹ thuật quay bằng tay để có được góc quay ổn định khi không dùng gimbal.
    - Cách sử dụng flycam để quay các đoạn video từ trên cao, tạo cảm giác bao quát.
    - Cách quay cảnh xe máy di chuyển trên đường, tạo hiệu ứng chuyển động cho video.
    - Mẹo thu âm trực tiếp khi quay trong môi trường gió, mưa.
    
c. Chỉnh sửa video:
    - Các phần mềm chỉnh sửa video phù hợp (Premiere Pro, DaVinci Resolve).
    - Cách cắt ghép các đoạn video sao cho mạch lạc, hấp dẫn.
    - Điều chỉnh âm thanh và thêm nhạc nền cho phù hợp với từng phân đoạn.
    - Các hiệu ứng màu sắc để làm nổi bật cảnh đẹp của Sapa và các điểm đến trên đường.
    - Tạo intro và outro, kêu gọi người xem like, share, và subscribe.

d. Tối ưu hóa SEO:
    - Hướng dẫn viết tiêu đề và mô tả video phù hợp với từ khóa "đi phượt Hà Nội - Sapa".
    - Cách thêm thẻ tag liên quan đến chủ đề du lịch và phượt.
    - Tạo thumbnail hấp dẫn, thu hút sự chú ý từ người xem.

e. Chia sẻ nội dung:
    - Đăng tải video trên các nền tảng (YouTube, Facebook, Instagram).
    - Cách chia sẻ video trên các group và cộng đồng du lịch để tăng lượt xem.
    - Sử dụng các công cụ quảng cáo để tăng độ phủ sóng của video.
    
Không cần tính chi phí ở phần này    
    """
    print("Đang tạo bước sản xuất video...")
    
    # Gọi hàm tạo kịch bản video
    script = generate_video_script(prompt, client)
    
    # Tạo file kết quả
    create_file("BuocSanXuat.txt", script)
    print("Bước sản xuất video đã được lưu vào file 'BuocSanXuat.txt'")

if __name__ == "__main__":
    main()
