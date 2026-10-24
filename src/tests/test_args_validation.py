import pytest

from args_validation import (
    _validate_color,
    _validate_functions,
    _validate_positive_integer,
    validate_config,
)

TEST_PARAM = "test_param"
VALID_COLOR = (255, 128, 0)
INVALID_COLOR_HIGH = (256, 128, 0)
INVALID_COLOR_SHORT = (255, 128)
VALID_WIDTH = 800
VALID_HEIGHT = 600
VALID_ITERATIONS = 1000000
VALID_THREADS = 4


class TestValidatePositiveInteger:
    """Тесты валидации чисел."""

    def test_valid_positive_integer(self) -> None:
        """Валидное число."""
        _validate_positive_integer(TEST_PARAM, 100)

    def test_zero_is_invalid(self) -> None:
        """Ноль - невалидно."""
        with pytest.raises(ValueError, match="должна быть положительным"):
            _validate_positive_integer(TEST_PARAM, 0)

    def test_negative_is_invalid(self) -> None:
        """Отрицательное число - невалидно."""
        with pytest.raises(ValueError, match="должна быть положительным"):
            _validate_positive_integer(TEST_PARAM, -5)


class TestValidateColor:
    """Тесты валидации цветов."""

    def test_valid_color(self) -> None:
        """Валидный RGB цвет."""
        _validate_color(VALID_COLOR)

    def test_invalid_color_range(self) -> None:
        """Значение вне диапазона."""
        with pytest.raises(ValueError, match="диапазоне"):
            _validate_color(INVALID_COLOR_HIGH)

    def test_invalid_color_length(self) -> None:
        """Неправильное количество компонент."""
        with pytest.raises(ValueError, match="три компоненты"):
            _validate_color(INVALID_COLOR_SHORT)


class TestValidateFunctions:
    """Тесты валидации трансформаций."""

    def test_valid_functions(self) -> None:
        """Валидные функции."""
        _validate_functions({"swirl": 1.0, "horseshoe": 0.8})

    def test_invalid_function_name(self) -> None:
        """Несуществующая функция."""
        with pytest.raises(ValueError, match="не существует"):
            _validate_functions({"nonexistent": 1.0})

    def test_invalid_weight_zero(self) -> None:
        """Вес 0 невалиден."""
        with pytest.raises(ValueError, match="положительным"):
            _validate_functions({"swirl": 0.0})

    def test_invalid_weight_negative(self) -> None:
        """Отрицательный вес невалиден."""
        with pytest.raises(ValueError, match="положительным"):
            _validate_functions({"swirl": -1.0})


class TestValidateConfig:
    """Тесты валидации конфига."""

    def test_valid_config(self) -> None:
        """Валидная конфигурация."""
        config = {
            "width": VALID_WIDTH,
            "height": VALID_HEIGHT,
            "iteration_count": VALID_ITERATIONS,
            "threads": VALID_THREADS,
            "output_path": "test.png",
            "functions": {"swirl": 1.0},
            "affine_params": [
                {
                    "a": 0.5,
                    "b": 0,
                    "c": 0,
                    "d": 0,
                    "e": 0.5,
                    "f": 0,
                    "color": (255, 100, 100),
                }
            ],
        }
        validate_config(config)

    def test_invalid_width(self) -> None:
        """Невалидная ширина."""
        config = {
            "width": -100,
            "height": VALID_HEIGHT,
            "iteration_count": VALID_ITERATIONS,
            "threads": VALID_THREADS,
            "output_path": "test.png",
            "functions": {"swirl": 1.0},
            "affine_params": [],
        }
        with pytest.raises(ValueError, match="положительным"):
            validate_config(config)
