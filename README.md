# GitGurus-Project


# Project Overview

The Crime App is a web-based application that provides users with violent crime statistics in different states across the United States of America, with a particular focus on crime statistics in Denver, Colorado. The application is designed to help users understand the prevalence and nature of violent crimes in different locations.

Users of the Crimalysis application can access detailed data on violent crime rates in different states and report crime anonymously. The data is presented in an easily understandable format, with interactive charts and maps that allow users to explore crime statistics in different locations and over different time periods.


Login page details in the web form

<img width="366" alt="Screenshot 2023-05-04 at 1 32 08 AM" src="https://user-images.githubusercontent.com/70309623/236139047-f130915e-61ea-4fdb-a54b-b8d5b9be3088.png">


Publicly Accessible URL : https://gitgurus-fse.herokuapp.com/login


# Project Rubric


* [Web application basic form, reporting](https://gitgurus-fse.herokuapp.com/login)


* [Data collection](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/app.py#L40)
   * This code is used to collect data on crime rates in the US between 1975 and 2015. The data is obtained from a database using a ```SQL``` query, which is executed using the psycopg2 library. The query retrieves all data from a tabl


* [Data analyzer](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/app.py#L80)

    * Description for Data Analyzer: To explore our Crime data we are identifying the patterns and trends to understand and derive insights for the data.


* [Unit tests](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/test_app.py)
  * The unit test is written using the Python built-in unittest framework. It tests various aspects of a Flask-based web application, which have multiple pages and routes. The purpose of the tests is to ensure that the application behaves correctly in different scenarios and with different inputs.


* [Data persistence any data store](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/source/connector.py)


* [API endpoint](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/app.py#L474)


* Product environment:

    * Created staging and production pipeline.
The staging pipeline is used for testing new changes before they are deployed to the production environment, allowing developers to catch and fix issues before they affect end-users. The production pipeline, on the other hand, is used to deploy new changes to the live application and ensure that it is running smoothly.


![Production environment](https://user-images.githubusercontent.com/78723743/236376001-2a5eda16-8bc4-4d34-9de1-c12a249d6fe0.jpeg)


* [Integration tests](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/test_integration.py)


    * [Description for Integration Tests]( https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/wiki/Test-Cases#integration-tests)


* Using mock objects or any test doubles
  * In software testing, mock objects and test doubles are both used to replace real objects or dependencies with simplified, pre-programmed objects that can simulate their behavior. This is done to isolate the unit under test (i.e., the code being tested) and ensure that it is functioning properly, free of external factors or dependencies.


* Production monitoring instrumenting:

    * Added the New Relic addon to a Heroku app allowing for real-time monitoring of the application's performance, logs, and metrics. It provides a range of features, such as transaction tracing, error analytics, database monitoring, and custom dashboards, that can help identify performance bottlenecks, errors, and potential issues before they affect end-users. Integrating this with our Heroku app helped gain visibility into how the app is behaving, what is causing errors, and how to optimize its performance.


![Production monitoring](https://user-images.githubusercontent.com/78723743/236375608-ab053381-a4b1-4a62-87cb-3062f0beedc3.jpeg)


* [Acceptance tests](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/test_acceptance.py)


    * [Description for Acceptance tests](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/wiki/Test-Cases#acceptance-tests)


* [Event collaboration messaging](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/templates/error.html)
    * We have used Kafka for displaying the Flask error logs.


* [Continuous delivery and integration](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/.github/workflows/heroku.yml)


    * [Description for Continuous delivery and integration](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/wiki/Git-Gurus#continuous-integration-and-continuous-deployment)

    * [Docker File](https://github.com/CSCI-5828-Foundations-Sftware-Engr/GitGurus-Project/blob/main/Dockerfile)


![CICD](https://user-images.githubusercontent.com/78723743/236375857-4180db3c-35be-4265-bda5-e9edb7cc7474.jpeg)
