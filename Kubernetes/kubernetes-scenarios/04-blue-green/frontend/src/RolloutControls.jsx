import React, { useState } from 'react';
import './RolloutControls.css';

const RolloutControls = ({ percent, onRollout, loading }) => {
  const [value, setValue] = useState(percent);

  const handleChange = (e) => {
    setValue(Number(e.target.value));
  };

  const handleClick = () => {
    onRollout(value);
  };

  return (
    <div className="rollout-controls">
      <label>
        Rollout to Green: {value}%
        <input
          type="range"
          min={0}
          max={100}
          value={value}
          onChange={handleChange}
          disabled={loading}
        />
      </label>
      <button onClick={handleClick} disabled={loading}>
        {loading ? 'Rolling out...' : 'Start Rollout'}
      </button>
    </div>
  );
};

export default RolloutControls; 