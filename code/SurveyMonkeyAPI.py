from client import Client
# If you do not have access_token, run
CLIENT_ID = 'D_kzOb9fSo2zC64qMNt7Xg'
# This should not be here!
CLIENT_SECRET = '32248023616401215046166317729204720865'
REDIRECT_URI = 'https://www.surveymonkey.com'

cl = client.Client(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, access_token=None)
# If you have access_token, run
survey_id = 190091421
client=Client(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, access_token=ACCESS_TOKEN)
    
    
# This curl comman works. I just don't know what it does    
curl -i -X GET -H "Authorization:bearer -MMu4iKFM1vKiFeMgM7kpEVLeQQ8AqhD-BnE-3hBeNHrwupDZfsyE-sIZ9.cmyFKGnWrHHr0g0k2exW1BS.d0qzzCd.-Msqn9VqeVCN4RHkKGYaWC2QOYa1hvwQ9VXVh" -H "Content-Type": "application/json" https://api.surveymonkey.ca/v3/surveys/190091421/details

# The following tool might be helpful. It needs some modification to use a .ca domain instead of teh .net domain. 
# I forked the repo and I need to clone it locally to start working with it.
import surveymonty
client = surveymonty.Client(CLIENT_SECRET)

# See here
https://stackoverflow.com/questions/53068954/getting-all-survey-responses-from-surveymonkey-survey-into-csv


my_survey_id = 190091421
headers={"Authorization": "Bearer %s" % MY_ACCESS_TOKEN,
                           "Content-Type": "application/json"}
url = "https://api.surveymonkey.ca/v3/surveys/%s/details" % (my_survey_id)
response = requests.get(url, headers=headers)
survey_data = response.json()

answer_dict = {}
for page in survey_data['pages']:
    for question in page['questions']:
        # Rows, choices, other, and cols all make up the possible answers
        if question.get('answers'):
          # answers = question['answers'].get('rows', [])\
          #   + question['answers'].get('choices', [])\
          #   + question['answers'].get('other', [])\
          #    + question['answers'].get('cols', [])
            answers = question['answers'].get('choices', [])
            for answer in answers:
                answer_dict[answer['id']] = answer