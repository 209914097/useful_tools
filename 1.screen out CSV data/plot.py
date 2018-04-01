#用来画散点图http://blog.csdn.net/fennvde007/article/details/37693523
#PyCharm出现module 'matplotlib' has no attribute 'verbose'解决方案
#file-settings-tools-python scientific,将show plots in toolwindow前面的对号去掉http://blog.csdn.net/angelicYY/article/details/79518705
import pandas as pd
from matplotlib import pyplot as plt
iris = pd.read_csv('iris.csv')
iris.set_index('id')
iris.plot(x='id', y='Y',s=10,kind='scatter')#s是每个点的大小，kind='scatter'表示散点图，缺省为折线图
plt.title(u"激光", fontproperties='SimHei',fontsize='21')#fontproperties='SimHei'表示黑体字,fontsize='21'表示字体大小
plt.show()
