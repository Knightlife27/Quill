const KPIDisplay = ({ kpis }) => {
    return (
      <div className="kpi-container">
        {Object.entries(kpis).map(([key, kpi]) => (
          <div key={key} className="kpi-card">
            <h3>{kpi.metric_name}</h3>
            <p>{kpi.metric_value} {kpi.metric_unit}</p>
          </div>
        ))}
      </div>
    );
  };

  export default KPIDisplay