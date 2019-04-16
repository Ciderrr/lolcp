#算法流程：
#   1.开始
#   2.加载数据&预处理 (需要加载特征文件和标签文件的数据到内存中，并处理缺省值)
#   3.创建分类器
#   4.训练分类器
#   5.在测试集上得到预测结果
#   6.计算准确率和召回率
#   7.结束

import numpy as np
import pandas as pd

from sklearn.preprocessing import Imputer  # 预处理函数Imputer
from sklearn.model_selection import train_test_split  # 自动生成训练集和测试集的模块
from sklearn.metrics import classification_report  # 预测结果评估函数

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB


def load_dataset(feature_paths,label_paths):
    #  读取特征文件列表和标签文件列表的所有内容，并归后返回
    feature = np.ndarray(shape=(0,10)) 
    label = np.ndarray(shape=(0,1))
    #  定义空的特征、标签变量。列数量和原数据维度一致（10,1）
    for file in feature_paths:
        fd = pd.read_table(file,delimiter=",",na_values="?",header=None)
        # 使用逗号分隔符读取features数据，将问号替换标记为缺失值，文件中不包含表头
        imp = Imputer(missing_values="NaN",strategy="mean",axis=0)
        # 使用mean平均值对缺失数据进行补全
        imp.fit(fd)
        fd = imp.transform(fd)
        # fit()函数用于训练预处理器，transform()函数用于生成预处理结果
        feature = np.concatenate((feature,fd))
        # 将新读入的数据合并到特征集合中,concatenate()是数组拼接函数
    for file in label_paths:
        df = pd.read_table(file,header=None)
        label = np.concatenate((label,df))
    label = np.ravel(label)  #将标签规整为一维向量
    return feature,label
        
if __name__ == '__main__':
    num = 50      # num的值与getData.py中main的num相同
    feature_paths = []
    label_paths = []
    for i in range(num) :
        feature_paths.append("G:\\data\\c{}.txt".format(i))
        label_paths.append("G:\\data\\w{}.txt".format(i))
    # 设置feature label的路径
    x_train,y_train = load_dataset(feature_paths[:47],label_paths[:47])
    # 将前47个作为训练集读入
    x_test,y_test = load_dataset(feature_paths[47:],label_paths[47:])
    # 将最后3个作为测试集读入
    x_train,x_,y_train,y_ = train_test_split(x_train,y_train,test_size=0.0)
    # 使用这个函数，并将test_size=0 将数据随机打乱 便于后续分类器的初始化和训练

    # KNN 算法的构建：
    print("KNN training start")
    knn = KNeighborsClassifier().fit(x_train,y_train)
    print("KNN Training done!")
    answer_knn = knn.predict(x_test)
    print("KNN Prediction done!")
    
    # 决策树算法的构建：
    print("DT training start")
    dt = DecisionTreeClassifier().fit(x_train,y_train)
    print("DT Training done!")
    answer_dt = dt.predict(x_test)
    print("DT Prediction done!")
   
    # 适用于伯努利模型的贝叶斯分类器的构建：
    print("B-Bayes training start")
    bnb = BernoulliNB().fit(x_train,y_train)
    print("BNB Training done!")
    answer_bnb = bnb.predict(x_test)
    print("BNB Prediction done")
    
    # 高斯贝叶斯分类器的构建：
    print("G-Bayes training start")
    gnb = GaussianNB().fit(x_train,y_train)
    print("GNB Training done!")
    answer_gnb = gnb.predict(x_test)
    print("GNB Prediction done")
    
    
    # 针对多项式的贝叶斯分类器的构建：
    print("M-Bayes training start")
    mnb = MultinomialNB().fit(x_train,y_train)
    print("MNB Training done!")
    answer_mnb = mnb.predict(x_test)
    print("MNB Prediction done")
    
    
    
    # 计算准确率 召回率
    print("\n\nThe classification report for KNN:")
    print(classification_report(y_test,answer_knn))
    
    print("\n\nThe classification report for DT:")
    print(classification_report(y_test,answer_dt))
    
    print("\n\nThe classification report for BNB:")
    print(classification_report(y_test,answer_bnb))
    
    print("\n\nThe classification report for GNB:")
    print(classification_report(y_test,answer_gnb))
    
    print("\n\nThe classification report for MNB:")
    print(classification_report(y_test,answer_mnb))
