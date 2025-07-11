#!/bin/bash
set -e

# Kill any process using ports 8080 or 5000
for port in 8080 5000; do
  pid=$(lsof -ti tcp:$port)
  if [ -n "$pid" ]; then
    echo "Killing process on port $port (PID $pid)"
    kill -9 $pid
  fi
done

# Start port-forwarding in background
kubectl port-forward svc/bluegreen-backend-service 5000:5000 -n scaling-challenge &
BACKEND_PID=$!
kubectl port-forward svc/bluegreen-frontend-service 8080:80 -n scaling-challenge &
FRONTEND_PID=$!

# Wait a moment for port-forwarding to be ready
sleep 3

# Check backend API
echo "Checking backend API for pods..."
if curl -s http://localhost:5000/api/pods | jq .; then
  echo "Backend API is returning pods."
else
  echo "ERROR: Backend API is not returning pods. Check backend logs."
fi

# Open frontend in browser
if which xdg-open > /dev/null; then
  xdg-open http://localhost:8080
elif which open > /dev/null; then
  open http://localhost:8080
else
  echo "Please open http://localhost:8080 in your browser."
fi

# Wait for user to exit
echo "Press Ctrl+C to stop port-forwarding."
wait $BACKEND_PID $FRONTEND_PID 