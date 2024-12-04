import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Health Detection Dashboard", layout="wide")

# Add custom CSS for professional styling
st.markdown("""
    <style>
        /* General Body Styling */
        body {
            background-color: #f5f7fa;
            font-family: 'Arial', sans-serif;
            height:100vh;
            width:100%;
         
        
           
        }

        /* Navigation Bar Styling */
        .navbar {
        width:90%;
            background-color: #0077b6;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 40px;
           display:flex;    
           justify-content:center;
           position:fixed;
           z-index:2;
        height:55px;

           
        }
        .navbar a {
            color: #ffffff;
            text-decoration: none;
            margin: 0 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .navbar a:hover {
            color: #ffcc00;
            text-decoration: underline;
        }

        /* Card Styling */
        .card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            border:2px solid red    ;
        }
        .card-title {
            font-size: 22px;
            font-weight: bold;
            color: #0077b6;
            margin-bottom: 15px;
        }
        .card-text {
            font-size: 16px;
            color: #4a4a4a;
            margin-bottom: 20px;
        }
        .card button {
            background-color: #0077b6;
            color: #ffffff;
            border: none;
            padding: 12px 25px;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        .card button:hover {
            background-color: #005f8a;
        }

        /* Header Styling */
        h1 {
            color: #023e8a;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            margin-top:20px;
        }

        /* Section Description Styling */
        .description {
            text-align: center;
            font-size: 18px;
            color: #4a4a4a;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Define the navigation bar
def render_navbar():
    st.markdown("""
        <div class="navbar">
            <a href="?nav=home">Home</a>
            <a href="?nav=leukemia">Leukemia Detection</a>
            <a href="?nav=malaria">Malaria Detection</a>
            <a href="?nav=cbc">CBC Test</a>
            <a href="?nav=about">About App</a>
        </div>
    """, unsafe_allow_html=True)

# Define pages
def render_home():
    st.markdown("<h1>Health Detection Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="description">
            Welcome to the Health Detection Dashboard! This platform leverages advanced AI to provide accurate and reliable diagnostic tools for various health concerns.
            Explore our features below to learn more about how we can assist in early detection and diagnosis of critical conditions.
        </p>
    """, unsafe_allow_html=True)

    # Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="card">
                <h3 class="card-title">Leukemia Detection</h3>
                <p class="card-text">
                    Our AI models can analyze blood cell images with high precision to detect signs of leukemia early, ensuring timely treatment.
                </p>
                <button onclick="window.location.href='?nav=leukemia';">Learn More</button>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <h3 class="card-title">Malaria Detection</h3>
                <p class="card-text">
                    Using microscopic image analysis, our system identifies malaria parasites with cutting-edge accuracy.
                </p>
                <button onclick="window.location.href='?nav=malaria';">Learn More</button>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="card">
                <h3 class="card-title">CBC Test</h3>
                <p class="card-text">
                    Perform a complete blood count (CBC) analysis to gain insights into your health and detect any abnormalities.
                </p>
                <button onclick="window.location.href='?nav=cbc';">Learn More</button>
            </div>
        """, unsafe_allow_html=True)

def render_leukemia():

    st.markdown("<h1>Leukemia Detection</h1>", unsafe_allow_html=True)
    st.write("""
        Leukemia detection is powered by AI models trained to analyze blood cell images. This system provides early and precise detection,
        helping healthcare professionals to make informed decisions and ensure timely treatment for patients.
    """)

    # Collect user details
    st.header("User Details")
    with st.form("user_details"):
        name = st.text_input("Name", "")
        age = st.number_input("Age", min_value=1, step=1)
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        location = st.text_input("Location", "")
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Details submitted successfully!")

    # Upload an image
    uploaded_file = st.file_uploader("Choose a blood cell image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Preprocess the image
        image = Image.open(uploaded_file).convert("RGB")
        img_tensor = transform(image).unsqueeze(0).to(device)

        # Make predictions
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            _, predicted = torch.max(outputs, 1)
            class_name = class_names[predicted.item()]

        # Display the prediction
        st.write(f"### Prediction: {class_name}")
        st.write("### Confidence Scores:")
        for i, prob in enumerate(probabilities):
            st.write(f"{class_names[i]}: {prob:.2f}")

        # Display a bar chart
        st.write("### Confidence Distribution")
        fig, ax = plt.subplots()
        ax.bar(class_names, probabilities.cpu().numpy())
        ax.set_xlabel('Classes')
        ax.set_ylabel('Confidence')
        ax.set_title('Prediction Confidence for Leukemia Detection')
        st.pyplot(fig)

        # Generate a PDF report
        st.write("### Generate Report")
        if st.button("Download PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Leukemia Detection Report", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
            pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
            pdf.cell(200, 10, txt=f"Sex: {sex}", ln=True)
            pdf.cell(200, 10, txt=f"Location: {location}", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Prediction: {class_name}", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Confidence Scores:", ln=True)
            for i, prob in enumerate(probabilities):
                pdf.cell(200, 10, txt=f"{class_names[i]}: {prob:.2f}", ln=True)

            # Save bar chart as an image and include in PDF
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)

            # Save BytesIO buffer to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                tmp_file.write(buf.read())
                tmp_file_path = tmp_file.name

            # Add the image to the PDF
            pdf.image(tmp_file_path, x=10, y=pdf.get_y(), w=190)

            # Close the buffer and delete the temporary file
            buf.close()

            # Save PDF
            pdf_output = f"{name}_leukemia_report.pdf"
            pdf.output(pdf_output)
            st.success("Report generated!")
            with open(pdf_output, "rb") as f:
                st.download_button("Download Report", f, file_name=pdf_output)


def render_malaria():
    st.markdown("<h1>Malaria Detection</h1>", unsafe_allow_html=True)
    st.write("""
        Our malaria detection feature uses advanced image recognition to identify malaria parasites in blood smears. 
        This ensures fast and reliable diagnosis, aiding in early treatment and better outcomes.
    """)

def render_cbc():
    st.markdown("<h1>CBC Test</h1>", unsafe_allow_html=True)
    st.write("""
        The CBC test provides detailed insights into your blood composition, helping to detect conditions like anemia,
        infections, and more. Our AI-powered analysis makes the process efficient and accurate.
    """)

def render_about():
    st.markdown("<h1>About the App</h1>", unsafe_allow_html=True)
    st.write("""
        The Health Detection Dashboard is designed to harness the power of AI in healthcare. 
        It offers tools for early detection and diagnosis of various health conditions, empowering users to take proactive steps toward better health.
    """)

# Render the navigation and pages
render_navbar()
query_params = st.query_params  # Updated to use st.query_params
nav = query_params.get("nav", ["home"])[0]

if nav == "home":
    render_home()
elif nav == "leukemia":
    render_leukemia()
elif nav == "malaria":
    render_malaria()
elif nav == "cbc":
    render_cbc()
elif nav == "about":
    render_about() 
