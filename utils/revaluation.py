from pandas import *
from openpyxl import *
from utils.Revaluation_SGPA_Class import *
from utils.Statistics import *
from utils.branch_wise_analysis import *
def reval_calculation(regular_gpa_file,supply_result_df,grades_from_database,branch_codes_from_database):
    regular_SGPA_file=load_workbook(regular_gpa_file)
    branches_in_regular_SGPA_file=regular_SGPA_file.sheetnames
    objects_list=[]
    for branch in branches_in_regular_SGPA_file:
        if "Analysis" not in branch and branches_in_regular_SGPA_file[-1]=="Overall Analysis":            
            branch_wise_data=read_excel(regular_gpa_file,sheet_name=branch)
            objects_list.append(RevaluationSGPA(branch_wise_data.iloc[0,0][6:8] , branch_wise_data))
            branch_wise=False
        elif branches_in_regular_SGPA_file[-1]!="Overall Analysis":
            branch_wise_data=read_excel(regular_gpa_file,sheet_name=branch)
            objects_list.append(RevaluationSGPA(branch_wise_data.iloc[0,0][6:8], branch_wise_data))
            branch_wise=True
            break
    for i in range(len(supply_result_df)):
        for obj in objects_list:
            if obj.branch == supply_result_df.iloc[i,0][6:8]:                    
                obj.updateData(supply_result_df.iloc[i,0],supply_result_df.iloc[i,1],supply_result_df.iloc[i,-2],supply_result_df.iloc[i,-1],grades_from_database)
                break
    stats_object=[]
    for i in range(len(objects_list)):
        stats_object.append(FindStats(objects_list[i].branch))
    
    with ExcelWriter("Result.xlsx",engine='openpyxl',mode='w') as output:
        for i in range(len(objects_list)):
            for j in range(len(branch_codes_from_database)):
                if objects_list[i].branch==branch_codes_from_database[j][1]:
                    objects_list[i].regular_gpa_df.to_excel(output,sheet_name=branch_codes_from_database[j][2],index=False)
                    stats_object[i].statsCal(objects_list[i].regular_gpa_df,grades_from_database,branch_codes_from_database[j][2])
                    stats_object[i].toppersCal(objects_list[i].regular_gpa_df)
                    stats_object[i].stats_df.to_excel(output,sheet_name=branch_codes_from_database[j][2]+" Analysis",index=False)
                    stats_object[i].topper_df.to_excel(output,sheet_name=branch_codes_from_database[j][2]+" Analysis",index=False,startrow=1,startcol=8)
                    break
    if branch_wise:
        branchwise_analysis('Result.xlsx',branches_in_regular_SGPA_file[0],grades_from_database)
    else:
        with ExcelWriter("Result.xlsx",engine='openpyxl',mode='a',if_sheet_exists="overlay") as output:
            overall_data=stats_object[0].overall_data
            for i in range(1,len(objects_list)):
                overall_data=pd.concat([overall_data,stats_object[i].overall_data])
                overall_data.to_excel(output,sheet_name="Overall Analysis",index=False)