def require_htno(portal_data):

    htno_dict = {}
    for index, row in portal_data.iterrows():
        if row['EXAMTYPE'] == 'REG':
            htno = row['htno']
            key = htno[6:8]  # Extracting key from htno
            subcode = row['subcode']  # Assuming 'subcode' contains the name of the subcode
            
            # Check if key exists in htno_dict
            if key not in htno_dict:
                # If key doesn't exist, create a new nested dictionary
                htno_dict[key] = {}
            
            # Check if subcode is already a key in the nested dictionary
            if subcode not in htno_dict[key]:
                # If subcode is not a key, create a new list for that subcode
                htno_dict[key][subcode] = []
            
            # Append data to the list corresponding to the subcode
            htno_dict[key][subcode].append(row['htno'])

    # print(len(htno_dict['01']['R2031011']))
    # print(htno_dict)
    return htno_dict
