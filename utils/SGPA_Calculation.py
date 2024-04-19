import pandas as pd
from utils.Statistics import *
import utils.Regular_SGPA_Class

def SGPA_calculation(input_data,grades,branch_codes):
    
    #Separating supple data from regular data
    roll_list=[]
    try:
        for i in range(len(input_data)):
            if pd.notnull(input_data['Htno'][i]):
                roll_list.append(input_data['Htno'][i][0:5]) #Stores all the available hallticket number series of the provided data

    # Whenever wrong type of excel data is provided then the required columns 'Htno' won't be there so solving that exception
    except KeyError:
        return "The uploaded result file is incorrect. Check your file and  upload again or check user guide for knowing suitable format"
    new_roll_list=list(set(roll_list)) #stores the occurence each number series uniquely
    temp_list=[]
    for i in new_roll_list:
        temp_list.append(roll_list.count(i)) #stores the count of each series in the overall data

    # As it is the regular file data maximum occuring series will give the regular student data
    roll_series=new_roll_list[temp_list.index(max(temp_list))] # Saves the maxmimum occuring series
  
    roll_series1=str(int(roll_series[0:2])+1)+roll_series[2:4]+'5' #Getting the starting series for LE students

    # creating new dataframe for saving regular data only
    updated_data=pd.DataFrame(columns=input_data.columns)
    for i in range(len(input_data)):
        if pd.notnull(input_data['Htno'][i]):
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
                    objects_list.append(utils.Regular_SGPA_Class.RegularSGPA(branchcode_iter_variable))               
                for j in range(len(objects_list)):
                    if objects_list[j].branch == subjects[0]:
                        subjects.pop(0)
                        objects_list[j].subjectList(subjects)
                        break
                else:
                    objects_list.append(utils.Regular_SGPA_Class.RegularSGPA(branchcode_iter_variable))
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
                        return_value=objects_list[j].regularCalculation(student_data,grades)
                        if isinstance(return_value,str):
                            return return_value
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
                    stats_object[i].topper_df.to_excel(output,sheet_name=branch_codes[j][2]+" Analysis",index=False,startrow=1,startcol=8)
                    break
            else:
                return "Details about branch code "+objects_list[i].branch+" is missing in the database. So update the database by logging in"
        overall_data=stats_object[0].overall_data
        for i in range(1,len(objects_list)):
            overall_data=pd.concat([overall_data,stats_object[i].overall_data])
        overall_data.to_excel(output,sheet_name="Overall Analysis",index=False)
    return 0