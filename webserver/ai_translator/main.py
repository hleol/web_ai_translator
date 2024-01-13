import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator


def translate_pdf(model_type, openai_api_key, file_format, book, openai_model, target_language, output_file_path, pages):
    try:
        # Load configuration
        config_loader = ConfigLoader('config.yaml')
        config = config_loader.load_config()

        # Extract model and API key information
        model_name = openai_model if openai_model else config['OpenAIModel']['model']
        api_key = openai_api_key if openai_api_key else config['OpenAIModel']['api_key']

        # Validate OpenAIModel parameters
        if model_type == 'OpenAIModel' and not openai_model and not openai_api_key:
            raise ValueError("openai_model and openai_api_key are required when using OpenAIModel")

        # Initialize OpenAIModel
        model = OpenAIModel(model=model_name, api_key=api_key)

        # Extract file path and file format information
        pdf_file_path = book if book else config['common']['book']
        file_format = file_format if file_format else config['common']['file_format']

        # Instantiate PDFTranslator and call translate_pdf()
        translator = PDFTranslator(model)
        translator.translate_pdf(pdf_file_path, file_format, target_language, output_file_path, pages)

    except Exception as e:
        # Handle exceptions and log or raise accordingly
        print(f"An error occurred: {str(e)}")
        # You can raise the exception again if you want it to propagate to the caller
        raise


if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
    api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)


    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format)
