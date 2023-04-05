FROM python:3.10-slim-buster AS base


# copy project
RUN mkdir /users_api
COPY ./users_api /users_api/
COPY ./tests /tests/
COPY ./scripts /scripts/
COPY ./pyproject.toml /
COPY ./README.md /
COPY ./poetry.lock /

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install poetry==1.4.0
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# set work directory
WORKDIR /users_api

# idea to separate development and production stages using multi-stage builds
# seen from: https://blog.atulr.com/docker-local-production-image/
FROM base AS development

# installs editable packages to code in users_db package to be up to date
# runs migrations and starts server with reload option to detect changes 
# and restart the server automatically

CMD ["/bin/bash", "-c",  \
     "/scripts/install_editable_packages.sh && \
      /scripts/migrate.sh && \
      uvicorn app:app --host 0.0.0.0 --reload" ]

FROM base AS production
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]