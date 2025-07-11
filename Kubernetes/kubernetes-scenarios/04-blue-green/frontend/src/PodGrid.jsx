import React from 'react';
import PodCard from './PodCard';
import './PodGrid.css';

const PodGrid = ({ pods, killPod }) => (
  <div className="pod-grid">
    {pods.map((pod, idx) => (
      <PodCard key={pod.name || idx} pod={pod} killPod={killPod} />
    ))}
  </div>
);

export default PodGrid; 