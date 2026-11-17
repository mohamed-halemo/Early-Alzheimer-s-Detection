import React from 'react';

function RedPopup({ warningType,message, onClose }) {
  return (
    <div className="popUpBG">
      <p className="typePop">{warningType}</p>
      <p className='messagePop'>{message}</p>
      <div className="closeButtonPop" onClick={onClose}>x</div>
      <img src="/images/redpop.png"  alt="pop" className='imagePop'/>
      <div className='circlePop'><p className='xPop'>x</p></div>
    </div>
  );
}

export default RedPopup;
