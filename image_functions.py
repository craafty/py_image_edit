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

def adjust_stretch(img, stretch_hor, stretch_vert):
    w, h = img.size
    img = img.resize(
        (int(w * stretch_hor), int(h * stretch_vert)),
        Image.LANCZOS
    )
    return img

def adjust_flip(img, flip_hor, flip_vert):
    if flip_hor:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if flip_vert:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
    return img
