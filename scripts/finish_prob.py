# /usr/bin/python3

import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import *


def getProb():
    finish_cnt = sys.argv.count('完走')
    faild_cnt = sys.argv.count('失敗')
    if finish_cnt + faild_cnt != len(sys.argv)-1:
        raise ValueError("引数として、完走か失敗のみしか受け付けていません")
    return finish_cnt/(len(sys.argv)-1)


def plot(prob, data):
    plt.xlabel("データ", fontname='IPAGothic', fontsize=30)
    plt.ylabel("確率", fontname='IPAGothic', fontsize=30)
    plt.ylim(0.0, 1.0)
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(1))
    plt.plot(data, prob, lw=5, label="percentage of finishes")
    plt.tick_params(labelsize=20)
    plt.legend(loc="upper right", fontsize=15)
    plt.grid()
    plt.show()


def main():
    prob = [0]
    try:
        prob.append(getProb())
    except ValueError as e:
        print(e)
        exit(1)

    print("完走率:", prob[1])

    data = np.linspace(0, 1, 2)
    data = [1, 1]

    plot(prob, data)


if __name__ == '__main__':
    main()
