import React, { useState, useEffect } from 'react';
import Chart from './chart';
import { subDays } from 'date-fns';
import { BACKEND_URL } from './backendURL';
import DateRangePicker from './dateRangePicker';

const Dashboard = ({ name, containerStyle, onClickDashboardItem }) => {
  const [dashboard, setDashboard] = useState(null);
  const [dateRange, setDateRange] = useState({
    startDate: subDays(new Date(), 90),
    endDate: new Date()
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, [name]);

  const fetchDashboard = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/dashboard/${encodeURIComponent(name)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch dashboard');
      }
      const data = await response.json();
      setDashboard(data);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      setError('Failed to load dashboard. Please try again later.');
    }
  };

  const handleDateChange = (newDateRange) => {
    setDateRange(newDateRange);
    if (dashboard && dashboard.charts) {
      const filteredCharts = dashboard.charts.map(chart => ({
        ...chart,
        data: chart.data.filter(item => {
          const itemDate = new Date(item[chart.xAxisField]);
          return itemDate >= newDateRange.startDate && itemDate <= newDateRange.endDate;
        })
      }));
      setDashboard(prevDashboard => ({ ...prevDashboard, charts: filteredCharts }));
    }
  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!dashboard) {
    return <div>Loading...</div>;
  }

  return (
    <div style={containerStyle}>
      <h2>{dashboard.dashboard.name}</h2>
      <DateRangePicker onChange={handleDateChange} />
      <div>
        {dashboard.charts.map(chart => (
          <Chart
            key={chart.id}
            chartData={chart}
            containerStyle={{ margin: '10px' }}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;