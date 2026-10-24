from pathlib import Path

from PIL import Image

from flame_generator import FlameGenerator


class TestIntegration:
    """Интеграционные тесты."""

    def test_end_to_end_generation(
        self,
        temp_png_path: str,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
    ) -> None:
        """Генерируем изображения и проверяем размеры."""
        gen = FlameGenerator(320, 240, 50000, 42)
        gen.set_threads(1)
        gen.generate(
            standard_affine_transforms, standard_function_weights, temp_png_path
        )

        assert Path(temp_png_path).exists()
        img = Image.open(temp_png_path)
        assert img.size == (320, 240)
        assert img.mode == "RGB"

    def test_multithread_same_size(
        self,
        temp_png_path: str,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
    ) -> None:
        """Сверяем много и одно поточные версии."""
        gen1 = FlameGenerator(200, 150, 50000, 42)
        gen1.set_threads(1)
        path1 = temp_png_path.replace(".png", "_single.png")
        gen1.generate(standard_affine_transforms, standard_function_weights, path1)

        gen2 = FlameGenerator(200, 150, 50000, 42)
        gen2.set_threads(4)
        path2 = temp_png_path.replace(".png", "_multi.png")
        gen2.generate(standard_affine_transforms, standard_function_weights, path2)

        img1 = Image.open(path1)
        img2 = Image.open(path2)
        assert img1.size == img2.size
        assert img1.mode == img2.mode == "RGB"
