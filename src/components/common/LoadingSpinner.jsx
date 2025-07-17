import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ size = 40, color = '#4361ee' }) => {
  return (
    <div 
      className="loading-spinner"
      style={{
        width: `${size}px`,
        height: `${size}px`,
        borderColor: `${color} transparent transparent transparent`
      }}
    >
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  );
};

export default LoadingSpinner;
