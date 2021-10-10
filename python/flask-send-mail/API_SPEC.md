# API SPEC

## Get All Event Emails

Request :

- Method : GET
- Endpoint : `/api/event_emails`
- Header :
    - Accept: application/json
- Param:

| Parameter | Required | Valid Options | Default Value | Description |
| :--------:| :------: | :------------:| :-----------: | :---------: |
|include_deleted| No| true, false, 1, 0 | | if True will display all data include soft deleted data |

\
Example:

`localhost:5000/api/event_emails?include_deleted=true`

Response :

- Status: 200 OK

```json 
[
    {
        "event_id": 1,
        "recipients": [
            {
                "email": "irhamdz@gmail.com",
                "name": "Irham Dzuhri",
                "id": 1
            }
        ],
        "timestamp": "2021-04-10T23:00:00",
        "email_content": "Lorem ipsum dolor sir amet praesent sapien massa, convallis a pellentesque nec",
        "is_active": true,
        "id": 1,
        "email_subject": "Future AI Event"
    },
    {
        "event_id": 2,
        "recipients": [
            {
                "email": "irhamdz@gmail.com",
                "name": "Irham Dzuhri",
                "id": 1
            }
        ],
        "timestamp": "2021-04-11T10:05:44",
        "email_content": "Lorem ipsum dolor sir amet praesent sapien massa, convallis a pellentesque nec",
        "is_active": False,
        "id": 2,
        "email_subject": "Jakarta Fair Event"
    }
]
```

## Create Event Emails

Request :

- Method : POST
- Endpoint : `/api/save_emails`
- Header :
    - Conten-Type: application/json
    - Accept: application/json
- Body:

```json
{
  "event_id": 45,
  "email_subject": "Test New Subject",
  "email_content": "Test New Content Email",
  "timestamp": "2021-04-10 23:10:10"
}
```

Response :

- Status: 201 Created

```json 
{
    "event_id": 45,
    "recipients": [],
    "timestamp": "2021-04-10T23:10:10",
    "email_content": "Test New Content Email",
    "is_active": true,
    "id": 3,
    "email_subject": "Test New Subject"
}
```

## Get Detail Event Emails

Request :

- Method : GET
- Endpoint : `/api/event_emails/<id>`
- Header :
    - Accept: application/json

Example:

`localhost:5000/api/event_emails/1`

Response :

- Status: 200 OK

```json 
{
    "event_id": 1,
    "recipients": [
        {
            "email": "irhamdz@gmail.com",
            "name": "Irham Dzuhri",
            "id": 1
        }
    ],
    "timestamp": "2021-04-10T23:00:00",
    "email_content": "Lorem ipsum dolor sir amet praesent sapien massa, convallis a pellentesque nec",
    "is_active": true,
    "id": 1,
    "email_subject": "Future AI Event"
}
```

## Patch Event Emails

Request :

- Method : PATCH
- Endpoint : `/api/event_emails/<id>`
- Header :
    - Accept: application/json

Example :

`localhost:5000/api/event_emails/1`

- Body:

```json
{
  "event_id": 45,
  "email_subject": "Test New Subject",
  "email_content": "Test New Content Email",
  "timestamp": "2021-04-10 23:10:10"
}
```

Response :

- Status: 200 OK

```json 
{
    "event_id": 45,
    "recipients": [
        {
            "email": "irhamdz@gmail.com",
            "name": "Irham Dzuhri",
            "id": 1
        }
    ],
    "timestamp": "2021-04-10T23:10:10",
    "email_content": "Test New Content Email",
    "is_active": true,
    "id": 1,
    "email_subject": "Test New Subject"
}
```

## Delete Events Email

Request :

- Method : DELETE
- Endpoint : `/api/event_emails/<id>`
- Header :
    - Content-Type: application/json
    - Accept: application/json

Response :

- Status: 204 No Content

## Get All Recipients

Request :

- Method : GET
- Endpoint : `/api/recipients`
- Header :
    - Accept: application/json

Example:

`localhost:5000/api/recipients`

Response :

- Status: 200 OK

```json 
[
    {
        "email": "irhamdz@gmail.com",
        "name": "Irham Dzuhri",
        "id": 1
    }
]
```

## Create Recipient

Request :

- Method : POST
- Endpoint : `/api/recipients`
- Header :
    - Conten-Type: application/json
    - Accept: application/json
- Body:

```json
{
  "name": "new recipient",
  "email": "new-recipient@gmail.com"
}
```

Response :

- Status: 201 Created

```json 
{
    "email": "new-recipient@gmail.com",
    "name": "new recipient",
    "id": 2
}
```

## Get Detail Recipient

Request :

- Method : GET
- Endpoint : `/api/recipients/<id>`
- Header :
    - Accept: application/json

Example:

`localhost:5000/api/recipients/2`

Response :

- Status: 200 OK

```json 
{
    "email": "new-recipient@gmail.com",
    "name": "new recipient",
    "id": 2
}
```

## Patch Recipient

Request :

- Method : PATCH
- Endpoint : `/api/recipient/<id>`
- Header :
    - Accept: application/json

Example :

`localhost:5000/api/recipients/2`

- Body:

```json
{
  "name": "latest new recipient"
}
```

Response :

- Status: 200 OK

```json 
{
    "email": "new-recipient@gmail.com",
    "name": "latest new recipient",
    "id": 2
}
```

## Delete Recipient

Request :

- Method : DELETE
- Endpoint : `/api/recipient/<id>`
- Header :
    - Content-Type: application/json
    - Accept: application/json

Response :

- Status: 204 No Content

