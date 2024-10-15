import streamlit as st
from utils.authentication import verify_user, register_user
from utils.chatbot import query_gemini_api
from utils.flight_prices import get_flight_prices  # Hàm để lấy giá vé máy bay
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Khởi tạo session state nếu chưa có
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Hàm hiển thị trang đăng nhập
def login_page():
    st.subheader("Đăng nhập")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Đăng nhập"):
        if verify_user(username, password):
            st.session_state.logged_in = True  # Đánh dấu trạng thái đăng nhập thành công
            st.session_state.username = username
            st.success(f"Đăng nhập thành công!")  # Hiển thị thông báo đăng nhập thành công
            st.experimental_rerun()
        else:
            st.warning('username or password is invalid, please try again!')

# Hàm hiển thị trang đăng ký
def register_page():
    st.subheader("Đăng ký tài khoản")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Đăng ký"):
        if register_user(new_user, new_password):
            st.success("Đăng ký thành công!")
        else:
            st.warning("Tài khoản đã tồn tại!")

# Hàm hiển thị chatbot sau khi đăng nhập thành công
def chatbot_page():
    st.subheader(f"Welcome to {st.session_state.username}")
    
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]['role'] != 'assistant':
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query_gemini_api(prompt)
                st.write(response)
            
            message = {'role': "assistant", 'content': response}
            st.session_state.messages.append(message)

# Hàm hiển thị trang tra cứu giá vé máy bay
def flight_price_page():
    st.subheader("Tra cứu giá vé máy bay")

    # Input từ người dùng
    departure = st.text_input("Điểm khởi hành")
    destination = st.text_input("Điểm đến")
    flight_date = st.date_input("Ngày bay")
    flight_date = flight_date.strftime("%Y%m%d")

    if st.button("Tìm kiếm giá vé"):
        if departure and destination and flight_date:
            with st.spinner('Đang tra cứu giá vé...'):
                prices = get_flight_prices(departure, destination, flight_date)  # Gọi API lấy giá vé
                print(prices)
                if prices:
                    st.write(f"Giá vé từ {departure} đến {destination} vào ngày {flight_date}:")
                    st.write(prices)
                else:
                    st.error("Không tìm thấy giá vé!")
        else:
            st.warning("Vui lòng nhập đầy đủ thông tin.")

# Add background
img_file = './data/gemini_backgroundv2.png'
img_base64 = get_base64(img_file)
page_bg_img = f'''
<style>
.stApp {{
background-image: url("data:image/jpg;base64,{img_base64}");
background-size: cover;
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
    
# Add logo FPT Edu
st.image('./data/Logo_FPT_Education.png', width=200)
# Kiểm tra trạng thái để hiển thị page tương ứng
if st.session_state.logged_in:
    st.sidebar.title("Menu")
    menu = ["Chatbot", "Tra cứu vé máy bay", "Đăng xuất"]
    choice = st.sidebar.selectbox("Chọn trang", menu)

    if choice == "Chatbot":
        chatbot_page()  # Hiển thị chatbot
    elif choice == "Tra cứu vé máy bay":
        flight_price_page()  # Hiển thị trang tra cứu giá vé máy bay
    elif choice == "Đăng xuất":
        if st.button("Thoát"):
            st.session_state.logged_in = False  # Đặt lại trạng thái đăng nhập
            st.session_state.username = ""

            if 'chat_history' in st.session_state:
                st.session_state['chat_history'] = []
            st.experimental_rerun()
else:
    st.sidebar.title("Chatbot Tư Vấn Tâm Lý")
    menu = ["Đăng Nhập", "Đăng ký"]
    choice = st.sidebar.selectbox("Chọn chức năng", menu)

    if choice == "Đăng Nhập":
        login_page()  # Hiển thị trang đăng nhập
    elif choice == "Đăng ký":
        register_page()  # Hiển thị trang đăng ký
