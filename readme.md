# 🔬 ResearchLens — Research Paper Analyzer


<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white" alt="spaCy"/>
  <img src="https://img.shields.io/badge/NLTK-154F3C?style=for-the-badge&logo=python&logoColor=white" alt="NLTK"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/PyMuPDF-555555?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="PyMuPDF"/>
</p>

---

## 📌 Overview

**ResearchLens** is an NLP-powered web application that analyzes academic research papers and extracts meaningful insights from PDF documents. It helps users explore research content through extractive summarization, keyword extraction, named entity recognition, text statistics, and interactive visualizations.

Built with Python and traditional Natural Language Processing (NLP) techniques, ResearchLens performs text analysis **without using Large Language Models (LLMs)** or requiring a labeled training dataset.



<p align="center">
  <img src="./home_page%20(2).png" alt="ResearchLens Application Dashboard" width="850">
</p>


## 🌐 Live Demo

**Try ResearchLens online:** [Launch ResearchLens on Streamlit](https://share.streamlit.io/)


## ✨ Features

- 📄 **PDF Text Extraction** — Extract readable text and page counts from uploaded research papers.
- 📝 **Extractive Summarization** — Identify important sentences from the original document using word-frequency scoring.
- 🔑 **TF-IDF Keyword Extraction** — Rank important words and phrases to identify key concepts.
- 🧠 **Named Entity Recognition (NER)** — Detect entities such as organizations, people, locations, and other categories using spaCy.
- 📊 **Interactive Visualizations** — Explore frequently occurring terms and keyword scores through Plotly charts.
- 📈 **Document Statistics** — View page count, word count, and sentence count.
- 📥 **Downloadable Reports** — Export the analysis as a Markdown report.
- 🖥️ **Interactive Web Interface** — Analyze papers through a user-friendly Streamlit dashboard.
- 🚫 **No LLM Required** — Uses traditional NLP and machine learning methods rather than generative language models.
- 🔍 **No Labeled Dataset Required** — Analyze uploaded papers without training a custom model.

## 🧰 Methodology

ResearchLens combines several text-processing techniques:

| Component | Technique | Purpose |
|---|---|---|
| PDF processing | PyMuPDF | Extract text from PDF documents |
| Text preprocessing | Python string operations | Normalize extracted text |
| Sentence segmentation | NLTK | Divide documents into sentences |
| Keyword extraction | TF-IDF | Rank distinctive words and phrases |
| Summarization | Word-frequency scoring | Select important original sentences |
| Named entity recognition | spaCy | Identify named entities |
| Text statistics | Python and Pandas | Calculate and organize document metrics |
| Visualization | Plotly | Present analysis results interactively |
| Web application | Streamlit | Provide the user interface |

## 🏗️ Project Structure

```text
research-paper-analyzer/
│
├── app.py                 # Streamlit web application
├── analyzer.py            # PDF processing and NLP pipeline
├── requirements.txt       # Python dependencies
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/research-paper-analyzer.git
cd research-paper-analyzer
```

Replace `YOUR_USERNAME` and the repository name with your actual GitHub details.

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the spaCy English model

```bash
python -m spacy download en_core_web_sm
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 📦 Dependencies

The `requirements.txt` file should contain:

```text
streamlit
pymupdf
scikit-learn
pandas
plotly
spacy
nltk
```

The spaCy English model is installed separately using the command provided above.

## 🚀 Deployment

ResearchLens is hosted on **Streamlit Community Cloud**.

To deploy your own instance:

1. Push the project files to a GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account and select the repository.
4. Choose `app.py` as the application entry point.
5. Deploy the application.

Ensure `requirements.txt` is present in the repository. The spaCy English model must also be installed in the deployment environment. Configure the deployment's setup process accordingly if the model is not installed automatically.

## 📖 How to Use

1. Open the deployed ResearchLens application.
2. Upload a text-based academic research paper in PDF format.
3. Wait for the document text to be extracted and analyzed.
4. Review the extractive summary and document statistics.
5. Explore important keywords and their TF-IDF scores.
6. Inspect the detected named entities.
7. View interactive charts of frequently occurring terms.
8. Download the generated Markdown analysis report.

**Note:** Scanned PDFs may require OCR before their text can be analyzed. Extractive summaries select sentences from the source document and do not generate new content. Keyword rankings and entity recognition may vary with document quality and structure.

## 🎯 Project Objective

The objective of ResearchLens is to make academic literature easier to explore by combining conventional NLP techniques with an interactive web interface. It demonstrates how useful research insights can be extracted from documents without relying on generative AI.

## 👨‍💻 Author

**MILAN**


## 📄 License

This project is available under the MIT License if you choose to distribute it under that license. Add a `LICENSE` file to the repository before claiming that the project is MIT-licensed.
