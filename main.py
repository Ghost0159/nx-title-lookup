import os
import json
import requests
from bs4 import BeautifulSoup

def nintendoTitleLookup(titleid, region="US"):
    """
    Retrieves all raw data for a specific Nintendo title.
    """
    url = f"https://ec.nintendo.com/apps/{titleid}/{region}"
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        next_data = soup.find('script', id='__NEXT_DATA__')
        if next_data:
            # Parse the raw JSON
            tJson = json.loads(next_data.string)
            tData = tJson['props']['pageProps']['initialApolloState']
            return tData
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def saveToJson(data, titleid, region):
    """
    Saves the data in JSON format in a structured path: /data/[region]/[titleid].json
    """
    # Create the folder path
    folder_path = os.path.join("data", region)
    os.makedirs(folder_path, exist_ok=True)
    
    # Determine the file path
    file_path = os.path.join(folder_path, f"{titleid}.json")
    
    # Save all raw data to a JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Saved all data to {file_path}")

def main():
    # Example usage
    titleid = "01008AF01AD22000"  # Replace with the desired title ID
    region = "US"  # Replace with the desired region (e.g., "JP", "EU", etc.)
    
    # Retrieve the complete data
    data = nintendoTitleLookup(titleid, region)
    if data:
        # Save all extracted data
        saveToJson(data, titleid, region)
    else:
        print("No data found or an error occurred.")

if __name__ == "__main__":
    main()
