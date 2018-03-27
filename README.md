# Dabba App

## Setup
* ##### Dependencies
    * [Docker for Mac](https://download.docker.com/mac/stable/Docker.dmg) - ensure it is running with the whale icon in the menubar
    * [Python 2.7](https://www.python.org/download/releases/2.7/)
    * [MongoDB](https://www.mongodb.com/) - currently run as a docker container so standalone installation is not required
    * *virtualenv* - `pip install virtualenv`
    * (optional) [Robo 3T for Mac](https://download.robomongo.org/1.2.1/osx/robo3t-1.2.1-darwin-x86_64-3e50a65.dmg) - For MongoDB visualisation

* ##### First Time Local Setup
    * `git clone https://github.com/dabba-fyp/dabba-app`
    * `cd dabba-app`
    * `virtualenv venv`
    * `source venv/bin/activate`
    * `sudo pip install -r requirements.txt`
    * `docker rm -f mongodb-docker-dabba` (It's alright if you get *Error: No such container: mongodb-docker-dabba*)
    * `docker run --name mongodb-docker-dabba -p 27017:27017 -d mongo` 
    * `sudo docker exec -it mongodb-docker-dabba mongo admin`
    * `db.createCollection("bin_data")`
    * `use charts`
    * `db.createCollection("views")`
    * `exit`
* ##### Running the app
    * `python app.py`

**Mock Dashboard Setup** - Open `localhost:8080`, create a Dashboard, Click on *Add Widget*, select *Type* as C3 timeseries chart, *Data Source* as `http://localhost:8000/test-chart`, Tick *Use Custom Configuration* on top right, Click *preview* at the bottom to verify that endpoint is right and finally, see the chart on the dashboard in action.

## API Documentation

##### **Note that trailing slash in every endpoint is mandatory**

#### 1. /bins/ [GET, POST, DELETE]

* `GET /bins/` fetches all the bin data in the system
* `POST /bins/` allows to put new data into the system. Example data format below:
    ```
    { 
        "USER_NAME": "piyush",
        "U_ID":"1234",
        "LEVEL":34,
        "TIMESTAMP":"2018-02-20 13:48:09.431429",
        "URL":"http://dropbox.com/someUrl",
        "LAT":"1.12345",
        "LONG":"2.2345",
        "TAGS":[  
          "tag1",
          "tag2",
          "tag3"
        ]
    }
    
    ```
* `DELETE /bins/?u_id="your_u_id"` deletes bin data with specified U_ID in system

    
    
#### 2. /bin/<USER_NAME>/ [GET]

* Fetches all data with bin having USER_NAME as passed, eg `/bins/piyush/`

#### 3. /bin/<USER_NAME>/chart/ [GET]

* Fetches C3js formatted data for plotting all USER_NAME bin data in DB. eg `/bins/piyush/chart/`

#### 4. /bin/<USER_NAME>/chart/yyyy-mm-dd/ [GET]

* Fetches C3js formatted data for plotting data for specified *yyyy-mm-dd* for USER_NAME bin. eg `/bins/piyush/chart/2018-02-20/`

#### 5. /heatmap [GET]

* Shows heatmap
