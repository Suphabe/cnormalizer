import streamlit as st
import pandas as pd
import re
from io import BytesIO

def clean_company_name(name):
    if pd.isna(name):
        return name
        
    # Convert to string and clean up initial whitespace
    name = str(name).strip()
    
    # Define patterns to remove common suffixes
    patterns = [
        r'\s*,?\s*inc(?:\.*?|\b)\s*$',      # Matches "Inc", "Inc.", "INC", "inc."
        r'\s*,?\s*incorporated\s*$',        # Matches "Incorporated"
        r'\s*,?\s*llc(?:\.*?|\b)\s*$',      # Matches "LLC", "LLC.", "llc"
        r'\s*,?\s*llp(?:\.*?|\b)\s*$',      # Matches "LLP", "LLP.", "llp"
        r'\s*,?\s*ltd(?:\.*?|\b)\s*$',      # Matches "Ltd", "Ltd.", "LTD"
        r'\s*,?\s*limited\s*$',             # Matches "Limited"
        r'\s*,?\s*co(?:\.*?|\b)\s*$',       # Matches "Co", "Co.", "CO"
        r'\s*,?\s*company\s*$',             # Matches "Company"
        r'\s*,?\s*corp(?:\.*?|\b)\s*$',     # Matches "Corp", "Corp.", "CORP"
        r'\s*,?\s*corporation\s*$',         # Matches "Corporation"
    ]
    
    # Apply each pattern to remove suffixes
    for pattern in patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Clean up any remaining artifacts
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[,\s\.]+$', '', name)
    name = name.strip()
    
    return name

def find_company_column(df):
    # Possible company column name variations
    company_variations = [
        'company', 'Company', 'COMPANY',
        'company name', 'Company Name', 'COMPANY NAME',
        'companies', 'Companies', 'COMPANIES',
        'company_name', 'Company_Name', 'COMPANY_NAME'
    ]
    
    # Find the first matching column
    for col in df.columns:
        if col.strip() in company_variations:
            return col
    return None

def process_csv(file):
    try:
        # Read CSV with explicit parameters
        df = pd.read_csv(
            file,
            encoding='utf-8',
            skip_blank_lines=True
        )
        
        # Find and clean the company column
        company_col = find_company_column(df)
        if company_col:
            df[company_col] = df[company_col].apply(clean_company_name)
        else:
            st.warning("No company-related column found in CSV. Looking for: 'Company', 'Company Name', 'COMPANY', 'Companies', etc.")
            return df
        
        # Remove any unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        return df
        
    except UnicodeDecodeError:
        try:
            file.seek(0)
            df = pd.read_csv(
                file,
                encoding='ISO-8859-1',
                skip_blank_lines=True
            )
            company_col = find_company_column(df)
            if company_col:
                df[company_col] = df[company_col].apply(clean_company_name)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            return df
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return None
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def convert_df(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

# Streamlit UI
st.title("Company Name Normalizer")

st.write("Examples of cleaning:")
examples = pd.DataFrame({
    'Original': ['Columbia Manufacturing Inc.', 'Tech Corp.', 'Global Ltd.', 'Solutions, Inc', 'Systems Inc.', 'Company,Inc'],
    'Cleaned': ['Columbia Manufacturing', 'Tech', 'Global', 'Solutions', 'Systems', 'Company']
})
st.table(examples)

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = process_csv(uploaded_file)
    if df is not None:
        st.write("### Preview of Cleaned Data")
        company_col = find_company_column(df)
        if company_col:
            st.dataframe(df[[company_col]].head())
        else:
            st.dataframe(df.head())
        
        st.download_button(
            label="Download Cleaned CSV",
            data=convert_df(df),
            file_name="cleaned_companies.csv",
            mime="text/csv"
        )

# Add test section
with st.expander("Test individual company name"):
    test_name = st.text_input("Enter a company name to test:")
    if test_name:
        cleaned = clean_company_name(test_name)
        st.write(f"Original: {test_name}")
        st.write(f"Cleaned: {cleaned}")