import React, { useState } from 'react';

function DecisionComponent() {
  const [decision, setDecision] = useState(null);

  const handleDecision = (userDecision) => {
    setDecision(userDecision);
    // You can add logic here to handle the decision, e.g., send it to an endpoint
  };

  return (
    <div>
      <h2>Make a Decision</h2>
      <button onClick={() => handleDecision('Accept')}>Accept</button>
      <button onClick={() => handleDecision('Reject')}>Reject</button>
      {decision && <p>You have chosen to: {decision}</p>}
    </div>
  );
}

export default DecisionComponent;
