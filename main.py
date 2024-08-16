from fastapi import FastAPI, File, UploadFile, Form, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db, Feedback  # Ensure you have these in your `database` module
from pydantic import BaseModel
import shutil
import os
from detectron2_code import Detectron2Model  # Ensure the correct import path

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ensure the uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Serve static files
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# Initialize the Detectron2 model
detectron2_model = Detectron2Model()

class FeedbackModel(BaseModel):
    image_filename: str
    feedback: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Run image segmentation
        result_image_path = detectron2_model.predict(file_location)
        
        # Adjust path for serving
        result_image_url = f"{result_image_path}"
        
        return {"result_image": result_image_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/feedback/")
async def submit_feedback(image_filename: str = Form(...), feedback: str = Form(...),db: Session = Depends(get_db)):
    try:
        if feedback.lower() == "negative":
            new_feedback = Feedback(image_filename=image_filename, feedback=feedback)
            db.add(new_feedback)
            db.commit()
            return {"message": "Feedback recorded."}
        # return {"message": "Feedback not recorded. Only negative feedback is stored."}
        elif feedback.lower() =="positive":
            new_feedback = Feedback(image_filename=image_filename, feedback=feedback)
            db.add(new_feedback)
            db.commit()
            return {"message": "Feedback recorded."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
