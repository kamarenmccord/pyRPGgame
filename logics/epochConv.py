
"""takes a file and strips out the date from string"""

""" makes the save files readable dates when loading """

# TODO: use this module to read the save data epoch strings
#       convert to human readable format and display on load screen

# TODO: create load file selection screen

def date_strip(fDate, cDate):

    """ note: check the crud_module (file) for conversion of epoch"""
    current_date = cDate  # the current epoch time used to iter fDate
    date_list = []
    for file in fDate:
        if 'save_data+' in file:
            epoch = file[10:]
            # delta time
            dTime = current_date - epoch
            # sort to list

