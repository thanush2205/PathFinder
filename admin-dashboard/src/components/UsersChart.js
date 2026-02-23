// Users Chart with Recharts
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { analyticsAPI } from '../services/api';

function UsersChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    analyticsAPI.getUserTrend(7).then(response => {
      setData(response.trend);
    });
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="count" stroke="#8884d8" strokeWidth={2} name="New Users" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default UsersChart;
