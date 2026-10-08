import AI_note_QA_bot as QA_Bot
from fastapi import HTTPException,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import vector_store as vs
import gemini_client as gc
from fastapi import UploadFile ,Form
import os
import shutil


allowed_extensions = (".pdf",".txt")
NOTES_DIR = "./"
MAX_UPLOAD_BYTES = 3 * 1024 * 1024

app = FastAPI()

class Query_data(BaseModel):
    question:str
    file_name:str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/files')
def file_data():
    known_files = QA_Bot.load_known_files()
    return{
        "known_files":known_files
    }

@app.post('/ask')
def ask_query_data(data:Query_data):
    known_files = QA_Bot.load_known_files()
    found = any(file["filename"] == data.file_name for file in known_files)

    if not found:
        raise HTTPException(status_code=404, detail="File not found")
    relevant_chunk= QA_Bot.query_collection(filename=data.file_name,question=data.question,n_results=3)
    try:
        gemini_answer = gc.ask_gemini(question=data.question,content_chunk=relevant_chunk)
    except Exception as e:
        print("Error:",e)
        raise HTTPException(status_code=502, detail="Gemini has failed")  
    return{
        "answer":gemini_answer
        }
@app.post('/upload')
def user_file_upload(file:UploadFile,subject:str = Form(...)):
    clean_name =os.path.basename(file.filename or "")
    if not clean_name:
        raise HTTPException(status_code=400, detail="Invalid file name")
    if not subject:
        raise HTTPException(status_code=400, detail="Invalid subject")
    extension = QA_Bot.file_extension_extractor(clean_name).lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=415, detail="unsupported file type")
    if file.size is not None:
        if file.size > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="file size too large(MAX:5MB)")
    found = any(clean_name == saved_files['filename'] for saved_files in QA_Bot.load_known_files())
    if found:
        raise HTTPException(status_code=409,detail="File already exists")
    path = os.path.join(NOTES_DIR,clean_name)
    with open (path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    delete_file = True
    try:
        chunk_count = QA_Bot.new_chunks_creator(file_name=clean_name,subject=subject)
    except QA_Bot.FileAlreadyExistsError as e:
        delete_file = False
        print(e)
        raise HTTPException(status_code=409,detail="File already exists")
    except QA_Bot.EmptyTextError as e:
        print(e)
        raise HTTPException(status_code=400,detail="empty file name uploaded")
    except QA_Bot.UnSupportedFileType as e:
        raise HTTPException(status_code=415,detail="Unsupported file type uploaded")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Something went wrong..")
    finally:
        if  delete_file and os.path.exists(path):
            os.remove(path=path)
    return {
        "file_name":clean_name,
        "chunk_count":chunk_count,
        "size":file.size
    }



    

   