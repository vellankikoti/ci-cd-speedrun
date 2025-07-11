# 🚀 Scenario 04 — Docker Layer Analyzer Lab

---

## 🎯 Scenario Goal

**Mission:**  
Turn learners from Dockerfile scribblers into Docker surgeons who:

✅ Understand Docker layers deeply  
✅ Know how layer order affects:
- build speed
- cache efficiency
- image size
✅ Master multi-stage builds for production-ready images  
✅ Gain instant visual insight into:
- Layer commands
- Layer sizes
- Cache hits/misses
✅ Learn via a **fun, interactive, gamified experience**

---

## 💡 High-Level Concept

We'll build:

✅ A **universal Docker learning lab utility**:

- CLI-driven interactive tool
- Learners select:
    - Technology (Python, Jenkins, Node.js, etc.)
    - Scenario level (bad, good, best)
- Each scenario:
    - Builds a real Docker image
    - Captures:
        - build time
        - image size
        - per-layer data
- Automatically launches a local **web UI** showing:
    - Layer breakdown tree
    - Per-layer size
    - Build logs
    - Image history visualization
- Gamified scoring system:
    - Learners try to reach best scores:
        - fastest builds
        - smallest images
        - cleanest Dockerfiles

---

## ✅ Features Overview

✅ 5 Technologies:
- Python
- Jenkins
- Node.js
- Golang
- Nginx

✅ 3 Dockerfile Scenarios for each:
- Bad → naive, large images
- Optimized → layered correctly
- Multi-Stage → minimal production images

✅ Interactive CLI prompts

✅ After each build:
- Total build time
- Total image size
- Visual per-layer breakdown:
    - layer command
    - size
    - cache status
- Comparison graphs:
    - Bad vs Optimized vs Multi-stage

✅ Real app running:
- Web app accessible in browser
- Shows app’s output → visible differences

✅ Clean-up routines

---

# ✅ Folder Structure

```

docker-layer-lab/
│
├── dockerfiles/
│    ├── python/
│    │     ├── bad.Dockerfile
│    │     ├── optimized.Dockerfile
│    │     └── multistage.Dockerfile
│    ├── jenkins/
│    │     ...
│    ├── nodejs/
│    │     ...
│    ├── golang/
│    │     ...
│    └── nginx/
│          ...
│
├── scripts/
│     └── docker-lab.sh
│
├── webui/
│     ├── app.py
│     ├── templates/
│     │      └── results.html
│     └── static/
│            └── js/
│
└── results/
├── build\_logs.txt
├── layer\_data.json
└── summary.txt

````

---

# ✅ CLI User Journey

---

## Step 1 — Run Lab

```bash
./docker-lab.sh
````

---

## Step 2 — Choose Technology

```
Choose a technology:

1. Python
2. Jenkins
3. Node.js
4. Golang
5. Nginx

Enter choice:
```

---

## Step 3 — Choose Scenario Type

```
Choose Dockerfile type:

1. Standard (BAD)
2. Optimized (GOOD)
3. Multi-stage (BEST)

Enter choice:
```

---

## Step 4 — Build Kicks Off

```
Building Dockerfile...
-----------------------------------
[DOCKER BUILD LOGS...]
-----------------------------------

Total build time: 18.3 seconds
Final image size: 348 MB

Layers built:
- FROM python:3.10     - 125 MB
- RUN pip install ...  - 150 MB
- COPY app.py ...      - 20 MB
- ...

[ View in Browser → http://localhost:5000/results ]
```

---

## Step 5 — Browser UI

---

### Display:

✅ Dockerfile content (syntax highlighted)
✅ Layer tree:

```
FROM python:3.10    → 125 MB
  RUN pip install   → 150 MB
  COPY app.py       → 20 MB
```

✅ Click any layer → popover shows:

* Docker command
* Size
* Cache hit/miss info

✅ Graphs:

* Build time
* Image size
* Bad vs Good vs Best

✅ Run app directly from UI:

* Preview e.g. Flask web page
* Jenkins UI
* etc.

---

# ✅ Scenario Examples

---

## Technology: Python

---

### **BAD Dockerfile**

```Dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

✅ Big problems:

* No pinning of dependencies
* COPY . . breaks cache
* Huge images

---

### **Optimized Dockerfile**

```Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

✅ Better:

* Cacheable dependency layer
* Smaller context
* Faster rebuilds

---

### **Multi-Stage Dockerfile**

```Dockerfile
FROM python:3.10 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --target=/deps -r requirements.txt
COPY app.py .

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /deps /usr/local/lib/python3.10/site-packages
COPY app.py .
CMD ["python", "app.py"]
```

✅ Best:

* Small final image
* Minimal attack surface

---

# ✅ How We'll Implement It

---

## **docker-lab.sh**

✅ Prompts user for choices
✅ Copies correct Dockerfile into temp build context
✅ Times:

```bash
time docker build -t my-lab-image -f selected.Dockerfile .
```

✅ Captures:

```bash
docker history --no-trunc --format '{{json .}}' my-lab-image
```

✅ Parses output → JSON:

```json
[
  {
    "ID": "...",
    "Size": "25.3MB",
    "CreatedBy": "RUN pip install ...",
    "Comment": "",
    ...
  }
]
```

✅ Launches:

```bash
python3 webui/app.py
```

---

## **Web UI Features**

✅ Flask app displays:

* Dockerfile text
* Build logs
* Total build time
* Final image size
* Interactive tree view of layers
* Graphs:

  * Layer sizes
  * Build times

✅ Click layer node → shows:

* Command
* Size
* Whether layer was cached

✅ Shows app output:

* e.g. Flask running
* or Jenkins UI
* etc.

---

# ✅ Gamification

✅ Score each build:

* Slow builds → penalty
* Big images → penalty
* Multi-stage → bonus

✅ Display:

```
Your optimization score: 82/100
```

---

# ✅ Cleanup

After each test:

```bash
docker rm -f my-lab-image
docker rmi my-lab-image
```

---

