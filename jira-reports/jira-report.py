# Import the required libraries
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd

# URL to Search all issues.
url = "xxxxx"
#url = "https://portworx.atlassian.net/rest/api/3/issue/{issueIdOrKey}"
# Create an authentication object,using
# registered emailID, and, token received.
auth = HTTPBasicAuth("xxxxxx")

# The Header parameter, should mention, the
# desired format of data.
headers = {
	"Accept": "application/json"
}
# Mention the JQL query.
# Here, all issues, of a project, are
# fetched,as,no criteria is mentioned.
query = {
	'jql': 'project="CNBU Engineering Escalation"'
}

# Create a request object with above parameters.
response = requests.request(
	"GET",
	url,
	headers=headers,
	auth=auth,
	params=query
)

# Get all project issues,by using the
# json loads method.
projectIssues = json.dumps(json.loads(response.text),
						sort_keys=True,
						indent=4,
						separators=(",", ": "))

# The JSON response received, using
# the requests object,
# is an intricate nested object.
# Convert the output to a dictionary object.
dictProjectIssues = json.loads(projectIssues)

#print(dictProjectIssues)

# We will append,all issues,in a list object.
listAllIssues = []

# The Issue details, we are interested in,
# are "Key" , "Summary" and "Reporter Name"
keyIssue, keySummary, keyReporter = "", "", ""


def iterateDictIssues(oIssues, listInner):

	# Now,the details for each Issue, maybe
	# directly accessible, or present further,
	# in nested dictionary objects.
	for key, values in oIssues.items():

		# If key is 'fields', get its value,
		# to fetch the 'summary' of issue.
		if(key == "fields"):

			# Since type of object is Json str,
			# convert to dictionary object.
			fieldsDict = dict(values)

			# The 'summary' field, we want, is
			# present in, further,nested dictionary
			# object. Hence,recursive call to
			# function 'iterateDictIssues'.
			iterateDictIssues(fieldsDict, listInner)

		# If key is 'reporter',get its value,
		# to fetch the 'reporter name' of issue.
		elif (key == "reporter"):

			# Since type of object is Json str
			# convert to dictionary object.
			reporterDict = dict(values)

			# The 'displayName', we want,is present
			# in,further, nested dictionary object.
			# Hence,recursive call to function 'iterateDictIssues'.
			iterateDictIssues(reporterDict, listInner)

		# Issue keyID 'key' is directly accessible.
		# Get the value of key "key" and append
		# to temporary list object.
		elif(key == 'key'):
			keyIssue = values
			listInner.append(keyIssue)

		# Get the value of key "summary",and,
		# append to temporary list object, once matched.
		elif(key == 'summary'):
			keySummary = values
			listInner.append(keySummary)

		# Get the value of key "displayName",and,
		# append to temporary list object,once matched.
		elif(key == "displayName"):
			keyReporter = values
			listInner.append(keyReporter) 


# Iterate through the API output and look
# for key 'issues'.
for key, value in dictProjectIssues.items():

	# Issues fetched, are present as list elements,
	# against the key "issues".
	if(key == "issues"):

		# Get the total number of issues present
		# for our project.
		totalIssues = len(value)

		# Iterate through each issue,and,
		# extract needed details-Key, Summary,
		# Reporter Name.
		for eachIssue in range(totalIssues):
			listInner = []

			# Issues related data,is nested
			# dictionary object.
			iterateDictIssues(value[eachIssue], listInner)

			# We append, the temporary list fields,
			# to a final list.
			listAllIssues.append(listInner)

# Prepare a dataframe object,with the final
# list of values fetched.
dfIssues = pd.DataFrame(listAllIssues, columns=["Reporter",
												"Summary",
												"Key"])

# Reframing the columns to get proper
# sequence in output.
columnTiles = ["Key", "Summary", "Reporter"]
dfIssues = dfIssues.reindex(columns=columnTiles)
#dfIssues.to_csv('/Users/sesrinivasan/Downloads/MyLists.csv', sep=";")
print(dfIssues)
