from fastapi import FastAPI, UploadFile, File, Form
import fitz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.post("/match/")
async def match_resume(job_description: str = Form(...), resume: UploadFile = File(...)):
    resume_text = extract_text_from_pdf(resume.file)
    
    embeddings = model.encode([job_description, resume_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    percentage = round(float(score) * 100, 2)
    
    status = "Highly Matched" if percentage > 70 else "Needs Improvement"
    
    return {"match_score": f"{percentage}%", "status": status}

@app.get("/")
def home():
    return {"message": "AI Resume Screener Backend is Running!"}