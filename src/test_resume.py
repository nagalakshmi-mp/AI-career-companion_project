from resume_parser import extract_resume_text
resume_path = r"uploads/Nagalakshmi MP RESUME.pdf"

text = extract_resume_text(resume_path)

print("\n========== EXTRACTED RESUME TEXT ==========\n")
print(text)
print("\n========== END ==========\n")

