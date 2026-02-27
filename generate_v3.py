import requests
import json
import base64
import os

def generate_seedance_image(prompt, filename):
    print(f"Trying SeedDance for {filename}...")
    url = "https://api.seedance.ai/v1/generate"
    api_key = "sk_664289ecd9c8ccfc0a2ba8834fc748a7abb04bbe4101b8583a9179a42ef8c"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "seedance-1.5-pro",
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "num_images": 1
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"SeedDance Status: {response.status_code}")
        data = response.json()
        print(f"SeedDance Response: {json.dumps(data, indent=2)}")
        # Handle response based on docs (assuming 'images' or 'url')
        if "images" in data and data["images"]:
            img_url = data["images"][0]["url"]
            img_res = requests.get(img_url)
            with open(filename, "wb") as f:
                f.write(img_res.content)
            return True
    except Exception as e:
        print(f"SeedDance Error: {e}")
    return False

def generate_minimax_image(prompt, filename):
    print(f"Trying MiniMax for {filename}...")
    url = "https://api.minimax.io/v1/image_generation"
    api_key = "sk-api-f-AmaD11Eug3CWVXw9ddSqnzTdNOcdunIdy8Ti1OcgLzCIO8WMTPCwE8b9sfjQEIg9erTsKId4faERdQTWii4nUrIxDkDwZrvwQTPY1a0Bd0Mg0V_9DP9Kg"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "response_format": "base64",
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        if "data" in data and data["data"] and "image_base64" in data["data"]:
            image_data = data["data"]["image_base64"][0]
            with open(filename, "wb") as f:
                f.write(base64.b64decode(image_data))
            return True
        else:
            print(f"MiniMax Error: {data.get('base_resp', {}).get('status_msg', 'Unknown error')}")
    except Exception as e:
        print(f"MiniMax Error: {e}")
    return False

# Prompts
prompt_logos = "A high-resolution grid showcase of a variety of professionally designed modern minimalist logos for tech startups. Different concepts: abstract geometric shapes, lettermarks, and sleek icons. Color palette: premium blues, teals, and silvers. High-end design agency portfolio style, clean and balanced layout. 16:9 aspect ratio."
prompt_hero = "A high-end website homepage hero section for a startup. Features a centered headline with bold futuristic typography that clearly reads 'YOUR BRAND HERE'. Below it is a call-to-action button. The background is a stunning cinematic 3D abstract motion scene with vibrant blue and teal colors. Premium SaaS aesthetic, clean, modern, 16:9 aspect ratio."

# Execution
path_logos = "/Users/nagavision/founders_launchpad_app/assets/logos/logos_grid_showcase.jpeg"
path_hero = "/Users/nagavision/founders_launchpad_app/assets/websites/website_hero_your_brand.jpeg"

if not generate_seedance_image(prompt_logos, path_logos):
    generate_minimax_image(prompt_logos, path_logos)

if not generate_seedance_image(prompt_hero, path_hero):
    generate_minimax_image(prompt_hero, path_hero)
