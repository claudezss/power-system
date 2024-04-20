import pytest

from pyohm.models.conductor import Conductor


def test_conductor():
    conductor = Conductor()

    conductor.use_default()

    assert conductor.t_film == 70.0

    assert conductor.number_of_day == 161

    assert conductor.p_f == pytest.approx(1.029, abs=0.01)

    assert conductor.u_f == pytest.approx(2.043e-5, abs=1e-7)

    assert conductor.k_f == pytest.approx(0.02945, abs=0.00001)

    assert conductor.N_Re == pytest.approx(865, abs=1)

    assert conductor.H_c == pytest.approx(74.9, abs=0.1)

    assert conductor.Z_c == pytest.approx(114, abs=1)

    assert conductor.Q_s == pytest.approx(1027, abs=1)

    assert conductor.q_cn == pytest.approx(42.42, abs=0.01)

    assert conductor.q_c == pytest.approx(82.1, abs=0.1)

    assert conductor.q_r == pytest.approx(39.11, abs=0.01)

    assert conductor.q_s == pytest.approx(22.45, rel=0.2)

    assert conductor.R_avg == pytest.approx(9.391e-5, rel=0.01)

    assert conductor.I == pytest.approx(1025, abs=1.3)

    conductor.conductor_surface_temperature = 119.6

    assert conductor.I == pytest.approx(1200, abs=1)
