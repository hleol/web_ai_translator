# web_server/app.py
from flask import Flask, render_template, request
from ai_translator.main import translate_pdf # Update the import path based on your project structure

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', message='No selected file')

        model_type = 'OpenAIModel'  # Set your default or configurable model type
        openai_api_key = 'your_default_key'  # Set your default or configurable API key
        file_format = 'pdf'  # Set your default or configurable file format
        book = file  # Assuming the uploaded file is the book
        openai_model = 'gpt-3.5-turbo'  # Set your default or configurable OpenAI model

        try:
            output_file = translate_pdf(model_type, openai_api_key, file_format, book, openai_model)
            return render_template('index.html', message=f'File {output_file} uploaded and translated successfully')
        except Exception as e:
            return render_template('index.html', message=f'Error: {str(e)}')

    return render_template('index.html', message='')


if __name__ == '__main__':
    app.run(debug=True)
