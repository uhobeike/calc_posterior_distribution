# /usr/bin/python3

import sys

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axisartist.axislines import SubplotZero

from statistics import stdev


def setUniformDistribution(step):
    return [1/step] * (step+1)


def getLikelihood(result, step):
    if result == "完走":
        return [1/step * i for i in range(step+1)]
    elif result == "失敗":
        return [1-(1/step * i) for i in range(step+1)]
    else:
        print("a")


def normalize(poster_dist):
    norm_const = 1/sum(poster_dist)
    return [(norm_const * i) for i in poster_dist]


def getPosteriorDistribution(likelihood, prior_dist):
    return [l*p for (l, p) in zip(likelihood, prior_dist)]


def plot(poster_dist, prob, step):
    prob_mean = sum([po*pr for (po, pr) in zip(poster_dist, prob)])
    prob_stdev = stdev([po*pr for (po, pr) in zip(poster_dist, prob)])*10
    prob_stdev_min = prob_mean - prob_stdev
    prob_stdev_max = prob_mean + prob_stdev
    if prob_stdev_min < 0:
        prob_stdev_min = 0
    if prob_stdev_max > 1:
        prob_stdev_max = 1

    fig = plt.figure()
    ax = SubplotZero(fig, 111)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 0.2)
    ax.bar(prob, poster_dist, width=1/step, edgecolor="black")
    ax.text(prob_mean - 0.02,
            np.max(poster_dist)*2.01, "平均", size=20)
    ax.plot([[prob_mean]for i in range(2)],
            [0, np.max(poster_dist)*2], lw=2, color="r")
    ax.fill_between([prob_stdev_min, prob_stdev_max],
                    [0, 0],
                    [np.max(poster_dist)*2, np.max(poster_dist)*2], alpha=0.2, color='red')
    ax.text(prob_mean-0.04, np.max(poster_dist)*1.51, "標準偏差", size=20)
    ax.annotate('',
                xy=[prob_stdev_min, np.max(poster_dist)*1.5],
                xytext=[prob_stdev_max, np.max(poster_dist)*1.5],
                arrowprops=dict(arrowstyle='<|-|>',
                                connectionstyle='arc3',
                                facecolor='C0',
                                edgecolor='C0'))

    for direction in ["right", "top"]:
        ax.axis[direction].set_visible(False)
    for direction in ["left",  "bottom"]:
        ax.axis[direction].set_axisline_style("-|>")
    ax.grid(which='major', color='black')
    ax.grid(which='minor', color='gray', linestyle='--')
    ax.tick_params(labelsize=30)
    ax.set_xlabel("完走率", fontname='IPAGothic', fontsize=50)
    ax.set_ylabel("確率", fontname='IPAGothic', fontsize=50)

    fig.add_subplot(ax)
    plt.show()


def main():
    step = 100
    prior_dist = []
    poster_dist = []
    likelihood = []

    prior_dist = setUniformDistribution(step)
    prob = [1/step * i for i in range(step+1)]

    for result in sys.argv[1:]:
        likelihood = getLikelihood(result, step)
        poster_dist = getPosteriorDistribution(likelihood, prior_dist)
        poster_dist = normalize(poster_dist)
        prior_dist = poster_dist

    plot(poster_dist, prob, step)


if __name__ == '__main__':
    main()
