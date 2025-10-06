# 💥 FRAGILE DOCKERFILE - Resilience Anti-Pattern Demo
# This demonstrates common Docker resilience mistakes that create fragile containers
# Shows what NOT to do in production

FROM python:3.10

# Install unnecessary packages (BAD - bloats image)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    tree \
    unzip \
    zip \
    tar \
    gzip \
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    autoconf \
    automake \
    libtool \
    pkg-config \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages (BAD - no requirements.txt)
RUN pip install \
    flask \
    django \
    fastapi \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scikit-learn \
    requests \
    beautifulsoup4 \
    selenium \
    pytest \
    coverage \
    black \
    flake8 \
    mypy \
    isort \
    pre-commit

# Copy entire project (BAD - includes unnecessary files)
COPY . /app
WORKDIR /app

# Copy the fragile app specifically
COPY fragile_app.py /app/app.py

# Install more packages (BAD - redundant)
RUN pip install --upgrade pip
RUN pip install flask-cors flask-restful flask-migrate

# Create unnecessary files (BAD - bloats image)
RUN mkdir -p /app/logs /app/temp /app/cache /app/uploads
RUN echo "This is a fragile Docker image" > /app/README.txt
RUN echo "Built on $(date)" > /app/build-info.txt

# Set environment variables (BAD - no resilience configuration)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV DEBUG=True
ENV SECRET_KEY=super-secret-key-123
ENV DATABASE_URL=sqlite:///app.db

# NO HEALTH CHECK (BAD - no failure detection)
# NO RESTART POLICY (BAD - manual recovery required)
# NO RESOURCE LIMITS (BAD - will crash from exhaustion)

# Expose port
EXPOSE 5000

# Run application as root (BAD - security risk!)
CMD ["python", "app.py"]
