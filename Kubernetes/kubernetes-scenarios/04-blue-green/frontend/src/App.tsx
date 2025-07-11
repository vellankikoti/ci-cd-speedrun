import React, { useEffect, useState } from 'react';
import PodCard from './PodCard';
import Confetti from 'react-confetti';
import './App.css';

interface Pod {
  name: string;
  version: 'blue' | 'green';
  health: 'healthy' | 'unhealthy' | 'pending';
  status?: string;
  created?: string;
}

interface DeploymentStatus {
  current_strategy: string;
  blue_pods: number;
  green_pods: number;
  last_deployment_time?: number;
}

const DEPLOYMENT_STRATEGIES = [
  { 
    label: 'Switch to Green', 
    value: 'blue-green',
    description: 'Instantly switch all traffic to green pods (zero downtime)',
    color: 'bg-green-600 hover:bg-green-700'
  },
  { 
    label: 'Progressive Rollout', 
    value: 'rollout',
    description: 'Gradually replace blue pods with green (rolling update)',
    color: 'bg-blue-600 hover:bg-blue-700'
  },
  { 
    label: 'Canary Deployment', 
    value: 'canary',
    description: 'Deploy small percentage to test before full rollout',
    color: 'bg-purple-600 hover:bg-purple-700'
  },
  { 
    label: 'Reset to 50/50', 
    value: 'reset',
    description: 'Reset to initial state with 5 blue and 5 green pods',
    color: 'bg-gray-600 hover:bg-gray-700'
  }
];

