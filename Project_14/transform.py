from PIL import Image, ImageFilter, ImageEnhance
import os

# Prompt user for input and output directories
# example: D:\Q3\25 python projects\Project_14\input

input_dir = input("Enter the path to the input directory: ").strip()
output_dir = input("Enter the path to the output directory: ").strip()

# Validate input directory
if not os.path.exists(input_dir):
    print(f"Error: The input directory '{input_dir}' does not exist.")
    exit()

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get all image files from the input directory
valid_extensions = ['.png', '.jpg', '.jpeg']
image_paths = [
    os.path.join(input_dir, file)
    for file in os.listdir(input_dir)
    if any(file.lower().endswith(ext) for ext in valid_extensions)
]

if not image_paths:
    print(f"No valid image files found in the directory '{input_dir}'.")
    exit()

# User inputs for transformations
brightness_factor = float(input("Enter brightness factor (0.0 to 2.0): "))
contrast_factor = float(input("Enter contrast factor (0.0 to 2.0): "))
blur_radius = float(input("Enter blur radius (0.0 to 10.0): "))

# Define functions
def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def apply_blur(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius))

# Process images
for image_path in image_paths:
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        continue  # Skip to the next file

    # Open image and ensure it's in RGB mode
    img = Image.open(image_path).convert("RGB")
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Adjust brightness
    img_bright = adjust_brightness(img, brightness_factor)

    # Adjust contrast
    img_contrast = adjust_contrast(img, contrast_factor)
    
    # Apply blur
    img_blur = apply_blur(img, blur_radius)

    # Combined version
    img_combined = adjust_brightness(img, brightness_factor)
    img_combined = adjust_contrast(img_combined, contrast_factor)
    
    # Save the processed images
    img_bright.save(os.path.join(output_dir, f"{base_name}_bright.png"))
    img_contrast.save(os.path.join(output_dir, f"{base_name}_contrast.png"))
    img_blur.save(os.path.join(output_dir, f"{base_name}_blur.png"))
    img_combined.save(os.path.join(output_dir, f"{base_name}_combined.png"))

    print(f"Processed and saved images for '{base_name}'.")

print("Image processing complete. Check the output directory.")