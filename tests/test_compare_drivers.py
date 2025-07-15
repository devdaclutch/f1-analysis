import numpy as np
import pandas as pd


def compute_delta(distance, speed1, speed2):
    """Replicates the delta time computation from compare_drivers.py."""
    speed1_ms = speed1 / 3.6
    speed2_ms = speed2 / 3.6
    dist_step = np.gradient(distance)
    return np.cumsum(dist_step * (1 / speed1_ms - 1 / speed2_ms))


def test_constant_speed_delta():
    common_distance = np.linspace(0, 4, 5)
    speed1 = np.full_like(common_distance, 10.0)
    speed2 = np.full_like(common_distance, 12.0)
    delta = compute_delta(common_distance, speed1, speed2)
    expected = np.array([0.06, 0.12, 0.18, 0.24, 0.30])
    assert np.allclose(delta, expected, atol=1e-8)


def test_interpolation_nearest():
    tel = pd.DataFrame({"Distance": [0, 2, 4], "Speed": [10, 20, 30]})
    common_distance = np.linspace(0, 4, 5)
    interp = tel.set_index("Distance").reindex(common_distance, method="nearest").interpolate()
    expected = [10, 20, 20, 30, 30]
    assert np.allclose(interp["Speed"].values, expected)
