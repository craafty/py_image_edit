from PIL import Image, ImageEnhance, ImageFilter

def rotate_image(img, degrees=90):
    return img.rotate(degrees, expand=True)

def flip_image(img, mode="horizontal"):
    if mode == "horizontal":
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == "vertical":
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("Mode must be 'horizontal' or 'vertical'")

def adjust_rgb(img, r_factor=1.0, g_factor=1.0, b_factor=1.0):
    r, g, b = img.split()
    r = r.point(lambda i: min(255, i * r_factor))
    g = g.point(lambda i: min(255, i * g_factor))
    b = b.point(lambda i: min(255, i * b_factor))
    return Image.merge("RGB", (r, g, b))

def adjust_saturation(img, factor=1.0):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)

def adjust_brightness(img, brightness=1.0):
    img = ImageEnhance.Brightness(img).enhance(brightness)
    return img

def adjust_sharpness(img, sharpness=1.0):
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img

def adjust_blur(img, blur=0.0):
    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    return img

def stretch_image(img, width_factor=1.0, height_factor=1.0):
    """
    Stretches (scales) the given PIL.Image.Image horizontally and/or vertically.
    Parameters:
        img (PIL.Image.Image): Input image.
        width_factor (float): Scaling factor for width. 1.0 = original width.
        height_factor (float): Scaling factor for height. 1.0 = original height.
    Returns:
        PIL.Image.Image: The stretched image.
    """
    if width_factor <= 0 or height_factor <= 0:
        raise ValueError("Scaling factors must be positive numbers.")
    
    orig_width, orig_height = img.size
    new_width = int(orig_width * width_factor)
    new_height = int(orig_height * height_factor)
    
    stretched_img = img.resize((new_width, new_height), Image.LANCZOS)
    return stretched_img
