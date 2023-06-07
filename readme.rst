Document database Readme

Pre-requirements
---------------------------------
* Git for Windows
* TortoiseGit
* Install Python3.8 (https://www.python.org/downloads/release/python-380/)
* Install PostgreSQL (https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
* Install Nodejs (https://nodejs.org/en/download/)



How do I get set up?
---------------------------------

* Clone repository:
    Get clone link by clicking 'Clone' option in bitbucket repository
    Create a folder to clone the Bitbucket repository
    Right-click the new folder and select TortoiseGit -> Clone
    Paste the clone link into the 'URL' box

* Backup database:
    Create user in PgAdmin: 
        Username: 'doc_user' (with superuser privileges)
        Password:  ***
    Create database in PgAdmin:
        Name: 'RGS_db'
        User: 'doc_user'
    Select binary path:
        Open preferences -> Paths -> Binary Paths -> PostgreSQL Binary Path -> Select Postgres bin path
    Right click on 'RGS_db' database select restore option and Select the 'database.backup' file

* Create a virtual environment using "py -3.8 -m venv env_name" 
* Select python interpreter in vscode:
    install python, django extensions
    ctl+shift+p  -> python: select interpreter -> select interpreter path -> Find -> Select python executable from virtual environment folder
    run the following command in PowerShell: set-executionpolicy remotesigned (this will allow to execute scripts)

* install the requirements specified in "requirements.txt" (pip install -r requirement.txt in Terminal)

* Run the following command: "npm install" (in root directory) so that all the "devDependencies" specified in "package.json" are installed. 
* ALERT! If the previous step does not work try: " npm install --save --legacy-peer-deps "

* Run "compile_with_webpack.bat" (located in /scripts)

* Do any necessary migration ("python manage.py migrate").

* Run "python manage.py runserver"

* For the integration tests Download ChromeDriver (https://sites.google.com/a/chromium.org/chromedriver/). Save the executable on a folder and add path to the folder in Windows settings (My Computer -> Properties -> System Properties -> Advanced -> Environment Variables -> Path -> Edit -> New - > (Select folder containing the executable))

* In case you can not access with your new password after forgetting credentials: go to https://www.google.com/recaptcha/admin/site/602951741 and create one with the corresponding domains (localhost and 127.0.0.1)