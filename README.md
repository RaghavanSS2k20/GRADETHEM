# GRADETHEM

This is a basic **Flask application** that was build to understand the core concepts of flask and assosiated libraries.


## Concepts used

   - **Flask**
   - **Flask blueprints**
   - **SQLAlchemy**
   - **Marshmallow**
   - **Gunicorn** as server for better scalability in production environment
   
   finally tested with **pytest** framework 
   

## Application 

There are 4 resources:
- Users
- Students
- Teachers
- Assignments

4 Users (2 students and 2 teachers) have already been created for you in the db fixture

- A student can create and edit a draft assignment
- A student can list all his created assignments
- A student can submit a draft assignment to a teacher
- A teacher can list all assignments submitted to him
- A teacher can grade an assignment submitted to him




## APIs
### Auth
- header: "X-Principal"
- value: {"user_id":1, "student_id":1}

For APIs to work you need a principal header to establish identity and context

### GET /student/assignments

List all assignments created by a student
```
headers:
X-Principal: {"user_id":1, "student_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T02:53:45.028101",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T02:53:45.034289"
        },
        {
            "content": "THESIS T1",
            "created_at": "2021-09-17T02:53:45.028876",
            "grade": null,
            "id": 2,
            "state": "DRAFT",
            "student_id": 1,
            "teacher_id": null,
            "updated_at": "2021-09-17T02:53:45.028882"
        }
    ]
}
```

### POST /student/assignments

Create an assignment
```
headers:
X-Principal: {"user_id":2, "student_id":2}

payload:
{
    "content": "some text"
}

response:
{
    "data": {
        "content": "some text",
        "created_at": "2021-09-17T03:14:08.572545",
        "grade": null,
        "id": 5,
        "state": "DRAFT",
        "student_id": 1,
        "teacher_id": null,
        "updated_at": "2021-09-17T03:14:08.572560"
    }
}
```

### POST /student/assignments

Edit an assignment
```
headers:
X-Principal: {"user_id":2, "student_id":2}

payload:
{
    "id": 5,
    "content": "some updated text"
}

response:
{
    "data": {
        "content": "some updated text",
        "created_at": "2021-09-17T03:14:08.572545",
        "grade": null,
        "id": 5,
        "state": "DRAFT",
        "student_id": 1,
        "teacher_id": null,
        "updated_at": "2021-09-17T03:15:06.349337"
    }
}
```

### POST /student/assignments/submit

Submit an assignment
```
headers:
X-Principal: {"user_id":1, "student_id":1}

payload:
{
    "id": 2,
    "teacher_id": 2
}

response:
{
    "data": {
        "content": "THESIS T1",
        "created_at": "2021-09-17T03:14:01.580467",
        "grade": null,
        "id": 2,
        "state": "SUBMITTED",
        "student_id": 1,
        "teacher_id": 2,
        "updated_at": "2021-09-17T03:17:20.147349"
    }
}
```





### GET /teacher/assignments

List all assignments submitted to this teacher
```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:14:01.584644"
        }
    ]
}
```

### POST /teacher/assignments/grade

Grade an assignment
```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

payload:
{
    "id":  1,
    "grade": "A"
}

response:
{
    "data": {
        "content": "ESSAY T1",
        "created_at": "2021-09-17T03:14:01.580126",
        "grade": "A",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2021-09-17T03:20:42.896947"
    }
}
```

## PYTEST COVERAGE
![Capture](https://user-images.githubusercontent.com/76263002/217569137-71c6ea14-d647-4e1c-8199-f98c1c1b6cf8.PNG)

