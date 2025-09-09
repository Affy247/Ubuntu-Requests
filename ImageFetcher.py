import requests
import os
from urllib.parse import urlparse

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Challenge 2: Implement a feature that prevents downloading duplicate images.
    # We use a set for efficient lookup of previously downloaded URLs.
    downloaded_urls = set()
    
    # Challenge 1: Modify the program to handle multiple URLs at once.
    # We use a while loop that runs until the user types 'done'.
    while True:
        # Get URL from user
        url = input("Please enter the image URL (or 'done' to exit): ")

        # Exit condition for the loop
        if url.lower() == 'done':
            print("Download session finished.")
            break
            
        # Check for duplicates before attempting to download
        if url in downloaded_urls:
            print("✗ This URL has already been downloaded. Skipping.")
            continue  # Skips the rest of the loop and prompts for the next URL

        try:
            # Create directory if it doesn't exist
            directory = "Fetched_Images"
            os.makedirs(directory, exist_ok=True)
            
            # Fetch the image with a timeout
            response = requests.get(url, stream=True, timeout=15)
            response.raise_for_status()  # Raise exception for bad status codes

            # Challenge 4: Implement what HTTP headers might be important to check.
            # Check the Content-Type to ensure it's a valid image
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                print(f"✗ The URL content is not a supported image type ({content_type}). Skipping.")
                continue

            # Check for a reasonable file size limit (e.g., 50 MB)
            content_length = int(response.headers.get('Content-Length', 0))
            max_size_bytes = 50 * 1024 * 1024 # 50 MB
            if content_length > max_size_bytes:
                print("✗ File is too large. Skipping.")
                continue

            # Extract filename from URL or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # Use a default filename if one cannot be extracted
            if not filename or '.' not in filename:
                import time
                filename = f"downloaded_image_{int(time.time())}.{content_type.split('/')[-1]}"
            
            # Sanitize filename to prevent directory traversal attacks
            filename = os.path.basename(filename)
                
            # Save the image
            filepath = os.path.join(directory, filename)
            
            # Use 'wb' for binary write mode
            with open(filepath, 'wb') as f:
                # Use iter_content for memory efficiency with large files
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                
            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")
            
            # Add the URL to our set of downloaded URLs
            downloaded_urls.add(url)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()