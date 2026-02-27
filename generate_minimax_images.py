import base64
import requests
import os
import sys
import json

def generate_image(prompt, filename):
    url = "https://api.minimax.io/v1/image_generation"
    api_key = "sk-api-f-AmaD11Eug3CWVXw9ddSqnzTdNOcdunIdy8Ti1OcgLzCIO8WMTPCwE8b9sfjQEIg9erTsKId4faERdQTWii4nUrIxDkDwZrvwQTPY1a0Bd0Mg0V_9DP9Kg"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "response_format": "base64",
    }

    print(f"Generating image for: {filename}...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        res_data = response.json()
        print(f"Response: {json.dumps(res_data, indent=2)}")
        
        if "data" in res_data and res_data["data"] and "image_base64" in res_data["data"]:
            image_data = res_data["data"]["image_base64"][0]
            with open(filename, "wb") as f:
                f.write(base64.b64decode(image_data))
            print(f"Successfully saved {filename}")
        else:
            print(f"Error: Unexpected response format for {filename}")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

# Image 1: Logo Showcase
prompt_logos = "A high-resolution grid showcase of a variety of professionally designed modern minimalist logos for tech startups. Different concepts: abstract geometric shapes, lettermarks, and sleek icons. Color palette: premium blues, teals, and silvers. High-end design agency portfolio style, clean and balanced layout. 16:9 aspect ratio."
generate_image(prompt_logos, "/Users/nagavision/founders_launchpad_app/assets/logos/logos_grid_showcase.jpeg")

# Image 2: YOUR BRAND HERE Website Hero
prompt_hero = "A high-end website homepage hero section for a startup. Features a centered headline with bold futuristic typography that clearly reads 'YOUR BRAND HERE'. Below it is a clear call-to-action button. The background is a stunning cinematic 3D abstract motion scene with vibrant blue and teal colors. Premium SaaS aesthetic, clean, modern, 16:9 aspect ratio."
generate_image(prompt_hero, "/Users/nagavision/founders_launchpad_app/assets/websites/website_hero_your_brand.jpeg")
