import React from 'react';

const PodCard = ({ pod, killPod, isKilling = false }) => {
  const getHealthColor = (health) => {
    switch (health) {
      case 'healthy': return 'bg-green-500';
      case 'unhealthy': return 'bg-red-500';
      case 'pending': return 'bg-yellow-400';
      default: return 'bg-gray-400';
    }
  };
  const getVersionColor = (version) => version === 'blue' ? 'border-blue-500' : 'border-green-400';
  const getVersionBadge = (version) => version === 'blue' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700';

  return (
    <div className={`rounded-xl shadow-md p-5 bg-white flex flex-col gap-2 transition-all hover:shadow-xl border-2 ${getVersionColor(pod.version)} ${
      isKilling ? 'animate-pulse opacity-50' : ''
    }`}>
      <div className="flex items-center justify-between">
        <span className="font-bold text-lg truncate" title={pod.name}>{pod.name}</span>
        <span className={`w-3 h-3 rounded-full ml-2 ${getHealthColor(pod.health)} ${
          isKilling ? 'animate-ping' : ''
        }`} title={`Health: ${pod.health}`}></span>
      </div>
      <span className={`inline-block px-2 py-1 rounded ${getVersionBadge(pod.version)} text-xs font-semibold w-fit`}>
        {pod.version}
      </span>
      <div className="text-gray-600 text-sm">Status: {pod.status}</div>
      <div className="text-gray-600 text-sm">Health: {pod.health}</div>
      <div className="flex justify-end mt-2">
        <button
          onClick={() => killPod(pod.name)}
          disabled={isKilling}
          className={`flex items-center gap-1 px-3 py-1 rounded transition font-semibold text-sm shadow ${
            isKilling 
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
              : 'bg-red-100 text-red-700 hover:bg-red-200'
          }`}
          title={isKilling ? "Pod is being killed..." : "Simulate pod failure"}
        >
          {isKilling ? (
            <>
              <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-400"></div>
              <span>Killing...</span>
            </>
          ) : (
            <>
              <span role="img" aria-label="kill">🗡️</span> 
              Kill Pod
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default PodCard; 