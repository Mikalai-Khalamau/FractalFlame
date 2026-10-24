import argparse

import pytest

from args_parse import merge_config, parse_affine_params, parse_functions

VALID_WEIGHT = 1.0
VALID_WEIGHT_2 = 0.8
AFFINE_SCALE = 0.5
AFFINE_SCALE_IDENTITY = 1.0
TEST_WIDTH = 1024
TEST_HEIGHT = 768
TEST_WIDTH_JSON = 800
TEST_HEIGHT_JSON = 600
AFFINE_COUNT_SINGLE = 1
AFFINE_COUNT_MULTIPLE = 2


class TestParseFunctions:
    """Тесты парсинга."""

    def test_parse_single_function(self) -> None:
        """Парсинг одной функции."""
        result = parse_functions("swirl:1.0")
        assert result == {"swirl": 1.0}

    def test_parse_multiple_functions(self) -> None:
        """Парсинг нескольких функций."""
        result = parse_functions("swirl:1.0,horseshoe:0.8")
        assert result == {"swirl": 1.0, "horseshoe": 0.8}

    def test_parse_functions_with_spaces(self) -> None:
        """Парсинг пробелов."""
        result = parse_functions("swirl: 1.0 , horseshoe: 0.8")
        assert result == {"swirl": 1.0, "horseshoe": 0.8}

    def test_parse_functions_empty(self) -> None:
        """Парсинг пустой строки."""
        result = parse_functions(None)
        assert result == {}

    def test_parse_functions_invalid_format(self) -> None:
        """Невалидный формат."""
        with pytest.raises(ValueError):
            parse_functions("swirl_1.0")

    def test_parse_functions_invalid_weight(self) -> None:
        """Невалидный вес."""
        with pytest.raises(ValueError):
            parse_functions("swirl:abc")


class TestParseAffineParams:
    """Парсинг афинных преобразований."""

    def test_parse_single_affine(self) -> None:
        """Парсинг одного преобразования."""
        result = parse_affine_params("0.5,0,0,0,0.5,0")
        assert len(result) == AFFINE_COUNT_SINGLE
        assert result[0]["a"] == AFFINE_SCALE
        assert result[0]["e"] == AFFINE_SCALE

    def test_parse_multiple_affines(self) -> None:
        """Несколько преобразований."""
        result = parse_affine_params("0.5,0,0,0,0.5,0/1,0,0,0,1,0")
        assert len(result) == AFFINE_COUNT_MULTIPLE
        assert result[0]["a"] == AFFINE_SCALE
        assert result[1]["a"] == AFFINE_SCALE_IDENTITY

    def test_parse_affine_invalid_count(self) -> None:
        """Не хватает параметров."""
        with pytest.raises(ValueError):
            parse_affine_params("0.5,0,0,0")

    def test_parse_affine_invalid_values(self) -> None:
        """Невалидные параметры."""
        with pytest.raises(ValueError):
            parse_affine_params("a,b,c,d,e,f")


class TestMergeConfig:
    """Тесты слияния входных параметров."""

    def test_merge_cli_overrides_defaults(self) -> None:
        """CLI перезаписывает базовые."""
        cli_args = argparse.Namespace(
            width=TEST_WIDTH,
            height=TEST_HEIGHT,
            iteration_count=5000000,
            seed=123,
            output_path="test.png",
            threads=4,
            functions=None,
            affine_params=None,
            config=None,
        )
        result = merge_config(cli_args, {})
        assert result["width"] == TEST_WIDTH
        assert result["height"] == TEST_HEIGHT

    def test_merge_json_config(self) -> None:
        """Json."""
        json_config = {
            "size": {"width": TEST_WIDTH_JSON, "height": TEST_HEIGHT_JSON},
            "iteration_count": 1000000,
        }
        cli_args = argparse.Namespace(
            width=None,
            height=None,
            iteration_count=None,
            seed=None,
            output_path=None,
            threads=None,
            functions=None,
            affine_params=None,
            config=None,
        )
        result = merge_config(cli_args, json_config)
        assert result["width"] == TEST_WIDTH_JSON
        assert result["height"] == TEST_HEIGHT_JSON
