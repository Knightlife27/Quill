import React from 'react';

const DataCard = ({ className }) => {
  return (
    <article className={`data-card ${className}`}>
      <style jsx>{`
        .data-card {
    display: inline-block !important;
    flex-direction: row; /* This ensures horizontal alignment */
    align-items: center; /* This vertically centers the content */
    justify-content: center; 
    border-radius: 14px;
    background-color: #fff;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25);
    width: 231px;
    height: 224px;
    margin: 1vw;
    min-width: 20vw; 
    max-width: 22vw;
    padding: 0 10px; 
    box-sizing: border-box; 
}
        @media (max-width: 91px) {
          .data-card {
            width: 100%;
          }
        }
      `}</style>
    </article>
  );
};

export default DataCard;