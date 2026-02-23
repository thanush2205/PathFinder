// Sessions Chart
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { analyticsAPI } from '../services/api';

function SessionsChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    analyticsAPI.getSessionTrend(7).then(response => {
      setData(response.trend);
    });
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#82ca9d" name="Sessions" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default SessionsChart;
