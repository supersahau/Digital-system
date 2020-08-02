import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 传入的vector是float数组，数组元素0-1之间
# path是图片保存路径
def create_vector_graph(vector,path):
    N = len(vector)
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    vector = np.array(vector)
    radii = vector
    width = np.pi / N

    ax = plt.subplot(111, projection='polar')
    ax.axes.get_yaxis().set_ticklabels([])
    bars = ax.bar(theta, radii, width=width, bottom=0.0)

    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.gnuplot(r))
        bar.set_alpha(0.8)

    try:
        plt.savefig(path)
        matplotlib.pyplot.close('all')
        return 0
        # 用于显示图片
        # plt.show()
    except Exception as e:
        print('vector graph save failed\n',e)
        return -1

# 传入的text是utf-8编码的中文字符串，每个词之间用空格分开
# path为图片保存路径
# 增加size参数，停用词取130，实词取80
def create_wordcloud(text,path,size):
    try:
        bg = plt._imread('background.jpg')
    except:
        print('read background picture failed')
        return -1
    reg = r"[\w']+"
    wc = WordCloud(font_path="msyh.ttc", mask=bg, background_color='white', max_font_size=size,regexp=reg)
    wc.generate(text)

    wc.to_file(path)
    # 用于显示图片
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    return 0