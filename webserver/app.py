# web_server/app.py
import os
from flask import Flask, render_template, request, get_flashed_messages
from ai_translator.main import translate_pdf # Update the import path based on your project structure

app = Flask(__name__)
app.secret_key = 'my-secret-key-random'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        model_type = request.form.get('model_type') or 'OpenAIModel'
        openai_api_key = request.form.get('openai_api_key') or os.environ.get('OPENAI_API_KEY')

        file_format = request.form.get('file_format')
        if file_format != 'pdf':
            return render_template('index.html', message='Now we only support pdf format')

        openai_model = request.form.get('openai_model') or 'gpt-3.5-turbo'
        target_language = request.form.get('target_language') or "中文"
        output_file_path = request.form.get('output_file_path') or os.getcwd()

        if not output_file_path:
            return render_template('index.html', message='please enter output file path!')

        pages = int(request.form.get("pages")) or 1

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', message='No selected file')

        try:
            output_file = translate_pdf(model_type, openai_api_key, file_format, file, openai_model, target_language, output_file_path, pages)
            messages = get_flashed_messages()
            return render_template('index.html', message=messages + f'File {output_file} uploaded and translated successfully')
        except Exception as e:
            return render_template('index.html', message=f'Error: {str(e)}')

    return render_template('index.html', message='')


if __name__ == '__main__':
    app.run(debug=True)
