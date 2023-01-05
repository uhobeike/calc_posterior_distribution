# /usr/bin/python3

import sys

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axisartist.axislines import SubplotZero

from statistics import stdev


def setUniformDistribution(step):
    return np.full(step + 1, 1/step)


def getLikelihood(result, step):
    if result == "完走":
        return [1/step * i for i in range(step+1)]
    elif result == "失敗":
        return [1-(1/step * i) for i in range(step+1)]
    else:
        print("a")


def normalize(poster_dist):
    norm_const = 1/sum(poster_dist)
    return norm_const * poster_dist


def getPosteriorDistribution(likelihood, prior_dist):
    return likelihood * prior_dist


def splitData(results_list):
    result = []
    results = []
    for r in results_list:
        if r == "," or r == "\n":
            results.append(result[:])
            result.clear()
            continue
        result.append(r)
    results.append(result)
    return results


def plot(poster_dists, prob, step):
    fig = plt.figure()
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    for poster_dist in poster_dists:
        prob_mean = sum([po*pr for (po, pr) in zip(poster_dist, prob)])
        prob_stdev = stdev([po*pr for (po, pr) in zip(poster_dist, prob)])*10
        prob_stdev_min = prob_mean - prob_stdev
        prob_stdev_max = prob_mean + prob_stdev
        if prob_stdev_min < 0:
            prob_stdev_min = 0
        if prob_stdev_max > 1:
            prob_stdev_max = 1

        ax.bar(prob, poster_dist, width=1/step, edgecolor="black", alpha=0.6)
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
        fig.add_subplot(ax)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 0.2)
    for direction in ["right", "top"]:
        ax.axis[direction].set_visible(False)
    for direction in ["left",  "bottom"]:
        ax.axis[direction].set_axisline_style("-|>")
    ax.grid(which='major', color='black')
    ax.grid(which='minor', color='gray', linestyle='--')
    ax.tick_params(labelsize=30)
    ax.set_xlabel("完走率", fontname='IPAGothic', fontsize=50)
    ax.set_ylabel("確率", fontname='IPAGothic', fontsize=50)
    plt.show()


def main():
    step = 100
    prob = [1/step * i for i in range(step+1)]

    prior_dist = np.array([])
    poster_dist = np.array([])
    poster_dist_list = []
    likelihood = np.array([])

    results_list = splitData(sys.argv[1:])

    for results in results_list:
        prior_dist = setUniformDistribution(step)
        for result in results:
            likelihood = getLikelihood(result, step)
            poster_dist = getPosteriorDistribution(likelihood, prior_dist)
            poster_dist = normalize(poster_dist)
            prior_dist = poster_dist
        poster_dist_list.append(poster_dist.tolist())

    plot(poster_dist_list, prob, step)


if __name__ == '__main__':
    main()
