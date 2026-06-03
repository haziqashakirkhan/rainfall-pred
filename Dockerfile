FROM python:3.10-slim

# Create a non-root user for security
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=user . .

# Expose the default port for Hugging Face Spaces
EXPOSE 7860

# Run the app with gunicorn binding to port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
