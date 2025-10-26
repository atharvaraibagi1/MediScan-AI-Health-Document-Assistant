
# 🏥 MediScan AI — Your Health Document Assistant

MediScan AI is a Streamlit-powered application that transforms complicated medical PDFs into **clear, friendly, and helpful health insights**.

No more scratching your head over test reports or prescriptions. Upload, tap… and bam! Your health data speaks human.

---

## ✨ Features

| Feature                      | What it does                                                     | Why you’ll love it                                      |
| ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- |
| 🔍 Health Document Q&A       | Ask specific questions about your medical document               | Instant clarity, no googling medical jargon             |
| 📝 Smart Summaries           | Generates structured summaries of PDF reports                    | Saves time, highlights only what matters to you         |
| 👶 ELI5 Explanations         | Breaks down complex medical terms in a kid-friendly way          | Because not everything needs to sound like a PhD thesis |
| 💊 Medication Tracker        | Extracts medication details like dosage, frequency, instructions | Keeps treatment information organized and clean         |
| 🌟 Lifestyle Recommendations | Provides actionable health tips based on your document           | Small changes, big health difference                    |

---

## 🧠 Powered By

* Streamlit UI
* OpenAI GPT Models
* PyPDF2 for PDF text extraction
* dotenv for API key handling

---

## 📦 Installation

Clone the repository and enter the project folder:

```bash
git clone https://github.com/yourusername/mediscan-ai.git
cd mediscan-ai
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Make sure your OpenAI API key is active and billing-enabled.

---

## 🚀 Run the App

```bash
streamlit run app.py
```

Your browser will open automatically at:

```
http://localhost:8501/
```

Upload a health document (PDF) and explore the features.

---

## 🧩 Code Overview

The app serves five major interactions:

| Section         | Code Component       | Description                                     |
| --------------- | -------------------- | ----------------------------------------------- |
| Q&A             | `process_document()` | Answers user questions based on the PDF         |
| Summary         | `process_document()` | Converts PDF content into structured highlights |
| ELI5            | `process_document()` | Simplifies medical terminology                  |
| Medications     | `process_document()` | Extracts and lists medicines with details       |
| Recommendations | `process_document()` | Suggests lifestyle improvements                 |

Text extraction: `extract_text_from_pdf()`
Model interaction: `get_completion()` using OpenAI ChatCompletion API

---

## 💡 Best Practices

* Ensure PDFs contain selectable text (scanned documents without OCR won’t extract well)
* Avoid sharing sensitive medical info publicly
* Always cross-check AI suggestions with a doctor

---

## ⚠️ Disclaimer

MediScan AI is **not a medical device**. It does not diagnose, treat, or replace professional medical advice. Always consult qualified healthcare professionals for concerns.

---

## 🤝 Contributing

Fork the project, create magic, and open a pull request.
Pull requests with healthy humor get bonus points.

---

## ⭐ Future Enhancements

* Support for **images** and **scanned documents** (OCR)
* Multi-language output
* Smart anomaly detection in lab results
* User history and secure login

---

## ❤️ Credits

Made with Python, caffeine, and the dream that medical reports shouldn’t require a translator.

---

If you’d like, I can also:

✅ Create a logo and branding theme
✅ Upload to GitHub with a polished README styling
✅ Package as a deployable app (Streamlit Cloud / HuggingFace Spaces)
✅ Add sample PDFs for users to test

Want me to generate the **requirements.txt** and **GitHub structure** as well?
