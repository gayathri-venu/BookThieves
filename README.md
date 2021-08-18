# BookThieves


 Web app for book exchange and reviewing.
 
 
 [Click here for Project Report](https://docs.google.com/document/d/1T4WCYEWISYQjbR0i_J3c6fc4yFabrG_26JjDYRGWbfw/edit?usp=sharing)


# Installation

* Fork & Clone the repo
```
  git clone https://github.com/[yourname]/BookThieves.git
```

* Navigate through the project
```
  cd BookThieves
```
* Install all requirements
  ``` 
  pip install -r requirements.txt
  ```
  
* Run :
  ```
  python3 main.py
  ```
  
* Copy the localhost url (usually localhost:5000/) and paste in browser



## The databases in the system

1. User
2. Book : Keeps track of all books 
3. Review : Keeps track of all reviews posted by  a user
4. Request : Keeps track of the exchange requests made by users


## File structure

```
| static

   | layout.css

| templates  Contains all the html files

   | index.html
   | register.html
   | login.html
   .....
| Main.py : Contains all the python code    
| db.sqlite3 : The database used is sqlite3
| requirements.txt : contains the list of all dependencies to be installed
| README.md

