import os
import tempfile

import streamlit as st

from parser import extract_text
from extractor import extract_project_details


st.set_page_config(
    page_title="CapWise Demo",
    page_icon="📄",
    layout="wide"
)


# st.title(" Document Intelligence")
st.title("Capital Budgeting Project Information Extraction")

st.write(
    "Upload a project document and extract project-specific "
    "information using an LLM."
)

st.divider()


uploaded_file = st.file_uploader(
    "Upload Project Document",
    type=["pdf", "docx", "txt"]
)


if uploaded_file is not None:

    st.success(f"File uploaded: {uploaded_file.name}")

    if st.button("Extract Project Details"):

        with st.spinner("Analyzing document..."):

            # Create a temporary file
            file_extension = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:

                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name

            try:

                # Step 1: Extract text from document
                text = extract_text(temp_file_path)

                # Step 2: Send text to Gemini
                project_details = extract_project_details(text)

                # Step 3: Display results

                st.success("Document analyzed successfully!")

                st.divider()

                st.header("📊 Extracted Project Details")

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Project Name",
                        project_details.projectName
                        or "Not found"
                    )

                    st.metric(
                        "Initial Investment",
                        (
                            f"₹{project_details.initialInvestment:,.0f}"
                            if project_details.initialInvestment is not None
                            else "Not found"
                        )
                    )

                    st.metric(
                        "Revenue Growth Rate",
                        (
                            f"{project_details.revenueGrowthRate * 100:.2f}%"
                            if project_details.revenueGrowthRate is not None
                            else "Not found"
                        )
                    )

                with col2:

                    st.metric(
                        "Inflation Rate",
                        (
                            f"{project_details.inflationRate * 100:.2f}%"
                            if project_details.inflationRate is not None
                            else "Not found"
                        )
                    )

                    st.metric(
                        "Discount Rate",
                        (
                            f"{project_details.discountRate * 100:.2f}%"
                            if project_details.discountRate is not None
                            else "Not found"
                        )
                    )

                st.divider()

                st.info(
                    "Market Growth Index and Sector Risk Index "
                    "are obtained separately through external "
                    "market and sector research."
                )

                # Optional raw JSON for demonstration
                with st.expander("View Extracted JSON"):

                    st.json(
                        project_details.model_dump()
                    )

            finally:

                # Remove temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)