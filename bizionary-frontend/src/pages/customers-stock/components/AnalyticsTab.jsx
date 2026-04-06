import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { customerAnalyticsApi } from '../../../services/customerAnalyticsApi';

const AnalyticsTab = () => {
    const [loyaltyData, setLoyaltyData] = useState([]);
    const [behaviorData, setBehaviorData] = useState([]);
    const [loading, setLoading] = useState(true);

    const COLORS = ['#10b981', '#0ea5e9', '#64748b'];

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                setLoading(true);
                const [loyaltyRes, behaviorRes] = await Promise.all([
                    customerAnalyticsApi.getLoyaltyDistribution(),
                    customerAnalyticsApi.getBehaviorFrequency()
                ]);

                setLoyaltyData(Array.isArray(loyaltyRes.data) ? loyaltyRes.data : []);

                setBehaviorData(Array.isArray(behaviorRes.data) ? behaviorRes.data : []);
            } catch (error) {
                console.error('Error fetching analytics', error);
                setLoyaltyData([]);
                setBehaviorData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchAnalytics();
    }, []);

    if (loading) return <div className="text-center py-10"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div></div>;

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-white p-3 border border-gray-100 shadow-lg rounded-xl">
                    <p className="text-sm font-bold text-slate-800 mb-1">{label || payload[0].payload.tier}</p>
                    <p className="text-xs font-semibold text-primary">
                        Value: {payload[0].value} {payload[0].payload.percentage ? `(${payload[0].payload.percentage}%)` : ''}
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Purchase Frequency Chart */}
            <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm lg:col-span-2 flex flex-col min-h-[350px]">
                <div className="mb-4">
                    <h3 className="text-lg font-bold text-textMain">Purchase Frequency Trends</h3>
                    <p className="text-xs text-textMuted mt-1">Monthly average orders per active user</p>
                </div>
                <div className="flex-1 w-full relative">
                    {behaviorData.length === 0 ? (
                        <div className="h-full min-h-[220px] flex items-center justify-center text-sm text-textMuted">
                            No behavior trend data available.
                        </div>
                    ) : (
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={behaviorData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                            <defs>
                                <linearGradient id="colorFreq" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                            <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12, fontWeight: 600}} dy={10} />
                            <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12, fontWeight: 600}} />
                            <RechartsTooltip content={<CustomTooltip />} />
                            <Area type="monotone" dataKey="frequency_index" stroke="#8b5cf6" strokeWidth={4} fill="url(#colorFreq)" activeDot={{ r: 6, fill: '#8b5cf6', stroke: '#fff', strokeWidth: 2 }} />
                        </AreaChart>
                    </ResponsiveContainer>
                    )}
                </div>
            </div>

            {/* Loyalty Tier Distribution */}
            <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm flex flex-col">
                <div className="mb-4">
                    <h3 className="text-lg font-bold text-textMain">Loyalty Tiers</h3>
                    <p className="text-xs text-textMuted mt-1">Customer distribution by status</p>
                </div>
                <div className="flex-1 w-full relative min-h-[220px]">
                    {loyaltyData.length === 0 ? (
                        <div className="h-full min-h-[220px] flex items-center justify-center text-sm text-textMuted">
                            No loyalty distribution data available.
                        </div>
                    ) : (
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie
                                data={loyaltyData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={80}
                                paddingAngle={5}
                                dataKey="count"
                                nameKey="tier"
                            >
                                {(loyaltyData || []).map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <RechartsTooltip content={<CustomTooltip />} />
                            <Legend 
                                verticalAlign="bottom" 
                                height={36} 
                                iconType="circle"
                                formatter={(value) => <span className="text-xs font-semibold text-slate-700 ml-1">{value}</span>}
                            />
                        </PieChart>
                    </ResponsiveContainer>
                    )}
                </div>
            </div>

        </div>
    );
};

export default AnalyticsTab;
