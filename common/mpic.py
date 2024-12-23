from PIL import Image


def compress_jpg(input_image_path, output_image_path, quality):
    try:
        with Image.open(input_image_path) as img:
            # 删除所有元数据
            img_no_exif = img.copy()
            img_no_exif.info.clear()  # 清除所有附加信息
            # 压缩并保存图片
            img_no_exif.save(
                output_image_path,
                "JPEG",
                quality=quality,
                optimize=True,
                subsampling=2,  # 设置色度采样
            )
    except Exception as e:
        global_logger.error(f"compressing jpg/jpeg: {input_image_path} error: {e}")


def compress_png(input_image_path, output_image_path):
    try:
        with Image.open(input_image_path) as img:
            # 转为调色板模式并启用优化
            img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            img.save(output_image_path, format="PNG", optimize=True)
            global_logger.debug(f"PNG 压缩完成（调色板模式）: {output_image_path}")
    except Exception as e:
        global_logger.error(f"压缩 PNG 文件时出错: {e}")
