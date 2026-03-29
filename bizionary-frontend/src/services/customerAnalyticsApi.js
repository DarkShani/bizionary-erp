import api from './api';

const BASE_URL = '/screen3/customer-analytics';

export const customerAnalyticsApi = {
    // Customers
    getCustomers: () => api.get(`${BASE_URL}/customers/`),
    createCustomer: (data) => api.post(`${BASE_URL}/customers/`, data),
    getDashboardKpis: () => api.get(`${BASE_URL}/customers/dashboard_kpis/`),
    getLoyaltyDistribution: () => api.get(`${BASE_URL}/customers/loyalty_distribution/`),
    getBehaviorFrequency: () => api.get(`${BASE_URL}/customers/behavior_frequency/`),
    getAtRiskCustomers: () => api.get(`${BASE_URL}/customers/at_risk_customers/`),
    getVipCustomers: () => api.get(`${BASE_URL}/customers/vip_customers/`),
    updateTier: (id, data) => api.post(`${BASE_URL}/customers/${id}/update_tier/`, data),

    // Behavior
    getBehaviors: () => api.get(`${BASE_URL}/behavior/`),
    getBehaviorByCustomer: (customerId) => api.get(`${BASE_URL}/behavior/by_customer/?customer_id=${customerId}`),

    // Purchases
    getPurchases: () => api.get(`${BASE_URL}/purchases/`),

    // Activities
    getRecentActivities: (limit = 10) => api.get(`${BASE_URL}/activities/?limit=${limit}`),

    // Insights
    getActiveInsights: () => api.get(`${BASE_URL}/insights/active_insights/`),

    // KPIs trend
    getKpiTrends: (days = 30) => api.get(`${BASE_URL}/kpis/trends/?days=${days}`)
};
