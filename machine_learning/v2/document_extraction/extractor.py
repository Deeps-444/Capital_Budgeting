"""
Gemini-based project information extractor for the V2
Capital Budgeting Decision Support System.

Purpose
-------
Convert unstructured project-document text into structured
ProjectDetails data.

Data flow
---------
Project document
      ↓
parser.py
      ↓
plain text
      ↓
Gemini
      ↓
structured JSON
      ↓
ProjectDetails
      ↓
Model Router / DSS pipeline

Important extraction rule
-------------------------
Gemini must extract information explicitly present in the
document. It must NOT invent, estimate, or derive values that
are not stated.

Fields such as complexity_index, risk_index, historical cash
flows, future inflation, and future market growth are deliberately
not extracted here because they come from other parts of the DSS.
"""

import os

from dotenv import load_dotenv
from google import genai

from .schemas import ProjectDetails


# -------------------------------------------------------------------
# Environment and Gemini client setup
# -------------------------------------------------------------------

# Load environment variables from the V2 document-extraction folder.
load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found in the V2 .env file."
    )

client = genai.Client(api_key=API_KEY)


# -------------------------------------------------------------------
# Project information extraction
# -------------------------------------------------------------------

def extract_project_details(text: str) -> ProjectDetails:
    """
    Extract project-specific information from document text.

    Only information explicitly stated in the document should
    be extracted.

    Missing information must remain null.

    Parameters
    ----------
    text : str
        Plain text extracted from the project document.

    Returns
    -------
    ProjectDetails
        Validated structured project information.
    """

    if not text or not text.strip():
        raise ValueError(
            "Cannot extract project details from empty document text."
        )

    prompt = f"""
You are extracting structured information from a project document
for a Capital Budgeting Decision Support System.

Your task is INFORMATION EXTRACTION, not prediction.

Extract only information that is explicitly stated in the document.

Do NOT:
- invent missing values
- estimate missing values
- infer values from context
- calculate values that are not explicitly provided
- assign default values
- use outside knowledge

If a field is not explicitly available, return null.

Important:
- Monetary values must be returned as numeric values.
- Convert monetary expressions such as crore/lakh into their
  corresponding numeric value when the conversion is explicit
  from the document.
- Percentage values must be returned as decimal numbers.
  Example: 25% → 0.25.
- Project duration must be returned as a number of years when
  explicitly stated.

Extract ONLY these fields:

1. project_name
2. project_type
3. project_scale
4. location
5. project_duration_years
6. initial_investment
7. annual_revenue
8. annual_operating_cost
9. tax_rate
10. discount_rate

Do NOT extract or invent:
- complexity_index
- risk_index
- historical cash flows
- future inflation
- future market growth
- predicted cash flows
- any other derived financial values

These will be obtained separately by the DSS pipeline.


Return the result according to the ProjectDetails schema.

DOCUMENT:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ProjectDetails,
        },
    )

    return ProjectDetails.model_validate_json(response.text)