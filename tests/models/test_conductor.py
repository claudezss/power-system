from pyohm.models.conductor import Conductor
import pytest


def test_conductor():
    conductor = Conductor()

    conductor.use_default()

    assert conductor.t_film == 70.0

    assert conductor.number_of_day == 161

    assert conductor.p_f == pytest.approx(1.029, abs=0.01)

    assert conductor.u_f == pytest.approx(2.043e-5, abs=1e-7)

    assert conductor.k_f == pytest.approx(0.02945, abs=0.00001)

    assert conductor.N_Re == pytest.approx(865, abs=1)

    assert conductor.q_cn == pytest.approx(42.42, abs=0.01)

    assert conductor.q_c == pytest.approx(101.14, abs=0.01)

    assert conductor.q_r == pytest.approx(39.11, abs=0.01)

    assert conductor.q_s == pytest.approx(22.45, abs=0.01)
