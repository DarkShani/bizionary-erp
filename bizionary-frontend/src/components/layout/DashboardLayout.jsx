import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

const DashboardLayout = () => {
    return (
        <div className="flex h-screen bg-background overflow-hidden relative">
            <Sidebar />
            <div className="flex-1 flex flex-col h-full overflow-hidden">
                <Navbar />
                <main className="flex-1 overflow-y-auto p-8 relative">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;
