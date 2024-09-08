# kidsnews-api


Child-Friendly News Feed API. Check out the project's [documentation](http://mdamire.github.io/kidsnews-api/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  


# Starting the server

Start the dev server:
```bash
docker-compose up app
```

Run a command inside the docker container:

```bash
docker-compose run --rm app [command]
```

# Admin usage
Create super user:
```bash
docker compose run app python manage.py createsuperuser
```

Access the admin at http://localhost:8000/admin


# Fetching the news data
It grabs the the from [newsapi](https://newsapi.org/docs/endpoints/everything) and filters and recreates using chatgpt. 
It uses both parallel and concurrent computing to fetch the create the data.

To make sure the this functionality work add `TNA_API_KEY` and `CHATGPT_API_KEY` environemnt variables in `compose.yaml` file's app service configuration.

#### Mannual process
Fetch a data manually between a time period:
```bash
python manage.py fetch_articles '2024-09-01' '2024-09-02'
```

#### Automated process
There is a celery beat schedule that runs every 6 hours and generates last 6 hours news.

# Endpoints
#### Authentication
Create user by using superuser command or from admin. Use the user's username and password for basic http authentication.
These endpoint has a ratelimit of 1000 requests per hour.

#### GET - /api/articles
- return list of articles
- Filter keys:
    - author
    - published_at
    - published_at_gte
    - published_at_lte
- Can be searched via title

#### GET - /api/article/{id}
- returns details of an article
