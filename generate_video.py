import requests
import json
import os
import time

def generate_minimax_video(prompt, filename):
    print(f"Trying MiniMax Video for {filename}...")
    url = "https://api.minimax.io/v1/video_generation"
    api_key = "sk-api-f-AmaD11Eug3CWVXw9ddSqnzTdNOcdunIdy8Ti1OcgLzCIO8WMTPCwE8b9sfjQEIg9erTsKId4faERdQTWii4nUrIxDkDwZrvwQTPY1a0Bd0Mg0V_9DP9Kg"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "video-01",
        "prompt": prompt
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if "task_id" in data:
            task_id = data["task_id"]
            print(f"Task ID: {task_id}. Polling for results...")
            
            # Polling loop
            for _ in range(30): # 5 minutes max
                status_url = f"https://api.minimax.io/v1/query_video_generation?task_id={task_id}"
                status_res = requests.get(status_url, headers=headers)
                status_data = status_res.json()
                print(f"Polling status: {status_data.get('status')}")
                
                if status_data.get("status") == "Success":
                    video_url = status_data["file_id"] # Or similar field
                    # The file_id might need a download call
                    print(f"Success! Video File ID: {video_url}")
                    return True
                elif status_data.get("status") == "Fail":
                    print(f"Generation failed: {status_data}")
                    return False
                time.sleep(10)
        else:
            print(f"Error: {data.get('base_resp', {}).get('status_msg', 'Unknown error')}")
    except Exception as e:
        print(f"MiniMax Video Error: {e}")
    return False

prompt_hero = "A stunning cinematic 3D abstract motion scene with vibrant blue and teal colors. Flowing interconnected luminous lines, floating geometric shards, high-end CGI, premium SaaS aesthetic, 16:9 aspect ratio."
generate_minimax_video(prompt_hero, "/Users/nagavision/founders_launchpad_app/assets/websites/hero_motion.mp4")
