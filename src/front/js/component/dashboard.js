import React, { useState, useEffect } from 'react';
import Chart from './chart';
import ChartInput from './chartInput'; // Import the ChartInput component
import { subDays, startOfMonth, isWithinInterval } from 'date-fns';
import { BACKEND_URL } from './backendURL';
import DateRangePicker from './dateRangePicker';

const PresetDateRangePicker = ({ onPresetChange }) => {
  const handlePresetChange = (event) => {
    const preset = event.target.value;
    let startDate, endDate = new Date();

    switch (preset) {
      case 'LAST_90_DAYS':
        startDate = subDays(new Date(), 90);
        break;
      case 'LAST_60_DAYS':
        startDate = subDays(new Date(), 60);
        break;
      case 'LAST_30_DAYS':
        startDate = subDays(new Date(), 30);
        break;
      case 'CURRENT_MONTH':
        startDate = startOfMonth(new Date());
        break;
      default:
        startDate = subDays(new Date(), 90);
    }

    onPresetChange({ startDate, endDate });
  };

  return (
    <select onChange={handlePresetChange} defaultValue="LAST_90_DAYS">
      <option value="LAST_90_DAYS">Last 90 Days</option>
      <option value="LAST_60_DAYS">Last 60 Days</option>
      <option value="LAST_30_DAYS">Last 30 Days</option>
      <option value="CURRENT_MONTH">Current Month</option>
    </select>
  );
};

const Dashboard = ({ name, containerStyle, onClickDashboardItem }) => {
  const [dashboard, setDashboard] = useState(null);
  const [initialData, setInitialData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
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
      console.log('Fetched Dashboard Data:', data);
      setDashboard(data);
      setInitialData(data.charts); // Store initial data
      setFilteredData(data.charts); // Initialize filtered data
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      setError('Failed to load dashboard. Please try again later.');
    }
  };

  const handleDateChange = (newDateRange) => {
    console.log(`New Date Range: ${newDateRange.startDate} to ${newDateRange.endDate}`);
    console.log(`Initial Date Range: ${dateRange.startDate} to ${dateRange.endDate}`);
    
    setDateRange(newDateRange);
    if (dashboard && initialData.length > 0) {
      const isWithinInitialRange = newDateRange.startDate >= dateRange.startDate && newDateRange.endDate <= dateRange.endDate;

      if (isWithinInitialRange) {
        console.log('Filtering data on the frontend');
        const filteredCharts = initialData.map(chart => ({
          ...chart,
          data: chart.data.filter(item => {
            const itemDate = new Date(item[chart.xAxisField]);
            return isWithinInterval(itemDate, { start: newDateRange.startDate, end: newDateRange.endDate });
          })
        }));
        console.log('Filtered Charts:', filteredCharts);
        setFilteredData(filteredCharts);
      } else {
        console.log('Fetching new data from the backend');
        fetchNewData(newDateRange);
      }
    }
  };

  const fetchNewData = async (newDateRange) => {
    try {
      console.log(`Fetching new data for range: ${newDateRange.startDate.toISOString()} to ${newDateRange.endDate.toISOString()}`);
      const response = await fetch(`${BACKEND_URL}/api/dashboard/${encodeURIComponent(name)}?startDate=${newDateRange.startDate.toISOString()}&endDate=${newDateRange.endDate.toISOString()}`);
      if (!response.ok) {
        throw new Error('Failed to fetch new data');
      }
      const data = await response.json();
      console.log('Fetched New Data:', data);
      setDashboard(data);
      setInitialData(data.charts); // Update initial data
      setFilteredData(data.charts); // Reset filtered data
    } catch (error) {
      console.error('Error fetching new data:', error);
      setError('Failed to load new data. Please try again later.');
    }
  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!dashboard) {
    return <div>Loading...</div>;
  }

  console.log('Rendering Charts with Data:', filteredData);

  return (
    <div style={containerStyle}>
      <h2>{dashboard.dashboard.name}</h2>
      <PresetDateRangePicker onPresetChange={handleDateChange} />
      <DateRangePicker onChange={handleDateChange} />
      
      {/* Add the ChartInput component here */}
      <ChartInput />

      <div>
        {filteredData.map(chart => (
          <Chart
            key={chart.id}
            chartData={chart}
            containerStyle={{ margin: '10px' }}
            onClick={() => onClickDashboardItem(chart)} // Pass the chart to the onClickDashboardItem callback
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;