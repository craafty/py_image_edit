from PIL import Image, ImageEnhance, ImageFilter

# Image Cropping
def crop_image(image_path, crop_box, save_path=None):
        """
        Crops the image to the specified box.
    
        Parameters:
            image_path (str): Path to the input image.
            crop_box (tuple): (left, upper, right, lower) pixel coordinates.
            save_path (str, optional): If given, saves the cropped image.
    
        Returns:
            PIL.Image.Image: The cropped image.
        """
        img = Image.open(image_path)
        width, height = img.size
        left, upper, right, lower = crop_box
        # Validate crop box
        if not (0 <= left < right <= width and 0 <= upper < lower <= height):
            raise ValueError("Crop box is out of image bounds.")
        cropped_img = img.crop(crop_box)
        if save_path:
            cropped_img.save(save_path)
        return cropped_img

def rotate_image(input_path, output_path, degrees=90):
    img = Image.open(input_path)
    # Rotate the image
    rotated_img = img.rotate(degrees, expand=True)
    # Save the new image
    rotated_img.save(output_path)


# Image Flipping
def flip_image(path, mode="horizontal"):
    img = Image.open(path)
    
    if mode == "horizontal":
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == "vertical":
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("Mode must be 'horizontal' or 'vertical'")
    
# RGB colour editing
def adjust_rgb(image_path, r_factor=1.0, g_factor=1.0, b_factor=1.0, save_path=None):
    """
    Adjusts the RGB channels of an image by scaling factors.
    Parameters:
        image_path (str): Path to the input image.
        r_factor (float): Multiplier for Red channel.
        g_factor (float): Multiplier for Green channel.
        b_factor (float): Multiplier for Blue channel.
        save_path (str, optional): If given, saves the edited image to this path.

    Returns:
        PIL.Image.Image: The edited image.
    """
    img = Image.open(image_path).convert("RGB")
    r, g, b = img.split()

    # Apply scaling to each channel
    r = r.point(lambda i: min(255, i * r_factor))
    g = g.point(lambda i: min(255, i * g_factor))
    b = b.point(lambda i: min(255, i * b_factor))

    edited = Image.merge("RGB", (r, g, b))

    if save_path:
        edited.save(save_path)

    return edited


def adjust_saturation(image_path, factor=1.0, save_path=None):
    """
    Adjusts the color saturation of an image.

    Parameters:
        image_path (str): Path to the input image.
        factor (float): Saturation factor.
                        0.0 = black & white
                        1.0 = original image
                        >1.0 = more saturated
        save_path (str, optional): If given, saves the edited image.

    Returns:
        PIL.Image.Image: The edited image.
    """
    img = Image.open(image_path).convert("RGB")

    # Create an enhancer for color saturation
    enhancer = ImageEnhance.Color(img)
    edited = enhancer.enhance(factor)

    if save_path:
        edited.save(save_path)

    return edited
    

def adjust_brightness_sharpness(image_path, brightness=1.0, sharpness=1.0, save_path=None):
    """
    Adjusts the brightness and sharpness of an image.

    Parameters:
        image_path (str): Path to the input image.
        brightness (float): Brightness factor.
                            0.0 = completely black
                            1.0 = original brightness
                            >1.0 = brighter
        sharpness (float): Sharpness factor.
                        0.0 = very blurry
                        1.0 = original sharpness
                        >1.0 = more sharp
        save_path (str, optional): If given, saves the edited image.

    Returns:
        PIL.Image.Image: The edited image.
    """
    img = Image.open(image_path).convert("RGB")

    # Adjust brightness
    bright_enhancer = ImageEnhance.Brightness(img)
    img = bright_enhancer.enhance(brightness)

    # Adjust sharpness
    sharp_enhancer = ImageEnhance.Sharpness(img)
    img = sharp_enhancer.enhance(sharpness)
    if save_path:
        img.save(save_path)
    return img
   



#Image Blur
def adjust_blur(image_path, blur=0.0, save_path=None):
    """
    Adjusts brightness, sharpness, and blur of an image.

    Parameters:
        image_path (str): Path to the input image.
        brightness (float): Brightness factor.
                            0.0 = completely black
                            1.0 = original
                            >1.0 = brighter
        sharpness (float): Sharpness factor.
                        0.0 = very blurry
                        1.0 = original
                        >1.0 = more sharp
        blur (float): Blur radius for GaussianBlur.
                    0.0 = no blur
                    higher values = stronger blur
        save_path (str, optional): If given, saves the edited image.

    Returns:
        PIL.Image.Image: The edited image.
    """
    img = Image.open(image_path).convert("RGB")
    # Blur
    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    if save_path:
        img.save(save_path)
    return img


