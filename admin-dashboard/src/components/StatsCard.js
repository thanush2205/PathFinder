// Stats Card Component
import React from 'react';

function StatsCard({ title, value, subtitle, icon, trend }) {
  return (
    <div className="stats-card">
      <div className="stats-icon">{icon}</div>
      <div className="stats-content">
        <h3>{title}</h3>
        <div className="stats-value">{value}</div>
        <div className="stats-subtitle">{subtitle}</div>
        {trend && <div className="stats-trend">{trend}</div>}
      </div>
    </div>
  );
}

export default StatsCard;
