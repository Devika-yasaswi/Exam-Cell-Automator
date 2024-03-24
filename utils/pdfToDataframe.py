import tabula
import pandas as pd
import pandas as pd
def pdfToDataframe(input_file):
    df=tabula.read_pdf(input_file,pages="all")
    data=pd.DataFrame()
    for i in range(len(df)):
        data=pd.concat([data,df[i]],ignore_index=True)
    try:
        if data[list(data.columns)[-1]].isnull().values.any():
            return "Error"   
        return data                                                                  
    except: 
        return "Error"