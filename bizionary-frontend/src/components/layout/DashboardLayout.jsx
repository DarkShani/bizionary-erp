import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

const DashboardLayout = () => {
    const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

    return (
        <div className="flex h-screen bg-transparent overflow-hidden relative transition-colors duration-300">
            <div className="pointer-events-none absolute inset-0 bg-white/24 dark:bg-slate-950/14"></div>
            <Sidebar isOpen={isMobileSidebarOpen} onClose={() => setIsMobileSidebarOpen(false)} />
            <div className="flex-1 flex flex-col h-full overflow-hidden relative z-10">
                <Navbar onToggleSidebar={() => setIsMobileSidebarOpen(true)} />
                <main className="flex-1 overflow-y-auto p-4 md:p-8 relative">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default DashboardLayout;
