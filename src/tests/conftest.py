import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def temp_png_path() -> Generator[str, Any, None]:
    """Путь для png."""
    with tempfile.TemporaryDirectory() as tmpdir:
        png_path = Path(tmpdir) / "test_output.png"
        yield str(png_path)


@pytest.fixture
def standard_affine_transforms() -> list[dict]:
    """Базовые афинные преобразования."""
    return [
        {
            "a": 0.5,
            "b": 0.0,
            "c": -0.5,
            "d": 0.0,
            "e": 0.5,
            "f": 0.0,
            "color": (255, 100, 100),
        },
        {
            "a": 0.5,
            "b": 0.0,
            "c": 0.5,
            "d": 0.0,
            "e": 0.5,
            "f": 0.0,
            "color": (100, 100, 255),
        },
    ]


@pytest.fixture
def standard_function_weights() -> dict[str, float]:
    """Базовые трансформации."""
    return {
        "swirl": 1.0,
        "horseshoe": 0.8,
    }
