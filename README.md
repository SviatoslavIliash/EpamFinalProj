## About project
**"Bicycle Repair" web-application which allows bicycle enthusiasts to maintain, upgrade or repair their beloved bicycles by easy online record**
___
## Instalation
1. Setup MySQL, Python3, pip, build, gunicorn, curl
2. Create and activate virtual environment 
3. Install from GitHub: `(venv)mydir> pip install git+https://https://github.com/SviatoslavIliash/EpamFinalProj.git`
4. Create Database: `> mysql -u <root or username> -p -e 'CREATE DATABASE bikerepair'`
5. Create MySql user `CREATE USER 'brepair'@'localhost' IDENTIFIED BY 'admin';`
6. Access MySql user `GRANT ALL PRIVILEGES ON bikerepair.* TO 'brepair'@'localhost';`
7. Run server with Gunicorn `(venv)mydir> gunicorn -w 4 'bikerepair.app:app'`. By default, the server will run on `localhost:8000`.
8. Or run with Flask run `(venv)mydir> flask --app bikerepair.app run`. By default, the server will run on `localhost:5000`.
9. Create database tables and default data `(venv)mydir> curl -X GET http://localhost:port/api/create_db_no_migrations`
10. Or browse to `http://localhost:port/api/create_db_no_migrations`
11. You are ready to use the server `http://localhost:port` (Web or REST API).

## Author
**Sviatoslav Iliash**

## Coveralls and Travis ci status
[![Coverage Status](https://coveralls.io/repos/github/SviatoslavIliash/EpamFinalProj/badge.svg?branch=master)](https://coveralls.io/github/SviatoslavIliash/EpamFinalProj?branch=master)
[![Build Status](https://app.travis-ci.com/SviatoslavIliash/EpamFinalProj.svg?branch=master)](https://app.travis-ci.com/SviatoslavIliash/EpamFinalProj)