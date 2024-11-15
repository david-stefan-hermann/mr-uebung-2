import os
from PIL import Image

def convert_png_to_jpg(folder_path):
    """
    Recursively converts all .png files in the given folder and its subdirectories to .jpg format.
    
    Args:
        folder_path (str): The path to the folder containing .png files.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                png_path = os.path.join(root, file)
                jpg_path = os.path.splitext(png_path)[0] + ".jpg"
                
                try:
                    with Image.open(png_path) as img:
                        # Convert image to RGB (to avoid issues with transparency)
                        rgb_image = img.convert("RGB")
                        rgb_image.save(jpg_path, "JPEG")
                    print(f"Converted: {png_path} -> {jpg_path}")
                except Exception as e:
                    print(f"Failed to convert {png_path}: {e}")

if __name__ == "__main__":
    # Get the current directory where the script is located
    current_folder = os.path.dirname(os.path.abspath(__file__))
    print(f"Converting .png files in the current directory and subdirectories: {current_folder}")
    convert_png_to_jpg(current_folder)
