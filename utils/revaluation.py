from pandas import *
from openpyxl import *
from utils.Revaluation_SGPA_Class import *
from utils.Statistics import *
def reval_calculation(gpa_file,supply_file,grades,branch_codes):
    original_file=load_workbook(gpa_file)
    branches=original_file.sheetnames
    obj_index=0
    objects_list=[]
    for branch in branches:
        if "Analysis" not in branch and branches[-1]=="Overall Analysis":            
            branch_data=read_excel(gpa_file,sheet_name=branch)
            objects_list.append(RevaluationSGPA(branch_data.iloc[0,0][6:8]), branch_data) 
        elif branches[-1]!="Overall Analysis":
            branch_data=read_excel(gpa_file,sheet_name=branch)
            objects_list.append(RevaluationSGPA(branch_data.iloc[0,0][6:8]), branch_data) 
            break
    for i in range(len(supply_file)):
        if objects_list[obj_index].branch !=supply_file.iloc[i,0][6:8]:
            for obj in range(len(objects_list)):
                if obj.branch == supply_file.iloc[i,0][6:8]:                    
                    obj.updateData(supply_file.iloc[i,0],supply_file.iloc[i,1],supply_file.iloc[i,-2],supply_file.iloc[i,-1],grades)
                    break
    stats_object=[]
    for i in range(len(objects_list)):
        stats_object.append(FindStats(objects_list[i].branch))
    
    with ExcelWriter("Result.xlsx",engine='openpyxl',mode='w') as output:
        for i in range(len(objects_list)):
            for j in range(len(branch_codes)):
                if objects_list[i].branch==branch_codes[j][1]:
                    objects_list[i].grades_df.to_excel(output,sheet_name=branch_codes[j][2],index=False)
                    stats_object[i].statsCal(objects_list[i].final_result_df,grades,branch_codes[j][2])
                    stats_object[i].toppersCal(objects_list[i].final_result_df)
                    stats_object[i].stats_df.to_excel(output,sheet_name=branch_codes[j][2]+" Analysis",index=False)
                    stats_object[i].topper_df.to_excel(output,sheet_name=branch_codes[j][2]+" Analysis",index=False,startrow=1,startcol=8)
                    break