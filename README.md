# 📄 Marker PDF to Markdown Converter

A web application built with Streamlit that converts PDF files to Markdown using the powerful [Marker](https://github.com/VikParuchuri/marker) library.

## 🌟 Features

- **PDF to Markdown Conversion**: High-quality conversion preserving formatting
- **Multiple Output Formats**: Markdown, JSON, and HTML
- **Image Extraction**: Extract and preserve images from PDFs
- **LLM Enhancement**: Optional AI-powered accuracy improvements
- **Web Interface**: Easy-to-use Streamlit interface
- **Cloud Deployment**: Ready for Streamlit Community Cloud

## 🚀 Live Demo

[Visit the deployed app on Streamlit Community Cloud](your-app-url-here)

## 🛠️ Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/marker-streamlit-app.git
cd marker-streamlit-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Docker Setup

```bash
docker build -t marker-app .
docker run -p 8501:8501 marker-app
```

## 📖 Usage

1. **Upload PDF**: Select a PDF file to convert
2. **Configure Settings**: 
   - Choose output format (Markdown, JSON, HTML)
   - Enable/disable LLM mode for higher accuracy
   - Toggle image extraction
3. **Convert**: Click "변환 시작" to start conversion
4. **Download**: Download the converted file

## ⚙️ Configuration

### Environment Variables

- `GEMINI_API_KEY`: For LLM-enhanced conversions (optional)

### Settings

- **LLM Mode**: Uses AI for improved accuracy (slower)
- **Output Format**: Markdown (recommended), JSON, or HTML
- **Image Extraction**: Preserves images from PDF

## 🔧 Tech Stack

- **Frontend**: Streamlit
- **PDF Processing**: Marker
- **AI/ML**: PyTorch, Transformers
- **Deployment**: Streamlit Community Cloud

## 📋 Requirements

- Python 3.10+
- 4GB+ RAM recommended
- GPU optional (for faster processing)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Marker](https://github.com/VikParuchuri/marker) - The core PDF processing library
- [Streamlit](https://streamlit.io) - Web application framework
- [Datalab](https://www.datalab.to) - Marker development team

## ⚠️ Limitations

- Large files may timeout on Streamlit Community Cloud
- Complex PDFs may have imperfect conversion results
- First-time model loading takes additional time

## 📞 Support

If you encounter issues:

1. Check the [Issues](https://github.com/your-username/marker-streamlit-app/issues) page
2. Review the [Marker documentation](https://github.com/VikParuchuri/marker)
3. Create a new issue with details

---

Made with ❤️ using [Marker](https://github.com/VikParuchuri/marker) and [Streamlit](https://streamlit.io)