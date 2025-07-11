# 📊 Metrics and Monitoring for Auto-scaling

**Comprehensive guide to monitoring Kubernetes auto-scaling performance**

---

## 🎯 **MONITORING OVERVIEW**

### **Why Monitor Auto-scaling?**
- 📈 **Validate scaling effectiveness** - Is HPA responding appropriately?
- 💰 **Optimize costs** - Are you over or under-provisioning resources?
- 🔍 **Troubleshoot issues** - Why didn't scaling work as expected?
- 📊 **Improve performance** - Fine-tune scaling policies for better results
- 🚨 **Prevent incidents** - Early warning of scaling problems

### **Monitoring Stack Components:**
1. **Metrics Server** - Core Kubernetes resource metrics
2. **HPA Controller** - Scaling decisions and status
3. **Application Metrics** - Custom business metrics
4. **Infrastructure Metrics** - Node and cluster health
5. **Alerting System** - Proactive issue detection

---

## 📡 **METRICS SERVER SETUP**

### **Verify Metrics Server Installation:**
```bash
# Check if metrics server is running
kubectl get deployment metrics-server -n kube-system

# Test metrics availability
kubectl top nodes
kubectl top pods -n scaling-challenge

# Check metrics server logs
kubectl logs -n kube-system -l k8s-app=metrics-server
```

### **Metrics Server Configuration:**
```yaml
# For local development clusters (Docker Desktop/Minikube)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-server
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - name: metrics-server
        image: k8s.gcr.io/metrics-server/metrics-server:v0.6.4
        args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
        # For local development only:
        - --kubelet-insecure-tls
```

### **Metrics Server Troubleshooting:**
```bash
# Common fixes for metrics server issues

# 1. Restart metrics server
kubectl rollout restart deployment/metrics-server -n kube-system

# 2. Check node connectivity
kubectl get nodes -o wide

# 3. Verify kubelet metrics endpoint
curl -k https://<node-ip>:10250/metrics

# 4. Check metrics server service
kubectl get svc metrics-server -n kube-system
```

---

## 📊 **CORE HPA METRICS**

### **Essential HPA Metrics to Monitor:**

#### **1. Replica Metrics:**
```bash
# Current vs desired replicas
kubectl get hpa -n scaling-challenge -o custom-columns=\
NAME:.metadata.name,\
CURRENT:.status.currentReplicas,\
DESIRED:.status.desiredReplicas,\
MIN:.spec.minReplicas,\
MAX:.spec.maxReplicas
```

#### **2. CPU Utilization Metrics:**
```bash
# Current CPU utilization vs target
kubectl get hpa scaling-demo-app-hpa -n scaling-challenge -o json | \
jq '.status.currentMetrics[0].resource.current.averageUtilization, .spec.metrics[0].resource.target.averageUtilization'
```

#### **3. Scaling Events:**
```bash
# Recent scaling events
kubectl get events -n scaling-challenge \
  --field-selector involvedObject.name=scaling-demo-app-hpa \
  --sort-by='.lastTimestamp'
```

#### **4. HPA Conditions:**
```bash
# HPA health status
kubectl get hpa scaling-demo-app-hpa -n scaling-challenge -o json | \
jq '.status.conditions[] | {type: .type, status: .status, reason: .reason}'
```

### **Key Metrics Explained:**

#### **Current vs Desired Replicas:**
- **Current Replicas:** How many pods are actually running
- **Desired Replicas:** How many pods HPA wants to run
- **Gap indicates:** Scaling lag or issues

#### **CPU Utilization:**
- **Current Utilization:** Actual CPU usage across all pods
- **Target Utilization:** What HPA is trying to maintain (50%)
- **Formula:** `(actual_cpu_usage / cpu_requests) * 100`

#### **Scaling Conditions:**
- **AbleToScale:** Can HPA make scaling decisions?
- **ScalingActive:** Is HPA monitoring metrics?
- **ScalingLimited:** Has HPA hit min/max bounds?

---

