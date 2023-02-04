FROM demers/python420w4a

COPY ./requirements.txt .
RUN pip install -r requirements.txt && \
        rm requirements.txt

# Copy model files
COPY ./model /model

# Copy app files
COPY ./app /app
WORKDIR /app/
RUN ls -lah /app/*

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]