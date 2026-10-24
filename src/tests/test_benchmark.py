from typing import Any

import pytest

from flame_generator import FlameGenerator


class TestBenchmark:
    """Бенчмарк тесты для замера производительности."""

    @pytest.mark.benchmark(group="flame_generation")
    def test_single_thread_performance(
        self,
        benchmark: Any,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
        temp_png_path: str,
    ) -> None:
        """1 поток."""
        gen = FlameGenerator(400, 300, 1000000, 42)
        gen.set_threads(1)
        benchmark(
            gen.generate,
            standard_affine_transforms,
            standard_function_weights,
            temp_png_path,
        )

    @pytest.mark.benchmark(group="flame_generation")
    def test_two_threads_performance(
        self,
        benchmark: Any,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
        temp_png_path: str,
    ) -> None:
        """2 потока."""
        gen = FlameGenerator(400, 300, 1000000, 42)
        gen.set_threads(2)
        benchmark(
            gen.generate,
            standard_affine_transforms,
            standard_function_weights,
            temp_png_path,
        )

    @pytest.mark.benchmark(group="flame_generation")
    def test_four_threads_performance(
        self,
        benchmark: Any,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
        temp_png_path: str,
    ) -> None:
        """4 потока."""
        gen = FlameGenerator(400, 300, 1000000, 42)
        gen.set_threads(4)
        benchmark(
            gen.generate,
            standard_affine_transforms,
            standard_function_weights,
            temp_png_path,
        )

    @pytest.mark.benchmark(group="flame_generation")
    def test_eight_threads_performance(
        self,
        benchmark: Any,
        standard_affine_transforms: list[dict],
        standard_function_weights: dict[str, float],
        temp_png_path: str,
    ) -> None:
        """8 потоков."""
        gen = FlameGenerator(400, 300, 1000000, 42)
        gen.set_threads(8)
        benchmark(
            gen.generate,
            standard_affine_transforms,
            standard_function_weights,
            temp_png_path,
        )
