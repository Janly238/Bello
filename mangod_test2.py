# -*- coding:UTF-8 -*-
from pymongo import MongoClient
import copy
import pprint
import datetime
import re

def to_array(content):
    result_num=[]
    for i in re.split('[,，/\、-]',content):
        result_num.append(str(i))
    return result_num

def toString(content):
    return str(content)

def to_number(content):
    if content.strip()=='':
        return None
    elif isinstance(content,float):
        return content
    else:
        return int(content)

def skill_type_correct(content):
    return {
            'hardSkill':'nski',
            'softSkill':'nsks',
            }.get(content,None)
    
    
#建立MongoDB数据库连接
client=MongoClient('localhost',27017)
#连接所需数据库，bello_annotation为数据库名
db=client.bello_annotation
#连接所需集合
collection=db.test_small
post=collection.find_one()
original_result=post['results']
corrected_result= copy.deepcopy(post['results'])

# #制作schema的dict，方便查询(非boolean非text)
# schema=db.schema
# schema_dict={}
# keys=schema.find_one()['properties'].keys()
# for i in keys:
#     if schema.find_one()['properties'][i]['type']!='boolean' and schema.find_one()['properties'][i]['type']!='text':
#         print(i,':',schema.find_one()['properties'][i]['type'])
#         schema_dict[i]=schema.find_one()['properties'][i]['type']

#location 成功测试
for i in range(len(corrected_result)):
  try:
    result_temp = corrected_result[i]["labelledData"]['location']
    if not type(result_temp) == list:
      print(result_temp)
      result_num=to_array(result_temp)
      corrected_result[i]['labelledData']['location']=result_num
  except:
    continue

#YearsOfExperience 成功测试
YearOfExperience=['minYearsOfExperience','maxYearsOfExperience','minYearOfInternshipWorkExp','maxYearOfInternshipWorkExp','minYearOfManagementWorkExp','maxYearOfManagementWorkExp','minYearOfRelevantWorkExp','maxYearOfRelevantWorkExp']
def year_of_exp_correct(exp_category):
    for i in range(len(corrected_result)):
        try:
            result_temp = corrected_result[i]["labelledData"][exp_category]
        #    if not isinstance(result_temp,int) and not isinstance(result_temp,float):
            if isinstance(result_temp,str):
                print('strContent:',result_temp)
                result_num=to_number(result_temp)
                print('corrected:',result_num)
                corrected_result[i]['labelledData'][exp_category]=result_num
        except:
            continue        
for exp_category in YearOfExperience:
    year_of_exp_correct(exp_category)

def degree_major_correct(degree_major_type):
    for i in range(len(corrected_result)):
        try:
            result_temp = corrected_result[i]["labelledData"][degree_major_type]
            if not type(result_temp) == list:
                print(result_temp)
                result_num=to_array(result_temp)
                corrected_result[i]['labelledData'][degree_major_type]=result_num
        except:
            continue    
degree_major = ['requiredDegreeMajor','relevantDegreeMajor']
for degree_major_type in degree_major:
    degree_major_correct(degree_major_type)

# #requiredDegreeMajor 成功测试
# for i in range(len(corrected_result)):
#   try:
#     result_temp = corrected_result[i]["labelledData"]['requiredDegreeMajor']
#     if not type(result_temp) == list:
#       print(result_temp)
#       result_num=to_array(result_temp)
#       corrected_result[i]['labelledData']['requiredDegreeMajor']=result_num
#   except:
#     continue

#'requiredSkills','otherSkills','optionalSkills' 成功测试
#修改  ‘hardSkill -> nski’;'softSkill'->'nsks'
def skill_correct(skillCategory):
    for i in range(len(corrected_result)):
        try:
            skillCategory_many = corrected_result[i]["labelledData"][skillCategory]
            for j in range(len(skillCategory_many)):
                skillCategory_many[j]['skillType']=skill_type_correct(skillCategory_many[j]['skillType'])
        except:
            continue

skillCategory=['requiredSkills','otherSkills','optionalSkills']
for i in skillCategory:
    skill_correct(i)       

print('#############################')
# for j in range(len(original_result)):
#   try:  
#     print(type(original_result[j]['labelledData']['requiredDegreeMajor']),type(corrected_result[j]['labelledData']['requiredDegreeMajor']))
#     print(original_result[j]['labelledData']['requiredDegreeMajor'])
#     print(corrected_result[j]['labelledData']['requiredDegreeMajor'])
# #    print(post1['results'][j]['labelledData']['requiredDegreeMajor'])
#   except:
#     continue
    
#collection.update({},{"results":corrected_result})
#post1=collection.find_one()
for i in range(len(corrected_result)):
    try:#print(post['results'][j]['id'])
        requiredSkills_many=corrected_result[i]['labelledData']['optionalSkills']
        for j in range(len(requiredSkills_many)):
            print(requiredSkills_many[j]['skillType'])
        #print(type(original_result[i]['parsedData']['requiredDegreeMajor']),post['results'][i]['parsedData']['requiredDegreeMajor'])
    except:
        continue    

