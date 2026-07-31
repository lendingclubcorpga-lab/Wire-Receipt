import streamlit as st
from fpdf import FPDF
import io
import random
import string
import datetime

# --- DYNAMIC INITIALIZATION LOGIC ---
# Using session_state to securely hold a dynamic transaction token across page interactions
if 'transaction_id' not in st.session_state:
    # Generates a standard banking tracking reference string (e.g., TXN-83920174-FT)
    random_digits = "".join(random.choices(string.digits, k=8))
    st.session_state.transaction_id = f"TXN-{random_digits}-FT"

class ReceiptPDF(FPDF):
    def header(self):
        # Top branding bar
        self.set_fill_color(24, 43, 73) # Deep corporate blue
        self.rect(0, 0, 210, 35, 'F')
        
        # Header text
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, "AVANT FINANCE", ln=True, align="L")
        
        self.set_font("Helvetica", "", 10)
        self.cell(0, 5, "Official Wire Transfer Confirmation Receipt", ln=True, align="L")
        self.ln(15)

    def footer(self):
        # Footer accent line
        self.set_y(-30)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        
        # Disclaimer notice
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, "This is an electronically generated document. No signature is required.", ln=True, align="C")
        self.cell(0, 5, "Avant Finance is a registered trademark. Confidential transaction record.", ln=True, align="C")

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="Avant Finance Receipt Generator", page_icon="📄", layout="wide")

st.title("📄 Avant Finance — Wire Transfer Receipt Generator")
st.write("Fill out the transaction ledger parameters below to render a secure verification document.")

# Layout organization
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏦 Transaction & Banking Ledger")
    customer_name = st.text_input("Customer Full Name", "Jane Doe")
    bank_name = st.text_input("Receiving Bank Name", "Chase Bank")
    account_num = st.text_input("Account Number", "XXXX-XXXX-1234")
    routing_num = st.text_input("Routing Number (ABA)", "021000021")
    
    st.markdown("---")
    st.subheader("💵 Financial Breakdown")
    loan_amount = st.number_input("Gross Loan Amount ($)", min_value=0.0, value=10000.0, step=100.0)
    processing_fees = st.number_input("Processing Fees ($)", min_value=0.0, value=250.0, step=10.0)
    
    # Precise operational mathematical calculation
    total_loan_deposited = loan_amount - processing_fees

with col2:
    st.subheader("📋 System Parameters & Contact Details")
    
    # Visual validation showing reference mappings directly inside the user interface
    st.text_input("Fixed Loan ID Block Reference", value="AFPL21102026", disabled=True)
    st.text_input("Dynamic Transaction Reference (Auto)", value=st.session_state.transaction_id, disabled=True)
    
    if st.button("🔄 Generate Fresh Transaction ID"):
        random_digits = "".join(random.choices(string.digits, k=8))
        st.session_state.transaction_id = f"TXN-{random_digits}-FT"
        st.rerun()

    st.markdown("---")
    support_phone = st.text_input("Support Phone Line", "(618)-506-0157")
    support_email = st.text_input("Support Email Address", "accounts@avantloans.online")
    corp_address = st.text_area("Corporate HQ Address", "Avant Finance HQ\n111 W Merchandise Mart Plaza\nChicago, IL 60654")

st.markdown("---")

# --- PDF GENERATION ENGINE ---
if st.button("🚀 Render & Compile PDF Document"):
    try:
        pdf = ReceiptPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=35)
        pdf.add_page()
        
        # Transaction Status Banner Block
        pdf.set_fill_color(240, 244, 248)
        pdf.rect(10, 40, 190, 15, 'F')
        pdf.set_xy(15, 44)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(40, 167, 69) # Green success text
        pdf.cell(0, 7, f"TRANSACTION STATUS: SETTLED / WIRE SENT SUCCESSFUL", ln=True)
        
        pdf.ln(10)
        
        # Meta Info Grid Column Header
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(24, 43, 73)
        pdf.cell(0, 7, "Beneficiary & Account Escrow Mapping", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        # Mapping complete system parameters matrix 
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        
        data_matrix = [
            ("Customer Name:", customer_name),
            ("Destination Bank:", bank_name),
            ("Account Number:", account_num),
            ("Routing Number:", routing_num),
            ("Fixed Loan ID Reference:", "AFPL21102026"),
            ("Dynamic Transaction ID:", st.session_state.transaction_id),
            ("Settlement Date Stamp:", datetime.date.today().strftime("%B %d, %Y"))
        ]
        
        for label, val in data_matrix:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(50, 7, label, border=0)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 7, str(val), ln=True, border=0)
            
        pdf.ln(10)
        
        # Financial Balancing Table
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(24, 43, 73)
        pdf.cell(0, 7, "Financial Ledger Breakdown", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        # Table Layout Header Rows
        pdf.set_fill_color(230, 235, 245)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(120, 8, "Item Description Line", border=1, fill=True)
        pdf.cell(70, 8, "Amount (USD)", border=1, ln=True, fill=True, align="R")
        
        # Data Elements Formatting Rows
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(120, 8, "Gross Loan Approved Base Amount", border=1)
        pdf.cell(70, 8, f"${loan_amount:,.2f}", border=1, ln=True, align="R")
        
        pdf.cell(120, 8, "Internal Origination & Processing Deductions", border=1)
        pdf.cell(70, 8, f"- ${processing_fees:,.2f}", border=1, ln=True, align="R")
        
        # Total Final Calculation Row Balance
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(120, 9, "Total Net Loan Capital Transferred / Deposited", border=1, fill=True)
        pdf.cell(70, 9, f"${total_loan_deposited:,.2f}", border=1, ln=True, fill=True, align="R")
        
        pdf.ln(12)
        
        # Dedicated Configurable Corporate Contact Tab Segment Area
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(24, 43, 73)
        pdf.cell(0, 7, "Corporate Dispatch & Support Matrix", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(35, 6, "Phone Support:")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, support_phone, ln=True)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(35, 6, "Email Desk:")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, support_email, ln=True)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(35, 6, "HQ Address:")
        pdf.set_font("Helvetica", "", 10)
        
        # Handle multi-line strings for corporate address neatly
        lines = corp_address.split('\n')
        for i, line in enumerate(lines):
            if i == 0:
                pdf.cell(0, 6, line, ln=True)
            else:
                pdf.cell(35, 6, "")
                pdf.cell(0, 6, line, ln=True)
        
        # Output binary object string to system memory stream download buffer
        pdf_output = pdf.output(dest='S')
        
        # Sanitize name to generate a clean, download-friendly filename
        clean_name = customer_name.strip().replace(" ", "_").lower()
        if not clean_name:
            clean_name = "customer"
        formatted_filename = f"{clean_name}_wire_transfer_receipt.pdf"
        
        st.success("🎉 Receipt successfully built!")
        st.download_button(
            label="💾 Download Signed Receipt PDF File",
            data=bytes(pdf_output),
            file_name=formatted_filename,
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"An operation compile failure occurred: {str(e)}")
