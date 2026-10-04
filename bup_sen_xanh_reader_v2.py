import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="Đọc Sách Điện Tử Giọng Nói & Điều Khiển Bằng Giọng Nói - Búp Sen Xanh",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. CẤU TRÚC ĐẦY ĐỦ 31 PHẦN TÁC PHẨM "BÚP SEN XANH" (Sơn Tùng)
# Grounded strictly from source: 7278-bup-sen-xanh-thuviensach.vn.pdf
# ---------------------------------------------------------
BOOK_DATA = {
    # TÁC GIẢ
    "c0_p0": {
        "chapter": "Giới Thiệu Tác Giả",
        "part": "Đôi Nét Về Tác Giả Sơn Tùng",
        "title": "Nhà Văn, Nhà Cách Mạng Sơn Tùng (1926 - 2021)",
        "content": """Nhà văn Sơn Tùng là nhà văn, nhà cách mạng đã dành trọn cuộc đời sưu tầm, nghiên cứu và khắc họa cuộc đời Chủ tịch Hồ Chí Minh.

Năm 1971, ông bị thương nặng tại chiến trường miền Nam mang trên mình 14 vết thương. Với nghị lực phi thường, ông khổ luyện phục hồi sức khỏe và lao vào sáng tác. "Búp Sen Xanh" là tác phẩm tiểu thuyết lịch sử xuất sắc nhất của ông về tuổi thơ và tuổi trẻ của Bác Hồ."""
    },
    # CHƯƠNG I: THỜI THƠ ẤU (12 PHẦN)
    "c1_p1": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 1 - Đầm Sen Làng Chùa",
        "title": "Sự Ra Đời Của Cậu Bé Nguyễn Sinh Côn",
        "content": """Cơn dông mùa hạ dấy lên ở phía nam. Mây đen từng khối ùn ùn từ dưới chân trời đùn lên. Bên gốc cây đa đầu làng Chùa, ông Xẩm ngước đôi mắt mù lòa đón nhận mùi hoa sen từ đầm làng đưa tới.

Bé Thanh - con gái đầu lòng của anh chị nho Sắc - biếu ông Xẩm mấy cái gương sen luộc. Trong căn nhà nhỏ bên đầm sen ngào ngạt hương, chị nho Sắc sinh hạ người con trai thứ hai. Ông đồ Hoàng Xuân Đường đặt tên cho cháu là Nguyễn Sinh Côn, tự Tất Thành."""
    },
    "c1_p2": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 2 - Gia Thế Mẹ Hoàng Thị Loan",
        "title": "Tấm Lòng Của Người Mẹ Xứ Nghệ",
        "content": """Ba cha con ông Sắc sống trong tình yêu thương của gia đình ông bà đồ Hoàng Xuân Đường. Cậu bé Côn lớn lên trong tiếng ru dịu dàng của mẹ Hoàng Thị Loan và những bài học làm người đầu tiên từ ông ngoại."""
    },
    "c1_p3": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 3 - Cội Nguồn Làng Sen",
        "title": "Chuyện Về Tuổi Thơ Vất Vả Của Anh Nho Sắc",
        "content": """Do có nhiều sen, cảnh trí trong làng ngoài đồng lại đẹp nên Trại Sen đổi tên thành làng Mỹ Liên, về sau các cụ đổi là Kim Liên. Nguyễn Sinh Sắc mồ côi cha từ lên ba, rồi mẹ qua đời khi cậu mới hơn bốn tuổi. Tấm gương hiếu học vượt khó của anh nho Sắc đã đơm hoa kết trái dưới sự chỉ bảo của thầy đồ Hoàng Xuân Đường."""
    },
    "c1_p4": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 4 - Đỗ Đạt Vinh Quy",
        "title": "Khoa Thi Giáp Ngọ Và Tấm Lòng Vượt Quan Trường",
        "content": """Năm Giáp Ngọ (1894), anh nho Sắc đỗ Cử nhân trường Nghệ. Tuy đỗ đạt vinh hiển nhưng anh Sắc luôn giữ nếp sống giản dị, khẳng định: "Tôi sinh từ làng Sen, lớn lên trên đất làng Chùa, tôi là dân và bao giờ cũng là người dân của xứ sở ta." """
    },
    "c1_p5": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 5 - Khăn Gói Vào Kinh",
        "title": "Chuyến Đi Bộ Đường Dài Vào Kinh Thành Huế",
        "content": """Sương sớm ám mái nhà. Gia đình anh cử Sắc lên đường vào Huế để anh học trường Quốc Tử Giám. Cậu bé Côn và anh Khiêm háo hức đi theo cha mẹ qua những đèo cao vực sâu, qua đèo Ngang bạt ngàn gió biển."""
    },
    "c1_p6": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 6 - Ấn Tượng Kinh Thành",
        "title": "Cậu Bé Côn Trước Cảnh Tượng Ngọ Môn Và Bến Đá",
        "content": """Vào tới kinh thành Huế, Côn ngơ ngác trước sự nguy nga của cung điện, lầu gác nhưng cũng tận mắt thấy nỗi cực khổ của phu xịt, người nghèo. Côn học tiếng Pháp và giao lưu cùng các bạn nhỏ thành nội như Công tôn nữ Huệ Minh, Diệp Văn Kỳ."""
    },
    "c1_p7": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 7 - Trí Tuệ Khôi Ngô",
        "title": "Sự Thông Minh Và Trí Nhớ Kỳ Diệu Của Côn",
        "content": """Tại làng Dương Nổ, Côn tỏ ra thông minh kiệt xuất. Cậu thuộc làu mười lăm trang sách và viết chữ đẹp như in trên đất làm các bạn học và cha rất khâm phục."""
    },
    "c1_p8": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 8 - Bi Kịch Nơi Kinh Kỳ",
        "title": "Ngày Mẹ Loan Qua Đời Khi Cha Đi Vắng",
        "content": """Mùa hè năm cuối thế kỷ 19, chị cử Sắc sinh thêm em bé Nguyễn Sinh Nhuận (tên gọi Xin). Trong lúc ông Sắc đi chấm thi ở Thanh Hóa, chị Sắc lâm bệnh nặng và trút hơi thở cuối cùng. Cậu bé Côn mới mười tuổi đầu một mình ẵm em thơ khóc nghẹn giữa kinh thành quạnh quẽ."""
    },
    "c1_p9": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 9 - Đau Thương Và Trưởng Thành",
        "title": "Cậu Bé Côn Tiễn Đưa Mẹ Và Em Xin",
        "content": """Ông Sắc trở về Huế bàng hoàng trước cảnh tang thương. Em Xin cũng yếu dần rồi qua đời. Những đau thương mất mát lớn lao đã tôi luyện tâm hồn cậu bé Côn trở nên sâu sắc và giàu tình yêu thương đồng bào."""
    },
    "c1_p10": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 10 - Trở Về Quê Mẹ",
        "title": "Những Ngày Bên Bà Ngoại Làng Chùa",
        "content": """Côn trở về quê ngoại. Cụ đồ An chăm sóc các cháu trong niềm thương nhớ người con gái xấu số. Côn hằng ngày nhai trầu, sắc thuốc cho bà và lắng nghe những câu chuyện lịch sử, những bài vè yêu nước."""
    },
    "c1_p11": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 11 - Nỗi Đau Mất Bà",
        "title": "Bà Ngoại Qua Đời - Tuổi Thơ Đầy Trăn Trở",
        "content": """Cụ đồ An tạ thế. Côn ngậm ngùi chứng kiến thêm một người thân yêu ra đi. Trí tuệ và tâm hồn Côn càng thêm chín chắn trước thời cuộc nước mất nhà tan."""
    },
    "c1_p12": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 12 - Gặp Gỡ Cụ Phan Bội Châu",
        "title": "Chiết Tự Độc Đáo Và Lời Chia Tay Đồng Chí",
        "content": """Năm 1904, Phan Bội Châu lập Duy Tân Hội. Nguyễn Sinh Côn đàm đạo và chiết tự thông minh khiến cụ Phan Bội Châu kinh ngạc và khen ngợi: "Lớp người sinh sau thật đáng sợ!" """
    },
    # CHƯƠNG II: THỜI NIÊN THIẾU (11 PHẦN)
    "c2_p1": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 1 - Búp Sen Xanh",
        "title": "Búp Sen Xanh - Món Quà Chia Tay Quê Hương",
        "content": """Đường làng Sen ngào ngạt hương. Những bông sen trong đầm xòe cánh lụa mượt mà dưới ánh nắng mai dìu dịu. Các bạn thân chạy đến trao cho Côn gói khoai luộc và một búp sen xanh vươn cao giữa đầm. Côn nâng niu búp sen xanh, đăm đăm nhìn lại quê nhà trước khi vào Nam."""
    },
    "c2_p2": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 2 - Tên Gọi Nguyễn Tất Thành",
        "title": "Chặng Đường Mới Tại Kinh Đô Huế",
        "content": """Ba cha con ông Sắc trở lại Huế với tên gọi mới: quan Phó bảng Nguyễn Sinh Huy và hai con Nguyễn Tất Đạt, Nguyễn Tất Thành. Thành theo học chữ Quốc ngữ và tiếng Pháp tại trường Tiểu học Đông Ba."""
    },
    "c2_p3": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 3 - Trường Đông Ba",
        "title": "Học Chữ Mới Mở Mang Đầu Óc",
        "content": """Tất Thành đạt kết quả xuất sắc tại trường Đông Ba. Thầy giáo khen ngợi Thành dịch câu tiếng Pháp ra ca dao tiếng Việt rất ngọt ngào. Thành đọc sách "Không gia đình" và trăn trở về thời cuộc."""
    },
    "c2_p4": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 4 - Đêm Kỷ Niệm",
        "title": "Cuộc Gặp Với Chí Sĩ Đặng Thái Thân",
        "content": """Trong đêm giỗ mẹ, chí sĩ Đặng Thái Thân đến thăm và trao đổi về phong trào yêu nước. Tất Thành thể hiện quyết tâm cứu nước, cứu đồng bào khỏi ách nô lệ."""
    },
    "c2_p5": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 5 - Quan Quát Cung Đình",
        "title": "Thăm Lăng Tẩm Và Trăn Trở Nỗi Đau Dân Tộc",
        "content": """Thành cùng bạn bè đi thăm các lăng tẩm Huế và chùa Thiên Mụ. Nhìn thấy cảnh vua Thành Thái bị thực dân Pháp truất ngôi và đày đi biệt xứ, lòng Thành sôi sục ý chí đấu tranh."""
    },
    "c2_p6": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 6 - Chia Tay Cha Vô Bình Khê",
        "title": "Lời Dặn Của Cha: Làm Dân Là Nguyện Ước Của Cha",
        "content": """Quan Phó bảng Nguyễn Sinh Huy nhận lệnh đi nhậm chức Tri huyện Bình Khê. Trước khi đi, ông dặn con: "Dân... làm người dân là nguyện ước của cha." Thành xòe tay che nắng nhìn theo bóng cha đi xa."""
    },
    "c2_p7": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 7 - Trường Quốc Học Huế",
        "title": "Học Tập Và Tự Lập Nơi Quán Trọ Ao Hồ",
        "content": """Tất Thành và Tất Đạt trọ học tại quán Ao Hồ. Thành vào học trường Quốc Học Huế, tự lập giặt giũ, ăn cơm bình dân và từ chối sống nhờ sự giúp đỡ của thầy Lê Văn Miến để rèn chí chịu khổ."""
    },
    "c2_p8": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 8 - Phong Trào Chống Thuế 1908",
        "title": "Đứng Về Phía Nhân Dân Biểu Tình Chống Pháp",
        "content": """Tháng 4 năm 1908, phong trào chống xâu thuế bùng nổ ở Thừa Thiên Huế. Tất Thành tham gia thông ngôn cho bà con nông dân biểu tình trước Tòa Khâm sứ Pháp và bị mật thám săn đuổi."""
    },
    "c2_p9": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 9 - Đi Vào Miền Trong",
        "title": "Quyết Định Rời Huế Tìm Hướng Đi Riêng",
        "content": """Thành quyết định rời Huế đi vào phía Nam. Anh đến Bình Khê thăm cha. Quan huyện Sắc khuyên con: "Nước mất con đi tìm nước... Con phải tự tìm ra cho mình một hướng đi!" """
    },
    "c2_p10": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 10 - Thầy Giáo Trường Dục Thanh",
        "title": "Dạy Học Ở Phan Thiết Và Tình Thương Học Trò",
        "content": """Nguyễn Tất Thành dừng chân tại Phan Thiết, trở thành thầy giáo trẻ yêu quý học trò tại trường Dục Thanh. Thầy truyền cho học trò tinh thần yêu nước, lòng tự trọng và tri thức."""
    },
    "c2_p11": {
        "chapter": "Chương II: Thời Niên Thiếu",
        "part": "Phần 11 - Rời Trường Dục Thanh",
        "title": "Bức Thư Tạm Biệt Học Trò Để Vào Sài Gòn",
        "content": """Tháng 10 năm 1910, thầy giáo Nguyễn Tất Thành âm thầm rời Phan Thiết vào Sài Gòn. Thầy để lại bức thư dặn dò học trò: "Hồn nước gọi chúng ta lên phía trước!" """
    },
    # CHƯƠNG III: TUỔI HAI MƯƠI (7 PHẦN)
    "c3_p1": {
        "chapter": "Chương III: Tuổi Hai Mươi",
        "part": "Phần 1 - Đặt Chân Đến Sài Gòn",
        "title": "Xóm Thợ Bến Nhà Rồng Và Anh Ba Nghệ",
        "content": """Anh Ba (Nguyễn Tất Thành) đến Sài Gòn, sống hòa mình vào cuộc sống gian lao của phu xóm thợ Bến Nhà Rồng. Anh được gia đình ông già Đờn và cô Út Huệ thương yêu, quý mọng."""
    },
    "c3_p2": {
        "chapter": "Chương III: Tuổi Hai Mươi",
        "part": "Phần 2 - Gặp Lại Cha Tại Sài Gòn",
        "title": "Cuộc Gặp Nhớ Đời Tại Tiệm Thuốc Tam Thiên Đường",
        "content": """Anh Ba gặp lại cha - quan Phó bảng Huy - đang ngồi bốc thuốc nam cứu người tại tiệm Tam Thiên Đường. Hai cha con nghẹn ngào trong giây phút đoàn tụ ngắn ngủi trước giờ đi xa."""
    },
    "c3_p3": {
        "chapter": "Chương III: Tuổi Hai Mươi",
        "part": "Phần 3 - Hình Ảnh Út Huệ",
        "title": "Tấm Khăn Mùi Soa Và Tình Cảm Thanh Cao",
        "content": """Anh Ba dành số tiền tiết kiệm mua chiếc khăn rằn và khăn mùi soa tặng Út Huệ. Cô gái Sài Gòn mang vẻ đẹp rạng rỡ như búp sen xanh ẩn chứa tình cảm sâu lắng dành cho anh Ba."""
    },
    "c3_p4": {
        "chapter": "Chương III: Tuổi Hai Mươi",
        "part": "Phần 4 - Lớp Học Ánh Sáng",
        "title": "Dạy Chữ Cho Anh Em Phu Bốc Vác Bến Cảng",
        "content": """Anh Ba mở lớp dạy chữ Quốc ngữ cho anh em thợ thuyền Bến Nhà Rồng. Trong căn nhà lụp xụp của ông già Đờn, ánh sáng tri thức do anh Ba thắp lên làm ấm lòng những người lao động."""
    },
    "c3_p5": {
        "chapter": "Chương III: Tuổi Hai Mươi",
        "part": "Phần 5 - Lời Dặn Của Cha",
        "title": "Con Hãy Gọi: Tổ Quốc! Đồng Bào! Đi... Đi Con!",
        "content": """Trước khi xuống tàu, anh Ba đến chào cha. Quan Phó bảng Huy ngăn giọt lệ dặn con: "Đừng! Con đừng gọi cha lúc này! Con phải gọi: Tổ quốc! Đồng bào! Đi... đi con!" """
    },
    "c3_p6": {
        "chapter": "Chương III: Tuổi Hai Mươi",
        "part": "Phần 6 - Xin Việc Trên Tàu Đô Đốc Latouche-Tréville",
        "title": "Gặp Thuyền Trưởng Mai-sen Và Nhận Việc Bồi Tàu",
        "content": """Ngày 2 tháng 6 năm 1911, anh Ba lên con tàu Amiral Latouche-Tréville gặp thuyền trưởng Louis Édouard Maisen xin làm việc. Anh chấp nhận làm phụ bếp, công việc nặng nhọc nhất để có cơ hội sang Pháp."""
    },
    "c3_p7": {
        "chapter": "Chương III: Tuổi Hai Mươi",
        "part": "Phần 7 - Ra Đi Tìm Đường Cứu Nước",
        "title": "Ngày 5 Tháng 6 Năm 1911 - Con Tàu Rời Bến Nhà Rồng",
        "content": """Ngày 5 tháng 6 năm 1911, con tàu Latouche-Tréville nhấc neo rời Bến Nhà Rồng. Người thanh niên Nguyễn Tất Thành rời Tổ quốc ra đi tìm đường cứu nước, mang theo hình ảnh quê hương và búp sen xanh đọng mãi trong tâm trí."""
    }
}

