import React, { useState } from 'react';
import Chart from './chart'; 

const ChartInput = () => {
  const [chartId, setChartId] = useState('');
  const [submittedChartId, setSubmittedChartId] = useState('');

  const handleInputChange = (event) => {
    setChartId(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmittedChartId(chartId);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="chart-id-input">Enter Chart ID:</label>
        <input
          id="chart-id-input"
          type="text"
          value={chartId}
          onChange={handleInputChange}
          placeholder="Enter chart ID"
        />
        <button type="submit">Load Chart</button>
      </form>

      {submittedChartId && (
        <Chart chartId={submittedChartId} containerStyle={{ margin: '20px' }} onClick={(data) => console.log(data)} />
      )}
    </div>
  );
};

export default ChartInput;