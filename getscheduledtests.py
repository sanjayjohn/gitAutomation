import os
import pathlib
import urllib
import requests
import json
from git import Repo

def get_config():
    # Check to ensure the configuration file exists and is readable.
    try:
        path = pathlib.Path("conf.json")
        if path.exists() and path.is_file():
            with open(path) as config_file:
                try:
                    qtest_config = json.load(config_file)
                    return qtest_config
                except json.JSONDecodeError:
                    print("Error: Configuration file not in valid JSON format.")
        else:
            raise IOError
    except IOError:
        print("Error: Configuration file not found or inaccessible.")
        return -1
    except Exception as e:
        print("Error: Unexpected error loading configuration: " + str(e))
        return -1

def get_test_runs():
    qtest_config = get_config()
    api_token = qtest_config["qtest_api_token"]
    qTestUrl = qtest_config["qtest_url"]
    projectid = os.environ["PROJECT_ID"]
    gitRepo = qtest_config["git_url"]
    URL = "{}/api/v3/projects/{}/settings/test-cases/fields"
    URL = URL.format(qTestUrl, projectid)
    API = api_token

    fileList = []
    APITOKEN = API
    GetTCURL = "{}/api/v3/projects/" + projectid + "/test-cases/"
    GetTRURL = "{}/api/v3/projects/" + projectid + "/test-runs/"
    GetTCURL = GetTCURL.format(qTestUrl)
    GetTRURL = GetTRURL.format(qTestUrl)

    local_repo = qtest_config["local_repository"]
    try:
        repo = Repo.clone_from(gitRepo, local_repo)
    except:
        repo = Repo(local_repo)

    if ('QTE_SCHEDULED_TX_DATA' in os.environ):
        processUrl = os.environ['QTE_SCHEDULED_TX_DATA']


        myResponse = requests.get(url=processUrl, headers={"Content-Type": "application/json"})

        if (myResponse.ok):
            try:
                response = json.loads(myResponse.content)
            except:
                return "None"

            for testRun in response["QTE"]["testRuns"]:
                myTestRunResponse = requests.get(url=GetTRURL + testRun["Id"],
                                             headers={"Content-Type": "application/json", "Authorization": APITOKEN})

                if (myTestRunResponse.ok):
                    myTestRun = json.loads(myTestRunResponse.content)

                    myTestCaseResponse = requests.get(url=GetTCURL + str(myTestRun["test_case"]["id"]),
                                                  headers={"Content-Type": "application/json",
                                                           "Authorization": APITOKEN})
                    if (myTestCaseResponse.ok):
                        myTestCase = json.loads(myTestCaseResponse.content)
                        for field in myTestCase["properties"]:
                            if field["field_name"] == "Git URL":
                                gitUrl = field['field_value']
                                if gitUrl == "":
                                    testCaseName = myTestCase["name"]
                                    f = open(local_repo + "/" + testCaseName + ".txt", "w+")
                                    f.close()
                                    fileList.append(testCaseName + ".txt")
                                    git_url = get_git_url(gitRepo, testCaseName)
                                    field['field_value'] = git_url
                                    try:
                                        r = requests.put(url=GetTCURL + str(myTestRun["test_case"]["id"]), data=json.dumps(myTestCase),
                                                          headers={"Content-Type": "application/json",
                                                           "Authorization": APITOKEN})
                                        print(r.text)
                                    except:
                                        print("Error: Unable to post data to qTest Manager API.")
                                        return -1
                    else:
                        myTestCaseResponse.raise_for_status()
                else:
                    myTestRunResponse.raise_for_status()

        else:
            myResponse.raise_for_status()
    else:
        pprint("Missing QTE_SCHEDULED_TX_DATA environment variable!")
    upload_to_github(fileList, local_repo)

def upload_to_github(fileList, localrepo):
    local_repo = localrepo
    repo = Repo(local_repo)
    file_list = fileList
    commit_message = 'Add simple text file for new test cases'
    repo.index.add(file_list)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.pull()
    origin.push()

def get_git_url(url, name):
    index = url.rfind('.')
    gitUrl = url[0:index]
    fileName = name + ".txt"
    fileNameUrl = urllib.parse.quote(fileName)
    specificUrl = "{}/blob/master/{}"
    specificUrl = specificUrl.format(gitUrl, fileNameUrl)
    return specificUrl


get_test_runs()
