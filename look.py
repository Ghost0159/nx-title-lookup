import requests
import json
from bs4 import BeautifulSoup

def nintendoTitleLookup(titleid,region="US"):
    url = f"https://ec.nintendo.com/apps/{titleid}/{region}"
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        next_data = soup.find('script',id='__NEXT_DATA__')
        if next_data:
            tJson = json.loads(next_data.string)
            tData = tJson['props']['pageProps']['initialApolloState']
            required_subkeys = ['name', 'metaTitle', 'metaDescription', 'descriptionImage', 'softwarePublisher']

            for key, value in tData.items():
                if key.startswith('StoreProduct'):
                    if isinstance(value, dict):
                        if all(subkey in value for subkey in required_subkeys):
                            return value
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


print(nintendoTitleLookup('010073C01AF34000'))