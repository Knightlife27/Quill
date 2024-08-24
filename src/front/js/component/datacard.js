// import React from 'react';

// const DataCard = ({ className }) => {
//   return (
//     <article className={`data-card ${className}`}>
//       <style jsx>{`
//         .data-card {
//     display: inline-block !important;
//     flex-direction: row; /* This ensures horizontal alignment */
//     align-items: center; /* This vertically centers the content */
//     justify-content: center; 
//     border-radius: 14px;
//     background-color: #fff;
//     box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25);
//     width: 50vw;
//     height: 21vw;
//     margin: 1vw;
//     min-width: 20vw; 
//     max-width: 27vw;
//     max-height: 14vw;
//     padding: 0 10px; 
//     box-sizing: border-box; 
// }
//         @media (max-width: 91px) {
//           .data-card {
//             width: 100%;
//           }
//         }
//       `}</style>
//     </article>
//   );
// };

// export default DataCard;

import React from 'react';

const DataCard = ({ className, kpiData }) => {
  return (
    <article className={`data-card ${className}`}>
      {kpiData ? (
        <>
          <h3>{kpiData.metric_name}</h3>
          <p className="kpi-value">{kpiData.metric_value} {kpiData.metric_unit}</p>
        </>
      ) : (
        <p>No data available</p>
      )}
      <style jsx>{`
        .data-card {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          border-radius: 14px;
          background-color: #fff;
          box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25);
          width: calc(33.33% - 2vw);
          margin: 1vw;
          padding: 20px;
          box-sizing: border-box;
          min-height: 200px;
          text-align: center;
        }

        h3 {
          margin-bottom: 10px;
          font-size: 1.2em;
        }

        .kpi-value {
          font-size: 1.5em;
          font-weight: bold;
        }

        @media (max-width: 768px) {
          .data-card {
            width: calc(33% - 1vw);
          }
        }
      `}</style>
    </article>
  );
};

export default DataCard;