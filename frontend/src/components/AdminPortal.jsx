import React, { useEffect } from 'react';

const AdminPortal = () => {
  useEffect(() => {
    // Redirect to the Railway admin portal
    window.location.href = 'https://aiinteltools-production.up.railway.app/admin';
  }, []);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      flexDirection: 'column'
    }}>
      <h2>Redirecting to Admin Portal...</h2>
      <p>If you are not redirected automatically, <a href="https://aiinteltools-production.up.railway.app/admin">click here</a></p>
    </div>
  );
};

export default AdminPortal;

