import pandas as pd
from utils.Result_Analysis_Database_Manager import *
from utils.Statistics import *
import utils.Total_Credits_Class

def SGPA_calculation(input_data):
    #getting grades from database that are expected be present in the excel file
    grades=gradesDatabaseManager()

    #getting branch codes from database that are expected be present in the excel file
    branch_codes=branchCodeDatabaseManager()
    
    #Separating supple data from regular data
    roll_list=[]
    for i in range(len(input_data)):
        roll_list.append(input_data['Htno'][i][0:5])
    new_roll_list=list(set(roll_list))
    temp_list=[]
    for i in new_roll_list:
        temp_list.append(roll_list.count(i))
    roll_series=new_roll_list[temp_list.index(max(temp_list))]
    updated_data=pd.DataFrame(columns=input_data.columns)
    roll_series1=str(int(roll_series[0:2])+1)+roll_series[2:4]+'5'
    for i in range(len(input_data)):
        if input_data.iloc[i,0][0:5]== roll_series or input_data.iloc[i,0][0:5]==roll_series1:
            updated_data.loc[len(updated_data.index)]=list(input_data.iloc[i,:])
    #Intializing basic variables
    student_data=[]
    subjects=[]

    objects_list=[]
    for i in range(len(updated_data)):
        branchcode_iter_variable=updated_data.iloc[i,0][6:8]
        if updated_data.iloc[i,0] not in student_data:
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
            student_data=[updated_data.iloc[i,0]]
        subjects.append(updated_data.iloc[i,2]+" "+updated_data.iloc[i,1])
    for j in range(len(objects_list)):
        if objects_list[j].branch == subjects[0]:
            subjects.pop(0)
            objects_list[j].subjectList(subjects)

    for i in range(len(objects_list)):
        objects_list[i].uniqueSubjectList()
        objects_list[i].finalCredits(updated_data,grades)

    #Reintialising to remove old data and to start storing new data
    student_data=[]
    student_data_dict={}
    for i in range(len(updated_data)):
        if updated_data.iloc[i,0] not in student_data:        
            if len(student_data)!=0:
                student_data.append(student_data_dict)
                for j in range(len(objects_list)):
                    if student_data[0][6:8] == objects_list[j].branch:
                        objects_list[j].regularCalculation(student_data,grades)
            student_data=[updated_data.iloc[i,0]]
            student_data_dict={}
            student_data_dict.update({updated_data.iloc[i,1]: [updated_data.iloc[i,-2], updated_data.iloc[i,-1]]})
        else:
            student_data_dict.update({updated_data.iloc[i,1]: [updated_data.iloc[i,-2], updated_data.iloc[i,-1]]})
    if len(student_data)!=0:
        student_data.append(student_data_dict)
        for j in range(len(objects_list)):
            if student_data[0][6:8] == objects_list[j].branch:
                objects_list[j].regularCalculation(student_data,grades)
    stats_object=[]
    for i in range(len(objects_list)):
        stats_object.append(FindStats(objects_list[i].branch))
        
    with pd.ExcelWriter("Result.xlsx",engine='openpyxl',mode='w') as output:
        for i in range(len(objects_list)):
            for j in range(len(branch_codes)):
                if objects_list[i].branch==branch_codes[j][1]:
                    objects_list[i].final_result_df.to_excel(output,sheet_name=branch_codes[j][2],index=False)
                    stats_object[i].statsCal(objects_list[i].final_result_df,grades,branch_codes[j][2])
                    stats_object[i].toppersCal(objects_list[i].final_result_df)
                    stats_object[i].stats_df.to_excel(output,sheet_name=branch_codes[j][2]+" Analysis",index=False)
                    stats_object[i].topper_df.to_excel(output,sheet_name=branch_codes[j][2]+" Analysis",index=False,startrow=len(stats_object[i].stats_df)+2)
        stats_object[0].overall_data.to_excel(output,sheet_name="Overall Analysis",index=False)