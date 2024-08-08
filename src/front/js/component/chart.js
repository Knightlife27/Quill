import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Chart = ({ chartData, containerStyle, onClick }) => {
  if (!chartData) {
    return <div>Loading chart...</div>;
  }

  const { chartType, data, xAxisField, yAxisField, name } = chartData;

  const ChartComponent = chartType === 'line' ? LineChart : BarChart;
  const DataComponent = chartType === 'line' ? Line : Bar;

  return (
    <div style={containerStyle}>
      <h3>{name}</h3>
      <ChartComponent width={600} height={300} data={data}>
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