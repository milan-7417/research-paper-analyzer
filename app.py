
import streamlit as st
import pandas as pd
import plotly.express as px

from analyzer import extract_pdf, analyze_paper


# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="ResearchLens",
    page_icon="🔬",
    layout="wide",
)


# ─────────────────────────────────────────────
# Footer Styling
# ─────────────────────────────────────────────

st.markdown(
    """
    <style>
    .footer-bottom {
        text-align: center;
        padding: 20px 10px 10px 10px;
        margin-top: 40px;
        border-top: 1px solid rgba(128, 128, 128, 0.25);
        font-size: 13px;
        line-height: 1.8;
        opacity: 0.75;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_footer():
    """Display the ResearchLens footer."""
    st.markdown(
        """
        <div class="footer-bottom">
            © 2026 ResearchLens · Built for research and discovery.
            <br>
            Made with ❤️ and Python.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# Application Header
# ─────────────────────────────────────────────

st.title("🔬 ResearchLens")

st.write(
    "Analyze academic research papers using NLP and traditional "
    "machine learning."
)


# ─────────────────────────────────────────────
# PDF Upload
# ─────────────────────────────────────────────

uploaded_file = st.file_uploader(
    "Upload a research paper",
    type=["pdf"],
)

if uploaded_file is None:
    st.info("Upload a text-based PDF to begin.")
    show_footer()
    st.stop()

if uploaded_file.size > 25 * 1024 * 1024:
    st.error("Please upload a PDF smaller than 25 MB.")
    show_footer()
    st.stop()


# ─────────────────────────────────────────────
# PDF Extraction and Analysis
# ─────────────────────────────────────────────

try:
    with st.spinner("Extracting and analyzing the paper..."):
        text, page_count = extract_pdf(uploaded_file.getvalue())

        if len(text.strip()) < 100:
            st.error(
                "Very little text was extracted. "
                "The PDF may be scanned and require OCR."
            )
            show_footer()
            st.stop()

        results = analyze_paper(text)

except Exception as error:
    st.error(f"Analysis failed: {error}")
    show_footer()
    st.stop()


st.success("Paper analyzed successfully!")

st.subheader(uploaded_file.name)


# ─────────────────────────────────────────────
# Document Statistics
# ─────────────────────────────────────────────

col1, col2, col3 = st.columns(3)

col1.metric("Pages", page_count)
col2.metric("Words", f"{results['word_count']:,}")
col3.metric("Sentences", f"{results['sentence_count']:,}")


# ─────────────────────────────────────────────
# Analysis Tabs
# ─────────────────────────────────────────────

overview, keywords, entities, full_text = st.tabs(
    [
        "📌 Summary",
        "🔑 Keywords",
        "🧠 Named Entities",
        "📄 Extracted Text",
    ]
)


# ─────────────────────────────────────────────
# Summary and Frequent Terms
# ─────────────────────────────────────────────

with overview:
    st.subheader("Extractive Summary")

    st.write(results["summary"])

    st.caption(
        "Selected from the original paper using word-frequency "
        "scoring. No new text is generated."
    )

    st.subheader("Most Frequent Terms")

    frequency_df = pd.DataFrame(
        results["frequent_terms"],
        columns=["Term", "Count"],
    )

    if not frequency_df.empty:
        chart = px.bar(
            frequency_df.sort_values("Count"),
            x="Count",
            y="Term",
            orientation="h",
            title="Frequent terms in the paper",
        )

        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("No frequent terms were found.")


# ─────────────────────────────────────────────
# Keywords
# ─────────────────────────────────────────────

with keywords:
    st.subheader("Important Keywords")

    keyword_df = pd.DataFrame(
        results["keywords"],
        columns=["Keyword", "TF-IDF Score"],
    )

    if not keyword_df.empty:
        st.dataframe(
            keyword_df,
            use_container_width=True,
            hide_index=True,
        )

        chart = px.bar(
            keyword_df.sort_values("TF-IDF Score"),
            x="TF-IDF Score",
            y="Keyword",
            orientation="h",
            title="Keyword ranking",
        )

        st.plotly_chart(chart, use_container_width=True)

    else:
        st.warning("No keywords could be extracted.")


# ─────────────────────────────────────────────
# Named Entity Recognition
# ─────────────────────────────────────────────

with entities:
    st.subheader("Named Entity Recognition")

    entity_df = pd.DataFrame(
        results["entities"],
        columns=["Entity", "Type"],
    )

    if entity_df.empty:
        st.info(
            "No entities detected. Check that the spaCy "
            "English model is installed."
        )
    else:
        st.dataframe(
            entity_df,
            use_container_width=True,
            hide_index=True,
        )


# ─────────────────────────────────────────────
# Extracted Text
# ─────────────────────────────────────────────

with full_text:
    st.text_area(
        "Extracted paper text",
        results["clean_text"][:100_000],
        height=400,
    )


# ─────────────────────────────────────────────
# Downloadable Analysis Report
# ─────────────────────────────────────────────

report_lines = [
    "# Research Paper Analysis",
    f"**File:** {uploaded_file.name}",
    f"**Pages:** {page_count}",
    f"**Word count:** {results['word_count']}",
    "",
    "## Extractive Summary",
    results["summary"],
    "",
    "## Keywords",
]

report_lines.extend(
    f"- {word} (TF-IDF: {score})"
    for word, score in results["keywords"]
)

report_lines.extend(["", "## Named Entities"])

report_lines.extend(
    f"- {entity} ({label})"
    for entity, label in results["entities"]
)

report = "\n".join(report_lines)

st.download_button(
    "⬇️ Download analysis report",
    data=report,
    file_name="research_analysis.md",
    mime="text/markdown",
)


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────

show_footer()
