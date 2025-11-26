# 1. Start from a Python 3.9 base image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements file in
COPY requirements.txt .

# 4. Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your main script in
COPY main.py .

# 5.1 Copy any additional files needed (PowerBI file in this case)
COPY index.pbix .

# 6. Command to run the script AND keep the container alive
CMD python main.py && tail -f /dev/null