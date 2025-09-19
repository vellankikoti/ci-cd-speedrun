FROM jenkins/jenkins:lts

# Switch to root user to install system dependencies
USER root

# Install Docker CLI, Python3, and other dependencies
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    python3-venv \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Add jenkins user to docker group
RUN groupadd -f docker && usermod -aG docker jenkins

# Fix pip externally-managed environment
RUN rm -f /usr/lib/python*/EXTERNALLY-MANAGED

# Switch back to jenkins user
USER jenkins

# Copy plugins.txt for automatic plugin installation
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Install plugins from plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Skip initial setup wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Create admin user automatically
ENV JENKINS_ADMIN_ID=admin
ENV JENKINS_ADMIN_PASSWORD=admin

# Copy initialization script
COPY init.groovy /usr/share/jenkins/ref/init.groovy.d/

# Expose Jenkins port
EXPOSE 8080
EXPOSE 50000

# Default command
CMD ["/usr/bin/tini", "--", "/usr/local/bin/jenkins.sh"]