import requests
import json
import os

def generate_ark_image(prompt, filename):
    print(f"Trying BytePlus Ark for {filename}...")
    url = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
    api_key = "dfdb054b-05fc-4180-abf2-20a1c0a668cb"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "seedream-4.5",
        "prompt": prompt,
        "width": 1280,
        "height": 720
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Ark Status: {response.status_code}")
        data = response.json()
        print(f"Ark Response: {json.dumps(data, indent=2)}")
        # Assuming response contains URL or base64 based on typical patterns
        if "data" in data and data["data"] and "url" in data["data"][0]:
            img_url = data["data"][0]["url"]
            img_res = requests.get(img_url)
            with open(filename, "wb") as f:
                f.write(img_res.content)
            return True
        elif "data" in data and data["data"] and "b64_json" in data["data"][0]:
            import base64
            with open(filename, "wb") as f:
                f.write(base64.b64decode(data["data"][0]["b64_json"]))
            return True
    except Exception as e:
        print(f"Ark Error: {e}")
    return False

prompt_logos = "A high-resolution grid showcase of a variety of professionally designed modern minimalist logos for tech startups. Different concepts: abstract geometric shapes, lettermarks, and sleek icons. Color palette: premium blues, teals, and silvers. High-end design agency portfolio style, clean and balanced layout. 16:9 aspect ratio."
prompt_hero = "A high-end website homepage hero section for a startup. Features a centered headline with bold futuristic typography that clearly reads 'YOUR BRAND HERE'. Below it is a call-to-action button. The background is a stunning cinematic 3D abstract motion scene with vibrant blue and teal colors. Premium SaaS aesthetic, clean, modern, 16:9 aspect ratio."

path_logos = "/Users/nagavision/founders_launchpad_app/assets/logos/logos_grid_showcase.jpeg"
path_hero = "/Users/nagavision/founders_launchpad_app/assets/websites/website_hero_your_brand.jpeg"

generate_ark_image(prompt_logos, path_logos)
generate_ark_image(prompt_hero, path_hero)
