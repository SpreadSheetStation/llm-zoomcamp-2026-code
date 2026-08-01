FROM python:3.12-slim

WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Make the start script executable
RUN chmod +x start.sh

# Expose both ports
EXPOSE 8501
EXPOSE 8502

# Run the start script
CMD ["./start.sh"]