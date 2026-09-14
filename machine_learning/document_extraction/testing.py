from parser import extract_text
from extractor import extract_project_details


file_path = "text.txt"


# Step 1: Extract raw text from document
text = extract_text(file_path)

print("\n========== DOCUMENT TEXT ==========\n")
print(text)


# Step 2: Extract structured project information
project_details = extract_project_details(text)


print("\n========== EXTRACTED PROJECT DETAILS ==========\n")

print(project_details.model_dump_json(indent=4))