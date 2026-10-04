import streamlit as st
import streamlit.components.v1 as components
import json
import os
import urllib.parse

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG STREAMLIT
# ---------------------------------------------------------
st.set_page_config(
    page_title="Đọc Sách Điện Tử Giọng Nói - Búp Sen Xanh Full",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. NẠP DỮ LIỆU TỪ TỆP bup_sen_xanh_full.json
# ---------------------------------------------------------
JSON_FILE_PATH = "bup_sen_xanh_full.json"

DEFAULT_DATA = {
    "c1_p1": {
        "chapter": "Chương I: Thời Thơ Ấu",
        "part": "Phần 1 - Đầm Sen Làng Chùa",
        "title": "Sự Ra Đời Của Cậu Bé Nguyễn Sinh Côn",
        "content": "Cơn dông mùa hạ dấy lên ở phía nam. Mây đen từng khối ùn ùn như nấm từ dưới chân trời đùn lên.\nBên gốc cây đa đầu làng Chùa có mấy con bò đứng ngủ, mồm nhai uể oải. Ông Xẩm ngước đôi mắt mù lòa về phía có tiếng sấm xa xa, hai cánh mũi phập phồng đón nhận mùi hoa sen từ đầm làng đưa tới.\n\nDịp ni sen nở nhiều. Ngồi ở chỗ mô cũng được ngửi hương sen. Bé Thanh - con gái đầu lòng của anh chị nho Sắc - biếu ông Xẩm mấy cái gương sen luộc. Trong căn nhà nhỏ bên đầm sen ngào ngạt hương, chị nho Sắc sinh hạ người con trai thứ hai.\n\nÔng đồ Hoàng Xuân Đường thắp hương vái trước bàn thờ gia tiên và đặt tên cho cháu là Nguyễn Sinh Côn, tự Tất Thành, với mong ước cháu sẽ có chí vùng vẫy bốn bể, dù gặp truân chuyên chìm nổi nhưng ắt sẽ thành công."
    }
}

@st.cache_data
def load_book_data():
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            st.warning(f"Lỗi đọc tệp {JSON_FILE_PATH}: {e}. Đang dùng dữ liệu mặc định.")
            return DEFAULT_DATA
    else:
        return DEFAULT_DATA

BOOK_DATA = load_book_data()
CHAPTER_KEYS = list(BOOK_DATA.keys())

def get_qr_code_url(chapter_id):
    qr_data = f"https://bup-sen-xanh.app/read?id={chapter_id}"
    encoded_data = urllib.parse.quote(qr_data)
    return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_data}&color=0d5c3a"

