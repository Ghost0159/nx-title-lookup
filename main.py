import os
import json
import requests
from bs4 import BeautifulSoup

def nintendoTitleLookup(titleid, region="US"):
    """
    Retrieve data for the first StoreProduct containing required keys.
    """
    url = f"https://ec.nintendo.com/apps/{titleid}/{region}"
    required_keys = ['name', 'metaTitle', 'metaDescription', 'productImage', 'softwarePublisher', 'productGallery']

    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        next_data = soup.find('script', id='__NEXT_DATA__')
        if next_data:
            data = json.loads(next_data.string)
            state = data['props']['pageProps']['initialApolloState']

            for key, value in state.items():
                if key.startswith('StoreProduct') and isinstance(value, dict):
                    if all(k in value for k in required_keys):
                        return value
        return None
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_json(data, titleid, region):
    """
    Save data as JSON in /data/[region]/[titleid].json.
    """
    folder_path = os.path.join("data", region)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{titleid}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path}")

def download_file(url, save_path):
    """
    Download a file from a URL and save it to the specified path.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {save_path}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

def download_banner(product_image, titleid, region):
    """
    Download the banner from productImage and save as /media/[region]/[titleid]/banner.jpg.
    """
    public_id = product_image.get("publicId")
    if public_id:
        url = f"https://assets.nintendo.com/image/upload/q_auto/f_auto/{public_id}"
        save_path = os.path.join("media", region, titleid, "banner.jpg")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        download_file(url, save_path)
    else:
        print("No valid publicId for banner.")

def download_gallery_images(product_gallery, titleid, region):
    """
    Download images from productGallery and save as /media/[region]/[titleid]/screens/.
    """
    base_url = "https://assets.nintendo.com/image/upload/q_auto/f_auto/"
    save_dir = os.path.join("media", region, titleid, "screens")
    os.makedirs(save_dir, exist_ok=True)

    for i, image in enumerate(product_gallery, start=1):
        public_id = image.get("publicId")
        if public_id:
            url = f"{base_url}{public_id}"
            save_path = os.path.join(save_dir, f"screen_{i}.jpg")
            download_file(url, save_path)

def main():
    """
    Main function to retrieve and process Nintendo game data.
    """
    titleid = "010012A01EE0E000"  # Replace with desired title ID
    region = "US"  # Replace with desired region (e.g., "JP", "EU", etc.)

    data = nintendoTitleLookup(titleid, region)
    if data:
        # Save JSON data
        save_to_json(data, titleid, region)

        # Download banner
        product_image = data.get("productImage")
        if product_image:
            download_banner(product_image, titleid, region)

        # Download gallery images
        product_gallery = data.get("productGallery", [])
        if product_gallery:
            download_gallery_images(product_gallery, titleid, region)
    else:
        print("No valid StoreProduct found.")

if __name__ == "__main__":
    main()
