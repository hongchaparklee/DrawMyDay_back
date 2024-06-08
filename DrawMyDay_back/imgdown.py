import os
import requests

def download_image(url, save_path):
    try:
        # Download the image from the URL
        response = requests.get(url)
        response.raise_for_status()

        # Save the image in binary mode
        with open(save_path, 'wb') as f:
            f.write(response.content)

        print(f"Image downloaded successfully. Saved file path: {os.path.abspath(save_path)}")
    except Exception as e:
        print(f"Error downloading image: {e}")

def read_url_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            url = file.readline().strip()
        return url
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

if __name__ == "__main__":
    # Read URL from TRresult.txt file
    file_path = "TRresult.txt"
    image_url = read_url_from_file(file_path)
    if image_url:
        save_path = "Imgdownload/downloaded_image.png"
        download_image(image_url, save_path)
    else:
        print("Failed to read URL.")

