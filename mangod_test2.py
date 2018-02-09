# -*- coding:UTF-8 -*-
from pymongo import MongoClient
import copy
import pprint
import datetime
#建立MongoDB数据库连接
client=MongoClient('localhost',27017)

#连接所需数据库，为数据库名
db=client.bello_annotation
#连接所需集合，也就是我们通常所说的表，taxonomy为表
collection=db.banchmark
schema=db.schema

# =============================================================================
# #制作schema的dict方便查询(非boolean非text)
# schema_dict={}
# keys=schema.find_one()['properties'].keys()
# for i in keys:
#     if schema.find_one()['properties'][i]['type']!='boolean' and schema.find_one()['properties'][i]['type']!='text':
#         print(i,':',schema.find_one()['properties'][i]['type'])
#         schema_dict[i]=schema.find_one()['properties'][i]['type']
# =============================================================================
def to_array(content):
    result_num=[]
    result_num.append(str(content))
    return result_num

def toString(content):
    return str(content)

def to_number(content):
    if content.strip()=='':
        return None
    else:
        return float(content)

def skill_type_correct(content):
    return {
            'hardSkill':'nski',
            'softSkill':'nsks',
            }.get(content,None)
    
    
post=collection.find_one()
corrected_result= copy.deepcopy(post['results'])
original_result=post['results']

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

# #minYearsOfExperience 成功测试
# for i in range(len(corrected_result)):
#     try:
#         result_temp = corrected_result[i]["labelledData"]['minYearsOfExperience']
#     #    if not isinstance(result_temp,int) and not isinstance(result_temp,float):
#         if isinstance(result_temp,str):
#             print('strContent:',result_temp)
#             result_num=to_number(result_temp)
#             print(result_num)
#             corrected_result[i]['labelledData']['minYearsOfExperience']=result_num
#     except:
#         continue


#requiredDegreeMajor 成功测试
for i in range(len(corrected_result)):
  try:
    result_temp = corrected_result[i]["labelledData"]['requiredDegreeMajor']
    if not type(result_temp) == list:
      print(result_temp)
      result_num=to_array(result_temp)
      corrected_result[i]['labelledData']['requiredDegreeMajor']=result_num
  except:
    continue

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

# #requiredSkills 成功测试    
# for i in range(len(corrected_result)):
#     try:
#         requiredSkills_many = corrected_result[i]["labelledData"]['requiredSkills']
#         for j in range(len(requiredSkills_many)):
#             requiredSkills_many[j]['skillType']=skill_type_correct(requiredSkills_many[j]['skillType'])
#     except:
#         continue

# #otherSkills 成功测试    
# for i in range(len(corrected_result)):
#     try:
#         otherSkills_many = corrected_result[i]["labelledData"]['otherSkills']
#         for j in range(len(otherSkills_many)):
#             otherSkills_many[j]['skillType']=skill_type_correct(otherSkills_many[j]['skillType'])
#     except:
#         continue

# #optionalSkills 成功测试    
# for i in range(len(corrected_result)):
#     try:
#         optionalSkills_many = corrected_result[i]["labelledData"]['optionalSkills']
#         for j in range(len(optionalSkills_many)):
#             optionalSkills_many[j]['skillType']=skill_type_correct(optionalSkills_many[j]['skillType'])
#     except:
#         continue        

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

