import React, { useState, useEffect } from 'react';
import Chart from './chart';
import ChartInput from './chartInput'; // Import the ChartInput component
import { subDays, startOfMonth, isWithinInterval } from 'date-fns';
import { BACKEND_URL } from './backendURL';
import DateRangePicker from './dateRangePicker';
import DashboardSelector from './dashboardSelector';

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

    // Ensure the time is set to cover the entire day
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(23, 59, 59, 999);

    onPresetChange({ startDate, endDate });
  };

  return (
    <select className="form-select" onChange={handlePresetChange} defaultValue="LAST_90_DAYS">
      <option value="LAST_90_DAYS">Last 90 Days</option>
      <option value="LAST_60_DAYS">Last 60 Days</option>
      <option value="LAST_30_DAYS">Last 30 Days</option>
      <option value="CURRENT_MONTH">Current Month</option>
    </select>
  );
};

const Dashboard = ({ containerStyle, onClickDashboardItem }) => {
  const [selectedDashboard, setSelectedDashboard] = useState('Sales Dashboard');
  const [dashboard, setDashboard] = useState(null);
  const [initialData, setInitialData] = useState([]);
  const [initialFetchRange, setInitialFetchRange] = useState({ startDate: null, endDate: null });
  const [filteredData, setFilteredData] = useState([]);
  const [dateRange, setDateRange] = useState({
    startDate: subDays(new Date(), 90),
    endDate: new Date()
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard(selectedDashboard);
  }, [selectedDashboard]);

  const fetchDashboard = async (dashboardName) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/dashboard/${encodeURIComponent(dashboardName)}?startDate=${dateRange.startDate.toISOString()}&endDate=${dateRange.endDate.toISOString()}`);
      if (!response.ok) {
        throw new Error('Failed to fetch dashboard');
      }
      const data = await response.json();
      console.log('Fetched Dashboard Data:', data);
      setDashboard(data);
      setInitialData(data.charts);
      setFilteredData(data.charts);
      setInitialFetchRange({
        startDate: new Date(dateRange.startDate.setHours(0, 0, 0, 0)),
        endDate: new Date(dateRange.endDate.setHours(23, 59, 59, 999))
      }); // Set the initial fetch range to cover whole days
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      setError('Failed to load dashboard. Please try again later.');
    }
  };

  const handleDateChange = (newDateRange) => {
    console.log(`New Date Range: ${newDateRange.startDate} to ${newDateRange.endDate}`);
    console.log(`Initial Fetch Range: ${initialFetchRange.startDate} to ${initialFetchRange.endDate}`);
    
    setDateRange(newDateRange);

    if (dashboard && initialData.length > 0) {
      const isWithinInitialRange = 
        newDateRange.startDate >= initialFetchRange.startDate && 
        newDateRange.endDate <= initialFetchRange.endDate;

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
    if (!newDateRange.startDate || !newDateRange.endDate) {
      console.error('Invalid date range:', newDateRange);
      setError('Invalid date range selected.');
      return;
    }

    try {
      console.log(`Fetching new data for range: ${newDateRange.startDate.toISOString()} to ${newDateRange.endDate.toISOString()}`);
      const response = await fetch(`${BACKEND_URL}/api/dashboard/${encodeURIComponent(selectedDashboard)}?startDate=${newDateRange.startDate.toISOString()}&endDate=${newDateRange.endDate.toISOString()}`);
      
      const contentType = response.headers.get("content-type");
      if (!response.ok || !contentType || !contentType.includes("application/json")) {
        throw new Error('Failed to fetch new data or invalid response format');
      }
      
      const data = await response.json();
      console.log('Fetched New Data:', data);
      setDashboard(data);
      setInitialData(data.charts);
      setFilteredData(data.charts);
      setInitialFetchRange(newDateRange);
    } catch (error) {
      console.error('Error fetching new data:', error);
      setError('Failed to load new data. Please try again later.');
    }
  };

  if (error) {
    return <div className="bg-red-500 text-white p-4 rounded">Error: {error}</div>;
  }

  return (
    <div className="container mx-auto p-4" style={containerStyle}>
      <h2 className="text-2xl font-bold mb-4">{selectedDashboard}</h2>
      <div className="mb-3">
        <PresetDateRangePicker onPresetChange={handleDateChange} />
      </div>
      <div className="mb-3">
        <DateRangePicker onChange={handleDateChange} />
      </div>
      <div className="mb-3">
        <DashboardSelector onSelectDashboard={setSelectedDashboard} />
      </div>
      <div className="mb-3">
        <ChartInput />
      </div>
      <div className="flex flex-wrap -mx-3">
        {filteredData.map(chart => (
          <div className="w-full md:w-1/2 px-3 mb-3" key={chart.id}>
            <Chart
              chartData={chart}
              containerStyle={{ margin: '10px' }}
              onClick={() => onClickDashboardItem(chart)}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;