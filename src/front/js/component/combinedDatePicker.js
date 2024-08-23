// import React from 'react';
// import DatePicker from 'react-datepicker';
// import "react-datepicker/dist/react-datepicker.css";

// const DateRangePicker = ({ onChange }) => {
//   const [startDate, setStartDate] = React.useState(new Date());
//   const [endDate, setEndDate] = React.useState(new Date());

//   const handleChange = (dates) => {
//     const [start, end] = dates;
//     setStartDate(start);
//     setEndDate(end);
//     onChange({ startDate: start, endDate: end });
//   };

//   return (
//     <DatePicker
//       selectsRange={true}
//       startDate={startDate}
//       endDate={endDate}
//       onChange={handleChange}
//       isClearable={true}
//     />
//   );
// };

// export default DateRangePicker;

import React, { useState, useRef, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { subDays, startOfMonth, format } from 'date-fns';

const CombinedDatePicker = ({ onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [startDate, setStartDate] = useState(subDays(new Date(), 90));
  const [endDate, setEndDate] = useState(new Date());
  const wrapperRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [wrapperRef]);

  const handlePresetChange = (days) => {
    const newStartDate = subDays(new Date(), days);
    const newEndDate = new Date();
    setStartDate(newStartDate);
    setEndDate(newEndDate);
    onChange({ startDate: newStartDate, endDate: newEndDate });
    setIsOpen(false);
  };

  const handleCustomChange = (dates) => {
    const [start, end] = dates;
    setStartDate(start);
    setEndDate(end);
    if (start && end) {
      onChange({ startDate: start, endDate: end });
    }
  };

  const formatDate = (date) => {
    return date ? format(date, 'MMM d, yyyy') : '';
  };

  return (
    <div className="combined-date-picker" ref={wrapperRef}>
      <button onClick={() => setIsOpen(!isOpen)} className="date-picker-button">
        {startDate && endDate ? `${formatDate(startDate)} - ${formatDate(endDate)}` : 'Select Date Range'}
      </button>
      {isOpen && (
        <div className="date-picker-dropdown">
          <div className="preset-options">
            <button onClick={() => handlePresetChange(30)}>Last 30 Days</button>
            <button onClick={() => handlePresetChange(60)}>Last 60 Days</button>
            <button onClick={() => handlePresetChange(90)}>Last 90 Days</button>
          </div>
          <DatePicker
            selectsRange={true}
            startDate={startDate}
            endDate={endDate}
            onChange={handleCustomChange}
            inline
          />
        </div>
      )}
    </div>
  );
};

export default CombinedDatePicker;