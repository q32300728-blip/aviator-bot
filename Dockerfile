FROM python:3.10-slim

# ব্রাউজার চালানোর জন্য প্রয়োজনীয় সিস্টেম ডিপেন্ডেন্সি ইনস্টল করা
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libgconf-2-4 \
    libxi6 \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright বা Selenium ব্রাউজার বাইনারি ইনস্টল করা
RUN playwright install --with-deps chromium

COPY . .

CMD ["python", "app.py"]
