import requests
from properties import *
import easyocr
from PIL import Image
from io import BytesIO

def ocr_image(image):
    reader = easyocr.Reader(['en'])  # Specify the languages you want to detect
    result = reader.readtext(image)
    extracted_text = ' '.join([res[1] for res in result])
    return extracted_text

def google_search(query):
    base_url = "https://www.googleapis.com/customsearch/v1"
    api_key = API_KEY  # Replace with your Google Custom Search API key
    cx = CX_ID  # Replace with your Custom Search Engine (CX) ID

    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        return search_results.get("items", [])

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return []

if __name__ == "__main__":
    # Google Custom Search API key and Custom Search Engine (CX) ID
    api_key = API_KEY
    cx = CX_ID

    # Step 1: Get the image path or URL from the user
    image_input = input("Enter the image path or URL: ")

    # Step 2: Load the image from path or download from URL
    if image_input.startswith("http"):
        # If the input is an image URL, download the image
        try:
            response = requests.get(image_input)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            print("Error downloading the image:", e)
            exit()
        except IOError as e:
            print("Error opening the image:", e)
            exit()
    else:
        # If the input is a local image path, open the image directly
        try:
            image = Image.open(image_input)
        except IOError as e:
            print("Error opening the image:", e)
            exit()

    # Step 3: Perform Optical Character Recognition (OCR) on the image
    extracted_text = ocr_image(image)
    print("Extracted Text:")
    print(extracted_text)

    # Step 4: Allow the user to choose a word from the extracted text
    words = extracted_text.split()
    selected_word = input("Enter the word to search for: ")

    # Step 5: Check if the selected word exists in the extracted text
    if selected_word.lower() in extracted_text.lower():
        # Step 6: Perform Google search using the selected word
        results = google_search(selected_word)

        if results:
            # Print search results
            print("\nSearch Results for:", selected_word)
            print("---------------------------")

            for item in results:
                print(item["title"], "-", item["link"])
        else:
            print("No results found.")
    else:
        print("The given word is not present in the image.")

