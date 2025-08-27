import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-blue-600">MyApp</div>
        <div>
          <a href="/" className="text-gray-700 hover:text-blue-600 mx-2">Home</a>
          <a href="/link-analysis" className="text-gray-700 hover:text-blue-600 mx-2">Link Analysis</a>
          <a href="/statistics" className="text-gray-700 hover:text-blue-600 mx-2">Statistics</a>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;