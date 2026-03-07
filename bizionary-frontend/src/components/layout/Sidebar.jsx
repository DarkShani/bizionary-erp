import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, ShoppingCart, Users, FolderKanban, Settings, Package, ShoppingBag, FileText } from 'lucide-react';

const Sidebar = () => {
    const navigation = [
        { name: 'Dashboard', href: '/', icon: LayoutDashboard },
        { name: 'Products', href: '/products', icon: Package },
        { name: 'Sales', href: '/sales', icon: ShoppingCart },
        { name: 'Purchases', href: '/purchases', icon: ShoppingBag },
        { name: 'Invoices', href: '/invoices', icon: FileText },
        { name: 'Customer & Stocks', href: '/customers-stock', icon: Users },
        { name: 'Accounts', href: '/accounts', icon: FolderKanban },
        { name: 'User Management', href: '/user-management', icon: Settings },
    ];

    return (
        <div className="flex flex-col w-64 h-screen bg-surface border-r border-gray-100 flex-shrink-0">
            {/* Logo Section */}
            <div className="h-24 flex items-center px-6 border-b border-transparent">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-sm shadow-primary/30">
                        <LayoutDashboard className="w-6 h-6" />
                    </div>
                    <div className="flex flex-col">
                        <h1 className="text-xl font-bold text-textMain tracking-tight leading-tight">Bizionary</h1>
                        <span className="text-xs text-textMuted tracking-wide font-medium">CRM Enterprise</span>
                    </div>
                </div>
            </div>

            {/* Navigation Links */}
            <div className="flex-1 overflow-y-auto py-6 px-4">
                <nav className="space-y-1.5">
                    {navigation.map((item) => {
                        const Icon = item.icon;
                        return (
                            <NavLink
                                key={item.name}
                                to={item.href}
                                className={({ isActive }) =>
                                    `flex items-center px-4 py-3 text-sm font-semibold rounded-2xl transition-all duration-200 ${isActive
                                        ? 'bg-sky-50 text-primary'
                                        : 'text-textMuted hover:bg-gray-50 hover:text-textMain'
                                    }`
                                }
                            >
                                <Icon className={`mr-4 h-5 w-5 flex-shrink-0 transition-colors ${({ isActive }) => isActive ? 'text-primary' : 'text-gray-400'}`} />
                                {item.name}
                            </NavLink>
                        );
                    })}
                </nav>
            </div>

            {/* Bottom Actions */}
            <div className="p-4 space-y-4">
                <button className="flex items-center justify-center w-full px-4 py-3.5 bg-primary text-white text-sm font-bold rounded-2xl hover:bg-primaryDark transition-all duration-200 shadow-md shadow-primary/20">
                    <svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    Add New Lead
                </button>
                <button className="flex items-center px-4 py-2 text-sm font-medium rounded-xl text-textMuted hover:bg-gray-50 hover:text-textMain w-full transition-all duration-200">
                    <Settings className="mr-3 h-5 w-5 text-gray-400" />
                    Settings
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
