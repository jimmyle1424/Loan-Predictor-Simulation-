#importing important modules#
import pandas as pd
import numpy as num
import os 
#importing and printing a data table I downloaded from kaggle#
Loan_df = pd.read_csv("C:\\Users\\15103\\Documents\loantable.csv")
print (Loan_df)
#producing some averages, later used for distributions-- using Numpy to do list math#
average_loan_amount = num.mean(Loan_df["LoanAmount"])
print("The average loan amount is:",average_loan_amount)
average_applicant_income = num.mean(Loan_df["ApplicantIncome"])
print ("The average applicant income is:",average_applicant_income)
average_coapplicant_income = num.mean(Loan_df["CoapplicantIncome"])
#importing and using statistics-- a very useful module with a standard deviation calculator#
import statistics
#calculating standard deviations which will be used in Gaussian distribution later#
stdev_loan_amount= statistics.pstdev(Loan_df["LoanAmount"])
stdev_applicant_income= statistics.pstdev(Loan_df["ApplicantIncome"])
stdev_coapplicant_income= statistics.pstdev(Loan_df["CoapplicantIncome"])
#prompting the user for a particular Loan ID#
Loan_ID_input_text = input ("Please input the Loan ID you would like a predictor for-if you are done, type 'end': ")
#grabbing the row of interest by its Loan ID using pandas#
index_data = pd.read_csv("C:\\Users\\15103\\Documents\loantable.csv", index_col = "Loan_ID")
output_data = index_data.loc[Loan_ID_input_text]
#these next three lines are used as a basis for a recursive loop, if the user inputs a Loan ID, it calculates the % probability the loan will be approved and prompts them for another User ID, until they say something like 'end'#
completion_indicators = ["done", "Done", "close", "Close", "end"]
new_input = Loan_ID_input_text
for new_input in Loan_df["Loan_ID"]:
    #at the end of this loop, i define a variable called new_input#
    index_data = pd.read_csv("C:\\Users\\15103\\Documents\loantable.csv", index_col = "Loan_ID")
    output_data = index_data.loc[Loan_ID_input_text]
    print (output_data)
    #the next 3 lines focus on grabbing 3 differentials from mean values, later used in Gaussian distribution#
    Loan_differential = output_data["LoanAmount"] - average_loan_amount
    income_differential = output_data["ApplicantIncome"] - average_applicant_income
    coapplicant_differential = output_data["CoapplicantIncome"] - average_coapplicant_income
    #using standard deviation to give an approval factor based on how many standard deviations away from the mean the loan amount is, with >2 stds away giving the maximum of 1, down to a minimum of 0.25#
    if Loan_differential > 2*stdev_loan_amount:
        approval_factor_1 = 1
    elif stdev_loan_amount < Loan_differential < 2*stdev_loan_amount:
            approval_factor_1 = 0.75
    elif 0 < Loan_differential < stdev_loan_amount:
                approval_factor_1 = 0.5
    else: 
            approval_factor_1 = 0.25
    #similar to approval factor 1, using a Gaussian distribution to give an approval factor based on applicant income relative to the mean#
    if income_differential > 2*stdev_applicant_income:
        approval_factor_2 = 1
    elif stdev_applicant_income < income_differential < 2*stdev_applicant_income:
            approval_factor_2 = 0.75
    elif 0 < income_differential < stdev_coapplicant_income:
            approval_factor_2 = 0.5
    else: 
            approval_factor_2 = 0.25
    #loan data shows that males have a higher approval rate than non-males, and since we have the data in the table I figured I would include some real world bias#
    gender = output_data["Gender"]
    if gender in ("Male"):
        approval_factor_3 = 1
    else: 
        approval_factor_3 = 0.8
    #calling on approval factor 2 to qualify income relative to property area. this utilizes a linear regression where the independent variable is property area and the dependent variable is the approval factor#
    property_area = output_data["Property_Area"]
    if property_area in ("Urban"):
        if approval_factor_2 > 0.5:
            approval_factor_4= 1
        else: 
            approval_factor_4 = 0.5
    if property_area in ("Semiurban"):
        if approval_factor_2 > 0.5:
            approval_factor_4 = 1
        else: 
            approval_factor_4 = 0.75
    if property_area in ("Rural"):
        if approval_factor_2 > 0.5:
            approval_factor_4 = 1
        else: 
            approval_factor_4 = 0.8
    #a simple binary to separate graduates from non-graduates#
    Graduation_status = output_data["Education"]
    if Graduation_status in ("Graduate"):
        approval_factor_5 = 1
    else: 
        approval_factor_5 = 0.5
    #the last of the Gaussian distributions, this time assigning an approval factor based on relative coapplicant income#
    if coapplicant_differential > 2*stdev_coapplicant_income:
        approval_factor_7 = 1
    elif stdev_coapplicant_income < coapplicant_differential < 2*stdev_coapplicant_income:
            approval_factor_7 = 0.75
    elif 0 < coapplicant_differential < stdev_coapplicant_income:
            approval_factor_7 = 0.5
    else: 
            approval_factor_7 = 0.25
    #assigning an approval factor based on loan term, where the longest loan term is favored#
    Loan_Term = output_data["Loan_Amount_Term"]  
    if Loan_Term > 360: 
        approval_factor_8 = 1
    elif 300< Loan_Term < 400:
            approval_factor_8 = 0.75
    elif 100 < Loan_Term < 200 :
            approval_factor_8 = 0.5
    else : 
            approval_factor_8 = 0
    #another binary, this time to qualify credit history. some did not list a credit history, and will receive a score of 0.3#
    Credit_History = output_data["Credit_History"]
    if Credit_History > 0:
        approval_factor_9 = 1
    else :
        approval_factor_9 = 0.3
    #qualifying self employment status, assigning approval factor thereof#
    Self_Employed = output_data["Self_Employed"]
    if Self_Employed in ("Yes"):
        approval_factor_10 = 1
    else:
        approval_factor_10 = 0.75
    #adding all the approval factors up, making a percentage, since the maximum is 9#
    Loan_prediction_score = (approval_factor_1 + approval_factor_2 + approval_factor_3 + approval_factor_4 + approval_factor_5 + approval_factor_7 + approval_factor_8 + approval_factor_9+approval_factor_10)*(100/9)
    if approval_factor_8 > 0:
        print ("The probability this loan will be approved is: ", Loan_prediction_score, "%")
        print ("Approval factor 1, based on loan amount is: ",approval_factor_1)
        print ("Approval factor 2, based on applicant income is: ",approval_factor_2)
        print ("Approval factor 3, based on applicant gender is: ",approval_factor_3)
        print ("Approval factor 4, based on applicant property area is: ",approval_factor_4)
        print ("Approval factor 5, based on applicant graduation status is: ",approval_factor_5)
        print ("Approval factor 6, based on coapplicant income is: ",approval_factor_7)
        print ("Approval factor 7, based on loan term is: ",approval_factor_8)
        print ("Approval factor 8, based on credit history is: ",approval_factor_9)
        print ("Approval factor 9, based on self employment status is: ", approval_factor_10)
   #loans only have terms of 180, 360 or 480, any others are invalid#
    else:
        print ("This loan could not be approved due to an invalid loan term, approval factor 7: ", approval_factor_8)
   #last 4 lines are important for recursive loop. final line prints a thank you message#
    new_input = input ("Please input the Loan ID you would like a predictor for-if you are done, type 'end': ")
    Loan_ID_input_text = new_input
    if new_input in completion_indicators:
        break
print ("Thank you for using this loan predictor")

    
            
        

  

    
    