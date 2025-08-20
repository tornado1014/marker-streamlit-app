---
title: Marker Document Converter
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
license: mit
---

# 📄 Marker Document to Markdown Converter

A powerful web application that converts various document formats to Markdown using the advanced [Marker](https://github.com/VikParuchuri/marker) library.

## 🌟 Features

- **Multi-Format Support**: PDF, DOCX, PPTX, XLSX, HTML, EPUB, Images (PNG, JPG)
- **High-Quality Conversion**: Preserves formatting, tables, and structure
- **Multiple Output Formats**: Markdown, JSON, HTML
- **Image Extraction**: Extract and preserve images from documents
- **AI Enhancement**: Optional LLM-powered accuracy improvements
- **16GB Memory**: Optimized for Hugging Face Spaces

## 🚀 Usage

1. Upload your document (PDF, DOCX, PPTX, XLSX, HTML, EPUB, PNG, JPG)
2. Configure conversion settings in the sidebar
3. Click "변환 시작" to start conversion
4. Download the converted Markdown file

## ⚙️ Settings

- **LLM Mode**: Uses AI for improved accuracy (slower but better)
- **Output Format**: Choose between Markdown, JSON, or HTML
- **Image Extraction**: Preserve images from documents

## 🔧 Tech Stack

- **Framework**: Streamlit
- **AI/ML**: Marker, PyTorch, Transformers
- **Platform**: Hugging Face Spaces (16GB Memory)

## 📋 Supported Formats

| Input Format | Description |
|--------------|-------------|
| 📄 PDF | Adobe PDF documents |
| 📝 DOCX | Microsoft Word documents |
| 📊 PPTX | Microsoft PowerPoint presentations |
| 📋 XLSX | Microsoft Excel spreadsheets |
| 🌐 HTML | Web page files |
| 📚 EPUB | E-book files |
| 🖼️ PNG/JPG | Image files |

## ⚠️ Limitations

- Large files may take longer to process
- Complex layouts may have imperfect conversion
- First-time model loading requires additional time

---

Made with ❤️ using [Marker](https://github.com/VikParuchuri/marker) and [Streamlit](https://streamlit.io)