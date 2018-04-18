import pandas as pd
import xgboost as xgb
pd.options.mode.chained_assignment = None
import numpy as np
import seaborn as sns
import time
from datetime import date
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 提取训练集一广告商品相关特征
train1_f = pd.read_csv('data/train1_f.csv')
tra = train1_f
# 该展示商品被点击次数
t = tra[['item_id']]
t['item_click']=1
t = t.groupby('item_id').agg('sum').reset_index()
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品被购买次数
t = tra[['item_id','is_trade']]
t = t.groupby('item_id').agg('sum').reset_index()
t = t.rename(columns={'is_trade':'item_buy'})
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品被购买率
tra['item_buy_rate'] = tra['item_buy']/tra['item_click']
# 该展示商品在上午购买的次数
t = tra[['item_id','is_am','is_trade']]
t = t[t.is_trade==1][['item_id','is_am']]
t = t.groupby('item_id').agg('sum').reset_index()
t.rename(columns={'is_am':'sale_on_am'},inplace=True)
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品再下午购买的次数
tra['sale_on_pm'] = tra['item_buy']-tra['sale_on_am']
# 该商品是否属于高销量类别
t = tra[['cate2','is_trade']]
t = tra.groupby('cate2').agg('sum').reset_index()
t['is_high_sale'] = t['is_trade'].apply(lambda x:1 if x>=1000 else 0)
tra = pd.merge(tra,t[['cate2','is_high_sale']],on='cate2',how='left')
#商品的属性列表处理
t = tra[['item_id','item_property_list','is_trade']]
#将属性列表从字符串转变为list
def getPropertySet(s):
     PropertySet=set(s.split(';'))
     return PropertySet
t['item_property_list']=t.item_property_list.apply(getPropertySet)
#获取受欢迎商品的属性
t1=t[t.is_trade==1]
Popular=set()
for i in t1['item_property_list']:
     Popular=set(list(Popular)+list(i))
#取出每种商品
t2=t[['item_id','item_property_list']]
t2.drop_duplicates(['item_id'],inplace=True)
#记录每个商品的属性总数
def setSum_propertys(s):
      return len(s)
t2['Sum_Propertys']=t2.item_property_list.apply(setSum_propertys)
#记录每个商品的受欢迎属性个数
t2['Sum_Popular_Propertys']=0
# t['Sum_Popular_Propertys']=len([i for i in t.item_property_list if i in list(Popular)])
def getSum_Popular_Propertys(s):
     return len(Popular.intersection(s))
t2['Sum_Popular_Propertys']=t2.item_property_list.apply(getSum_Popular_Propertys)
#记录每个商品受欢迎属性占总属性个数百分比
t2['Popular_rate']=t2['Sum_Popular_Propertys']/t2['Sum_Propertys']
#合并
tra=pd.merge(tra,t2[['item_id','Sum_Propertys','Sum_Popular_Propertys','Popular_rate']],on='item_id',how='left')

tra[['item_id','sale_on_pm','item_click','item_buy','item_buy_rate','sale_on_am','is_high_sale','Sum_Propertys','Sum_Popular_Propertys',
     'Popular_rate'
     ]].to_csv('data/item_feature1.csv',index=None)



# 提取训练集一广告商品相关特征
train1_f = pd.read_csv('data/train2_f.csv')
tra = train1_f
# 该展示商品被点击次数
t = tra[['item_id']]
t['item_click']=1
t = t.groupby('item_id').agg('sum').reset_index()
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品被购买次数
t = tra[['item_id','is_trade']]
t = t.groupby('item_id').agg('sum').reset_index()
t = t.rename(columns={'is_trade':'item_buy'})
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品被购买率
tra['item_buy_rate'] = tra['item_buy']/tra['item_click']
# 该展示商品在上午购买的次数
t = tra[['item_id','is_am','is_trade']]
t = t[t.is_trade==1][['item_id','is_am']]
t = t.groupby('item_id').agg('sum').reset_index()
t.rename(columns={'is_am':'sale_on_am'},inplace=True)
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品再下午购买的次数
tra['sale_on_pm'] = tra['item_buy']-tra['sale_on_am']
# 该商品是否属于高销量类别
t = tra[['cate2','is_trade']]
t = tra.groupby('cate2').agg('sum').reset_index()
t['is_high_sale'] = t['is_trade'].apply(lambda x:1 if x>=1000 else 0)
tra = pd.merge(tra,t[['cate2','is_high_sale']],on='cate2',how='left')
#商品的属性列表处理
t = tra[['item_id','item_property_list','is_trade']]
#将属性列表从字符串转变为list
def getPropertySet(s):
     PropertySet=set(s.split(';'))
     return PropertySet
