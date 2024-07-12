import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec


def plot_4x4_top_left(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('4x4 Top Left')

def plot_4x4_top_mid(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('4x4 Top Mid')

def plot_4x2_top_right(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('4x2 Top Right')

def plot_2x2_mid_left_left(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('2x2 Mid Left Left')

def plot_2x2_mid_left_mid(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('2x2 Mid Left Mid')

def plot_2x2_mid_mid_left(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('2x2 Mid Mid Left')

def plot_2x2_mid_mid_right(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('2x2 Mid Mid Right')

def plot_2x2_mid_right_right(ax):
    ax.plot(np.random.rand(10))
    ax.set_title('2x2 Mid Right Right')

def multi_graph():
    # Create a 10x10 grid of subplots
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(6, 10, figure=fig)

    # Add a 4x4 subplot at the top left corner
    ax1 = fig.add_subplot(gs[0:4, 0:4])
    plot_4x4_top_left(ax1)

    # Add a 4x4 subplot at the top middle
    ax2 = fig.add_subplot(gs[0:4, 4:8])
    plot_4x4_top_mid(ax2)

    # Add a 4x2 subplot at the top right
    ax3 = fig.add_subplot(gs[0:4, 8:10])
    plot_4x2_top_right(ax3)

    # Add 2x2 subplots in the middle section
    plot_functions = [plot_2x2_mid_left_left, plot_2x2_mid_left_mid,
                      plot_2x2_mid_mid_left, plot_2x2_mid_mid_right,
                      plot_2x2_mid_right_right]

    for idx, (row, col, title) in enumerate([(4, 0, '2x2 Mid Left Left'),
                                             (4, 2, '2x2 Mid Left Mid'),
                                             (4, 4, '2x2 Mid Mid Left'),
                                             (4, 6, '2x2 Mid Mid Right'),
                                             (4, 8, '2x2 Mid Right Right')]):
        ax = fig.add_subplot(gs[row:row+2, col:col+2])
        plot_functions[idx](ax)

    plt.tight_layout()
    plt.show()

multi_graph()

# def multi_graph():
#     # Create a 10x10 grid of subplots
#     fig = plt.figure(figsize=(12, 10))
#     gs = gridspec.GridSpec(6, 10, figure=fig)
#
#     # Add a 4x4 subplot at the top left corner
#     ax1 = fig.add_subplot(gs[0:4, 0:4])
#     ax1.plot(np.random.rand(10))
#     ax1.set_title('4x4 Top Left')
#
#     # Add a 4x4 subplot at the top middle
#     ax2 = fig.add_subplot(gs[0:4, 4:8])
#     ax2.plot(np.random.rand(10))
#     ax2.set_title('4x4 Top Mid')
#
#     # Add a 4x2 subplot at the top right
#     ax3 = fig.add_subplot(gs[0:4, 8:10])
#     ax3.plot(np.random.rand(10))
#     ax3.set_title('4x2 Top Right')
#
#     # Add 2x2 subplots in the middle section
#     positions = [(4, 0, '2x2 Mid Left Left'), (4, 2, '2x2 Mid Left Mid'),
#                  (4, 4, '2x2 Mid Mid Left'), (4, 6, '2x2 Mid Mid Right'),
#                  (4, 8, '2x2 Mid Right Right')]
#
#     for (row, col, title) in positions:
#         ax = fig.add_subplot(gs[row:row+2, col:col+2])
#         ax.plot(np.random.rand(10))
#         ax.set_title(title)
#
#     plt.tight_layout()
#     plt.show()
#
# multi_graph()

# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.gridspec as gridspec
#
# # Create a 10x10 grid of subplots
# fig = plt.figure(figsize=(10, 6))
# gs = gridspec.GridSpec(10, 10, figure=fig)
#
# # Add a 4x4 subplot at the top left corner
# ax1 = fig.add_subplot(gs[0:4, 0:4])
# ax1.plot(np.random.rand(10))
# ax1.set_title('4x4 Top Left')
#
# # 4x4 mid top
# ax2 = fig.add_subplot(gs[0:4, 4:8])
# ax2.plot(np.random.rand(10))
# ax2.set_title('4x4 Top Mid')
#
# # 2 x 4 top right
# ax2 = fig.add_subplot(gs[0:4, 8:10])
# ax2.plot(np.random.rand(10))
# ax2.set_title('2x4 Top Right')
#
# # 2x2 left left
# ax2 = fig.add_subplot(gs[4:6, 0:2])
# ax2.plot(np.random.rand(10))
# ax2.set_title('2x2 mid Right')
#
# # 2x2 left mid
# ax2 = fig.add_subplot(gs[4:6, 0:2])
# ax2.plot(np.random.rand(10))
# ax2.set_title('2x2 mid Right')
#
# # 2x2 mid mid
# ax2 = fig.add_subplot(gs[4:6, 2:4])
# ax2.plot(np.random.rand(10))
# ax2.set_title('2x2 mid Right')
#
# # 2x2 mid mid
# ax2 = fig.add_subplot(gs[4:6, 4:6])
# ax2.plot(np.random.rand(10))
# ax2.set_title('2x2 mid Right')
#
# # 2x2 right mid
# ax2 = fig.add_subplot(gs[4:6, 6:8])
# ax2.plot(np.random.rand(10))
# ax2.set_title('2x2 mid Right')
#
# # 2x2 right right
# ax2 = fig.add_subplot(gs[4:6, 8:10])
# ax2.plot(np.random.rand(10))
# ax2.set_title('2x2 mid Right')
#
#
# plt.tight_layout()
# plt.show()
