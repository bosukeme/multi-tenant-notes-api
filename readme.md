# Multi-Tenant Notes API

A multi-tenant note management system with organization-level isolation, role-based access control for note access. <br/>
It features full CRUD endpoints, request rate limiting, centralized error handling, and tenant-aware MongoDB isolation via Beanie ODM using FastAPI as a web-framework

## Features

- Multi-organization (tenant) structure
- Role-based access control: admin, writer, reader
- CRUD for organizations, users, and notes
- Request rate limiting per router
- Centralized error & exception handling
- MongoDB persistence via Beanie ODM
- Full test coverage with pytest and httpx.AsyncClient
- Docker + Docker Compose setup

## Tech Stack
- Backend: FastAPI + Python 3.x
- Database: MongoDB with Beanie ODM
- Testing: pytest + httpx
- SlowAPI: Rate limiting middleware
- Deployment: Docker + Docker Compose


## Set Up
#### Clone Repo
```sh
git clone https://github.com/bosukeme/multi-tenant-notes-api.git
cd multi-tenant-notes-api
```

#### Configure environment variables:
```sh
MONGO_URI=
DB_NAME=multi_tenant_notes_db
```

#### Docker Setup
1. Run Docker compose
```sh
docker compose up --build
```

2. Access the API
```sh
API Server: http://localhost:8000
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

#### Local Setup
1. Create Virtual Environment and Install Dependencies
```sh
python -m venv venv

venv\Scripts\activate    # (Windows)
source venv/bin/activate #(macOS/Linux)

pip install -r requirements.txt
```

2. Run FastAPI Server
```sh
unvicorn src.main:app --reload
```

3. Access the API
```sh
API Server: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
```


## Example Requests

#### Organization
1. `POST /organizations/`
```sh
curl -X POST http://localhost:8000/organizations/ \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Techify Labs",
        "description": "An AI-driven research company"
      }'

```

2. `GET /organizations/` 
```sh
curl -X GET http://localhost:8000/organizations/
```

#### Users
1. `POST /organizations/{org_id}/users/`
```sh
curl -X POST http://localhost:8000/organizations/{org-id}/users/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "user1@example.com",
        "full_name": "User One",
        "role": "writer"
      }'
```

2. `GET /organizations/` 
```sh
curl -X GET http://localhost:8000/organizations/{org-id}/users/
```


#### Notes
1. `POST /notes/`
```sh
curl -X POST http://localhost:8000/notes/ \
  -H "Content-Type: application/json" \
  -H "X-Org-ID: {org-id}" \
  -H "X-User-ID: {user-id}" \
  -d '{
    "title": "Project Update",
    "content": "Completed phase one of the migration plan."
  }'

```

2. `GET /notes/` 
```sh
curl -X GET http://localhost:8000/notes/ \
  -H "X-Org-ID: {org-id}" \
  -H "X-User-ID: {user-id}"

```

3. `GET /notes/{note_id}` 
```sh
curl -X GET http://localhost:8000/notes/{note_id} \
  -H "X-Org-ID: {org-id}" \
  -H "X-User-ID: {user-id}"
```

4. `DELETE /notes/{note_id}` 
```sh
curl -X DELETE http://localhost:8000/notes/{note_id} \
  -H "X-Org-ID: {org-id}" \
  -H "X-User-ID: {user-id}"
```


### Running Tests
```sh
pytest -v
```


## Contributing

If you would like to contribute, please follow these steps:

1. Fork repo.
2. Create feature branch: `git checkout -b feature/your-feature`.
3. Commit changes and push.
4. Open a Pull Request.

## Author

Ukeme Wilson

- <a href="https://www.linkedin.com/in/ukeme-wilson-4825a383/">Linkedin</a>.
- <a href="https://medium.com/@ukemeboswilson">Medium</a>.
- <a href="https://www.ukemewilson.site/">Website</a>.
