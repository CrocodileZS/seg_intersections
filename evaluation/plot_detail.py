import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df1 = pd.read_csv('../time_static_05_1.csv', header=None, names=['#segments', 'brute-force', 'plane-sweep'])
x1 = df1['#segments'][:25]
y11 = df1['brute-force'][:25]
y21 = df1['plane-sweep'][:25]

df2 = pd.read_csv('../time_static_05_2.csv', header=None, names=['#segments', 'brute-force', 'plane-sweep'])
x2 = df2['#segments'][:25]
y12 = df2['brute-force'][:25]
y22 = df2['plane-sweep'][:25]

df3 = pd.read_csv('../time_static_05_5.csv', header=None, names=['#segments', 'brute-force', 'plane-sweep'])
x3 = df3['#segments'][:25]
y13 = df3['brute-force'][:25]
y23 = df3['plane-sweep'][:25]

def draw_plot(ax, x, y1, y2, title):
    ax.plot(x, y1, label='Brute-force', color='teal', marker=None, linestyle='-', linewidth=2)
    ax.plot(x, y2, label='Plane-sweep', color='goldenrod', marker=None, linestyle='-', linewidth=2)

    idx = np.argwhere(np.diff(np.sign(y1 - y2))).flatten()
    if idx.size > 0:
        x_intersect = x[idx[0]]
        y_intersect = y1[idx[0]]

        ax.plot(x_intersect, y_intersect, 'ro')

        ax.annotate(f'({x_intersect}, {y_intersect:.5f})', (x_intersect, y_intersect), textcoords="offset points",
                    xytext=(0, 10), ha='center')

        ax.axvline(x=x_intersect, color='gray', linestyle='--', linewidth=1)


    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend(loc='upper left')
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('Number of segments', fontsize=12)
    ax.set_ylabel('Running time', fontsize=12)
    ax.set_ylim(bottom=0)

# 创建1行3列的子图布局
fig, axs = plt.subplots(1, 3, figsize=(18, 6))  # 总体图的尺寸

# 更新全局字体大小
plt.rcParams.update({'font.size': 12})

# 循环绘制每个子图
draw_plot(axs[0], x1, y11, y21, f'Running time for SHORT segments')
draw_plot(axs[1], x2, y12, y22, f'Running time for MEDIUM segments')
draw_plot(axs[2], x3, y13, y23, f'Running time for LONG segments')

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()

