import streamlit as st
from utils.authentication import verify_user, register_user
from utils.chatbot import query_gemini_api
from utils.flight_prices import get_flight_prices  # Hàm để lấy giá vé máy bay
from utils.analysis import visualization
from utils.markdown import centered_subheader, centered_title, add_background



# Khởi tạo session state nếu chưa có
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Hàm hiển thị trang đăng nhập
def login_page():
    centered_subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.logged_in = True  # Đánh dấu trạng thái đăng nhập thành công
            st.session_state.username = username
            st.success(f"Login Successfully!")  # Hiển thị thông báo đăng nhập thành công
            st.experimental_rerun()
        else:
            st.warning('Username or password is invalid, please try again!')

# Hàm hiển thị trang đăng ký
def register_page():
    centered_subheader("Account Register")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if register_user(new_user, new_password):
            st.success("Register Succesfully!")
        else:
            st.warning("Account is already exists!")

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
                st.write(f"This is prices: {prices}")
                if prices:
                    st.write(f"Giá vé từ {departure} đến {destination} vào ngày {flight_date}:")
                    st.write(prices)
                else:
                    st.error("Không tìm thấy giá vé!")
        else:
            st.warning("Vui lòng nhập đầy đủ thông tin.")
            
st.set_page_config(layout="wide")

add_background()

# Add logo FPT Edu
st.image('./data/Logo_FPT_Education.png', width=200)

# Kiểm tra trạng thái để hiển thị page tương ứng
if st.session_state.logged_in:
    st.sidebar.title("Menu")
    menu = ["Chatbot", "Tra cứu vé máy bay", "Analysis Student Mental Health", "Exit"]
    choice = st.sidebar.selectbox("Select Page", menu)

    if choice == "Chatbot":
        chatbot_page()  # Hiển thị chatbot
    elif choice == "Tra cứu vé máy bay":
        flight_price_page()  # Hiển thị trang tra cứu giá vé máy bay
    elif choice == "Analysis Student Mental Health":
        visualization()
    elif choice == "Exit":
        if st.button("Quit"):
            st.session_state.logged_in = False  # Đặt lại trạng thái đăng nhập
            st.session_state.username = ""

            if 'chat_history' in st.session_state:
                st.session_state['chat_history'] = []
            st.experimental_rerun()
else:
    st.sidebar.title("Psychological Consulting Chatbot")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.radio("Select Option", menu)
    if choice == "Login":
        login_page()  # Hiển thị trang đăng nhập
    elif choice == "Sign Upq":
        register_page()  # Hiển thị trang đăng ký
