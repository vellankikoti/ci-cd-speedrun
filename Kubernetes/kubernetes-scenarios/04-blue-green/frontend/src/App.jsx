import React, { useEffect, useState } from 'react';
import PodGrid from './PodGrid';
import RolloutControls from './RolloutControls';
import Confetti from 'react-confetti';
import './App.css';

const FUN_FACTS = [
  'Blue-green deployments minimize downtime and risk!',
  'You can instantly rollback by switching traffic back to blue!',
  'Blue-green is great for database migrations with zero downtime.',
  'Netflix and Amazon use blue-green for safe releases.',
  'You can A/B test with blue-green by splitting traffic.'
];

function App() {
  const [pods, setPods] = useState([]);
  const [percent, setPercent] = useState(0);
  const [loading, setLoading] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [funFact, setFunFact] = useState('');

  // Fetch pods from backend
  const fetchPods = async () => {
    try {
      const res = await fetch('/api/pods');
      const data = await res.json();
      setPods(data);
    } catch (error) {
      console.log('Backend not available, using mock data');
      // Mock data for demo when backend is not available
      setPods([
        { name: 'blue-pod-1', version: 'blue', health: 'healthy', status: 'Running' },
        { name: 'blue-pod-2', version: 'blue', health: 'healthy', status: 'Running' },
        { name: 'green-pod-1', version: 'green', health: 'healthy', status: 'Running' },
        { name: 'green-pod-2', version: 'green', health: 'healthy', status: 'Running' }
      ]);
    }
  };

  useEffect(() => {
    fetchPods();
    setFunFact(FUN_FACTS[Math.floor(Math.random() * FUN_FACTS.length)]);
    const interval = setInterval(fetchPods, 2000);
    return () => clearInterval(interval);
  }, []);

  // Handle rollout
  const handleRollout = async (newPercent) => {
    setLoading(true);
    setPercent(newPercent);
    try {
      await fetch('/api/rollout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ percent: newPercent })
      });
    } catch (error) {
      console.log('Backend not available, simulating rollout');
    }
    setLoading(false);
    fetchPods();
  };

  // Kill pod handler
  const killPod = async (podName) => {
    try {
      await fetch(`/api/kill-pod`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: podName })
      });
    } catch (error) {
      console.log('Backend not available, simulating pod kill');
    }
    fetchPods();
  };

  // Progress calculation
  const total = pods.length;
  const green = pods.filter(p => p.version === 'green').length;
  const healthyGreen = pods.filter(p => p.version === 'green' && p.health === 'healthy').length;
  const progress = total ? Math.round((green / total) * 100) : 0;

  // Confetti when all pods are green and healthy
  useEffect(() => {
    if (total > 0 && healthyGreen === total) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 4000);
    }
  }, [healthyGreen, total]);

  return (
    <div className="App">
      {showConfetti && <Confetti numberOfPieces={300} recycle={false} />}
      <header>
        <h1>Blue-Green Deployment Demo</h1>
      </header>
      <div className="progress-bar-container">
        <div className="progress-bar" style={{ width: `${progress}%` }} />
        <span className="progress-label">{progress}% Green</span>
      </div>
      <RolloutControls percent={percent} onRollout={handleRollout} loading={loading} />
      <PodGrid pods={pods} killPod={killPod} />
      <div className="fun-fact">💡 Fun fact: {funFact}</div>
    </div>
  );
}

export default App; 