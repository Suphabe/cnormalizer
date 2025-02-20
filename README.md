Company Name Normalizer/Cnormaliser

A Streamlit app that cleans company names by removing common suffixes like Inc., LLC, Corp., Ltd., etc. from a CSV file.

🚀 Features
✅ Upload a CSV file with a "Company" column
✅ Automatically removes suffixes like Inc., LLC, LLP, Ltd., Corp., etc.
✅ Displays a preview of the cleaned data
✅ Download the cleaned CSV

🛠 Installation
Make sure you have Python 3.7+ and install dependencies:

bash
Copy
Edit
pip install streamlit pandas
▶️ Usage
Run the Streamlit app:

bash
Copy
Edit
streamlit run app.py

📂 Input CSV Example
Company Name
Suphestic Inc.
Alpha Solutions LLC
BetaTech Ltd.

🔍 Output CSV Example
Company Name	Clean_Company
Suphestic Inc.	Suphestic
Alpha Solutions LLC	Alpha Solutions
BetaTech Ltd.	BetaTech

⚙️ How It Works
Upload a CSV file with a "Company" column

The app cleans the names by removing suffixes

Preview the cleaned data

Download the cleaned CSV

🎯 Supported Suffixes
The app removes:

Inc.
LLC
LLP
Ltd.
Corp.
Co.
PLC
Pvt.
AG
GmbH
📌 Notes
Ensure your CSV has a "Company" column
Supports ISO-8859-1 encoding for broader compatibility
📜 License
This project is open-source under the MIT License.
