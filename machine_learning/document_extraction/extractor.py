import os

from dotenv import load_dotenv
from google import genai

from schemas import ProjectDetails


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")


client = genai.Client(api_key=api_key)


def extract_project_details(text: str) -> ProjectDetails:

    prompt = f"""
You are a document extraction system for a capital budgeting
decision support system.

Your task is to extract ONLY information that is explicitly
present in the provided project document.

Extract the following fields:

1. projectName
2. initialInvestment
3. revenueGrowthRate
4. inflationRate
5. discountRate

IMPORTANT RULES:

- Do NOT invent or estimate values.
- Do NOT use your general knowledge.
- Do NOT infer values that are not explicitly stated.
- If a value is not present in the document, return null.
- Extract only project-specific information from the document.
- Do not extract marketGrowthIndex or sectorRiskIndex.
  Those values will be obtained separately through external
  market research.
- Convert percentages into decimal form.
  For example, 10% should become 0.10.
- Preserve monetary values as numerical values.
- If a monetary amount is expressed in crore, convert it to
  its corresponding base currency value.
  For example, 25 crore INR = 250000000 INR.

PROJECT DOCUMENT:

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