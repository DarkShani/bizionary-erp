import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import AIChatbotWidget from '../common/AIChatbotWidget';

const DashboardLayout = () => {
    const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

    return (
        <div className="flex h-screen bg-background dark:bg-[#0b1120] overflow-hidden relative transition-colors duration-300">
            <Sidebar isOpen={isMobileSidebarOpen} onClose={() => setIsMobileSidebarOpen(false)} />
            <div className="flex-1 flex flex-col h-full overflow-hidden">
                <Navbar onToggleSidebar={() => setIsMobileSidebarOpen(true)} />
                <main className="flex-1 overflow-y-auto p-4 md:p-8 relative">
                    <Outlet />
                </main>
            </div>
            {/* Floating AI Chatbot Widget */}
            <AIChatbotWidget />
        </div>
    );
};

export default DashboardLayout;
