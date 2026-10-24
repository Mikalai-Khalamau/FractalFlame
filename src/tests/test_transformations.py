import math

from transformations import TRANSFORMATIONS

EPS = 1e-6
PRECISION = 1e-8


class TestTransformations:
    """Числовые тесты трансформаций."""

    def test_linear(self) -> None:
        """Линейная."""
        x, y = 1.5, -2.3
        rx, ry = TRANSFORMATIONS["linear"](x, y)
        assert abs(rx - 1.5) < EPS
        assert abs(ry - (-2.3)) < EPS

    def test_sinusoidal_zero(self) -> None:
        """Синус."""
        rx, ry = TRANSFORMATIONS["sinusoidal"](0.0, 0.0)
        assert abs(rx - 0.0) < EPS
        assert abs(ry - 0.0) < EPS

    def test_sinusoidal_pi_over_2(self) -> None:
        """Синус с pi/2."""
        x = y = math.pi / 2
        rx, ry = TRANSFORMATIONS["sinusoidal"](x, y)
        assert abs(rx - 1.0) < EPS
        assert abs(ry - 1.0) < EPS

    def test_spherical(self) -> None:
        """Сферическая."""
        rx, ry = TRANSFORMATIONS["spherical"](1.0, 2.0)
        assert abs(rx - 0.19999999996) < PRECISION
        assert abs(ry - 0.39999999992) < PRECISION

    def test_swirl(self) -> None:
        """Вихревая."""
        rx, ry = TRANSFORMATIONS["swirl"](0.5, -0.3)
        assert abs(rx - 0.44956994610024226) < PRECISION
        assert abs(ry - 0.37133120467235886) < PRECISION

    def test_horseshoe(self) -> None:
        """Подкова."""
        rx, ry = TRANSFORMATIONS["horseshoe"](1.0, 0.5)
        assert abs(rx - 0.6708203926499369) < PRECISION
        assert abs(ry - 0.8944271901999158) < PRECISION

    def test_polar(self) -> None:
        """Полярные."""
        rx, ry = TRANSFORMATIONS["polar"](1.0, 1.0)
        assert abs(rx - 0.25) < PRECISION
        assert abs(ry - 0.41421356337309523) < PRECISION

    def test_handkerchief(self) -> None:
        """Платок."""
        rx, ry = TRANSFORMATIONS["handkerchief"](-0.7, 0.4)
        assert abs(rx - (-0.22828493535782732)) < PRECISION
        assert abs(ry - (-0.19588711657032665)) < PRECISION

    def test_heart(self) -> None:
        """Сердце."""
        rx, ry = TRANSFORMATIONS["heart"](0.3, -0.8)
        assert abs(rx - (-0.7349087712722076)) < PRECISION
        assert abs(ry - (-0.4357856119882517)) < PRECISION

    def test_disc(self) -> None:
        """Дискообразная."""
        rx, ry = TRANSFORMATIONS["disc"](0.4, 0.2)
        assert abs(rx - 0.1455589369838061) < PRECISION
        assert abs(ry - 0.02436226719608926) < PRECISION

    def test_fisheye(self) -> None:
        """Рыбий глаз."""
        rx, ry = TRANSFORMATIONS["fisheye"](1.0, -0.5)
        assert abs(rx - (-0.472135954776667)) < PRECISION
        assert abs(ry - 0.944271909553334) < PRECISION

    def test_tangent(self) -> None:
        """Тангенциальная."""
        rx, ry = TRANSFORMATIONS["tan"](0.3, 0.7)
        assert abs(rx - 0.38638063013257673) < PRECISION
        assert abs(ry - 0.6107259643892086) < PRECISION

    def test_cross(self) -> None:
        """Крест."""
        rx, ry = TRANSFORMATIONS["cross"](1.5, 0.5)
        assert abs(rx - 0.75) < PRECISION
        assert abs(ry - 0.25) < PRECISION

    def test_all_transformations_exist(self) -> None:
        """Доступность всех трансформаций."""
        expected = {
            "linear",
            "sinusoidal",
            "spherical",
            "swirl",
            "horseshoe",
            "polar",
            "handkerchief",
            "heart",
            "disc",
            "fisheye",
            "tan",
            "cross",
        }
        actual = set(TRANSFORMATIONS.keys())
        assert expected == actual
