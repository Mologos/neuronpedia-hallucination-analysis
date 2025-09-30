from token_data import generate_graph
from data_analysis import TokenDataAnalyzer
import requests
import json

def main():
 text = input("Enter text to analyze: ")

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

     # analyzer = TokenDataAnalyzer('s3_graph_data.json')
     # print("Total tokens:", analyzer.token_count())
     # print("Most common tokens:", analyzer.most_common_tokens())
     # print("Average token length:", analyzer.average_token_length())

 except Exception as e:
    print("Error creating graph:", e)

if __name__ == "__main__":
    main()
