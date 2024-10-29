import React, { useState } from 'react';
import RedPopup from './RedPopup';
import OrangePopup from './OrangePopup';
import GreenPopup from './GreenPopup';
import { useNavigate } from 'react-router-dom';

function WarningMessages() {
  const [showRedWarning, setShowRedWarning] = useState(false);
  const [showOrangeWarning, setShowOrangeWarning] = useState(false);
  const [showGreenWarning, setShowGreenWarning] = useState(false);
  const navigate = useNavigate();

  function handleCloseRed() {
    setShowRedWarning(false);
    navigate('/visualize');
  }

  function handleCloseOrange() {
    setShowOrangeWarning(false);
    navigate('/visualize');
  }
  function handleCloseGreen() {
    setShowGreenWarning(false);
    navigate('/visualize');
  }

  return (
    <div>
      <button onClick={() => setShowRedWarning(true)}>Red warning</button>
      {showRedWarning && (
        <RedPopup warningType="Oh Snap!" message="You have failed to read this failure message. Please try again! " onClose={handleCloseRed} />
      )}

<button onClick={() => setShowOrangeWarning(true)}>Orange warning</button>
      {showOrangeWarning && (
        <OrangePopup warningType="Warning!" message="Sorry! There was a problem with your request." onClose={handleCloseOrange} />
      )}

<button onClick={() => setShowGreenWarning(true)}>Green warning</button>
      {showGreenWarning && (
        <GreenPopup warningType="Well Done!" message="Lorem ipsum dolor sit amet, consectetur adipiscing elit! " onClose={handleCloseGreen} />
      )}
    </div>
  );
}

export default WarningMessages;
