import matplotlib.pyplot as plt

import matplotlib

import re
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

import extraction as et
import timerecognize as tc

# 构造数据
# names = ['v2.2.4', 'v3.0.3', 'v3.0.2', 'v3.0.1', 'v3.0.0', 'v2.2.3',
#              'v2.2.2', 'v2.2.1', 'v2.2.0', 'v2.1.2', 'v2.1.1', 'v2.1.0',
#              'v2.0.2', 'v2.0.1', 'v2.0.0', 'v1.5.3', 'v1.5.2', 'v1.5.1',
#              'v1.5.0', 'v1.4.3', 'v1.4.2', 'v1.4.1', 'v1.4.0','何']
#
# dates = ['2019-02-26 00:00:00', '2019-02-26 00:00:00', '2018-11-10 00:00:00', '2018-11-10 00:00:00',
# 		 '2018-09-18 00:00:00', '2018-08-10 00:00:00', '2018-03-17 00:00:00', '2018-03-16 00:00:00',
# 		 '2018-03-06 00:00:00', '2018-01-18 00:00:00', '2017-12-10 00:00:00', '2017-10-07 00:00:00',
# 		 '2017-05-10 00:00:00', '2017-05-02 00:00:00', '2017-01-17 00:00:00', '2016-09-09 00:00:00',
# 		 '2016-07-03 00:00:00', '2016-01-10 00:00:00', '2015-10-29 00:00:00', '2015-02-16 00:00:00',
#
# 		 '2014-10-26 00:00:00', '2014-10-18 00:00:00', '2014-08-26 00:00:00','2014-08-28 00:00:00']
# str_pat1=re.compile(r'')
# str_pat2=re.compile(r'"(.*)"')
i=0
names=[]
dates=[]

for line in open(r"C:\Users\1\PycharmProjects\Extraction\moments1.txt",'r'):
    print(line)
    #{"moments": "中午去图书馆做完了作业", "date": "2020-07-20 15:00:00"}
    matchObj = re.match(r'{"moments":"(.*)","date":"(.*)"}', line)
    momentsinit=matchObj.group(1)
    print(momentsinit)
    timeinit=matchObj.group(2)
    print(timeinit)
    names.append(et.getMain(et.simlify(momentsinit)))
    dates.append(tc.time_extract(momentsinit,timeinit)[0])


# 转换类型 date strings (e.g. 2014-10-18) to datetime
print(dates)
print(names)
dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates]

# Choose some nice levels  定义纵轴长度
levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(dates)/6)))[:len(dates)]
# 上取整拼凑多块瓷砖，截取和dates一样长的一段
print(np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(dates)/6))))
print(levels)


# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
# 标题
ax.set(title="朋友圈事件时间轴图")

# 添加线条, basefmt设置中线的颜色，linefmt设置线的颜色以及类型
markerline, stemline, baseline = ax.stem(dates, levels,
                                         linefmt="C3-", basefmt="k-",
                                         )
# 交点空心,zorder=3设置图层,mec="k"外黑 mfc="w"内白
plt.setp(markerline, mec="k", mfc="w", zorder=3)

# 通过将Y数据替换为零，将标记移到基线
markerline.set_ydata(np.zeros(len(dates)))

matplotlib.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
# 构造描述底部、顶部的array
vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
print(np.array(['top', 'bottom']))
print(levels > 0)
print([(levels > 0).astype(int)])
print(vert)

# 添加文字注释
for d, l, r, va in zip(dates, levels, names, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                textcoords="offset points", va=va, ha="right")


# 设置x轴间隔为每四个月
ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y\n"))
# 逆时针30度，刻度右对齐
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# 隐藏y轴线
ax.get_yaxis().set_visible(False)
# 隐藏左、上、右的边框
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)
# 边距仅设置y轴
ax.margins(y=0.1)
plt.show()
