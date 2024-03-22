import pandas as pd
from utils.Result_Analysis_Database_Manager import *
from utils.Statistics import *
import utils.Total_Credits_Class
input_data=pd.read_excel(r"C:\Users\yasas\OneDrive\Desktop\3-2.xlsx")

#getting grades from database that are expected be present in the excel file
grades=gradesDatabaseManager()

#getting branch codes from database that are expected be present in the excel file
branch_codes=branchCodeDatabaseManager()

#Intializing basic variables
student_data=[]
subjects=[]

objects_list=[]
for i in range(len(input_data)):
    branchcode_iter_variable=input_data.iloc[i,0][6:8]
    if input_data.iloc[i,0] not in student_data:
        if i!=0:
            if len(objects_list)==0:
                objects_list.append(utils.Total_Credits_Class.TotalCredits(branchcode_iter_variable))               
            for j in range(len(objects_list)):
                if objects_list[j].branch == subjects[0]:
                    subjects.pop(0)
                    objects_list[j].subjectList(subjects)
                    break
            else:
                objects_list.append(utils.Total_Credits_Class.TotalCredits(branchcode_iter_variable))
                subjects.pop(0)
                objects_list[j+1].subjectList(subjects)
            
        subjects=[branchcode_iter_variable]
        student_data=[input_data.iloc[i,0]]
    subjects.append(input_data.iloc[i,2]+" "+input_data.iloc[i,1])
for j in range(len(objects_list)):
    if objects_list[j].branch == subjects[0]:
        subjects.pop(0)
        objects_list[j].subjectList(subjects)

for i in range(len(objects_list)):
    objects_list[i].uniqueSubjectList()
    objects_list[i].finalCredits(input_data,grades)

#Reintialising to remove old data and to start storing new data
student_data=[]
student_data_dict={}
for i in range(len(input_data)):
    if input_data.iloc[i,0] not in student_data:        
        if len(student_data)!=0:
            student_data.append(student_data_dict)
            for j in range(len(objects_list)):
                if student_data[0][6:8] == objects_list[j].branch:
                    objects_list[j].regularCalculation(student_data,grades)
        student_data=[input_data.iloc[i,0]]
        student_data_dict={}
        student_data_dict.update({input_data.iloc[i,1]: [input_data.iloc[i,-2], input_data.iloc[i,-1]]})
    else:
        student_data_dict.update({input_data.iloc[i,1]: [input_data.iloc[i,-2], input_data.iloc[i,-1]]})
if len(student_data)!=0:
    student_data.append(student_data_dict)
    for j in range(len(objects_list)):
        if student_data[0][6:8] == objects_list[j].branch:
            objects_list[j].regularCalculation(student_data,grades)
stats_object=[]
for i in range(len(objects_list)):
    stats_object.append(FindStats(objects_list[i].branch))
    
with pd.ExcelWriter("sample.xlsx",engine='openpyxl',mode='w') as output:
    for i in range(len(objects_list)):
        for j in range(len(branch_codes)):
            if objects_list[i].branch==branch_codes[j][1]:
                objects_list[i].final_result_df.to_excel(output,sheet_name=branch_codes[j][2],index=False)
                stats_object[i].statsCal(objects_list[i].final_result_df,grades,branch_codes[j][2])
                stats_object[i].toppersCal(objects_list[i].final_result_df)
                stats_object[i].stats_df.to_excel(output,sheet_name=branch_codes[j][2]+" Analysis",index=False)
                stats_object[i].topper_df.to_excel(output,sheet_name=branch_codes[j][2]+" Analysis",index=False,startrow=len(stats_object[i].stats_df)+2)
    stats_object[0].overall_data.to_excel(output,sheet_name="Overall Analysis",index=False)