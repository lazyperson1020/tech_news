import React from 'react';

const Loader = () => {
  return (
    <div className="flex items-center justify-center p-6">
      <div className="loader border-4 border-t-primary-600 rounded-full w-10 h-10 animate-spin" />
    </div>
  );
};

export default Loader;