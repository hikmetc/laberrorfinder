# Developed by Hikmet Can Çubukçu, MD, PhD, MSc, EuSpLM

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Lab Error Finder", page_icon="🔍")

# --- Custom CSS for an enhanced aesthetic interface with a unified card layout ---
st.markdown(
    """
    <style>
    /* Overall background with a subtle gradient and updated font styling */
    .reportview-container {
        background: linear-gradient(135deg, #e2e2e2, #ffffff);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Main title styling with text shadow */
    .main-title {
        text-align: center;
        color: #4CAF50;
        font-size: 3em;
        font-weight: bold;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    /* Subheader styling with a bottom border */
    .sub-title {
        text-align: center;
        color: #333;
        font-size: 2em;
        margin: 30px 0 20px 0;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
    }
    /* Card container styling */
    .card {
        background-color: #fff;
        border-radius: 8px;
        padding: 16px;
        margin: 16px auto;
        width: 90%;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    /* Card header styling */
    .card-header {
        font-size: 1.5em;
        font-weight: bold;
        color: #4CAF50;
        border-bottom: 1px solid #e1e1e1;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    /* Individual record styling within the card */
    .record {
        border-bottom: 1px solid #e1e1e1;
        padding: 8px 0;
    }
    .record:last-child {
        border-bottom: none;
    }
    .record p {
        font-size: 1em;
        color: #333;
        margin: 4px 0;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display the main title
st.image('./images/lab error finder head.png')
#st.markdown("<h1 class='main-title'>Laboratory Error Finder</h1>", unsafe_allow_html=True)

# --- Load Data ---
excel_file_path = "data/lab error list_v_20250308.xlsx"

@st.cache_data
def load_data(path):
    try:
        return pd.read_excel(path)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None

df = load_data(excel_file_path)

if df is not None:
    # Choose search criteria: "Analyte" or "Laboratory errors"
    search_by = st.selectbox("**Search by**", ["Analyte", "Laboratory errors"])
    
    # Validate that the selected column exists in the DataFrame and get unique values
    if search_by in df.columns:
        options = sorted(df[search_by].dropna().unique())
    else:
        options = []
    
    if not options:
        st.error(f"No data found for the column '{search_by}'. Please check your Excel file.")
    else:
        # Let the user choose a specific value from the dropdown
        selected_value = st.selectbox(f"**Select {search_by}**", options)
        
        if st.button("Search"):
            with st.spinner("Searching..."):
                # Filter the DataFrame based on the selected value
                filtered = df[df[search_by] == selected_value]
            
            if filtered.empty:
                st.warning("No matching records found.")
            else:
                st.markdown("<h2 class='sub-title'>Search Results</h2>", unsafe_allow_html=True)
                
                # Begin a single card for the searched value
                card_html = f"<div class='card'>"
                card_html += f"<div class='card-header'>{selected_value}</div>"
                card_html += "<div class='card-body'>"
                
                # Define columns to display if they exist in the DataFrame
                columns_to_display = [
                    "Analyte", 
                    "Laboratory errors", 
                    "Effects on test results", 
                    "Reference"
                ]
                if "Reference 2" in filtered.columns:
                    columns_to_display.append("Reference 2")
                columns_to_display = [col for col in columns_to_display if col in filtered.columns]
                
                # Iterate over each row and add details as a record inside the card
                for index, row in filtered.iterrows():
                    card_html += "<div class='record'>"
                    for col in columns_to_display:
                        # Avoid repeating the searched item as it's already shown in the header.
                        if col == search_by:
                            continue
                        # For "Reference 2", show only if there is a valid value.
                        if col == "Reference 2" and pd.isna(row[col]):
                            continue
                        card_html += f"<p><strong>{col}:</strong> {row[col]}</p>"
                    card_html += "</div>"
                
                card_html += "</div></div>"
                st.markdown(card_html, unsafe_allow_html=True)

# --- Proposal Form ---
st.write('---')
st.write("  ")
st.info('*Developed by Hikmet Can Çubukçu, MD, PhD, MSc, EuSpLM*, contact: <hikmetcancubukcu@gmail.com>')
st.info("To enhance the application's comprehensiveness, please contribute any additional laboratory errors you are aware of, along with supporting references. Use the proposal form below to submit your contributions directly.")

# Toggle for showing the proposal form
if "show_proposal_form" not in st.session_state:
    st.session_state["show_proposal_form"] = False

if st.button("Propose New Laboratory Error"):
    st.session_state["show_proposal_form"] = True

if st.session_state["show_proposal_form"]:
    #st.markdown("### Propose New Laboratory Error")
    st.success("Please fill in the details below and click **Submit Proposal**. Your submission will be sent directly to **hikmetcancubukcu@gmail.com**")
    
    # HTML form using Formspree (replace YOUR_FORMSPREE_FORM_ID with your actual form ID)
    form_html = """
        <form action="https://formspree.io/f/xpwpwzpw" method="POST" style="font-family: sans-serif; font-size: 14px;">
        <label for="lab_error_type"><strong>Laboratory Error:</strong></label><br>
        <input type="text" id="lab_error_type" name="lab_error_type" required style="width: 100%; padding: 8px;"><br><br>
        
        <label for="effect_test_results"><strong>Impact on Test Results:</strong></label><br>
        <input type="text" id="effect_test_results" name="effect_test_results" required style="width: 100%; padding: 8px;"><br><br>
        
        <label for="affected_analyte"><strong>Affected Analyte:</strong></label><br>
        <input type="text" id="affected_analyte" name="affected_analyte" required style="width: 100%; padding: 8px;"><br><br>
        
        <label for="reference"><strong>Reference:</strong></label><br>
        <input type="text" id="reference" name="reference" required style="width: 100%; padding: 8px;"><br><br>
        
        <!-- Optional: Set a custom subject line for the email -->
        <input type="hidden" name="_subject" value="New Laboratory Error Proposal">
        
        <input type="submit" value="Submit Proposal" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 4px;">
        </form>
    """
    # Render the HTML form inside Streamlit
    components.html(form_html, height=500)
    st.session_state["show_proposal_form"] = False

