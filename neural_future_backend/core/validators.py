# validators.py
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from PIL import Image, UnidentifiedImageError


@deconstructible
class SVGOrRasterImageValidator:
    """
    • Разрешает SVG-файлы (image/svg+xml).
    • Для остальных — пытается открыть через Pillow, чтобы убедиться,
      что это реальное растровое изображение.
    """

    allowed_extensions = ("svg", "png", "jpg", "jpeg", "gif", "webp")

    def __call__(self, file_obj):
        ext = file_obj.name.lower().split(".")[-1]
        if ext == "svg":
            # SVG-файл пропускаем без проверки Pillow
            return
        if ext not in self.allowed_extensions:
            raise ValidationError("Неподдерживаемый формат файла.")
        try:
            # Pillow читает только растровые, SVG вызовет ошибку
            Image.open(file_obj).verify()
        except UnidentifiedImageError:
            raise ValidationError("Файл не является валидным изображением.")
