# Imports
import csv
import os

# I decided to pass in the paths for the input and output files as parameters
# to allow the users to more easily change where the data was coming from
# and going to.
def BudgetProcessor(input_path, output_path):
    # A counter of the total number of months processed
    total_months = 0
    # A total counter of the amount of profit / loss
    net_total_pl = 0
    # A variable to store the average profit / loss change between months
    # (calculated at the end of the file)
    average_pl_change = 0

    # This stores the initial profit/loss metric so that we can calculate the
    # average_pl_change at the end of the file 
    initial_pl_val = 0

    # These two variables store the date and amount of the greatest profit
    # achieved in one month
    greatest_increase_date = ''
    greatest_increase_amount = 0

    # These two variables store the date and amount of the greatest loss
    # achieved in one month
    greatest_decrease_date = ''
    greatest_decrease_amount = 0

    # This entire block just reads whatever is in the defined input file and
    # processes it
    with open(input_path) as budget_info:
        # This just initializes a csv_reader so that we can access the input
        # file data
        csv_reader = csv.reader(budget_info, delimiter=',')
        # This variable stores the profit / loss figure for the previous month
        # so that we can calculate the change between the current month and
        # last month
        previous_pl_val = 0
        # This variable just stores the current profit / loss figures for the
        # change for future calculations
        current_pl_val = 0

        # This statement just gets rid of the first line of the csv that stores
        # the header names for all of the columns. (passing in strings into
        # upcoming lines of code would throw errors)
        head = next(csv_reader)

        # This for loop iterates through all lines in the csv and makes the
        # current line accessible through the 'month_data' variable
        for month_data in csv_reader:
            # Getting the current month profit / loss value (stored in the
            # second column of the csv)
            current_pl_val = int(month_data[1])

            # Incrementing total months by one
            total_months += 1
            # Incrementing net profit / loss by the current profit / loss value
            net_total_pl += current_pl_val

            # this value represents the change in profit / loss between last
            # month and the current month
            dif_val = current_pl_val - previous_pl_val
            # We set the current month to the previous_pl_val for the next loop
            # iteration
            previous_pl_val = current_pl_val

            # This block just checks if this months change in profit / loss is
            # the greatest difference in profit or loss experience so far (and 
            # changes the appropriate values if it is)
            if dif_val > greatest_increase_amount:
                greatest_increase_amount = dif_val
                greatest_increase_date = month_data[0]
            elif dif_val < greatest_decrease_amount:
                greatest_decrease_amount = dif_val
                greatest_decrease_date = month_data[0]
            
            # This is just for the average_pl_change calculation later on - if
            # we are currently on the first month, we record the profit / loss 
            # value for that month
            if total_months == 1:
                initial_pl_val = current_pl_val

        # This calculates the average profit / loss per month for the entire
        # input file. We subtract the current_pl_val value (which is the
        # profit / loss amount for the last month) by the initial initial
        # profit / loss value found during the first loop iteration and 
        # divide it by the total number of periods between months (which is 
        # just the total number of months minus one). The result is rounded 
        # to two decimal places. 
        average_pl_change = round((current_pl_val - initial_pl_val) / (total_months - 1), 2)
                
    # This is basically a really long f-string that records all of the data
    # that we have generated in the form that was defined by the challenge
    # document.The weird format was chosen to prevent extra indents from being
    # added to the output.
    output_string = f'''Financial Analysis:
--------------------------------------------------
Total Months: {total_months}
Total: ${net_total_pl}
Average Change: ${average_pl_change}
Greatest Increase In Profits: {greatest_increase_date} (${greatest_increase_amount})
Greatest Decrease In Profits: {greatest_decrease_date} (${greatest_decrease_amount})'''

    # We print out our results here
    print(output_string)
    
    # Our output string is written to the output file here.
    with open(output_path, 'w', newline='\n') as output_file:
        output_file.write(output_string)

# This is just a call of the method defined above, running this file (and this
# function by extension) should output the expected values for this challenge.
BudgetProcessor(
    input_path='./PyBank/Resources/budget_data.csv',
    output_path='./PyBank/Analysis/output_data.txt'
)