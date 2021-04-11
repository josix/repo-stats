FROM python:3.8.2

ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/repo_stats


# Adding backend directory to make absolute filepaths consistent across services
WORKDIR $APP_DIR

# Install Python dependencies
RUN pip install pipenv
COPY Pipfile* $APP_DIR
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip3 install --upgrade pip -r $APP_DIR/requirements.txt
# Add the rest of the code
COPY . $APP_DIR

# Make port 8000 available for the app
EXPOSE 8000
 
# Be sure to use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won't be able to find it
CMD ["uvicorn", "repo_stats.main:app", "--host", "0.0.0.0", "--port", "8000"]
