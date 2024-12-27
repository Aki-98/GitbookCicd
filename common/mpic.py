from PIL import Image


def compress_jpg(input_image_path, output_image_path, quality):
    from common.mlogger import global_logger

    try:
        with Image.open(input_image_path) as img:
            # Remove all metadata
            img_no_exif = img.copy()
            img_no_exif.info.clear()  # Clear all additional information
            # Compress and save the image
            img_no_exif.save(
                output_image_path,
                "JPEG",
                quality=quality,
                optimize=True,
                subsampling=2,  # Set chroma subsampling
            )
    except Exception as e:
        global_logger.error(
            f"Error compressing JPG/JPEG: {input_image_path}, error: {e}"
        )


def compress_png(input_image_path, output_image_path):
    from common.mlogger import global_logger

    try:
        with Image.open(input_image_path) as img:
            # Convert to palette mode and enable optimization
            img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            img.save(output_image_path, format="PNG", optimize=True)
            global_logger.debug(
                f"PNG compression completed (palette mode): {output_image_path}"
            )
    except Exception as e:
        global_logger.error(f"Error compressing PNG file: {e}")