t['item_property_list']=t.item_property_list.apply(getPropertySet)
#获取受欢迎商品的属性
t1=t[t.is_trade==1]
Popular=set()
for i in t1['item_property_list']:
     Popular=set(list(Popular)+list(i))
#取出每种商品
t2=t[['item_id','item_property_list']]
t2.drop_duplicates(['item_id'],inplace=True)
#记录每个商品的属性总数
def setSum_propertys(s):
      return len(s)
t2['Sum_Propertys']=t2.item_property_list.apply(setSum_propertys)
#记录每个商品的受欢迎属性个数
t2['Sum_Popular_Propertys']=0
# t['Sum_Popular_Propertys']=len([i for i in t.item_property_list if i in list(Popular)])
def getSum_Popular_Propertys(s):
     return len(Popular.intersection(s))
t2['Sum_Popular_Propertys']=t2.item_property_list.apply(getSum_Popular_Propertys)
#记录每个商品受欢迎属性占总属性个数百分比
t2['Popular_rate']=t2['Sum_Popular_Propertys']/t2['Sum_Propertys']
#合并
tra=pd.merge(tra,t2[['item_id','Sum_Propertys','Sum_Popular_Propertys','Popular_rate']],on='item_id',how='left')

tra[['item_id','sale_on_pm','item_click','item_buy','item_buy_rate','sale_on_am','is_high_sale','Sum_Propertys','Sum_Popular_Propertys',
     'Popular_rate'
     ]].to_csv('data/item_feature2.csv',index=None)

# 提取训练集一广告商品相关特征
train1_f = pd.read_csv('data/train3_f.csv')
tra = train1_f
# 该展示商品被点击次数
t = tra[['item_id']]
t['item_click']=1
t = t.groupby('item_id').agg('sum').reset_index()
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品被购买次数
t = tra[['item_id','is_trade']]
t = t.groupby('item_id').agg('sum').reset_index()
t = t.rename(columns={'is_trade':'item_buy'})
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品被购买率
tra['item_buy_rate'] = tra['item_buy']/tra['item_click']
# 该展示商品在上午购买的次数
t = tra[['item_id','is_am','is_trade']]
t = t[t.is_trade==1][['item_id','is_am']]
t = t.groupby('item_id').agg('sum').reset_index()
t.rename(columns={'is_am':'sale_on_am'},inplace=True)
tra = pd.merge(tra,t,on='item_id',how='left')
# 该展示商品再下午购买的次数
tra['sale_on_pm'] = tra['item_buy']-tra['sale_on_am']
# 该商品是否属于高销量类别
t = tra[['cate2','is_trade']]
t = tra.groupby('cate2').agg('sum').reset_index()
t['is_high_sale'] = t['is_trade'].apply(lambda x:1 if x>=1000 else 0)
tra = pd.merge(tra,t[['cate2','is_high_sale']],on='cate2',how='left')
#商品的属性列表处理
t = tra[['item_id','item_property_list','is_trade']]
#将属性列表从字符串转变为list
def getPropertySet(s):
     PropertySet=set(s.split(';'))
     return PropertySet
t['item_property_list']=t.item_property_list.apply(getPropertySet)
#获取受欢迎商品的属性
t1=t[t.is_trade==1]
Popular=set()
for i in t1['item_property_list']:
     Popular=set(list(Popular)+list(i))
#取出每种商品
t2=t[['item_id','item_property_list']]
t2.drop_duplicates(['item_id'],inplace=True)
#记录每个商品的属性总数
def setSum_propertys(s):
      return len(s)
t2['Sum_Propertys']=t2.item_property_list.apply(setSum_propertys)
#记录每个商品的受欢迎属性个数
t2['Sum_Popular_Propertys']=0
# t['Sum_Popular_Propertys']=len([i for i in t.item_property_list if i in list(Popular)])
def getSum_Popular_Propertys(s):
     return len(Popular.intersection(s))
t2['Sum_Popular_Propertys']=t2.item_property_list.apply(getSum_Popular_Propertys)
#记录每个商品受欢迎属性占总属性个数百分比
t2['Popular_rate']=t2['Sum_Popular_Propertys']/t2['Sum_Propertys']
#合并
tra=pd.merge(tra,t2[['item_id','Sum_Propertys','Sum_Popular_Propertys','Popular_rate']],on='item_id',how='left')

tra[['item_id','sale_on_pm','item_click','item_buy','item_buy_rate','sale_on_am','is_high_sale','Sum_Propertys','Sum_Popular_Propertys',
     'Popular_rate'
     ]].to_csv('data/item_feature3.csv',index=None)