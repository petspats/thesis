from pyha.common.const import Const
from pyha.common.sfix import Sfix, resize, fixed_truncate
from pyha.common.hwsim import HW
import numpy as np
from pyha.simulation.simulation_interface import debug_assert_sim_match, SIM_GATE, plot_assert_sim_match, SIM_MODEL, \
    SIM_HW_MODEL, SIM_RTL
import matplotlib.pyplot as plt


class Counter(HW):
    def __init__(self):
        self.acc = 0

    def main(self, x):
        self.acc = self.acc + 1
        return self.acc


class TwoCounters(HW):
    def __init__(self):
        self.counters = [Counter(), Counter()]

    def main(self, x):
        first = self.counters[0].main(x)
        second = self.counters[1].main(x)
        return first, second


def test_two_counters():
    dut = TwoCounters()
    x = [int(x) for x in np.random.uniform(-5, 5, 64)]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')


def test_counter():
    dut = Counter()
    x = [int(x) for x in np.random.uniform(-5, 5, 64)]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    print(r)


class Accumulator(HW):
    def __init__(self):
        self.acc = Sfix(0.0, left=0)

    def main(self, x):
        self.acc = self.acc + x
        return self.acc


def test_accum():
    dut = Accumulator()
    x = [x for x in np.random.uniform(-5, 5, 64)]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    print(r)


class TwoAccumulators(HW):
    def __init__(self):
        self.accs = [Accumulator(), Accumulator()]

    def main(self, x):
        y0 = self.accs[0].main(x)
        y1 = self.accs[1].main(x)
        return y0, y1


def test_two_acc():
    dut = TwoAccumulators()
    x = [int(x) for x in np.random.uniform(-5, 5, 64)]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    print(r)


class Acc(HW):
    def __init__(self):
        self.acc = 0

    def main(self, x):
        self.acc = self.acc + x
        return self.acc

    def model_main(self, xl):
        return np.cumsum(xl)


def test_acc():
    dut = Acc()
    x = [int(x) for x in np.random.uniform(-5, 5, 64)]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 1.5))
    # plt.plot(x, label='x')
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')
    plt.legend(loc='upper right')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.savefig('img/acc_sim_delay_tmp.png', bbox_inches='tight')
    plt.show()

    dut._delay = 1
    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL],
                               dir_path='/home/gaspar/git/thesis/playground')

    plt.figure(figsize=(8, 1.5))
    # plt.plot(x, label='x')
    plt.plot(r[0], label='y: Model')
    plt.plot(r[1], label='y: Pyha')
    plt.plot(r[2], label='y: RTL')
    plt.plot(r[2], label='y: GATE')
    plt.legend(loc='upper right')

    plt.grid()
    plt.xlabel("Sample number")
    plt.ylabel("Value")
    plt.savefig('img/acc_sim_tmp.png', bbox_inches='tight')
    plt.show()

    print(r)


class LastAcc(HW):
    def __init__(self):
        # registers
        self.shr = [0, 0, 0, 0]
        self.sum = 0

        # module delay
        self._delay = 1

    def main(self, x):
        # add new element to shift register
        self.next.shr = [x] + self.shr[:-1]

        for a in self.shr:
            self.next.sum = self.sum + a

        return self.sum

    def model_main(self, xl):
        return np.cumsum(xl)


def test_lastacc():
    dut = LastAcc()
    x = [1, 2, 3, 4, 5, 6]

    r = debug_assert_sim_match(dut, None, x,
                               simulations=[SIM_MODEL, SIM_HW_MODEL, SIM_RTL, SIM_GATE],
                               dir_path='/home/gaspar/git/thesis/playground')

    # plt.figure(figsize=(8, 3))
    # plt.plot(r[0], label='Model')
    # plt.plot(r[1], label='Python simulation')
    # plt.plot(r[2], label='RTL simulation')
    # plt.plot(r[3], label='Quartus GATE simulation')
    #
    # plt.grid()
    # plt.xlabel("Sample number")
    # plt.ylabel("Value")
    # plt.legend()
    # plt.savefig('img/comb_sim.png', bbox_inches='tight')
    # plt.show()

    print(r)
