#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:44:57 2018

@author: janny
"""
import jieba
import jieba.posseg as pseg 
import jieba.analyse
import os  

jieba.enable_parallel(4)
jieba.load_userdict("/Users/janny/Documents/Bello_work/programing/skill_to_job/jieba_dict/hardskill_dict.txt")
#words=pseg.cut("他来到了投资咨询 android app开发互联网产品运营网易杭研大厦")

path = "/Users/janny/Documents/Bello_work/programing/skill_to_job/JDs/技术/总的技术/总的测试" #文件夹目录  
files= os.listdir(path)

content=[]
for file in files: #遍历文件夹  
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
          #f = open(path+"/"+file); #打开文件  
          try:
              f=open(path+"/"+file,'r')
              str_temp = '' 
              for line in f: #遍历文件，一行行遍历，读取文本  
                  str_temp += line.strip()  
              content.append(str_temp) #每个文件的文本存到list中  
          except:
              continue
          
nski_data1=[]
for line in content:
    line_cut_nski=''
    content_pseg=pseg.cut(line)          
    for word,pos in content_pseg:
        if pos=='nski':
            line_cut_nski+=word+' '
    nski_data1.append(line_cut_nski)

#合并成全部的all_test    
all_text=nski_dataAI+nski_dataweb
y=[]
for i in range(len(nski_dataAI)):
    y.append(1)
for i in range(len(nski_dataweb)):
    y.append(2)

#打乱，all_text 和标签y，用于划分数据集    
import numpy as np
random_order=np.random.permutation(len(all_text))
all_text_temp=copy.deepcopy(all_text)
all_text=[]
for i in random_order:
    all_text.append(all_text_temp[i])

y_temp=copy.deepcopy(y)
y=[]
for i in random_order:
    y.append(y_temp[i])
    
#划分数据集
VALIDATION_SPLIT=0.16
TEST_SPLIT=0.2
p1 = int(len(all_text)*(1-VALIDATION_SPLIT-TEST_SPLIT))
p2 = int(len(all_text)*(1-TEST_SPLIT))
x_train = all_text[:p1]
y_train = y[:p1]
x_val = all_text[p1:p2]
y_val = y[p1:p2]
x_test = all_text[p2:]
y_test = y[p2:]
print ('train docs: '+str(len(x_train)))
print ('val docs: '+str(len(x_val)))
print ('test docs: '+str(len(x_test)))

#转换数据
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer   
count_v0= CountVectorizer();  
counts_all = count_v0.fit_transform(all_text);
count_v1= CountVectorizer(vocabulary=count_v0.vocabulary_);  
counts_train = count_v1.fit_transform(x_train);   
print ("the shape of train is "+repr(counts_train.shape)  )
count_v2 = CountVectorizer(vocabulary=count_v0.vocabulary_);  
counts_test = count_v2.fit_transform(x_test);  
print ("the shape of test is "+repr(counts_test.shape)  )
  
tfidftransformer = TfidfTransformer();    
train_data = tfidftransformer.fit(counts_train).transform(counts_train);
test_data = tfidftransformer.fit(counts_test).transform(counts_test);

#建模预测
from sklearn.naive_bayes import MultinomialNB  
from sklearn import metrics
clf = MultinomialNB(alpha = 0.01)   
clf.fit(train_data, y_train);  
preds = clf.predict(test_data);
num = 0
preds = preds.tolist()
print ('precision_score:' , metrics.accuracy_score(preds, y_test))