## 🔍 **PROMETHEUS INTEGRATION**

### **HPA Metrics in Prometheus:**

#### **Core HPA Metrics:**
```promql
# Current replica count
kube_horizontalpodautoscaler_status_current_replicas{namespace="scaling-challenge"}

# Desired replica count
kube_horizontalpodautoscaler_status_desired_replicas{namespace="scaling-challenge"}

# Target CPU utilization
kube_horizontalpodautoscaler_spec_target_metric{namespace="scaling-challenge"}

# Current CPU utilization
kube_horizontalpodautoscaler_status_current_metrics_average_utilization{namespace="scaling-challenge"}

# Min/Max replica bounds
kube_horizontalpodautoscaler_spec_min_replicas{namespace="scaling-challenge"}
kube_horizontalpodautoscaler_spec_max_replicas{namespace="scaling-challenge"}
```

#### **Scaling Rate Metrics:**
```promql
# Scaling events per hour
increase(kube_horizontalpodautoscaler_status_desired_replicas[1h])

# Scaling frequency (events per minute)
rate(kube_horizontalpodautoscaler_status_desired_replicas[5m]) * 60

# Time between scaling events
timestamp() - timestamp(kube_horizontalpodautoscaler_status_desired_replicas != kube_horizontalpodautoscaler_status_desired_replicas offset 1m)
```

#### **Resource Efficiency Metrics:**
```promql
# CPU efficiency (actual usage vs requests)
(
  rate(container_cpu_usage_seconds_total{namespace="scaling-challenge"}[5m]) /
  kube_pod_container_resource_requests{resource="cpu",namespace="scaling-challenge"}
) * 100

# Memory efficiency
(
  container_memory_working_set_bytes{namespace="scaling-challenge"} /
  kube_pod_container_resource_requests{resource="memory",namespace="scaling-challenge"}
) * 100

# Pod utilization (running vs desired)
kube_deployment_status_replicas_ready{namespace="scaling-challenge"} /
kube_horizontalpodautoscaler_status_desired_replicas{namespace="scaling-challenge"}
```

### **Custom Application Metrics:**
```promql
# Application-specific metrics for scaling
# Request rate
sum(rate(http_requests_total{namespace="scaling-challenge"}[5m]))

# Response time percentiles
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{namespace="scaling-challenge"}[5m]))

# Error rate
sum(rate(http_requests_total{status=~"5..",namespace="scaling-challenge"}[5m])) /
sum(rate(http_requests_total{namespace="scaling-challenge"}[5m]))

# Active connections
sum(http_active_connections{namespace="scaling-challenge"})
```

---

## 📈 **GRAFANA DASHBOARDS**

### **HPA Overview Dashboard:**
```json
{
  "dashboard": {
    "title": "HPA Auto-scaling Overview",
    "panels": [
      {
        "title": "Replica Count",
        "type": "timeseries",
        "targets": [
          {
            "expr": "kube_horizontalpodautoscaler_status_current_replicas{namespace=\"scaling-challenge\"}",
            "legendFormat": "Current Replicas"
          },
          {
            "expr": "kube_horizontalpodautoscaler_status_desired_replicas{namespace=\"scaling-challenge\"}",
            "legendFormat": "Desired Replicas"
          }
        ]
      },
      {
        "title": "CPU Utilization",
        "type": "timeseries",
        "targets": [
          {
            "expr": "kube_horizontalpodautoscaler_status_current_metrics_average_utilization{namespace=\"scaling-challenge\"}",
            "legendFormat": "Current CPU %"
          },
          {
            "expr": "kube_horizontalpodautoscaler_spec_target_metric{namespace=\"scaling-challenge\"}",
            "legendFormat": "Target CPU %"
          }
        ]
      },
      {
        "title": "Scaling Events",
        "type": "table",
        "targets": [
          {
            "expr": "changes(kube_horizontalpodautoscaler_status_desired_replicas{namespace=\"scaling-challenge\"}[1h])",
            "legendFormat": "Scaling Events/Hour"
          }
        ]
      },
      {
        "title": "HPA Status",
        "type": "stat",
        "targets": [
          {
            "expr": "kube_horizontalpodautoscaler_status_condition{namespace=\"scaling-challenge\",condition=\"AbleToScale\",status=\"true\"}",
            "legendFormat": "Able to Scale"
          },
          {
            "expr": "kube_horizontalpodautoscaler_status_condition{namespace=\"scaling-challenge\",condition=\"ScalingActive\",status=\"true\"}",
            "legendFormat": "Scaling Active"
          }
        ]
      }
    ]
  }
}
```

