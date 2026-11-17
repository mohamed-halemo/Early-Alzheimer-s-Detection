import React from 'react';

function RedPopup({ warningType,message, onClose }) {
  return (
    <div className="OrangepopUpBG">
      <p className="typePop">{warningType}</p>
      <p className='messagePop'>{message}</p>
      <div className="closeButtonPop" onClick={onClose}>x</div>
      <img src="/images/orangepop.png"  alt="pop" className='imagePop'/>
      <div className='OrangecirclePop'><div className='iPop'>!</div></div>
    </div>
  );
}

export default RedPopup;