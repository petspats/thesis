from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate, fixed_wrap
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class MAC(HW):
    def __init__(self, coef):
        self.coef = Sfix(coef, 0, -17)
        self.y = Sfix(left=1, round_style=fixed_truncate, overflow_style=fixed_wrap)

        self._delay = 1

    def main(self, x, sum_in):
        mul = self.coef * x
        self.next.y = sum_in + mul
        return self.y

    def model_main(self, sample_in, sum_in):
        muls = np.array(sample_in) * float(self.coef)
        sums = muls + sum_in
        return sums


def test_seq():
    dut = MAC(0.658)
    x = [0.1, -0.6, 0.3, 0.4, -0.5, 0.1]
    sum_in = [0.9, -0.43, 0.2, 0.67, -0.12, -0.5]

    r = debug_assert_sim_match(dut, None, x, sum_in,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 3))
    plt.plot(r[0], label='Model')
    plt.plot(r[1], label='Python simulation')
    # plt.plot(r[2], label='RTL simulation')
    # plt.plot(r[3], label='Quartus GATE simulation')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig('img/mac_fixed.png', bbox_inches='tight')
    plt.show()

    print(r)


class MAC_comb(HW):
    def __init__(self, coef):
        self.coef = coef
        self.acc = 0.0

        self._delay = 1

    def main(self, x, coef):
        mul = x * coef
        self.acc = self.acc + mul
        return self.acc

    def model_main(self, xl, hl):

        y = []
        acc = 0.0
        for x, h in zip(xl, hl):
            mul = x * h
            acc = acc + mul
            y.append(acc)

        return y

    def model_main(self, xl, hl):
        return np.cumsum(np.array(xl) * np.array(hl))


def test_comb():
    dut = MAC_comb(0.658)
    x = [0.1, -0.6, 0.3, 0.4, -0.5, 0.1]
    sum_in = [0.9, -0.43, 0.2, 0.67, -0.12, -0.5]

    r = debug_assert_sim_match(dut, None, x, sum_in,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 3))
    plt.plot(r[0], label='Model')
    plt.plot(r[1], label='Python simulation')
    # plt.plot(r[2], label='RTL simulation')
    # plt.plot(r[3], label='Quartus GATE simulation')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.legend()
    # plt.savefig('img/mac_fixed.png', bbox_inches='tight')
    plt.show()

    print(r)
