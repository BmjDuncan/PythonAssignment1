# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:08:52 2022

@author: Ben
"""

def main(filename):
    """
    
    Parameters
    ----------
    filename : <filename>.txt The name of the .txt file with list of names
    
    Returns: Makes .txt file with abbreviations
    
    """
    import re 
    from operator import itemgetter 
    
    
    if filename[:-4]==".txt":
        filename=filename[:-4]
    
    #open text file with names or return error
    try:
        with open(filename+".txt") as name_file:
            names=[i.strip() for i in name_file.readlines()]
    except FileNotFoundError as err: 
         return print(err)
    
    
    
    #open text file with letter scores
    try:
        with open("values.txt") as score_file:
            values=score_file.read()
    except FileNotFoundError as err:
         return print(err)
    
    #Converts all letters to upper case    
    letters=[i.upper() for i in values.split()[::2]] 
    #converts all numbers from string to int
    scores=list(map(int,values.split()[1::2]))
    #creates dictionary of letters and their scores
    values={letters[i]:scores[i] for i in range(26)}
    
    
    
    all_abbr=() #will store all possible combinations 
    
    # go through each word and create combinations
    for name in names:
        chars=[*name]; #convert name into list of characters 
        
        try: #checks if there is any "-"
            chars.index("-") #turn "-" into spaces
        except: #if no "-"
            tidy_name = re.sub(r'[^a-zA-Z ]', '', "".join(chars).upper()).split() #remove non letter and space symbols
        else: #if there is "-"
            chars[chars.index("-")]=" " #turn "-" into spaces
            tidy_name = re.sub(r'[^a-zA-Z ]', '', "".join(chars).upper()).split() #remove non letter and space symbols
            
            
            
        letter_score=[0]*sum(len(i) for i in tidy_name) #list to store letter scores based on position+commonality
        
        count_letters=0 #counts what letter of name
        for i in tidy_name:       
            for j in i:                     
                j_pos=i.index(j)     #position of letter in word 
                #applies scoring conditions
                if j_pos==0:
                    letter_score[count_letters]=0
                    count_letters=count_letters+1
                elif j_pos+1==len(i):
                    if j=="e":
                        letter_score[count_letters]=20
                        count_letters=count_letters+1
                    else:
                        letter_score[count_letters]=5
                        count_letters=count_letters+1
                elif j_pos==1:
                    letter_score[count_letters]=1+values[j]
                    count_letters=count_letters+1
                elif j_pos==2:
                    letter_score[count_letters]=2+values[j]
                    count_letters=count_letters+1
                else:
                    letter_score[count_letters]=3+values[j]
                    count_letters=count_letters+1      
            
                    
            
        tidy_letter=[*"".join(tidy_name)] #converts tidy names into letters
        abbr={} #dictionary stores all combinations for current name:score for combination 
        countI=2 #offsets 3rd letter to be after 2nd to avoid repeats
        for i in tidy_letter[1:]:
            for j in tidy_letter[countI:]:  #makes combination and gives a score
                comb=tidy_letter[0]+i+j
                comb_score=letter_score[tidy_letter.index(i)]+letter_score[tidy_letter.index(j)]
                if comb not in abbr or comb_score<abbr[comb]:    
                    abbr[comb]= comb_score        
            countI=countI+1;
        
        sort_abbr=dict(sorted(abbr.items(), key=itemgetter(1))) #sorts combinations of lowest score first
        all_abbr=all_abbr+(sort_abbr,) #add current name combinations to all combinations
    
    
    
    final_abbr=[] #store best abbreviation
    
    #loop checks best abbreviation for each word against other abbreviation.
    for i in range(len(all_abbr)):
        keys=list(all_abbr[i].keys())
        count=0
        best_abbr=[]
        max_key=len(keys)
        while keys[count] in all_abbr[:i] or keys[count] in all_abbr[i+1:]:
            count+1
        if count<=max_key:
            best_abbr.append(keys[count]) #put abbreviation in final list
            if count<max_key-1: # make sure there is another abbreviation after current
                while all_abbr[i][keys[count]]==all_abbr[i][keys[count+1]]: #checks score of current and next abbreviation
                    if keys[count+1] in all_abbr[:i] or keys[count+1] in all_abbr[i+1:]: #checks next abbreaviations is unqiue
                        best_abbr.append(keys[count+1])
                    count=count+1
        else:
            best_abbr.append(" ") #if no valid combinations return empty 
        final_abbr.append(best_abbr)
     
    
    #write txt file with abbreviations
    with open("Duncan_"+filename+"_abbrevs.txt", "w") as newfile:
        for i in range(len(final_abbr)):
            newfile.write(names[i]+"\n")
            for j in final_abbr[i]:
                newfile.write(j+" ")
            newfile.write("\n")







    