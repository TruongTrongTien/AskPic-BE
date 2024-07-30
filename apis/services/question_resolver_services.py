import google.generativeai as genai
from apis.configs.genai_configs import model
from apis.configs.llm_configs import llm, json_parser, str_parser
from apis.utils.prompts import question_resolver_prompt_template
from apis.utils.const import GENERATIVE_MODELS_GENERATION_CONFIGS, GENERATIVE_MODELS_SAFETY_SETTINGS

class AskByImagesServices():

    def __init__(self) -> None:
        pass
        
    async def get_questions(self, uploaded_file_path: str):

        uploaded_file = genai.upload_file(
            path=f"{uploaded_file_path}",
            display_name="uploaded_file"
        )

        response = model.generate_content([
            """
            Perform OCR on the given file.
            You MUST respond a string using this format:
                {{
                    "response": [
                        {{
                            "section requirements": "string",
                            "support information": any or null,
                            "section content": {{
                                "question": "string",
                            }}
                        }}
                        # repeat for each section
                    ]
                }}
            """, 
            uploaded_file
        ],
        generation_config=GENERATIVE_MODELS_GENERATION_CONFIGS,
        safety_settings=GENERATIVE_MODELS_SAFETY_SETTINGS
        )

        extracted_text = response.text

        genai.delete_file(uploaded_file.name)

        return extracted_text
    
    @staticmethod
    async def get_answers(questions: str):

        chain = question_resolver_prompt_template | llm | json_parser

        response = chain.invoke({"text": questions})

        answers = response["response"]

        return answers