function App() {
  const [pods, setPods] = useState<Pod[]>([]);
  const [loading, setLoading] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [deploying, setDeploying] = useState<string | null>(null);
  const [deploymentStatus, setDeploymentStatus] = useState<DeploymentStatus | null>(null);
  const [killingPod, setKillingPod] = useState<string | null>(null);

  // Fetch pods from backend
  const fetchPods = async () => {
    setRefreshing(true);
    setError(null);
    try {
      const res = await fetch('/api/pods');
      if (!res.ok) throw new Error('Failed to fetch pods');
      const data = await res.json();
      setPods(data);
    } catch (error: any) {
      setError('Could not fetch pods from backend. Please check backend and cluster.');
      setPods([]);
    } finally {
      setRefreshing(false);
    }
  };

  // Fetch deployment status
  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/status');
      if (res.ok) {
        const data = await res.json();
        setDeploymentStatus(data);
      }
    } catch (error) {
      // Ignore status errors for demo
    }
  };

  useEffect(() => {
    fetchPods();
    fetchStatus();
    const interval = setInterval(fetchPods, 2000);
    const statusInterval = setInterval(fetchStatus, 5000);
    return () => {
      clearInterval(interval);
      clearInterval(statusInterval);
    };
  }, []);

  // Trigger deployment strategy
  const triggerDeployment = async (strategy: string) => {
    setDeploying(strategy);
    setError(null);
    setActionMessage(null);
    
    try {
      if (strategy === 'reset') {
        const res = await fetch('/api/reset', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        if (!res.ok) throw new Error('Failed to reset deployment');
        setActionMessage('Deployment reset to 5 blue, 5 green pods!');
      } else {
        const res = await fetch('/api/deploy', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ strategy }),
        });
        if (!res.ok) throw new Error('Failed to trigger deployment');
        
        const strategyName = DEPLOYMENT_STRATEGIES.find(s => s.value === strategy)?.label || strategy;
        setActionMessage(`${strategyName} deployment started!`);
      }
    } catch (error: any) {
      setError('Failed to trigger deployment. Backend or cluster issue.');
    } finally {
      setDeploying(null);
      setTimeout(() => {
        fetchPods();
        fetchStatus();
      }, 1000);
    }
  };

  // Kill pod handler with animation
  const killPod = async (podName: string) => {
    setKillingPod(podName);
    setActionMessage(null);
    setError(null);
    
    try {
      const res = await fetch(`/api/kill-pod`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: podName })
      });
      if (!res.ok) throw new Error('Failed to kill pod');
      setActionMessage(`Pod ${podName} killed! Watch it self-heal...`);
    } catch (error: any) {
      setError('Failed to kill pod. Backend or cluster issue.');
    } finally {
      setTimeout(() => {
        setKillingPod(null);
        fetchPods();
      }, 2000);
    }
  };

  // Progress calculation
  const bluePods = pods.filter(p => p.version === 'blue');
  const greenPods = pods.filter(p => p.version === 'green');
  const total = pods.length;
  const healthyGreen = greenPods.filter(p => p.health === 'healthy').length;
  const healthyBlue = bluePods.filter(p => p.health === 'healthy').length;

  // Confetti when all pods are green and healthy
  useEffect(() => {
    if (greenPods.length > 0 && healthyGreen === greenPods.length && greenPods.length >= 8) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 4000);
    }
  }, [healthyGreen, greenPods.length]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-center">
            <div className="flex items-center space-x-3">
              <svg className="w-12 h-12 text-blue-600" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="20" cy="20" r="20" fill="#326CE5"/>
                <text x="50%" y="55%" textAnchor="middle" fill="white" fontSize="18" fontFamily="Arial" dy=".3em">⎈</text>
              </svg>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Kubernetes Deployment Demo</h1>
                <p className="text-gray-600">Visual Blue-Green, Rollout & Canary Strategies</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Deployment Strategy Controls */}
      <section className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex flex-wrap justify-center gap-4">
            {DEPLOYMENT_STRATEGIES.map(strategy => (
              <button
                key={strategy.value}
                className={`px-6 py-3 rounded-lg font-semibold shadow-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed ${strategy.color} text-white`}
                onClick={() => triggerDeployment(strategy.value)}
                disabled={!!deploying}
                title={strategy.description}
              >
                {deploying === strategy.value ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Deploying...</span>
                  </div>
                ) : (
                  strategy.label
                )}
              </button>
            ))}
          </div>
          
          {/* Status Display */}
          {deploymentStatus && (
            <div className="mt-4 text-center">
              <div className="inline-flex items-center space-x-4 bg-gray-100 rounded-lg px-4 py-2">
                <span className="text-sm font-medium text-gray-700">
                  Current Strategy: <span className="font-bold capitalize">{deploymentStatus.current_strategy}</span>
                </span>
                <span className="text-sm text-gray-600">
                  Blue: {deploymentStatus.blue_pods} | Green: {deploymentStatus.green_pods}
                </span>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Blue Pods Panel */}
          <section className="bg-white rounded-2xl shadow-xl border-2 border-blue-500 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
              <h2 className="text-2xl font-bold text-white flex items-center">
                <div className="w-4 h-4 bg-white rounded-full mr-3"></div>
                Blue Pods ({bluePods.length})
              </h2>
              <p className="text-blue-100 text-sm">Version 1.0 - Stable</p>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {bluePods.map(pod => (
                  <PodCard 
                    key={pod.name} 
                    pod={pod} 
                    killPod={killPod}
                    isKilling={killingPod === pod.name}
                  />
                ))}
                {bluePods.length === 0 && (
                  <div className="col-span-2 text-center py-8 text-gray-500">
                    <div className="text-4xl mb-2">🔵</div>
                    <p>No blue pods running</p>
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Green Pods Panel */}
          <section className="bg-white rounded-2xl shadow-xl border-2 border-green-500 overflow-hidden">
            <div className="bg-gradient-to-r from-green-500 to-green-600 px-6 py-4">
              <h2 className="text-2xl font-bold text-white flex items-center">
                <div className="w-4 h-4 bg-white rounded-full mr-3"></div>
                Green Pods ({greenPods.length})
              </h2>
              <p className="text-green-100 text-sm">Version 2.0 - New Release</p>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {greenPods.map(pod => (
                  <PodCard 
                    key={pod.name} 
                    pod={pod} 
                    killPod={killPod}
                    isKilling={killingPod === pod.name}
                  />
                ))}
                {greenPods.length === 0 && (
                  <div className="col-span-2 text-center py-8 text-gray-500">
                    <div className="text-4xl mb-2">🟢</div>
                    <p>No green pods running</p>
                  </div>
                )}
              </div>
            </div>
          </section>
        </div>

        {/* Health Summary */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Cluster Health Summary</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{total}</div>
              <div className="text-sm text-blue-600">Total Pods</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{healthyBlue + healthyGreen}</div>
              <div className="text-sm text-green-600">Healthy Pods</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{healthyBlue}</div>
              <div className="text-sm text-blue-600">Healthy Blue</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{healthyGreen}</div>
              <div className="text-sm text-green-600">Healthy Green</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col items-center space-y-2">
            <button 
              className="px-4 py-2 bg-gray-200 rounded-lg shadow hover:bg-gray-300 transition text-gray-700 font-semibold" 
              onClick={fetchPods} 
              disabled={refreshing}
            >
              {refreshing ? 'Refreshing...' : 'Refresh Pods'}
            </button>
            
            {error && (
              <div className="text-red-600 font-semibold bg-red-50 px-4 py-2 rounded-lg">
                {error}
              </div>
            )}
            
            {actionMessage && (
              <div className="text-green-600 font-semibold bg-green-50 px-4 py-2 rounded-lg">
                {actionMessage}
              </div>
            )}
            
            <div className="text-center text-sm text-gray-600 max-w-2xl">
              <p className="font-medium">🎯 Demo Features:</p>
              <p>• Kill pods to see Kubernetes self-healing • Switch deployments with zero downtime • Watch progressive rollouts • Test canary deployments</p>
            </div>
          </div>
        </div>
      </footer>

      {showConfetti && <Confetti numberOfPieces={300} recycle={false} />}
    </div>
  );
}

export default App;
