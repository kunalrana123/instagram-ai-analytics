from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from sentiment import analyze_sentiment
from clip_analysis import analyze_image_clip, extract_colors
from instagram_analyzer import InstagramAnalyzer
from scrape_creator import scrape_instagram_profile
import asyncio

app = FastAPI(title="Instagram AI Analytics API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    text: str

class CLIPRequest(BaseModel):
    image_url: str
    prompt: str

class AnalysisRequest(BaseModel):
    username: str
    posts_limit: int = 12

class ImageAnalysisRequest(BaseModel):
    image_urls: List[str]

# Initialize analyzer
analyzer = InstagramAnalyzer()

@app.get("/")
def root():
    return {"message": "Instagram AI Analytics API", "version": "1.0.0"}

@app.post("/sentiment")
async def sentiment(req: SentimentRequest):
    try:
        score = analyze_sentiment(req.text)
        return {"score": score, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clip")
async def clip(req: CLIPRequest):
    try:
        similarity = analyze_image_clip(req.image_url, req.prompt)
        return {"similarity": similarity, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-profile")
async def analyze_profile(req: AnalysisRequest):
    try:
        # Get Instagram data (you'll need to implement proper API integration)
        profile_data = await scrape_instagram_profile(req.username, req.posts_limit)
        
        # Analyze the profile
        analysis = analyzer.analyze_profile(profile_data)
        
        return {"analysis": analysis, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-images")
async def analyze_images(req: ImageAnalysisRequest):
    try:
        results = []
        for url in req.image_urls:
            colors = extract_colors(url)
            aesthetic_score = analyze_image_clip(url, "aesthetic beautiful professional photography")
            results.append({
                "url": url,
                "colors": colors,
                "aesthetic_score": aesthetic_score
            })
        return {"results": results, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Instagram AI Analytics"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
