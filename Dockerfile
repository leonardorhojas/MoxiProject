FROM python:3.10

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Default command to run when the container starts
CMD ["sh", "-c", "python3.10 manage.py migrate && python3.10 manage.py runserver 0.0.0.0:8000"]
