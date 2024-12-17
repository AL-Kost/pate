import os
import streamlit as st
from utils.fb2_extractor import extract_fb2_content
from utils.epub_extractor import extract_epub_content
from utils.llm_translator import translate_text_ollama
from app_config import AppConfig

def main():
    st.set_page_config(page_title="Pate 📚", layout="wide")
    st.title("Pate - Your AI FB2/EPUB Reader & Translator 📚")

    try:
        with open(AppConfig.PATE_LOGO_PATH, "r", encoding="utf-8") as svg_file:
            svg_logo = svg_file.read()
        st.sidebar.markdown(
            f"""<div style='text-align: center;'>
                <div style='width: 150px; margin: 20px auto;'>
                    {svg_logo}
                </div>
            </div>""", 
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.sidebar.error("SVG logo not found.")

    st.sidebar.header("Upload your FB2, EPUB, or ZIP")

    uploaded_file = st.sidebar.file_uploader("Upload an FB2, EPUB, or ZIP", type=["fb2", "epub", "zip"])

    if uploaded_file:
        file_path = os.path.join("temp.fb2")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        try:
            if uploaded_file.name.endswith(".fb2") or uploaded_file.name.endswith(".zip"):
                titles, chapters = extract_fb2_content(file_path)
            elif uploaded_file.name.endswith(".epub"):
                titles, chapters = extract_epub_content(file_path)
            else:
                st.error("Unsupported file format.")
                return

            chapter_selection = st.sidebar.selectbox("Select Chapter", titles)
            selected_chapter_index = titles.index(chapter_selection)
            st.header(chapter_selection)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Text")
            with col2:
                st.subheader("Translated Text")

            paragraphs = chapters[selected_chapter_index]
            for paragraph in paragraphs:
                if paragraph.strip():
                    translated_text = translate_text_ollama(paragraph)
                    
                    orig_len = len(paragraph)
                    trans_len = len(translated_text)
                    max_len = max(orig_len, trans_len)
                    
                    paragraph_padded = paragraph + ' ' * (max_len - orig_len)
                    translated_text_padded = translated_text + ' ' * (max_len - trans_len)
                    
                    box_style = """
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-start;
                        border: 1px solid;
                        border-color: var(--primary-border-color);
                        padding: 15px;
                        border-radius: 5px;
                        min-height: 150px;
                        height: 100%;
                        background-color: var(--box-background-color);
                        color: var(--text-color);
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        white-space: pre-wrap;
                        word-wrap: break-word;
                        font-size: 1rem;
                        line-height: 1.5;
                    """

                    theme_style = """
                        <style>
                            [data-testid="stAppViewContainer"] {
                                --primary-border-color: #e0e0e0;
                                --box-background-color: #ffffff;
                                --text-color: #000000;
                            }
                            
                            [data-theme="dark"] [data-testid="stAppViewContainer"] {
                                --primary-border-color: #4a4a4a;
                                --box-background-color: #262626;
                                --text-color: #ffffff;
                            }
                        </style>
                    """
                    
                    st.markdown(theme_style, unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
                    
                    para_cols = st.columns(2)
                    
                    with para_cols[0]:
                        st.markdown(f"""
                        <div style="{box_style}">
                            {paragraph_padded}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with para_cols[1]:
                        st.markdown(f"""
                        <div style="{box_style}">
                            {translated_text_padded}
                        </div>
                        """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
