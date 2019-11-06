import pandas as pd
import requests

my_survey_id = 190097018
headers={"Authorization": "Bearer %s" % MY_ACCESS_TOKEN,
                           "Content-Type": "application/json"}

# Get information about the survey in question.
# Note that the url uses .CA instead of .NET
# This is important because a lot of the code examples are coming from the USA 
# The collowing request gets the details about a survey but not the data
# The details are used to create a dictionary to be used for understanding the data
# GET DETAIL ABOUT A SURVEY
# The PANAS Survey has the following structure
# The part ID
# What session? 1 NP testing or s MRI at Royal
# What time of day with a pull down menu
# 20 questions, each with 5 choices
url = "https://api.surveymonkey.ca/v3/surveys/%s/details" % (my_survey_id)
response = requests.get(url, headers=headers)
survey_data = response.json()

answer_dict = {}
for page in survey_data['pages']:
    for question in page['questions']:
        # Rows, choices, other, and cols all make up the possible answers
        if question.get('answers'):
          answers = question['answers'].get('rows', [])\
            + question['answers'].get('choices', [])\
            + question['answers'].get('other', [])\
             + question['answers'].get('cols', [])

          for answer in answers:
              answer_dict[answer['id']] = answer
# This answer dictionary has a structure for eahc question and for eahc possible response

df = pd.DataFrame(answer_dict)
df.to_csv('output.csv')

# GET DATA FROM A SURVEY
url2 = "https://api.surveymonkey.ca/v3/surveys/%s/responses/bulk" % (my_survey_id)
response = requests.get(url2, headers=headers)
survey_data2 = response.json()
# Once the data is received you can see how many responses are in the survey 
survey_data2['total']
# ANd how many are in this is pull of data
survey_data2['per_page']
# The data from this page is
data = survey_data2['data']

# To get the subject IDs you can cycle over the rows of data
for i in data:
    p = i['pages'][0]['questions'][0]['answers'][0]['text']
    print(p)
data[5]['pages'][0]['questions'][0]['answers'][0]['text']

answer_dict['507273538']['text']

page['questions'][0]['answers']