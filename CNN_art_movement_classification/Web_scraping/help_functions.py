import unicodedata
import re
import os
    
    
def artist_name_cleaner(txt):
    """
    A function that cleans the name of the artists
    Input: str
    Output: str
    """  
    
    # here I deal with numbers, special charachters and other noise
    step1 = re.sub("[0-9]","", txt).replace("Dezember", "")
    step2 = re.sub("""['"\/;:.(),-]""", "", step1) # here 'bad' charachters
    t = "_".join(step2.strip().lower().split())
    
    # here I remove the letters with accents
    text=unicodedata.normalize('NFD', t).encode('ascii', 'ignore').decode("utf-8")

    return str(text)



def title_cleaner(txt):
    """
    A function that cleans the title
    Imp
    """  
    
    # here I deal with numbers, special charachters and other noise
    step1 = re.sub("[0-9]","", txt).replace("c.", "")
    step2 = re.sub("""['"\/;:.()?,-]""", "", step1) .replace("\\", "").replace("/", "") # other bad charachters
    t = "_".join(step2.strip().lower().split())
    
    # here I remove the letters with accents
    text=unicodedata.normalize('NFD', t).encode('ascii', 'ignore').decode("utf-8")

    return str(text)


def length_checker(l):
    
    """
    A function that checks if a list contains double entries or not
    """
    if len(l) == len(set(l)):
        return True
    else:
        return False
    

def intersection_checker(l1, l2, l3):
    """
    Function that checks that there is no overlap among three lists.
    """
    
    if not len(set(l1).intersection(set(l2)).intersection(set(l3))) == 0:
        return False
    else:
        return True
    
    
def split_checker(train_index: list, val_index: list, test_index: list):
    
    """
    Function to check that the random splits have been done accordingly
    Input: 3 lists of integers, the indexes of the 3 dataframes
    Output: bool. True if splits are OK, False otherwise
    """
    if not length_checker(train_index) and length_checker(val_index) and length_checker(test_index):
        raise Exception("You have a problem with your train-val-test split. Elements are duplicated")
    if not intersection_checker(train_index, val_index, test_index):
        raise Exception("You have a problem with your train-val-test split. There is overlap among the three splits.")
    else:
        return True
    
    
def is_file_saved(directory, filename):
    """
    Function to check that a file called filename exists in a directory
    Returns True if exists, False if not.
    """

    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
        except:
            raise ValueError("Invalid directory was passed.")
    os.chdir(directory)
    set_of_files = set(os.listdir())
    if set([filename]).issubset(set_of_files):
        return True
    else:
        return False
