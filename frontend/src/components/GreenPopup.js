import React from 'react';

function GreenPopup({ warningType,message, onClose }) {
  return (
    <div className="GreenpopUpBG">
      <p className="typePop">{warningType}</p>
      <p className='messagePop'>{message}</p>
      <div className="closeButtonPop" onClick={onClose}>x</div>
      <img src="/images/greenpop.png"  alt="pop" className='imagePop'/>
      <div className='GreencirclePop'><p className='xPop'>&#x2713;</p></div>
    </div>
  );
}

export default GreenPopup;