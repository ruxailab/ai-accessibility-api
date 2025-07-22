# Install necessary libraries if you haven't already
# !pip install transformers pillow

from transformers import pipeline
from PIL import Image
import requests

# 1. Initialize the image captioning pipeline
# We'll use a pre-trained model for image captioning.
# "Salesforce/blip-image-captioning-base" is a good general-purpose model.
# You can explore other models on Hugging Face if this one doesn't meet your needs.
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# 2. Function to get caption from an image
def get_image_caption(image_input):
    """
    Generates a caption for the given image input.

    Args:
        image_input: Can be a file path (str), a URL (str), or a PIL Image object.

    Returns:
        str: The generated caption for the image.
    """
    try:
        # If the input is a URL, download the image
        if isinstance(image_input, str) and (image_input.startswith('http://') or image_input.startswith('https://')):
            image = Image.open(requests.get(image_input, stream=True).raw).convert("RGB")
        # If the input is a file path, open the image
        elif isinstance(image_input, str):
            image = Image.open(image_input).convert("RGB")
        # If the input is already a PIL Image
        elif isinstance(image_input, Image.Image):
            image = image_input.convert("RGB")
        else:
            print("Invalid image input. Please provide a file path, URL, or PIL Image object.")
            return None

        # Generate the caption
        # The pipeline returns a list of dictionaries, we want the 'generated_text' from the first item.
        result = captioner(image)
        if result and len(result) > 0 and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            return "Could not generate caption."

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Example Usage ---

# Example 1: Using a URL
print("--- Example 1: Captioning from a URL ---")
image_url = "https://www.fourpaws.com/-/media/Project/OneWeb/FourPaws/Images/articles/family-matters/dog-playtime/dog-playtime-927x388.jpg" # Placeholder image URL
caption_from_url = get_image_caption(image_url)
if caption_from_url:
    print(f"Image URL: {image_url}")
    print(f"Generated Caption: {caption_from_url}\n")

# Example 2: Using a local image file (uncomment and replace with your image path)
# To run this, you'll need an image file named 'your_image.jpg' (or any other format)
# in the same directory as your notebook, or provide its full path.
# print("--- Example 2: Captioning from a local file ---")
# try:
#     # Create a dummy image file for demonstration if it doesn't exist
#     dummy_image_path = "dummy_image.jpg"
#     try:
#         Image.new('RGB', (600, 400), color = 'red').save(dummy_image_path)
#         print(f"Created a dummy image at: {dummy_image_path}")
#     except Exception as e:
#         print(f"Could not create dummy image: {e}. Please ensure you have write permissions or create an image manually.")

#     caption_from_file = get_image_caption(dummy_image_path)
#     if caption_from_file:
#         print(f"Local Image Path: {dummy_image_path}")
#         print(f"Generated Caption: {caption_from_file}\n")
# finally:
#     # Clean up the dummy image if it was created
#     import os
#     if 'dummy_image_path' in locals() and os.path.exists(dummy_image_path):
#         os.remove(dummy_image_path)
#         print(f"Cleaned up dummy image: {dummy_image_path}")


# # Example 3: Using a PIL Image object directly
# print("--- Example 3: Captioning from a PIL Image object ---")
# # Create a simple PIL Image object
# pil_image = Image.new('RGB', (400, 300), color = 'blue')
# caption_from_pil = get_image_caption(pil_image)
# if caption_from_pil:
#     print(f"PIL Image Object (400x300, blue)")
#     print(f"Generated Caption: {caption_from_pil}\n")