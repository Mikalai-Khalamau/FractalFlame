import json
from typing import Any
from unittest.mock import patch

from main import load_json_config, main

EXPECTED_ERROR_CODE = 2
EXPECTED_SUCCESS_CODE = 0


class TestLoadJsonConfig:
    """Тесты загрузки json."""

    def test_load_json_config_empty_path(self) -> None:
        """Пустой путь - пустой словарь."""
        result = load_json_config("")
        assert result == {}

    def test_load_json_config_none(self) -> None:
        """Нет пути - пустой словарь."""
        result = load_json_config(None)
        assert result == {}

    def test_load_json_config_valid_json(self, tmp_path: Any) -> None:
        """Загрузка валидного json."""
        config_file = tmp_path / "config.json"
        config_data = {"size": {"width": 800, "height": 600}, "seed": 42}
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

        with patch("main.logger"):
            result = load_json_config(str(config_file))
            assert result == config_data


class TestMain:
    """Тесты main."""

    @patch("main.parse_args")
    def test_main_file_not_found(self, mock_parse_args: Any) -> None:
        """FileNotFoundError."""
        mock_parse_args.side_effect = FileNotFoundError("config not found")

        with patch("main.logger"):
            result = main()

        assert result == EXPECTED_ERROR_CODE