# ---------------------------------------------------------
# 3. DANH SÁCH KHÓA CHƯƠNG ĐỂ LẬT TRANG
# ---------------------------------------------------------
CHAPTER_KEYS = list(BOOK_DATA.keys())

def get_qr_code_url(chapter_id):
    qr_data = f"https://bup-sen-xanh.app/read?id={chapter_id}"
    encoded_data = urllib.parse.quote(qr_data)
    return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_data}&color=0d5c3a"

# ---------------------------------------------------------
# 4. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.markdown("""
    <style>
    .main-header { text-align: center; color: #1b4d3e; font-size: 2.2rem; font-weight: bold; margin-bottom: 5px; }
    .sub-header { text-align: center; color: #3b7a57; font-size: 1.05rem; margin-bottom: 20px; }
    .content-card { background-color: #f7faf7; border-left: 6px solid #2d8a4e; padding: 22px; border-radius: 8px; font-size: 1.1rem; line-height: 1.8; color: #111; }
    .chapter-tag { background-color: #e2f0d9; color: #1b4d3e; padding: 5px 14px; border-radius: 15px; font-weight: bold; font-size: 0.95rem; }
    .voice-box { background-color: #eef7f2; border: 1px solid #b8e0c8; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .status-badge { background-color: #0d5c3a; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🪷 Web Đọc Sách Giọng Nói & Điều Khiển Lật Trang Bằng Giọng Nói</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tác Phẩm Hoàn Chỉnh: <b>BÚP SEN XANH</b> (Tác Giả: Sơn Tùng)</div>', unsafe_allow_html=True)

# Navigation
st.sidebar.title("📌 Menu Chức Năng")
app_mode = st.sidebar.radio("Chọn trải nghiệm:", [
    "🎙️ Trình Đọc & Điều Khiển Bằng Giọng Nói (Voice-Controlled Reader)",
    "📷 Quét Mã QR Sách Giấy (QR Reader Simulation)",
    "🏷️ Danh Mục Mã QR 31 Phần Sách (QR Code Manager)"
])

# ---------------------------------------------------------
# MODE 1: TRÌNH ĐỌC SÁCH + ĐIỀU KHIỂN GIỌNG NÓI (VOICE COMMAND + TTS)
# ---------------------------------------------------------
if app_mode == "🎙️ Trình Đọc & Điều Khiển Bằng Giọng Nói (Voice-Controlled Reader)":
    st.subheader("🎙️ Trình Đọc Giọng Nói & Nhận Diện Khẩu Lệnh Lật Trang")
    
    # Session state for chapter index
    if "current_index" not in st.session_state:
        st.session_state.current_index = 1 # Start at Chapter 1 Part 1
        
    # Read query params if scanned via QR
    query_params = st.query_params
    if "id" in query_params:
        qid = query_params["id"]
        if qid in CHAPTER_KEYS:
            st.session_state.current_index = CHAPTER_KEYS.index(qid)
            
    # Controls
    col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
    with col_nav1:
        if st.button("⬅️ Phần Trước", use_container_width=True):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.rerun()
    with col_nav3:
        if st.button("Phần Tiếp ➡️", use_container_width=True):
            if st.session_state.current_index < len(CHAPTER_KEYS) - 1:
                st.session_state.current_index += 1
                st.rerun()
                
    # Selectbox sync
    selected_key = CHAPTER_KEYS[st.session_state.current_index]
    
    def on_chapter_change():
        st.session_state.current_index = CHAPTER_KEYS.index(st.session_state.select_key)

    st.sidebar.selectbox(
        "Chuyển nhanh phần sách:",
        CHAPTER_KEYS,
        index=st.session_state.current_index,
        format_func=lambda k: f"{BOOK_DATA[k]['chapter']} - {BOOK_DATA[k]['part']}",
        key="select_key",
        on_change=on_chapter_change
    )
    
    data = BOOK_DATA[selected_key]
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown(f"<span class='chapter-tag'>{data['chapter']}</span>", unsafe_allow_html=True)
        st.markdown(f"### {data['title']}")
        st.caption(f"📍 {data['part']} | Trang {st.session_state.current_index + 1} / {len(CHAPTER_KEYS)}")
        
        paragraphs = data["content"].split("\n\n")
        formatted = "".join([f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()])
        st.markdown(f'<div class="content-card">{formatted}</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown("### 🎙️ Điều Khiển Bằng Giọng Nói")
        st.info("💡 **Khẩu lệnh hỗ trợ (Nói vào Micro):**\n- **'trang tiếp' / 'tiếp tục'**: Sang phần tiếp theo\n- **'quay lại' / 'trở lại'**: Về phần trước\n- **'đọc' / 'phát'**: Đọc nội dung\n- **'dừng'**: Dừng đọc")
        
        clean_text_js = data["content"].replace("\n", " ").replace("'", "\\\'").replace('"', '\\"')
        
        # Embedded Web Speech API: Voice Commands + Speech Synthesis
        voice_html = f"""
        <div class="voice-box" style="text-align: center;">
            <div style="margin-bottom: 12px;">
                <button onclick="playTTS()" style="background-color: #2d8a4e; color: white; border: none; padding: 10px 18px; font-size: 15px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-right: 5px;">
                    ▶️ Đọc Giọng Nói
                </button>
                <button onclick="stopTTS()" style="background-color: #c94c4c; color: white; border: none; padding: 10px 15px; font-size: 15px; font-weight: bold; border-radius: 6px; cursor: pointer;">
                    ⏹️ Dừng
                </button>
            </div>
            
            <hr style="border: 0.5px solid #ccc; margin: 10px 0;">
            
            <button id="mic-btn" onclick="toggleRecognition()" style="background-color: #1b4d3e; color: white; border: none; padding: 12px 20px; font-size: 15px; font-weight: bold; border-radius: 25px; cursor: pointer; width: 100%;">
                🎙️ Bật Nhận Diện Khẩu Lệnh
            </button>
            
            <p id="speech-status" style="margin-top: 10px; font-size: 13px; color: #333; font-weight: 500;">Micro đang tắt.</p>
            <p id="speech-result" style="font-size: 13px; color: #2d8a4e; font-style: italic;"></p>
        </div>

        <script>
        var synth = window.speechSynthesis;
        var recognition = null;
        var isListening = false;

        function playTTS() {{
            if (!('speechSynthesis' in window)) {{ alert('Trình duyệt không hỗ trợ TTS.'); return; }}
            synth.cancel();
            var text = "{clean_text_js}";
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'vi-VN';
            u.rate = 0.95;
            document.getElementById('speech-status').innerText = '🔊 Đang đọc giọng nói tiếng Việt...';
            u.onend = function() {{ document.getElementById('speech-status').innerText = '✅ Đã đọc xong.'; }};
            synth.speak(u);
        }}

        function stopTTS() {{
            if (synth) synth.cancel();
            document.getElementById('speech-status').innerText = '⏹️ Đã dừng phát giọng nói.';
        }}

        // SPEECH RECOGNITION (WEB SPEECH API)
        function initRecognition() {{
            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {{
                alert('Trình duyệt của bạn không hỗ trợ Web Speech Recognition (Khuyên dùng Chrome/Edge).');
                return null;
            }}
            var rec = new SpeechRecognition();
            rec.lang = 'vi-VN';
            rec.continuous = true;
            rec.interimResults = false;

            rec.onstart = function() {{
                isListening = true;
                document.getElementById('mic-btn').innerText = '🔴 Đang Lắng Nghe... (Bấm để tắt)';
                document.getElementById('mic-btn').style.backgroundColor = '#c94c4c';
                document.getElementById('speech-status').innerText = '🎙️ Hãy nói khẩu lệnh (VD: "Trang tiếp", "Quay lại", "Đọc")...';
            }};

            rec.onresult = function(event) {{
                var last = event.results.length - 1;
                var command = event.results[last][0].transcript.trim().toLowerCase();
                document.getElementById('speech-result').innerText = '🗣️ Khẩu lệnh nhận diện: "' + command + '"';
                
                // Process Voice Commands
                if (command.includes('tiếp') || command.includes('sau') || command.includes('next')) {{
                    document.getElementById('speech-status').innerText = '🚀 Đang chuyển sang phần tiếp...';
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'NEXT'}}, '*');
                    window.top.location.href = window.top.location.pathname + '?cmd=next';
                }} else if (command.includes('quay lại') || command.includes('trở lại') || command.includes('trước') || command.includes('back')) {{
                    document.getElementById('speech-status').innerText = '⬅️ Đang quay lại phần trước...';
                    window.top.location.href = window.top.location.pathname + '?cmd=prev';
                }} else if (command.includes('đọc') || command.includes('phát') || command.includes('bắt đầu')) {{
                    playTTS();
                }} else if (command.includes('dừng') || command.includes('ngừng') || command.includes('tắt')) {{
                    stopTTS();
                }}
            }};

            rec.onerror = function(e) {{
                document.getElementById('speech-status').innerText = '⚠️ Lỗi Micro: ' + e.error;
            }};

            rec.onend = function() {{
                if (isListening) {{ rec.start(); }} // auto-restart
                else {{
                    document.getElementById('mic-btn').innerText = '🎙️ Bật Nhận Diện Khẩu Lệnh';
                    document.getElementById('mic-btn').style.backgroundColor = '#1b4d3e';
                    document.getElementById('speech-status').innerText = 'Micro đã tắt.';
                }}
            }};

            return rec;
        }}

        function toggleRecognition() {{
            if (!recognition) recognition = initRecognition();
            if (!recognition) return;

            if (isListening) {{
                isListening = false;
                recognition.stop();
            }} else {{
                recognition.start();
            }}
        }}
        </script>
        """
        components.html(voice_html, height=270)
        
        st.divider()
        st.image(get_qr_code_url(selected_key), width=160, caption=f"Mã QR ID: {selected_key}")

# Handle URL command from JS
if "cmd" in st.query_params:
    cmd = st.query_params["cmd"]
    st.query_params.clear()
    if cmd == "next" and st.session_state.current_index < len(CHAPTER_KEYS) - 1:
        st.session_state.current_index += 1
        st.rerun()
    elif cmd == "prev" and st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        st.rerun()

# ---------------------------------------------------------
# MODE 2: QUÉT MÃ QR SÁCH GIẤY
# ---------------------------------------------------------
elif app_mode == "📷 Quét Mã QR Sách Giấy (QR Reader Simulation)":
    st.subheader("📷 Mô Phỏng Quét Mã QR Khi Đọc Sách Búp Sen Xanh")
    st.write("Nhập mã QR hoặc sử dụng camera điện thoại quét mã QR trên sách giấy để tự động tải chương tương ứng:")
    
    qr_in = st.text_input("Nhập URL/ID mã QR:", value="https://bup-sen-xanh.app/read?id=c1_p1")
    
    key = qr_in.split("id=")[-1] if "id=" in qr_in else qr_in.strip()
    if key in BOOK_DATA:
        st.success(f"🎯 Đã nhận diện thành công mã QR ID: `{key}`")
        item = BOOK_DATA[key]
        st.markdown(f"## {item['title']}")
        st.caption(f"📍 {item['chapter']} - {item['part']}")
        st.markdown(f'<div class="content-card">{item["content"].replace("\n", "<br>")}</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Chưa tìm thấy mã QR. Vui lòng nhập ID hợp lệ (Ví dụ: `c1_p1`, `c2_p1`, `c3_p7`).")

# ---------------------------------------------------------
# MODE 3: DANH MỤC MÃ QR 31 PHẦN SÁCH
# ---------------------------------------------------------
elif app_mode == "🏷️ Danh Mục Mã QR 31 Phần Sách (QR Code Manager)":
    st.subheader("🏷️ Danh Mục Mã QR Cho Tất Cả 31 Phần Của Cuốn Sách Búp Sen Xanh")
    st.write("Bạn có thể in bộ mã QR này ra giấy để dán trực tiếp vào từng phần/chương của sách giấy Búp Sen Xanh.")
    
    search_q = st.text_input("🔍 Tìm kiếm chương/phần:", "")
    
    filtered = {k: v for k, v in BOOK_DATA.items() if search_q.lower() in v["title"].lower() or search_q.lower() in v["chapter"].lower() or search_q.lower() in v["part"].lower()}
    
    cols = st.columns(3)
    for idx, (k, v) in enumerate(filtered.items()):
        with cols[idx % 3]:
            st.markdown(f"**{v['chapter']}**")
            st.caption(f"**{v['part']}**: {v['title']}")
            st.image(get_qr_code_url(k), width=150)
            st.code(f"ID: {k}", language="text")
            st.divider()
