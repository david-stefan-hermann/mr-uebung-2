import os
from PIL import Image
import numpy as np

def get_dominant_color(image_path):
    """
    Calculate the dominant color of an image as a hex value.

    Args:
        image_path (str): Path to the image.

    Returns:
        str: Hex color string representing the dominant color.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Ensure the image is in RGB mode
            img_array = np.array(img)
            
            # Flatten to a list of RGB values
            pixels = img_array.reshape(-1, 3)
            
            # Calculate the mean color
            mean_color = pixels.mean(axis=0).astype(int)
            
            # Convert to hex
            hex_color = "#{:02x}{:02x}{:02x}".format(*mean_color)
            return hex_color
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def analyze_galaxies(base_folder):
    """
    Analyze all subdirectories for galaxy images and determine the dominant color for each.

    Args:
        base_folder (str): Path to the base folder containing subdirectories of galaxy images.

    Returns:
        dict: Mapping of subdirectory names to dominant colors.
    """
    galaxy_colors = {}
    
    for subdir in os.listdir(base_folder):
        subdir_path = os.path.join(base_folder, subdir)
        if os.path.isdir(subdir_path):
            dominant_colors = []
            
            for file in os.listdir(subdir_path):
                if file.lower().endswith(".jpg"):
                    file_path = os.path.join(subdir_path, file)
                    color = get_dominant_color(file_path)
                    if color:
                        dominant_colors.append(color)
            
            if dominant_colors:
                # Average the hex colors for all images in the subdirectory
                avg_color = calculate_average_hex_color(dominant_colors)
                galaxy_colors[subdir] = avg_color
    
    return galaxy_colors

def calculate_average_hex_color(hex_colors):
    """
    Calculate the average of a list of hex colors.

    Args:
        hex_colors (list): List of hex color strings.

    Returns:
        str: The average hex color.
    """
    rgb_values = [tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) for color in hex_colors]
    avg_rgb = tuple(int(np.mean([rgb[i] for rgb in rgb_values])) for i in range(3))
    return "#{:02x}{:02x}{:02x}".format(*avg_rgb)

def save_colors_to_file(galaxy_colors, output_file):
    """
    Save the galaxy colors to a text file.

    Args:
        galaxy_colors (dict): Mapping of subdirectory names to dominant colors.
        output_file (str): Path to the output text file.
    """
    with open(output_file, "w") as f:
        for galaxy, color in galaxy_colors.items():
            f.write(f"{galaxy}: {color}\n")
    print(f"Galaxy colors saved to {output_file}")

if __name__ == "__main__":
    # Get the current directory where the script is located
    current_folder = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_folder, "galaxy_colors.txt")
    
    print("Analyzing galaxies for dominant colors...")
    galaxy_colors = analyze_galaxies(current_folder)
    save_colors_to_file(galaxy_colors, output_file)
