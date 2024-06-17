import google.generativeai as genai
from apis.configs.genai_configs import model
from apis.configs.llm_configs import llm, parser
from apis.utils.prompts import prompt_template

class Services():

    def __init__(self) -> None:
        pass
        
    def get_questions(self, image_path: str):

        uploaded_file = genai.upload_file(path=f"{image_path}",
                            display_name="image")

        response = model.generate_content(["""
            Perform OCR on the image and extract the text from it.""", 
            uploaded_file
        ])

        extracted_text = response.text

        genai.delete_file(uploaded_file.name)

        return extracted_text
    
    @staticmethod
    async def get_answers(questions: str):

        chain = prompt_template | llm | parser

        response = chain.invoke({"text": questions})

        answers = response["response"]

        return answers