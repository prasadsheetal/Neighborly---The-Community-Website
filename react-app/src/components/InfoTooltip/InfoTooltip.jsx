import React from 'react';
import './InfoTooltip.css';

const InfoTooltip = ({ text, size = 16 }) => {
  return (
    <span className="tooltip-wrapper">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="#888"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="info-icon"
      >
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="16" x2="12" y2="12" />
        <line x1="12" y1="8" x2="12.01" y2="8" />
      </svg>
      <span className="tooltip-box">{text}</span>
    </span>
  );
};

export default InfoTooltip;