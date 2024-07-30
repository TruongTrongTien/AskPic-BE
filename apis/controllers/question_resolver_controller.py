import http
import os

from fastapi import APIRouter, UploadFile, File, Form

from apis.schemas.base import GenericResponseModel
from apis.services.question_resolver_services import AskByImagesServices
from apis.utils.get_file import get_image_file, get_pdf_file, get_docx_file

question_resolver_router = APIRouter(prefix="/apis/question_resolver", tags=["Question Resolver"])

@question_resolver_router.post("/ask_by_media", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel)
async def ask_by_media(uploaded_file: UploadFile = File(..., description="Upload the file to extract questions from")):
    try:
        file_extension = uploaded_file.filename.split('.')[-1].lower()
        
        # Check if the file is in the allowed format
        if file_extension not in ['jpg', 'jpeg', 'png', 'pdf', 'docx']:
            return GenericResponseModel(error="Invalid file format", status_code=http.HTTPStatus.BAD_REQUEST, message="Only jpg, jpeg and png files are allowed")
        
        if not os.path.exists('tmp'):
            os.makedirs('tmp')

        request_object_content = await uploaded_file.read()
        uploaded_file_name = uploaded_file.filename

        if file_extension in ['jpg', 'jpeg', 'png']:
            uploaded_file_path = get_image_file(
                object_content=request_object_content,
                file_name=uploaded_file_name
            )

        elif file_extension in ['pdf']:
            uploaded_file_path = get_pdf_file(
                object_content=request_object_content,
                file_name=uploaded_file_name
            )

        elif file_extension in ['docx']:
            uploaded_file_path, docx_file_path = get_docx_file(
                object_content=request_object_content,
                file_name=uploaded_file_name
            )

        # Extract questions from the image and get answers
        services = AskByImagesServices()
        questions = await services.get_questions(uploaded_file_path=uploaded_file_path)
        answers = await services.get_answers(questions=questions)
        
        # Delete the files in tmp folder
        os.remove(uploaded_file_path)
        if file_extension == 'docx':
            os.remove(docx_file_path)

        return GenericResponseModel(data=answers, status_code=http.HTTPStatus.OK, message="Questions extracted and answered successfully")
    
    except Exception as e:
        return GenericResponseModel(error=str(e), status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, message="An error occurred")
    
@question_resolver_router.post("/ask_by_text", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel)
async def ask_by_text(text: str = Form(..., description="Enter your questions")):
    try:
        services = AskByImagesServices()
        answers = await services.get_answers(questions=text)
        
        return GenericResponseModel(data=answers, status_code=http.HTTPStatus.OK, message="Questions answered successfully")
    except Exception as e:
        return GenericResponseModel(error=str(e), status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, message="An error occurred")
    
@question_resolver_router.post("/get_feedback", status_code=http.HTTPStatus.OK, response_model=GenericResponseModel)
async def get_feedback(qa: str = Form(..., description="Enter the questions and answers")):
    try:
        services = AskByImagesServices()
        feedback = await services.get_feedback(qa=qa)
        
        return GenericResponseModel(data=feedback, status_code=http.HTTPStatus.OK, message="Feedback generated successfully")
    except Exception as e:
        return GenericResponseModel(error=str(e), status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, message="An error occurred")
