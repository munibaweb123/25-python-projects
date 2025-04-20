import streamlit as st
import qrcode
import io

# Function to generate QR Code
def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

# Function to convert image format
def get_image_bytes(img, format):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()

# Add custom CSS for pink and purple gradient background and highlighted button
st.markdown(
    """
    <style>
    /* Use a more specific selector to ensure the background is applied */
    .stApp {
        background: linear-gradient(to right,rgb(255, 126, 229),rgb(183, 0, 255)); /* Pink to Purple gradient */
    }
    .stButton > button {
        background-color:rgb(255, 0, 157); /* Highlighted button background color */
        color: white; /* Button text color */
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s; /* Smooth transition for hover effect */
    }
    .stButton > button:hover {
        background-color:rgb(252, 219, 254); /* Darker shade on hover */
        color:black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("🔗 QR Code Generator")

# Input for the URL
link = st.text_input("Enter a link to generate a QR Code:", "")

# Add a button to generate the QR code
if st.button("Generate QR Code") or (link and st.session_state.get("enter_pressed", False)):
    qr_image = generate_qr_code(link)
    
    # Convert QR image to bytes
    qr_image_bytes = get_image_bytes(qr_image, "PNG")  # Convert to bytes

    # Show QR Code
    st.image(qr_image_bytes, caption="Generated QR Code", use_container_width=True)  # Use bytes here

    # Provide download options
    st.write("📥 Download your QR Code:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button("PNG", data=get_image_bytes(qr_image, "PNG"), file_name="qr_code.png", mime="image/png")
    with col2:
        st.download_button("JPEG", data=get_image_bytes(qr_image, "JPEG"), file_name="qr_code.jpeg", mime="image/jpeg")
    with col3:
        st.download_button("PDF", data=get_image_bytes(qr_image, "PDF"), file_name="qr_code.pdf", mime="application/pdf")

# Capture Enter key press
if st.session_state.get("enter_pressed", False):
    st.session_state["enter_pressed"] = False

# JavaScript to capture Enter key press
st.markdown(
    """
    <script>
    const input = document.querySelector('input[type="text"]');
    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const button = document.querySelector('button[data-baseweb="button"]');
            button.click();
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown("💡 Built with Streamlit & Python")
