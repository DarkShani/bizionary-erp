import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Moon, Sun, Monitor, User, Bell, Shield, KeyRound, MonitorSmartphone, Globe, Puzzle, Eye, EyeOff } from 'lucide-react';
import api from '../../services/api';

const Settings = () => {
    const { user } = useAuth();
    const [activeSection, setActiveSection] = useState('Appearance');

    // State for Password Visibility
    const [showCurrentPassword, setShowCurrentPassword] = useState(false);
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    // State for Profile Update
    const [profileData, setProfileData] = useState({
        firstName: user?.name?.split(' ')[0] || '',
        lastName: user?.name?.split(' ').slice(1).join(' ') || '',
        email: user?.email || ''
    });
    const [isUpdatingProfile, setIsUpdatingProfile] = useState(false);
    const [profileUpdateStatus, setProfileUpdateStatus] = useState({ type: '', message: '' });

    const handleProfileUpdate = async (e) => {
        e.preventDefault();
        setIsUpdatingProfile(true);
        setProfileUpdateStatus({ type: '', message: '' });

        try {
            await api.put('/user/profile/update/', {
                first_name: profileData.firstName,
                last_name: profileData.lastName,
                email: profileData.email
            });
            setProfileUpdateStatus({ type: 'success', message: 'Profile updated successfully!' });
        } catch (error) {
            setProfileUpdateStatus({ type: 'error', message: 'Failed to update profile. Please try again.' });
        } finally {
            setIsUpdatingProfile(false);
            
            // Clear message after 3 seconds
            setTimeout(() => setProfileUpdateStatus({ type: '', message: '' }), 3000);
        }
    };

    const sidebarLinks = [
        { name: 'Account Info', icon: User },
        { name: 'Appearance', icon: MonitorSmartphone },
        { name: 'Language & Region', icon: Globe },
        { name: 'Notifications', icon: Bell },
        { name: 'Integrations', icon: Puzzle },
        { name: 'Privacy & Security', icon: Shield },
    ];

    const renderLeftSidebar = () => (
        <div className="md:col-span-1 space-y-1">
            {sidebarLinks.map(link => {
                const Icon = link.icon;
                const isActive = activeSection === link.name;
                return (
                    <button
                        key={link.name}
                        onClick={() => setActiveSection(link.name)}
                        className={`w-full flex items-center gap-3 px-4 py-3 font-medium rounded-xl transition-all duration-300 ${
                            isActive 
                            ? 'bg-primary/10 text-primary dark:bg-primary/20 dark:text-sky-300 font-bold' 
                            : 'text-textMuted dark:text-gray-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-textMain dark:hover:text-white'
                        }`}
                    >
                        <Icon className="w-5 h-5" />
                        {link.name}
                    </button>
                );
            })}
        </div>
    );

    const renderAppearance = () => (
        <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        <MonitorSmartphone className="w-5 h-5 text-primary" />
                        Appearance
                    </h3>
                    <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Customize the display mode for your workspace.</p>
                </div>
            </div>
            
            <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
                <button 
                    onClick={() => {
                        document.documentElement.classList.remove('dark');
                    }}
                    className="p-6 rounded-xl border-2 border-gray-200 dark:border-slate-700 flex flex-col items-center gap-3 transition-all duration-300 hover:scale-105 hover:shadow-lg active:scale-95 text-textMain dark:text-gray-300 hover:border-primary/50"
                >
                    <Sun className="w-8 h-8" />
                    <span className="font-bold text-sm">Light Mode</span>
                </button>
                <button 
                    onClick={() => {
                        document.documentElement.classList.add('light');
                    }}
                    className="p-6 rounded-xl border-2 border-gray-200 dark:border-slate-700 flex flex-col items-center gap-3 transition-all duration-300 hover:scale-105 hover:shadow-lg active:scale-95 text-textMain dark:text-gray-300 hover:border-primary/50"
                >
                    <Moon className="w-8 h-8" />
                    <span className="font-bold text-sm">Dark Mode</span>
                </button>
            </div>
        </div>
    );

    const renderPrivacySecurity = () => (
        <div className="space-y-6">
            {/* Change Password */}
            <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
                <div className="mb-6">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        <KeyRound className="w-5 h-5 text-primary" />
                        Change Password
                    </h3>
                    <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Ensure your account is using a long, random password to stay secure.</p>
                </div>
                
                <div className="space-y-4 max-w-md">
                    <div className="relative">
                        <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-1">Current Password</label>
                        <div className="relative flex items-center">
                            <input 
                                type={showCurrentPassword ? "text" : "password"} 
                                placeholder="••••••••" 
                                className="w-full p-2.5 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary transition-all duration-300 pr-10" 
                            />
                            <button 
                                type="button"
                                className="absolute right-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                                onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                            >
                                {showCurrentPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                            </button>
                        </div>
                    </div>
                    <div className="relative">
                        <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-1">New Password</label>
                        <div className="relative flex items-center">
                            <input 
                                type={showNewPassword ? "text" : "password"} 
                                placeholder="••••••••" 
                                className="w-full p-2.5 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary transition-all duration-300 pr-10" 
                            />
                            <button 
                                type="button"
                                className="absolute right-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                                onClick={() => setShowNewPassword(!showNewPassword)}
                            >
                                {showNewPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                            </button>
                        </div>
                    </div>
                    <div className="relative">
                        <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-1">Confirm New Password</label>
                        <div className="relative flex items-center">
                            <input 
                                type={showConfirmPassword ? "text" : "password"} 
                                placeholder="••••••••" 
                                className="w-full p-2.5 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary transition-all duration-300 pr-10" 
                            />
                            <button 
                                type="button"
                                className="absolute right-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            >
                                {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                            </button>
                        </div>
                    </div>
                    <button className="px-5 py-2.5 bg-primary text-white text-sm font-bold rounded-xl transition-all duration-300 hover:scale-105 hover:bg-primaryDark hover:shadow-lg active:scale-95 shadow-primary/20">
                        Update Password
                    </button>
                </div>
            </div>

            {/* 2FA */}
            <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300 flex items-center justify-between gap-6">
                <div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Two-Factor Authentication</h3>
                    <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Add an extra layer of security to your account by requiring an authenticator app code logging in.</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer flex-shrink-0">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary transition-all duration-300"></div>
                </label>
            </div>

            {/* Active Sessions */}
            <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h3 className="text-lg font-bold text-slate-900 dark:text-white">Active Sessions</h3>
                        <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Review your active login sessions across devices.</p>
                    </div>
                    <button className="px-4 py-2 bg-rose-50 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400 text-xs font-bold rounded-xl transition-all duration-300 hover:bg-rose-100 dark:hover:bg-rose-500/20 active:scale-95">
                        Log Out All Other Sessions
                    </button>
                </div>
                <div className="space-y-3">
                    <div className="p-4 border border-gray-100 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800/50 flex items-center justify-between">
                        <div className="flex flex-col">
                            <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                                <Monitor className="w-4 h-4 text-primary" />
                                Chrome on Windows (Current)
                            </h4>
                            <p className="text-xs text-textMuted dark:text-gray-400 mt-1">Sheikhupura, PK • IP: 192.168.1.100</p>
                        </div>
                        <span className="text-[10px] bg-emerald-100 text-emerald-600 font-bold px-2 py-1 rounded-md">Active Now</span>
                    </div>
                    <div className="p-4 border border-gray-100 dark:border-slate-700 rounded-xl flex items-center justify-between opacity-75">
                        <div className="flex flex-col">
                            <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                                <MonitorSmartphone className="w-4 h-4 text-textMuted" />
                                Safari on iOS
                            </h4>
                            <p className="text-xs text-textMuted dark:text-gray-400 mt-1">Lahore, PK • IP: 203.0.113.45</p>
                        </div>
                        <span className="text-[10px] text-textMuted dark:text-gray-400 font-medium">Last active 2 hrs ago</span>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderAccountInfo = () => (
        <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
            <div className="mb-6">
                <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <User className="w-5 h-5 text-primary" />
                    Profile Information
                </h3>
                <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Update your account identity and email credentials.</p>
            </div>
            
            <form onSubmit={handleProfileUpdate} className="space-y-4">
                {profileUpdateStatus.message && (
                    <div className={`p-3 rounded-xl text-sm font-bold border ${profileUpdateStatus.type === 'success' ? 'bg-emerald-50 text-emerald-600 border-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20' : 'bg-rose-50 text-rose-600 border-rose-200 dark:bg-rose-500/10 dark:text-rose-400 dark:border-rose-500/20'}`}>
                        {profileUpdateStatus.message}
                    </div>
                )}
                
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-1">First Name</label>
                        <input 
                            type="text" 
                            value={profileData.firstName} 
                            onChange={(e) => setProfileData({...profileData, firstName: e.target.value})}
                            className="w-full p-2.5 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary transition-all duration-300" 
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-1">Last Name</label>
                        <input 
                            type="text" 
                            value={profileData.lastName} 
                            onChange={(e) => setProfileData({...profileData, lastName: e.target.value})}
                            className="w-full p-2.5 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary transition-all duration-300" 
                        />
                    </div>
                </div>
                <div>
                    <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-1">Email Address</label>
                    <input 
                        type="email" 
                        value={profileData.email} 
                        onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                        className="w-full p-2.5 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary transition-all duration-300" 
                    />
                </div>
                <button 
                    type="submit"
                    disabled={isUpdatingProfile}
                    className="px-5 py-2.5 bg-primary text-white text-sm font-bold rounded-xl transition-all duration-300 hover:scale-105 hover:bg-primaryDark hover:shadow-lg active:scale-95 shadow-primary/20 disabled:opacity-70 disabled:hover:scale-100 disabled:cursor-not-allowed"
                >
                    {isUpdatingProfile ? 'Saving...' : 'Save Profile Changes'}
                </button>
            </form>
        </div>
    );

    const renderNotifications = () => (
        <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
            <div className="mb-6">
                <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <Bell className="w-5 h-5 text-primary" />
                    Notification Preferences
                </h3>
                <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Choose exactly what we notify you about.</p>
            </div>
            
            <div className="space-y-4">
                {[
                    { title: 'Low Stock Warnings', desc: 'Get alerted when inventory falls below 15 units.' },
                    { title: 'Overdue Invoices', desc: 'Receive immediate alerts for missing client payments.' },
                    { title: 'Daily Sales Report', desc: 'A compressed summary of day-to-day revenue metrics.' }
                ].map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                        <div>
                            <h4 className="font-bold text-sm text-slate-900 dark:text-white">{item.title}</h4>
                            <p className="text-xs text-textMuted dark:text-gray-500">{item.desc}</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" className="sr-only peer" defaultChecked={idx !== 2} />
                            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary transition-all duration-300"></div>
                        </label>
                    </div>
                ))}
            </div>
        </div>
    );

    const renderLanguageRegion = () => (
        <div className="bg-white dark:bg-slate-800 p-6 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
            <div className="mb-6">
                <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <Globe className="w-5 h-5 text-primary" />
                    Language & Region
                </h3>
                <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Configure your preferred language and regional formatting settings.</p>
            </div>
            
            <div className="space-y-6 max-w-md">
                <div>
                    <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-2">Display Language</label>
                    <div className="relative">
                        <select className="w-full p-3 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary appearance-none cursor-pointer transition-all duration-300">
                            <option value="en-US">English (US)</option>
                            <option value="en-UK">English (UK)</option>
                            <option value="ur">Urdu (اردو)</option>
                            <option value="ar">Arabic (العربية)</option>
                            <option value="es">Spanish (Español)</option>
                            <option value="fr">French (Français)</option>
                            <option value="zh">Mandarin (中文)</option>
                        </select>
                        <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none">
                            <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                        </div>
                    </div>
                </div>
                
                <div>
                    <label className="block text-xs font-bold text-textMuted dark:text-gray-400 mb-2">Timezone</label>
                    <div className="relative">
                        <select className="w-full p-3 rounded-xl border border-gray-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 dark:text-white outline-none focus:border-primary appearance-none cursor-pointer transition-all duration-300">
                            <option value="Asia/Karachi">Asia/Karachi (GMT+5:00)</option>
                            <option value="Asia/Dubai">Asia/Dubai (GMT+4:00)</option>
                            <option value="Europe/London">Europe/London (GMT+0:00)</option>
                            <option value="America/New_York">America/New_York (GMT-5:00)</option>
                        </select>
                        <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none">
                            <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderPlaceholder = () => (
        <div className="flex h-64 items-center justify-center p-8 bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 shadow-sm">
            <h2 className="text-xl font-bold text-textMuted dark:text-gray-400">{activeSection} configuration coming soon.</h2>
        </div>
    );

    return (
        <div className="max-w-5xl mx-auto space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-textMain dark:text-white">Settings</h1>
                <p className="text-sm text-textMuted dark:text-gray-400 mt-1">Manage your account settings, preferences, and notifications.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left Tabs/Navigation Sidebar */}
                {renderLeftSidebar()}

                {/* Main Settings Panel */}
                <div className="md:col-span-2 space-y-6">
                    {activeSection === 'Account Info' && renderAccountInfo()}
                    {activeSection === 'Appearance' && renderAppearance()}
                    {activeSection === 'Language & Region' && renderLanguageRegion()}
                    {activeSection === 'Privacy & Security' && renderPrivacySecurity()}
                    {activeSection === 'Notifications' && renderNotifications()}
                    {activeSection === 'Integrations' && renderPlaceholder()}
                </div>
            </div>
        </div>
    );
};

export default Settings;
