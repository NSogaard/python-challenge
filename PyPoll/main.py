# Imports
import csv
import os

# I decided to pass in the paths for the input and output files as parameters
# to allow the users to more easily change where the data was coming from
# and going to.
def PyPolFunc(input_path, output_path):
    # This variable stores the total number of votes cast during the election
    total_votes_cast = 0
    # This dictionary stores all of the candidates in the election and how many
    # votes they have gotten
    candidate_info_dict = {}

    # These lines initialize the variables for who won the election and how
    # many votes they received.
    # This variable in particular is only used to find who actually won the 
    # election and isn't output anywhere.
    election_winner_amount = 0
    election_winner_name = ''

    # This variable is just used to record the name of the candidate for the
    # current vote in the below for loop (its declared here to prevent repeated
    # memory allocation).
    candidate = ''

    # This is the block of code that processes the csv values - it opens the
    # file at the path defined by the user in the parameters.
    with open(input_path) as voter_rec:
        # These two lines of code initializes the csv_reader and remove the
        # head of the csv to prevent errors from being thrown in the code
        # later.
        reader = csv.reader(voter_rec, delimiter=',')
        head = next(reader)

        # This for loop goes through each votes and increments the vote count
        # for whichever candidate the vote was for
        for vote in reader:
            candidate = vote[2]

            if candidate_info_dict.get(candidate, -1) == -1:
                candidate_info_dict[candidate] = 1
            else:
                candidate_info_dict[candidate] += 1
    
    # This for loop calculates the total vote count for the election - it is
    # done here instead of as an iterator in the above for loop so that it 
    # can be done in far fewer calculations (in this case 3 instead of 36k).
    for candidate_votes in candidate_info_dict.values():
        total_votes_cast += candidate_votes

    # This block of code generates the vote share for each candidate and puts
    # that in addition to the total vote count for each candidate into a string
    # that will be used below to produce the string output for this file
    candidate_result_info = ''
    for candidate in candidate_info_dict.items():
        if int(candidate[1]) > election_winner_amount:
            election_winner_amount = candidate[1]
            election_winner_name = candidate[0]
        candidate_percentage = round(100 * (candidate[1] / total_votes_cast), 3)
        candidate_result_info = candidate_result_info + f'{candidate[0]}: {candidate_percentage}% ({candidate[1]})\n'
    # This line removes the new line character from the end of the last line of
    # candidate_result_info for formatting purposes in the output_string below.
    candidate_result_info = candidate_result_info[:len(candidate_result_info)-1]

    # This is the string that we will be outputting in the output text
    # file and printing into the console. It is just a f-string that we have
    # inserted the candidate_result_info string from above into in addition
    # to all other information outlined in the challenge document. I tried to
    # follow the styling of the example we were given to the best of my
    # ability. The weird format was chosen to prevent extra indents from being
    # added to the output.
    output_string = f'''Election Results:
--------------------------------------------------
Total Votes: {total_votes_cast}
--------------------------------------------------
{candidate_result_info}
--------------------------------------------------
Winner: {election_winner_name}
--------------------------------------------------'''
    # We print out our results here
    print(output_string)

    # Our output string is written to the output file here.
    with open(output_path, 'w', newline='\n') as output_txt:
        output_txt.write(output_string)

# This is just a call of the method defined above, running this file (and this
# function by extension) should output the expected values for this challenge.
PyPolFunc(
    input_path='./PyPoll/Resources/election_data.csv',
    output_path='./PyPoll/Analysis/output_data.txt'
)