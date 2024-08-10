import React, { useState, useEffect } from 'react';
import { BACKEND_URL } from './backendURL'; // Ensure this path is correct

const DashboardSelector = ({ onSelectDashboard }) => {
  const [dashboards, setDashboards] = useState([]);
  const [selectedDashboard, setSelectedDashboard] = useState('');

  useEffect(() => {
    const fetchDashboards = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/api/dashboards`);
        if (!response.ok) {
          throw new Error('Failed to fetch dashboards');
        }
        const data = await response.json();
        setDashboards(data);
      } catch (error) {
        console.error('Error fetching dashboards:', error);
      }
    };

    fetchDashboards();
  }, []);

  const handleChange = (event) => {
    const dashboardName = event.target.value;
    setSelectedDashboard(dashboardName);
    onSelectDashboard(dashboardName);
  };

  return (
    <select value={selectedDashboard} onChange={handleChange}>
      <option value="" disabled>Select a Dashboard</option>
      {dashboards.map((dashboard) => (
        <option key={dashboard.id} value={dashboard.name}>
          {dashboard.name}
        </option>
      ))}
    </select>
  );
};

export default DashboardSelector;