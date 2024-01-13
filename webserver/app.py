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

        model_type = request.form.get('model_type') or 'OpenAIModel'
        openai_api_key = request.form.get('openai_api_key')
        file_format = request.form.get('file_format')
        book = request.form.get('book')
        openai_model = request.form.get('openai_model') or 'gpt-3.5-turbo'
        target_language = request.form.get('target_language') or "中文"
        output_file_path = request.form.get('output_file_path')
        pages = request.form.get("pages")

        # model_type = 'OpenAIModel'  # Set your default or configurable model type
        # openai_api_key = 'your_default_key'  # Set your default or configurable API key
        # file_format = 'pdf'  # Set your default or configurable file format
        # book = file  # Assuming the uploaded file is the book
        # openai_model = 'gpt-3.5-turbo'  # Set your default or configurable OpenAI model
        # target_language = "中文"
        # output_file_path = "/Users/hao.li/Downloads"
        # pages = 1
        try:
            output_file = translate_pdf(model_type, openai_api_key, file_format, book, openai_model, target_language, output_file_path, pages)
            return render_template('index.html', message=f'File {output_file} uploaded and translated successfully')
        except Exception as e:
            return render_template('index.html', message=f'Error: {str(e)}')

    return render_template('index.html', message='')


if __name__ == '__main__':
    app.run(debug=True)
