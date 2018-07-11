# Upload Git URL to qTest Manager – A Python Script for the Automation Host

## Overview:

This example illustrates how to utilize custom fields with qTest Manager and the Automation Host

## Set up Computer:

1) Install Python 3.6 from [https://www.python.org/downloads/](https://www.python.org/downloads/)


### From Terminal (Mac) or Command Prompt (Windows):

1. Make sure pip was installed correctly with python on your machine by running the following command. It should output the pip version:

 `pip --version`

 Note: pip3 will work as well. Try `pip3 --version`

2. If pip is not installed, run the following command to install pip:

 `python -m -ensurepip --default-pip`

More information about downloading pip can be found at [https://packaging.python.org/tutorials/installing-packages/](https://packaging.python.org/tutorials/installing-packages/)

3. After you have ensured pip is installed, run the following commands individually:

`pip install requests`

`pip install gitpython`


Note: If using pip3 run commands with pip3 instead e.g. `pip3 install requests`

These commands will install the necessary modules required to run the python script.


## Update Configuration File:

**git\_url:** The python script uses the url to clone a repository and send pull/push requests everytime it runs

**local\_repository:** The folder containing the test cases template files. The python script will use this to know where to pull/push to GitHub. 

**qtest\_api\_token:** The token used to authorize the connection to qTest Manager

**qtest\_url:** The personal url that is used to access QASymphony API


Open the conf.json file and update with your personal information. Enter your own qTest URL and API Token found in the qTest Manager Environment.



## Set Up Automation:

1. Navigate to your Automation Host


2. Add a new agent and fill out the path directory and enter the script into the kick off script field


 
**Agent Name:** Name (Git Automation)

**qTest Manager Project:** Choose your project

**Agent Type:** Choose Shell Agent

**Directory:** The directory containing your getscheduledtests.py script

**Set Allocated Execution Time:** Amount of time you expect the script to take to execute in minutes

**Kick-off scripts:**

`python getscheduledtests.py`


 
## Scheduling Tests:

1.  Ensure Automation Status is On, in the Automation Settings


2. Click on Field Settings, choose Test Case Artifact and add a custom field called Git Url. For the field type choose URL. In the next window check searchable, but not required

3. Go to Test Design, create your test case, convert it to an automated test case, approve it, and create a Test Run.

 
4. Go to Test Execution and schedule specific test cases that you want to create Git Urls for and click on schedule under the &quot;More&quot; drop down menu. You can schedule more than one.
 

4. Select the Git Automation shell agent from under the drop down menu for agent, and click ok


5. Now that the tests have been scheduled to start them go back to the Automation Host and click Poll Now.

 
The shell script will create text files and upload them to GitHub, and add the URL to the Git Url custom field in qTest Manager under Test Design.

## Note:

Make sure that your machine is a trusted computer for the GitHub Repository to upload files to by adding an SSH Key, so that during the Automation it does not prompt you for your username and password.


