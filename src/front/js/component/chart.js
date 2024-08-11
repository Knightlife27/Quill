// import React, { useState, useEffect } from 'react';
// import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
// import { BACKEND_URL } from './backendURL';


// const Chart = ({ chartId, chartData, containerStyle, onClick }) => {
//   const [fetchedChartData, setFetchedChartData] = useState(null); // State for fetched data
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     if (!chartData && chartId) {
//       const fetchChartById = async (chartId) => {
//         try {
//           const response = await fetch(`${BACKEND_URL}/api/chart/${chartId}`);
//           if (!response.ok) {
//             throw new Error(`Failed to fetch chart: ${response.status} ${response.statusText}`);
//           }

//           const contentType = response.headers.get("content-type");
//           if (!contentType || !contentType.includes("application/json")) {
//             throw new Error("Received non-JSON response");
//           }

//           const data = await response.json();
//           setFetchedChartData(data); // Update the state with fetched data
//         } catch (error) {
//           console.error('Error fetching chart:', error);
//           setError('Failed to load chart. Please try again later.');
//         }
//       };

//       fetchChartById(chartId);
//     }
//   }, [chartId, chartData]);

//   if (error) {
//     return <div>Error: {error}</div>;
//   }

//   const dataToUse = fetchedChartData || chartData; // Determine which data to use

//   if (!dataToUse) {
//     return <div>Loading chart...</div>;
//   }

//   const { chartType, data, xAxisField, yAxisField, name } = dataToUse;

//   const ChartComponent = chartType === 'line' ? LineChart : BarChart;
//   const DataComponent = chartType === 'line' ? Line : Bar;

//   const handleClick = () => {
//     console.log(`Chart clicked: ${name}`); // Add console log to verify click
//     onClick(dataToUse); // Call the onClick function passed as a prop with the appropriate data
//   };

//   return (
//     <div style={containerStyle} onClick={handleClick}> {/* Use handleClick for onClick */}
//       <h3>{name}</h3>
//       <ChartComponent width={600} height={300} data={data}>
//         <CartesianGrid strokeDasharray="3 3" />
//         <XAxis dataKey={xAxisField} />
//         <YAxis />
//         <Tooltip />
//         <Legend />
//         <DataComponent type="monotone" dataKey={yAxisField} stroke="#8884d8" />
//       </ChartComponent>
//     </div>
//   );
// };

// export default Chart;



import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { BACKEND_URL } from './backendURL';

const Chart = ({ chartId, chartData, containerStyle, onClick }) => {
  const [fetchedChartData, setFetchedChartData] = useState(null); // State for fetched data
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!chartData && chartId) {
      const fetchChartById = async (chartId) => {
        try {
          const response = await fetch(`${BACKEND_URL}/api/chart/${chartId}`);
          if (!response.ok) {
            throw new Error(`Failed to fetch chart: ${response.status} ${response.statusText}`);
          }

          const contentType = response.headers.get("content-type");
          if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Received non-JSON response");
          }

          const data = await response.json();
          setFetchedChartData(data); // Update the state with fetched data
        } catch (error) {
          console.error('Error fetching chart:', error);
          setError('Failed to load chart. Please try again later.');
        }
      };

      fetchChartById(chartId);
    }
  }, [chartId, chartData]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  const dataToUse = fetchedChartData || chartData; // Determine which data to use

  if (!dataToUse) {
    return <div>Loading chart...</div>;
  }

  const { chartType, data, xAxisField, yAxisField, name } = dataToUse;

  // Sort the data by date
  const sortedData = [...data].sort((a, b) => new Date(a[xAxisField]) - new Date(b[xAxisField]));

  const ChartComponent = chartType === 'line' ? LineChart : BarChart;
  const DataComponent = chartType === 'line' ? Line : Bar;

  const handleClick = () => {
    console.log(`Chart clicked: ${name}`); // Add console log to verify click
    onClick(dataToUse); // Call the onClick function passed as a prop with the appropriate data
  };

  return (
    <div style={containerStyle} onClick={handleClick}> {/* Use handleClick for onClick */}
      <h3>{name}</h3>
      <ChartComponent width={600} height={300} data={sortedData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={xAxisField} />
        <YAxis />
        <Tooltip />
        <Legend />
        <DataComponent type="monotone" dataKey={yAxisField} stroke="#8884d8" />
      </ChartComponent>
    </div>
  );
};

export default Chart;