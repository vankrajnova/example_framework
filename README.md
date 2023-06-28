# Example project for autotests in Python

____________________________________________

## Tools ###

- **Pytest**
- **Selenium**
- **requests**
- **Allure**
- **Docker**
- **Jenkins**
- **paramiko**
- **psycopg2/pymssql**

# Description of the project structure #

- **fixture** - some fixtures that are initialized at the start
- **forms** - the level contains classes Page Object and Page Element
- **helpers** - the level contains the PowerShellHelper class for working with Active Directory due to SSH
- **hr** - the level contains classes for working with Data Bases
- **model** - some classes with object models
- **rest** - the level contains classes for working with REST API
- **steps** - the level contains classes with functions that call functions from rest, forms, hr levels, depending on
  the action mode. Each function contains allure annotation
- **tests** - the level contains tests

# How to start tests #

There is integration with Jenkins to run tests.

**For start job:**

- Add SUITE_NAME - path to test suite what you want to start
- Click Build

![img.png](img.png)

**Job steps**:

1. **Declarative: Checkout SCM** - checkout repository from GitHub
2. **Build image** - create docker image
3. **Run Tests** - run docker container and start tests from ${SUITE_NAME}. The allure-results copy from docker container
   and place to ${WORKSPACE}
4. **Reports** - create a report and add to the build
5. **Post actions** - stop docker container

![img_1.png](img_1.png)

**Allure report generated after build completes**

![img_2.png](img_2.png)