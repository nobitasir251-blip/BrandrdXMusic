import os
import textwrap
import aiohttp

from PIL import Image, ImageDraw, ImageFont, ImageFilter

THUMB_DIR = "cache/thumbnails"
FONT_FILE = "cache/font.ttf"
LOGO_FILE = "cache/logo.png"

os.makedirs(THUMB_DIR, exist_ok=True)


async def download_image(url: str, path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(path, "wb") as f:
                    f.write(await resp.read())
                return path
    return None


async def gen_thumb(
    videoid: str,
    title: str,
    user_name: str,
    duration: str,
    views: str = "Unknown",
    channel: str = "YouTube",
):
    thumb_url = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"

    background = f"{THUMB_DIR}/{videoid}_bg.jpg"
    final = f"{THUMB_DIR}/{videoid}.png"

    await download_image(thumb_url, background)

    if not os.path.isfile(background):
        thumb_url = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
        await download_image(thumb_url, background)

    image = Image.open(background).convert("RGB")
    image = image.resize((1280, 720))

    # Blur Effect
    blur = image.filter(ImageFilter.GaussianBlur(8))

    # Dark Overlay
    overlay = Image.new("RGBA", blur.size, (0, 0, 0, 120))
    blur = Image.alpha_composite(blur.convert("RGBA"), overlay)

    # Main Thumbnail
    thumb = Image.open(background).convert("RGB")
    thumb = thumb.resize((500, 300))

    # Rounded Corners
    mask = Image.new("L", thumb.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle(
        [(0, 0), thumb.size],
        radius=40,
        fill=255,
    )
    thumb.putalpha(mask)

    blur.paste(thumb, (60, 180), thumb)

    draw = ImageDraw.Draw(blur)

    # Fonts
    try:
        title_font = ImageFont.truetype(FONT_FILE, 45)
        small_font = ImageFont.truetype(FONT_FILE, 30)
        tiny_font = ImageFont.truetype(FONT_FILE, 24)
    except:
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        tiny_font = ImageFont.load_default()

    # Title Wrap
    title = textwrap.fill(title, width=28)

    # Title
    draw.text(
        (620, 190),
        title,
        font=title_font,
        fill="white",
    )

    # Requested By
    draw.text(
        (620, 400),
        f"Requested By : {user_name}",
        font=small_font,
        fill="#00FFCC",
    )

    # Duration
    draw.text(
        (620, 455),
        f"Duration : {duration}",
        font=small_font,
        fill="#FFFFFF",
    )

    # Views
    draw.text(
        (620, 510),
        f"Views : {views}",
        font=small_font,
        fill="#FFFFFF",
    )

    # Channel
    draw.text(
        (620, 565),
        f"Channel : {channel}",
        font=small_font,
        fill="#FFFFFF",
    )

    # Bottom Line
    draw.rounded_rectangle(
        [(50, 650), (1230, 665)],
        radius=20,
        fill="#00FFCC",
    )

    # Playing Text
    draw.text(
        (70, 610),
        "NOW PLAYING",
        font=small_font,
        fill="#00FFCC",
    )

    # Add Logo
    if os.path.isfile(LOGO_FILE):
        logo = Image.open(LOGO_FILE).convert("RGBA")
        logo = logo.resize((120, 120))

        mask = Image.new("L", logo.size, 0)
        draw_logo = ImageDraw.Draw(mask)
        draw_logo.ellipse((0, 0, 120, 120), fill=255)

        logo.putalpha(mask)

        blur.paste(logo, (1100, 30), logo)

    blur = blur.convert("RGB")
    blur.save(final, quality=95)

    if os.path.exists(background):
        os.remove(background)

    return final
