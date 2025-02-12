# Job-Application-Helper

## [AI Resume Analyzer and Cover Letter Generator](https://huggingface.co/spaces/rajaatreja/ATS_Helper) - A HuggingFace App

### Overview

**Job-Application-Helper** is an AI-powered tool designed to analyze resumes and generate personalized cover letters. It leverages the capabilities of **Gradio** for the user interface and integrates with **Google's Generative Language API** for content generation.

### Features

- **Resume Analysis**: Analyze resumes against job descriptions to determine match percentage and identify missing keywords.
- **Cover Letter Generation**: Generate personalized cover letters tailored to specific job applications.
- **PDF Generation**: Create and download cover letters in PDF format.

### Installation

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

### Usage

1. Ensure you have set the `GOOGLE_API_KEY` environment variable with your Google API key.
2. Run the application:

   ```sh
   python app.py
   ```

3. Access the application through the provided local URL.

### Project Structure

```
├── app.py                # Main application file containing the logic for resume analysis, cover letter generation, and the Gradio interface.
├── requirements.txt      # List of dependencies required for the project.
├── LICENSE              # License information for the project.
├── README.md            # Project documentation.
```

### Configuration

This project is configured to run as a **HuggingFace Space** with the following settings:

```yaml
---
title: ATS Helper
emoji: 🏢
colorFrom: yellow
colorTo: blue
sdk: gradio
sdk_version: 5.15.0
app_file: app.py
pinned: false
short_description: Resume Analyzer and Cover Letter Generator
---
```

Check out the configuration reference at [HuggingFace Spaces Config Reference](https://huggingface.co/docs).

### License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

### Acknowledgements

This project utilizes the following technologies:

- [Gradio](https://www.gradio.app/)
- [Google Generative Language API](https://ai.google.dev/)
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/)
- [FPDF](http://www.fpdf.org/)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)
- [Requests](https://docs.python-requests.org/en/latest/)
- [Pyperclip](https://github.com/asweigart/pyperclip)
