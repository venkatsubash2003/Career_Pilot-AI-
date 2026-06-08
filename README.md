# CareerPilot AI

CareerPilot AI is an AI-powered job application assistant designed for international students in the U.S. It helps users evaluate job descriptions for visa sponsorship signals, check company H1B sponsorship history, analyze resume-job fit, calculate ATS scores, generate resume improvement suggestions, and create cover letters or recruiter emails.

## Features

- Visa and sponsorship classification using Ollama Llama 3.1
- H1B sponsorship history lookup using a company dataset
- Resume PDF/TXT parsing
- Resume vs job description analysis
- ATS match score calculation
- Keyword match analysis
- Resume improvement recommendations
- Cover letter generation
- Recruiter email generation
- SQLite-based application tracker
- Streamlit-based user interface

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Ollama Llama 3.1 |
| AI Framework | LangChain |
| Data Processing | Python, Pandas |
| Resume Parsing | PyPDF |
| Database | SQLite |
| Storage | CSV Dataset |
| Future Backend | FastAPI |
| Future Frontend | React |

## Project Architecture

```text
CareerPilot_AI/
│
├── app/
│   ├── application_writer.py
│   ├── chains.py
│   ├── config.py
│   ├── data_loader.py
│   ├── database.py
│   ├── generators.py
│   ├── parser.py
│   ├── scoring.py
│   ├── sponsorship.py
│   ├── sponsorship_history.py
│   └── graph.py
│
├── data/
│   ├── sponsorship_companies_10yrs.csv
│   └── applications.db
│
├── ui/
│   └── streamlit_app.py
│
├── requirements.txt
├── .gitignore
└── README.md