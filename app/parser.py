from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_txt(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8")


def extract_resume_text(uploaded_file) -> str:
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    if uploaded_file.name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)

    return ""