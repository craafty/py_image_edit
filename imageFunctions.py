from PIL import Image
from PIL import Image
##def main():
    ##return("hello world")


    def rotate_image(input_path, output_path, degrees=90):
    # Open the image
    img = Image.open(input_path)

    # Rotate the image
    rotated_img = img.rotate(degrees, expand=True)

    # Save the new image
    rotated_img.save(output_path)

    print(f"Rotated image saved to {output_path}")

   