### **Scaling Performance Dashboard:**
```json
{
  "dashboard": {
    "title": "Scaling Performance Analysis",
    "panels": [
      {
        "title": "Scaling Response Time",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(hpa_scaling_duration_seconds_bucket[5m]))",
            "legendFormat": "95th Percentile Scaling Time"
          }
        ]
      },
      {
        "title": "Resource Efficiency",
        "type": "timeseries",
        "targets": [
          {
            "expr": "(rate(container_cpu_usage_seconds_total{namespace=\"scaling-challenge\"}[5m]) / kube_pod_container_resource_requests{resource=\"cpu\",namespace=\"scaling-challenge\"}) * 100",
            "legendFormat": "CPU Efficiency %"
          },
          {
            "expr": "(container_memory_working_set_bytes{namespace=\"scaling-challenge\"} / kube_pod_container_resource_requests{resource=\"memory\",namespace=\"scaling-challenge\"}) * 100",
            "legendFormat": "Memory Efficiency %"
          }
        ]
      },
      {
        "title": "Application Performance During Scaling",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{namespace=\"scaling-challenge\"}[5m]))",
            "legendFormat": "Response Time P95"
          },
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\",namespace=\"scaling-challenge\"}[5m])) / sum(rate(http_requests_total{namespace=\"scaling-challenge\"}[5m]))",
            "legendFormat": "Error Rate"
          }
        ]
      }
    ]
  }
}
```

---

## 🚨 **ALERTING RULES**

### **Critical HPA Alerts:**

#### **HPA Health Alerts:**
```yaml
groups:
- name: hpa-health
  rules:
  - alert: HPAUnableToScale
    expr: kube_horizontalpodautoscaler_status_condition{condition="AbleToScale",status="false"} == 1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "HPA cannot scale {{ $labels.horizontalpodautoscaler }}"
      description: "HPA {{ $labels.horizontalpodautoscaler }} in {{ $labels.namespace }} has been unable to scale for 5 minutes"
      runbook_url: "https://runbooks.company.com/hpa-unable-to-scale"

  - alert: HPAMetricsUnavailable
    expr: kube_horizontalpodautoscaler_status_condition{condition="ScalingActive",status="false"} == 1
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "HPA metrics unavailable for {{ $labels.horizontalpodautoscaler }}"
      description: "HPA {{ $labels.horizontalpodautoscaler }} cannot get metrics for scaling decisions"

  - alert: HPAAtMaxReplicas
    expr: kube_horizontalpodautoscaler_status_current_replicas == kube_horizontalpodautoscaler_spec_max_replicas
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "HPA {{ $labels.horizontalpodautoscaler }} at maximum replicas"
      description: "HPA has been at max replicas for 10 minutes - consider increasing maxReplicas"
```

#### **Scaling Performance Alerts:**
```yaml
groups:
- name: hpa-performance
  rules:
  - alert: HPAScalingThrashing
    expr: changes(kube_horizontalpodautoscaler_status_desired_replicas[15m]) > 6
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "HPA {{ $labels.horizontalpodautoscaler }} scaling too frequently"
      description: "HPA has changed desired replicas {{ $value }} times in 15 minutes"

  - alert: HPASlowScaling
    expr: histogram_quantile(0.95, rate(hpa_scaling_duration_seconds_bucket[10m])) > 300
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "HPA scaling taking too long"
      description: "95th percentile scaling time is {{ $value