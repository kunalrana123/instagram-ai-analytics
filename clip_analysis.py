# =================== backend/clip_analysis.py ===================
from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
from sklearn.cluster import KMeans

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def analyze_image_clip(image_url, prompt):
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        image = Image.open(response.raw).convert('RGB')
        inputs = processor(text=[prompt], images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        return probs[0][0].item()
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return 0.0

def extract_colors(image_url, num_colors=5):
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        image = Image.open(response.raw).convert('RGB')
        image = image.resize((150, 150))
        
        data = np.array(image)
        data = data.reshape((-1, 3))
        
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(data)
        
        colors = kmeans.cluster_centers_
        colors = colors.round(0).astype(int)
        
        hex_colors = []
        for color in colors:
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            hex_colors.append(hex_color)
        
        return hex_colors
    except Exception as e:
        print(f"Error extracting colors: {e}")
        return ["#000000", "#FFFFFF", "#808080"]
