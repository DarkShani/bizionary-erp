import React from 'react';
import { Bell, Search, Settings, User, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLocation } from 'react-router-dom';

const Navbar = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    return (
        <header className="h-24 bg-surface border-b border-gray-100 flex items-center justify-between px-8 z-10 sticky top-0">
            {/* Search Bar - Left Side */}
            <div className="flex-1 max-w-xl">
                <div className="relative flex items-center w-full h-11 rounded-xl bg-background focus-within:bg-white focus-within:ring-2 focus-within:ring-primary/20 focus-within:border-primary border border-transparent transition-all overflow-hidden shadow-sm">
                    <div className="grid place-items-center h-full w-12 text-gray-400">
                        <Search className="h-5 w-5" />
                    </div>
                    <input
                        className="peer h-full w-full outline-none text-sm text-textMain bg-transparent pr-2"
                        type="text"
                        id="search"
                        placeholder="Search customers, transactions, or reports..."
                    />
                </div>
            </div>

            {/* Right Actions */}
            <div className="flex items-center space-x-4 pl-6">
                {/* Notifications & Settings */}
                <div className="flex items-center space-x-3">
                    <button className="p-2.5 text-textMuted hover:text-primary hover:bg-sky-50 rounded-xl transition-colors relative bg-background border border-gray-100 shadow-sm">
                        <Bell className="h-5 w-5" />
                        <span className="absolute top-2.5 right-2 h-2.5 w-2.5 rounded-full bg-danger border-2 border-white"></span>
                    </button>
                    <button className="p-2.5 text-textMuted hover:text-primary hover:bg-sky-50 rounded-xl transition-colors bg-background border border-gray-100 shadow-sm">
                        <Settings className="h-5 w-5" />
                    </button>
                    <div className="h-8 w-px bg-gray-200 mx-2"></div>
                </div>

                {/* User Profile */}
                <div className="flex items-center space-x-3 group cursor-pointer relative">
                    <div className="hidden md:flex flex-col items-end text-sm">
                        <p className="font-bold text-textMain leading-snug">{user?.name || 'Ali'}</p>
                        <p className="text-xs text-textMuted">{user?.role || 'Administrator'}</p>
                    </div>

                    <div className="h-11 w-11 rounded-full bg-sky-100 border-2 border-white shadow-sm flex items-center justify-center text-primary font-bold overflow-hidden relative">
                        {/* Fallback to simple icon since we don't have an actual image asset */}
                        <User className="h-6 w-6 text-primary" />
                    </div>

                    <button
                        onClick={logout}
                        className="absolute -right-2 top-10 mt-2 p-2 text-white bg-danger rounded-lg transition-all opacity-0 group-hover:opacity-100 shadow-md invisible group-hover:visible"
                        title="Logout"
                    >
                        <LogOut className="h-4 w-4" />
                    </button>
                </div>
            </div>
        </header>
    );
};

export default Navbar;
