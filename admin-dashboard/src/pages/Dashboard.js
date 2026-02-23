/**
 * Dashboard Page Component
 * Main analytics dashboard with charts and metrics
 */

import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import StatsCard from '../components/StatsCard';
import UsersChart from '../components/UsersChart';
import SessionsChart from '../components/SessionsChart';
import HazardsChart from '../components/HazardsChart';
import '../styles/Dashboard.css';

function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAnalytics();
    // Refresh every 30 seconds
    const interval = setInterval(fetchAnalytics, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAnalytics = async () => {
    try {
      const data = await analyticsAPI.getDashboard();
      setAnalytics(data);
      setError('');
    } catch (err) {
      setError('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Real-time analytics and system metrics</p>
      </div>

      {/* Key Performance Indicators */}
      <div className="stats-grid">
        <StatsCard
          title="Total Users"
          value={analytics.users.total_users}
          subtitle={`${analytics.users.active_users_today} active today`}
          icon="👥"
          trend={`+${analytics.users.new_users_today} new today`}
        />
        <StatsCard
          title="Total Sessions"
          value={analytics.sessions.total_sessions}
          subtitle={`${analytics.sessions.sessions_today} today`}
          icon="📊"
          trend={`Avg ${analytics.sessions.average_duration_minutes} min`}
        />
        <StatsCard
          title="Hazards Detected"
          value={analytics.sessions.total_hazards_detected}
          subtitle="Total alerts triggered"
          icon="⚠️"
          trend="Real-time detection"
        />
        <StatsCard
          title="Open Complaints"
          value={analytics.complaints.open_complaints}
          subtitle={`${analytics.complaints.resolved_complaints} resolved`}
          icon="💬"
          trend={`Avg ${analytics.complaints.average_resolution_time_hours}h`}
        />
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        <div className="chart-card">
          <h2>User Activity Trend</h2>
          <UsersChart />
        </div>
        
        <div className="chart-card">
          <h2>Session Activity</h2>
          <SessionsChart />
        </div>
        
        <div className="chart-card full-width">
          <h2>Hazard Distribution</h2>
          <HazardsChart data={analytics.hazards} />
        </div>
      </div>

      {/* System Efficiency */}
      <div className="efficiency-section">
        <h2>System Efficiency</h2>
        <div className="efficiency-grid">
          <div className="efficiency-card">
            <span className="efficiency-label">Response Time</span>
            <span className="efficiency-value">
              {analytics.system_efficiency.average_response_time_ms}ms
            </span>
          </div>
          <div className="efficiency-card">
            <span className="efficiency-label">Detection FPS</span>
            <span className="efficiency-value">
              {analytics.system_efficiency.detection_fps} FPS
            </span>
          </div>
          <div className="efficiency-card">
            <span className="efficiency-label">API Uptime</span>
            <span className="efficiency-value">
              {analytics.system_efficiency.api_uptime_percent}%
            </span>
          </div>
          <div className="efficiency-card">
            <span className="efficiency-label">Alert Delay</span>
            <span className="efficiency-value">
              {analytics.system_efficiency.average_alert_delay_ms}ms
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