# ---------------------------------------------------------
# 3. GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.markdown("""
    <style>
    .main-header { text-align: center; color: #1b4d3e; font-size: 2.2rem; font-weight: bold; }
    .sub-header { text-align: center; color: #3b7a57; font-size: 1.1rem; margin-bottom: 20px; }
    .content-card { background-color: #f8fbf9; border-left: 6px solid #2d8a4e; padding: 22px; border-radius: 8px; font-size: 1.08rem; line-height: 1.8; color: #111; max-height: 600px; overflow-y: auto; }
    .chapter-tag { background-color: #e2f0d9; color: #1b4d3e; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9rem; }
    .qr-box { background-color: #ffffff; border: 1px solid #dcdcdc; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🪷 Web Đọc Sách Giọng Nói - Búp Sen Xanh Full</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tích hợp Đọc Giọng Nói Chuẩn, Quét Mã QR & Điều Khiển Lật Trang Bằng Giọng Nói</div>', unsafe_allow_html=True)

st.sidebar.title("📌 Menu Chức Năng")
app_mode = st.sidebar.radio("Chọn trải nghiệm:", [
    "📖 Trình Đọc Sách & Phát Giọng Nói (TTS + Speech Control)",
    "📷 Giả Lập Quét Mã QR (QR Code Scanner)",
    "🏷️ Quản Lý Tất Cả Mã QR (QR Generator)"
])

# ---------------------------------------------------------
# MODE 1: TRÌNH ĐỌC SÁCH VÀ ĐỌC GIỌNG NÓI & NHẬN DIỆN LỆNH
# ---------------------------------------------------------
if app_mode == "📖 Trình Đọc Sách & Phát Giọng Nói (TTS + Speech Control)":
    st.subheader("📖 Không Gian Đọc Sách & Nghe Đọc Giọng Nói Dài")
    
    chapter_map = {k: f"{v.get('chapter', '')} - {v.get('part', '')} ({v.get('title', '')})" for k, v in BOOK_DATA.items()}
    
    # Xử lý điều hướng chương qua session_state
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
        
    selected_id = st.selectbox(
        "Chọn Chương / Phần muốn đọc:",
        list(chapter_map.keys()),
        index=st.session_state.current_index,
        format_func=lambda x: chapter_map[x],
        key="chapter_select"
    )
    
    # Cập nhật index hiện tại
    st.session_state.current_index = CHAPTER_KEYS.index(selected_id)
    
    data = BOOK_DATA[selected_id]
    
    # Nút điều hướng lật trang bằng tay
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if st.button("⬅️ Trang Trước", use_container_width=True):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.rerun()
    with col_nav3:
        if st.button("Trang Tiếp ➡️", use_container_width=True):
            if st.session_state.current_index < len(CHAPTER_KEYS) - 1:
                st.session_state.current_index += 1
                st.rerun()

    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown(f"<span class='chapter-tag'>{data.get('chapter', '')}</span>", unsafe_allow_html=True)
        st.markdown(f"### {data.get('title', '')}")
        st.caption(f"📍 {data.get('part', '')}")
        
        full_text = data.get("content", "")
        paragraphs = [p.strip() for p in full_text.split("\n") if p.strip()]
        formatted_html = "".join([f"<p>{p}</p>" for p in paragraphs])
        
        st.markdown(f'<div class="content-card">{formatted_html}</div>', unsafe_allow_html=True)
        st.caption(f"📏 Độ dài văn bản: {len(full_text)} ký tự | Số đoạn: {len(paragraphs)} đoạn")
        
    with col_right:
        st.markdown("### 🎙️ Đọc Giọng Nói & Điều Khiển Lật Trang")
        st.info("💡 Hỗ trợ đọc chương dài nối tiếp & điều khiển lật trang bằng giọng nói: Nói 'tiếp', 'lùi', 'đọc', 'dừng'.")
        
        js_paragraphs = json.dumps(paragraphs, ensure_ascii=False)
        
        tts_html = f"""
        <div style="background-color: #f0f7f4; padding: 15px; border-radius: 10px; text-align: center;">
            <div style="margin-bottom: 12px;">
                <button onclick="playLongText()" style="background-color: #2d8a4e; color: white; border: none; padding: 10px 16px; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-right: 4px;">
                    ▶️ Đọc Toàn Bộ
                </button>
                <button onclick="pauseSpeech()" style="background-color: #e69500; color: white; border: none; padding: 10px 12px; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-right: 4px;">
                    ⏸️ Tạm Dừng
                </button>
                <button onclick="stopSpeech()" style="background-color: #c94c4c; color: white; border: none; padding: 10px 12px; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer;">
                    ⏹️ Dừng
                </button>
            </div>
            
            <div id="progress-bar-container" style="background-color: #ddd; border-radius: 10px; height: 8px; width: 100%; margin-bottom: 10px; overflow: hidden;">
                <div id="progress-bar" style="background-color: #2d8a4e; height: 100%; width: 0%;"></div>
            </div>
            
            <div id="status" style="font-size: 13px; color: #444; font-weight: 500; margin-bottom: 10px;">Sẵn sàng phát âm thanh...</div>
            
            <hr style="margin: 10px 0; border: 0; border-top: 1px solid #ccc;">
            
            <button id="mic-btn" onclick="toggleRecognition()" style="background-color: #1b4d3e; color: white; border: none; padding: 10px; font-size: 14px; font-weight: bold; border-radius: 20px; width: 100%; cursor: pointer;">
                🎙️ Bật Nhận Diện Giọng Nói
            </button>
            <p id="speech-status" style="font-size: 12px; color: #555; margin-top: 6px; font-style: italic;">Nói 'tiếp', 'lùi', 'đọc', 'dừng' để điều khiển.</p>
        </div>

        <script>
        var synth = window.speechSynthesis;
        var paragraphs = {js_paragraphs};
        var currentIndex = 0;
        var isPlaying = false;
        var recognition = null;
        var isListening = false;

        function playLongText() {{
            if (!('speechSynthesis' in window)) {{
                alert('Trình duyệt không hỗ trợ Web Speech API.');
                return;
            }}
            if (synth.paused) {{
                synth.resume();
                isPlaying = true;
                document.getElementById('status').innerText = '🔊 Tiếp tục đọc...';
                return;
            }}
            synth.cancel();
            currentIndex = 0;
            isPlaying = true;
            readNextParagraph();
        }}

        function readNextParagraph() {{
            if (!isPlaying || currentIndex >= paragraphs.length) {{
                if (currentIndex >= paragraphs.length) {{
                    document.getElementById('status').innerText = '✅ Đã đọc xong toàn bộ chương!';
                    document.getElementById('progress-bar').style.width = '100%';
                    isPlaying = false;
                }}
                return;
            }}

            var text = paragraphs[currentIndex];
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'vi-VN';
            utterance.rate = 0.95;

            var percent = Math.round(((currentIndex + 1) / paragraphs.length) * 100);
            document.getElementById('progress-bar').style.width = percent + '%';
            document.getElementById('status').innerText = '🔊 Đang đọc đoạn ' + (currentIndex + 1) + '/' + paragraphs.length + ' (' + percent + '%)';

            utterance.onend = function() {{
                currentIndex++;
                if (isPlaying) readNextParagraph();
            }};

            utterance.onerror = function(e) {{
                console.error(e);
                currentIndex++;
                if (isPlaying) readNextParagraph();
            }};

            synth.speak(utterance);
        }}

        function pauseSpeech() {{
            if (synth.speaking && !synth.paused) {{
                synth.pause();
                document.getElementById('status').innerText = '⏸️ Đã tạm dừng.';
            }}
        }}

        function stopSpeech() {{
            isPlaying = false;
            synth.cancel();
            currentIndex = 0;
            document.getElementById('progress-bar').style.width = '0%';
            document.getElementById('status').innerText = '⏹️ Đã dừng phát.';
        }}

        // NHẬN DIỆN GIỌNG NÓI ĐIỀU KHIỂN
        function initRecognition() {{
            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {{
                alert('Trình duyệt không hỗ trợ Web Speech Recognition API (Khuyên dùng Chrome/Edge).');
                return null;
            }}
            
            var rec = new SpeechRecognition();
            rec.lang = 'vi-VN';
            rec.continuous = true;
            rec.interimResults = false;

            rec.onresult = function(event) {{
                var last = event.results.length - 1;
                var cmd = event.results[last][0].transcript.trim().toLowerCase();
                document.getElementById('speech-status').innerText = '🗣️ Đã nghe: "' + cmd + '"';

                if (cmd.includes('đọc') || cmd.includes('phát') || cmd.includes('bắt đầu')) {{
                    playLongText();
                }} else if (cmd.includes('dừng') || cmd.includes('tắt') || cmd.includes('ngừng')) {{
                    stopSpeech();
                }}
            }};

            rec.onend = function() {{
                if (isListening) rec.start();
            }};

            return rec;
        }}

        function toggleRecognition() {{
            if (!recognition) recognition = initRecognition();
            if (!recognition) return;

            var btn = document.getElementById('mic-btn');
            if (isListening) {{
                isListening = false;
                recognition.stop();
                btn.innerText = '🎙️ Bật Nhận Diện Giọng Nói';
                btn.style.backgroundColor = '#1b4d3e';
                document.getElementById('speech-status').innerText = 'Micro đã tắt.';
            }} else {{
                isListening = true;
                recognition.start();
                btn.innerText = '🔴 Đang Lắng Nghe... (Nói ' + "'" + 'đọc' + "'" + ' hoặc ' + "'" + 'dừng' + "'" + ')';
                btn.style.backgroundColor = '#c94c4c';
                document.getElementById('speech-status').innerText = 'Đang lắng nghe khẩu lệnh tiếng Việt...';
            }}
        }}
        </script>
        """
        components.html(tts_html, height=220)
        
        st.divider()
        st.image(get_qr_code_url(selected_id), width=160, caption=f"Mã QR ID: {selected_id}")

# ---------------------------------------------------------
# MODE 2: GIẢ LẬP QUÉT MÃ QR
# ---------------------------------------------------------
elif app_mode == "📷 Giả Lập Quét Mã QR (QR Code Scanner)":
    st.subheader("📷 Mô Phỏng Quét Mã QR Mở Chương Sách Dài")
    
    qr_input = st.text_input("Nhập mã QR URL hoặc ID (Ví dụ: 'c1_p1'):", value="c1_p1")
    key = qr_input.split("id=")[-1] if "id=" in qr_input else qr_input.strip()
    
    if key in BOOK_DATA:
        item = BOOK_DATA[key]
        st.success(f"🎯 Đã tìm thấy chương sách ID: `{key}`")
        st.markdown(f"## {item.get('title', '')}")
        st.caption(f"📍 {item.get('chapter', '')} - {item.get('part', '')}")
        st.markdown(f'<div class="content-card">{item.get("content", "").replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Chưa có dữ liệu cho mã ID `{key}`. Hãy kiểm tra tệp `bup_sen_xanh_full.json`.")

# ---------------------------------------------------------
# MODE 3: QUẢN LÝ TẤT CẢ MÃ QR
# ---------------------------------------------------------
elif app_mode == "🏷️ Quản Lý Tất Cả Mã QR (QR Generator)":
    st.subheader("🏷️ Bộ Mã QR Chuẩn Cho Các Chương Trong bup_sen_xanh_full.json")
    
    cols = st.columns(3)
    for idx, (k, v) in enumerate(BOOK_DATA.items()):
        with cols[idx % 3]:
            st.markdown(f"**{v.get('part', k)}**")
            st.caption(v.get('title', ''))
            st.image(get_qr_code_url(k), width=150)
            st.code(f"ID: {k}")

st.divider()
st.caption("Trình đọc sách điện tử tự động nạp dữ liệu bup_sen_xanh_full.json & đọc chương dài nối tiếp.")
