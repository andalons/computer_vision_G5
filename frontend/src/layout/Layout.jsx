import React from 'react';
import { Outlet } from 'react-router-dom';  
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const Layout = () => { 
  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      <Navbar />
      <main className="flex-1 w-full pb-12 mx-auto sm:px-8">
        <Outlet />  
      </main>
      <Footer />
    </div>
  );
};

export default Layout;