import tabula
import pandas as pd
def pdfToDataframe(input_file):
    df=tabula.read_pdf(input_file,pages="all")
    data=pd.DataFrame()
    for i in range(len(df)):
        data=pd.concat([data,df[i]],ignore_index=True)
    try:
        if data[list(data.columns)[-1]].isnull().values.any():
            return "The uploaded file is in incorrect format. Check user guide for knowing correct format or try uploading excel"   
        return data                                                                  
    except: 
        return "The uploaded result file is incorrect. Check your file and  upload again or check user guide for knowing suitable format"