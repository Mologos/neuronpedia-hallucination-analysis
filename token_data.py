import requests
import json
import time

API_BASE = "https://www.neuronpedia.org/api"
API_KEY = "sk-np-tF4x3X90amNPAhUTjynAJAPhOre0osCUtvQ0fzHsizU0" 

def generate_graph(prompt, slug=None):
    url = f"{API_BASE}/graph/generate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # if no slug is provided, create one automatically with timestamp
    if slug is None:
        slug = f"graph-{int(time.time())}"

    payload = {
        "prompt": prompt,
        "modelId": "gemma-2-2b",
        "sourceSetName": "gemmascope-transcoder-16k",
        "slug": slug,
        "maxNLogits": 10,
        "desiredLogitProb": 0.95,
        "nodeThreshold": 0.8,
        "edgeThreshold": 0.85,
        "maxFeatureNodes": 5000
    }

    resp = requests.post(url, headers=headers, json=payload)
    print("Status:", resp.status_code)
    print("Raw response:", resp.text)

    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    text = "Artificial intelligence will transform software architecture."

    try:
        graph = generate_graph(text)  # slug auto-generated
        print(" Graph created successfully!")
        print(" View it here:", graph["url"])
        print("Stored in S3:", graph["s3url"])

        # Download and save graph JSON from S3
        s3_url = graph["s3url"]
        s3_resp = requests.get(s3_url)
        s3_resp.raise_for_status()
        
        graph_json = s3_resp.json()
        with open("s3_graph_data.json", "w", encoding="utf-8") as f:
            json.dump(graph_json, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print("Error creating graph:", e)
