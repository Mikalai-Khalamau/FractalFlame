from pathlib import Path

import numpy as np

from flame_generator import FlameGenerator

WIDTH = 800
HEIGHT = 600
ITERATIONS = 1000
SEED = 42
DEFAULT_THREADS = 1
SMALL_WIDTH = 100
SMALL_HEIGHT = 100
SMALL_ITERATIONS = 100
VALID_THREADS = 4


class TestFlameGeneratorInit:
    """Тесты инициализации генератора."""

    def test_init(self) -> None:
        """Инициализация с параметрами."""
        gen = FlameGenerator(WIDTH, HEIGHT, ITERATIONS, SEED)
        assert gen.width == WIDTH
        assert gen.height == HEIGHT
        assert gen.iterations == ITERATIONS
        assert gen.seed == SEED
        assert gen.threads == DEFAULT_THREADS

    def test_init_default_threads(self) -> None:
        """Количество потоков по умолчанию - 1."""
        gen = FlameGenerator(SMALL_WIDTH, SMALL_HEIGHT, SMALL_ITERATIONS, SEED)
        assert gen.threads == DEFAULT_THREADS


class TestSetThreads:
    """Тесты установки количества потоков."""

    def test_set_threads_valid(self) -> None:
        """Установка валидного количества потоков."""
        gen = FlameGenerator(SMALL_WIDTH, SMALL_HEIGHT, SMALL_ITERATIONS, SEED)
        gen.set_threads(VALID_THREADS)
        assert gen.threads == VALID_THREADS

    def test_set_threads_zero_becomes_one(self) -> None:
        """0 потоков становится 1."""
        gen = FlameGenerator(SMALL_WIDTH, SMALL_HEIGHT, SMALL_ITERATIONS, SEED)
        gen.set_threads(0)
        assert gen.threads == 1

    def test_set_threads_negative_becomes_one(self) -> None:
        """Отрицательное число становится 1."""
        gen = FlameGenerator(SMALL_WIDTH, SMALL_HEIGHT, SMALL_ITERATIONS, SEED)
        gen.set_threads(-5)
        assert gen.threads == 1

    def test_set_threads_capped_by_cpu_count(self) -> None:
        """Потоки ограничены количеством ядер."""
        from multiprocessing import cpu_count

        gen = FlameGenerator(SMALL_WIDTH, SMALL_HEIGHT, SMALL_ITERATIONS, SEED)
        gen.set_threads(1000)
        assert gen.threads <= cpu_count()


class TestProcessHistograms:
    """Тесты создания гистограмм."""

    def test_process_histograms_output_range(self) -> None:
        """Интенсивность в диапазоне [0, 1]."""
        gen = FlameGenerator(SMALL_WIDTH, SMALL_HEIGHT, SMALL_ITERATIONS, SEED)
        hist_freq = np.random.default_rng().random((SMALL_WIDTH, SMALL_HEIGHT)) * 100
        intensity = gen._process_histograms(hist_freq)
        assert np.all(intensity >= 0)
        assert np.all(intensity <= 1)

    def test_process_histograms_empty(self) -> None:
        """Пустая гистограмма."""
        gen = FlameGenerator(SMALL_WIDTH, SMALL_HEIGHT, SMALL_ITERATIONS, SEED)
        hist_freq = np.zeros((SMALL_WIDTH, SMALL_HEIGHT))
        intensity = gen._process_histograms(hist_freq)
        assert np.allclose(intensity, 0)


class TestGenerate:
    """Тесты генерации."""

    def test_generate_single_thread(
        self,
        temp_png_path: str,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
    ) -> None:
        """Генерация с 1 потоком."""
        gen = FlameGenerator(200, 150, 10000, SEED)
        gen.set_threads(1)
        gen.generate(
            standard_affine_transforms, standard_function_weights, temp_png_path
        )
        assert Path(temp_png_path).exists()
        assert Path(temp_png_path).stat().st_size > 0

    def test_generate_multiple_threads(
        self,
        temp_png_path: str,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
    ) -> None:
        """Генерация с 4 потоками."""
        gen = FlameGenerator(200, 150, 10000, SEED)
        gen.set_threads(VALID_THREADS)
        gen.generate(
            standard_affine_transforms, standard_function_weights, temp_png_path
        )
        assert Path(temp_png_path).exists()
        assert Path(temp_png_path).stat().st_size > 0
