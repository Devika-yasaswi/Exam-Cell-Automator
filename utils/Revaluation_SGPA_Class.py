class RevaluationSGPA:
    def __init__(self,branch,original_df):
        self.branch=branch 
        self.grades_df=original_df
    def updateData(self,roll_no,subjectCode,Grade,credits,grades):
        pass_status=[]
        total_subs=0
        for i in range(len(self.grades_df)):
            if self.grades_df.iloc[i,0]==roll_no:
                for subject in self.grades_df.columns:
                    if subjectCode in subject:
                        if Grade!= self.grades_df.loc[i,subject]:
                            for grade in grades:
                                if self.grades_df.loc[i,subject]==grade[0]:
                                    existing_points=grade
                                if Grade==grade[0]:
                                    new_points=grade
                            self.grades_df.loc[i,subject]=Grade
                            self.grades_df.iloc[i,-7]-= (existing_points[1] * 10) + (new_points[1]*10) #Changing GBM
                            self.grades_df.iloc[i,-2]-= (existing_points[1] * credits) + (new_points[1] * credits) #Changing points
                            self.grades_df.iloc[i,-1]= self.grades_df.iloc[i,-2]/self.grades_df.iloc[i,-6] #Changing SGPA
                            student_data=self.grades_df.iloc[i,1:-7]
                            for j in student_data:
                                for grade in grades:
                                    if j==grade[0]:
                                        pass_status.append(grade[2].capitalize())
                                    if grade[1] !=0 and grades[i][2].capitalize()=="P":
                                        total_subs+=1
                            if "F" not in pass_status:
                                self.grades_df.iloc[i,-5]="Pass"
                            else:
                                self.grades_df.iloc[i,-5]="Fail"
                            self.grades_df.iloc[i,-4]=pass_status.count("F")
                            self.grades_df.iloc[i,-3]=self.grades_df.iloc[i,-7]/total_subs
                            
                             
