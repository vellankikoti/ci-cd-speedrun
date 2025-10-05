# 🚨 BLOATED DOCKERFILE - Anti-Pattern Demo
# This demonstrates common Docker mistakes that create massive images
# Shows what NOT to do in production

FROM python:3.10

# Install unnecessary packages (BAD - but fast)
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

# Install Node.js packages (BAD - no package.json)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g \
    create-react-app \
    vue-cli \
    angular-cli \
    express-generator \
    nodemon \
    pm2 \
    webpack \
    babel \
    eslint \
    prettier \
    typescript \
    jest \
    mocha \
    chai \
    sinon

# Copy entire project (BAD - includes unnecessary files)
COPY . /app
WORKDIR /app

# Copy the bloated app specifically
COPY bloated_app.py /app/app.py

# Install more packages (BAD - redundant)
RUN pip install --upgrade pip
RUN pip install flask-cors flask-restful flask-migrate

# Create unnecessary files (BAD - bloats image)
RUN mkdir -p /app/logs /app/temp /app/cache /app/uploads
RUN echo "This is a bloated Docker image" > /app/README.txt
RUN echo "Built on $(date)" > /app/build-info.txt

# Set environment variables (BAD - hardcoded)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV DEBUG=True
ENV SECRET_KEY=hardcoded-secret-key
ENV DATABASE_URL=sqlite:///app.db

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
