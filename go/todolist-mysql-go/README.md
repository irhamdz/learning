# Introduction
Todo list MySQL API Written in Golang

# Get Started
- run the container
```bash
docker-compose up -d
```

- run app
```bash
go run main.go
```

# API SPEC
## Get All Todo

Request :
- Method : GET
- Endpoint : `/todo`
- Header :
    - Accept: application/json

Response :
- Status: 200 OK

```json 
[
    {
        "ID": 1,
        "Description": "test",
        "Completed": false
    },
    {
        "ID": 2,
        "Description": "todo ke 2",
        "Completed": false
    },
    {
        "ID": 3,
        "Description": "testing",
        "Completed": true
    }
]
```

## Get Todo With Status Completed

Request :
- Method : GET
- Endpoint : `/todo-completed`
- Header :
    - Accept: application/json

Response :
- Status: 200 OK

```json 
[
    {
        "ID": 1,
        "Description": "test",
        "Completed": false
    },
    {
        "ID": 2,
        "Description": "todo ke 2",
        "Completed": false
    }
]
```

## Get Todo With Status Incompleted

Request :
- Method : GET
- Endpoint : `/todo-incompleted`
- Header :
    - Accept: application/json

Response :
- Status: 200 OK

```json 
[
    {
        "ID": 3,
        "Description": "testing",
        "Completed": true
    }
]
```

## Create Todo

Request :
- Method : POST
- Endpoint : `/todo/`
- Header :
    - Content-Type: application/json
    - Accept: application/json
- Body :

```json
{
    "description": "learn golang"
}
```

Response :
- Status: 201 Created

```json 
{
    "ID": 1,
    "Description": "learn golang",
    "Completed": false
}
```

## Update Todo

Request :
- Method : PUT, PATCH
- Endpoint : `/todo/{id}`
- Header :
    - Content-Type: application/json
    - Accept: application/json
- Body :

```json
{
    "description": "update learn golang",
    "completed": "true"
}
```

Response :
- Status: 204 No Content

## Delete Todo

Request :
- Method : DELETE
- Endpoint : `/todo/{id}`
- Header :
    - Content-Type: application/json
    - Accept: application/json

Response :
- Status: 204 No Content