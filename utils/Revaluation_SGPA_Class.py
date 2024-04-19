class RevaluationSGPA:
    def __init__(self,branch,original_df):
        self.branch=branch 
        self.regular_gpa_df=original_df
    def updateData(self,student_roll_no,subjectCode,changed_grade_after_supply,credits,grades_from_database):
        pass_status=[]
        total_subs=0
        new_points=None
        for i in range(len(self.regular_gpa_df)):
            if self.regular_gpa_df.iloc[i,0]==student_roll_no:
                for subject in self.regular_gpa_df.columns:
                    if subjectCode in subject:
                        if changed_grade_after_supply!= self.regular_gpa_df.loc[i,subject]:
                            for grade_list in grades_from_database:
                                if self.regular_gpa_df.loc[i,subject]==grade_list[0]:
                                    existing_points=grade_list
                                if changed_grade_after_supply==grade_list[0]:
                                    new_points=grade_list
                            if new_points==None:
                                return
                            self.regular_gpa_df.loc[i,subject]=changed_grade_after_supply
                            self.regular_gpa_df.iloc[i,-7]+= (new_points[1]*10) - (existing_points[1] * 10) #Changing GBM
                            self.regular_gpa_df.iloc[i,-2]+= (new_points[1] * int(credits)) - (existing_points[1] * int(credits)) #Changing points
                            self.regular_gpa_df.iloc[i,-1]= self.regular_gpa_df.iloc[i,-2]/self.regular_gpa_df.iloc[i,-6] #Changing SGPA
                            student_data=self.regular_gpa_df.iloc[i,1:-7]
                            for j in student_data:
                                for grade_list in grades_from_database:
                                    if j==grade_list[0]:
                                        pass_status.append(grade_list[2])  
                                        if grade_list[1]!=0 or grade_list[2]=="F":
                                            total_subs+=1
                            if "F" not in pass_status:
                                self.regular_gpa_df.iloc[i,-5]="Pass"
                            else:
                                self.regular_gpa_df.iloc[i,-5]="Fail"
                            self.regular_gpa_df.iloc[i,-4]=pass_status.count("F")                            
                            self.regular_gpa_df.iloc[i,-3]=self.regular_gpa_df.iloc[i,-7]/total_subs
                        break
                            
                             
