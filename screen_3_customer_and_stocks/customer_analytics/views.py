from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    Customer, CustomerBehavior, PurchaseRecord,
    RecentActivity, CustomerInsight, CustomerKPI
)
from .serializers import (
    CustomerSerializer, CustomerCreateSerializer, CustomerBehaviorSerializer,
    PurchaseRecordSerializer, RecentActivitySerializer, CustomerInsightSerializer,
    CustomerKPISerializer, DashboardKPISerializer, LoyaltyDistributionSerializer,
    BehaviorFrequencySerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customers
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        return CustomerSerializer
    
    def create(self, request, *args, **kwargs):
        """Quick customer entry"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        
        # Create activity
        RecentActivity.objects.create(
            customer=customer,
            activity_type='REGISTRATION',
            description=f"New customer registered: {customer.full_name}"
        )
        
        # Return full customer data
        return Response(
            CustomerSerializer(customer).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def dashboard_kpis(self, request):
        """
        Get dashboard KPIs with current values and changes
        Endpoint: /api/screen3/customer-analytics/customers/dashboard_kpis/
        """
        today = timezone.now().date()
        
        # Get or create today's KPIs
        try:
            current_kpi = CustomerKPI.objects.get(date=today)
        except CustomerKPI.DoesNotExist:
            # Calculate and create
            current_kpi = self._calculate_daily_kpis(today)
        
        serializer = DashboardKPISerializer({
            'total_customers': current_kpi.total_customers,
            'total_customers_change': current_kpi.total_customers_change,
            'retention_rate': current_kpi.retention_rate,
            'retention_rate_change': current_kpi.retention_rate_change,
            'avg_lifetime_value': current_kpi.avg_lifetime_value,
            'avg_lifetime_value_change': current_kpi.avg_lifetime_value_change,
            'churn_risk_percentage': current_kpi.churn_risk_percentage,
            'churn_risk_change': current_kpi.churn_risk_change,
        })
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def loyalty_distribution(self, request):
        """
        Get loyalty tier distribution with percentages
        Endpoint: /api/screen3/customer-analytics/customers/loyalty_distribution/
        """
        total_customers = Customer.objects.filter(is_active=True).count()
        
        if total_customers == 0:
            return Response([])
        
        tiers = Customer.objects.filter(is_active=True).values('loyalty_tier').annotate(
            count=Count('id')
        )
        
        tier_names = {
            'VIP': 'VIP Tier',
            'REGULAR': 'Regulars',
            'NEW': 'New Signups'
        }
        
        distribution = []
        for tier in tiers:
            percentage = (tier['count'] / total_customers) * 100
            distribution.append({
                'tier': tier_names.get(tier['loyalty_tier'], tier['loyalty_tier']),
                'count': tier['count'],
                'percentage': round(percentage, 2)
            })
        
        serializer = LoyaltyDistributionSerializer(distribution, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def behavior_frequency(self, request):
        """
        Get customer behavior frequency trends for the chart
        Endpoint: /api/screen3/customer-analytics/customers/behavior_frequency/
        """
        # Get last 6 months
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=180)
        
        # Get monthly aggregated data
        behaviors = CustomerBehavior.objects.filter(
            month__gte=start_date.strftime('%Y-%m')
        ).values('month').annotate(
            avg_frequency=Avg('purchase_frequency')
        ).order_by('month')
        
        data = []
        for behavior in behaviors:
            # Convert month to short format (JAN, FEB, etc.)
            month_date = datetime.strptime(behavior['month'], '%Y-%m')
            month_short = month_date.strftime('%b').upper()
            
            data.append({
                'month': month_short,
                'frequency_index': int(behavior['avg_frequency'] or 0)
            })
        
        serializer = BehaviorFrequencySerializer(data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def at_risk_customers(self, request):
        """
        Get list of at-risk customers for churn alerts
        Endpoint: /api/screen3/customer-analytics/customers/at_risk_customers/
        """
        at_risk = Customer.objects.filter(is_at_risk=True, is_active=True)
        serializer = CustomerSerializer(at_risk, many=True)
        
        return Response({
            'count': at_risk.count(),
            'customers': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def vip_customers(self, request):
        """
        Get VIP customers
        Endpoint: /api/screen3/customer-analytics/customers/vip_customers/
        """
        vip = Customer.objects.filter(loyalty_tier='VIP', is_active=True)
        serializer = CustomerSerializer(vip, many=True)
        
        return Response({
            'count': vip.count(),
            'customers': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def update_tier(self, request, pk=None):
        """
        Manually update customer tier
        Endpoint: /api/screen3/customer-analytics/customers/{id}/update_tier/
        """
        customer = self.get_object()
        new_tier = request.data.get('tier')
        
        if new_tier not in ['VIP', 'REGULAR', 'NEW']:
            return Response(
                {'error': 'Invalid tier'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_tier = customer.loyalty_tier
        customer.loyalty_tier = new_tier
        customer.is_vip = (new_tier == 'VIP')
        customer.save()
        
        # Create activity
        RecentActivity.objects.create(
            customer=customer,
            activity_type='TIER_CHANGE',
            description=f"Tier changed from {old_tier} to {new_tier}"
        )
        
        return Response(CustomerSerializer(customer).data)
    
    def _calculate_daily_kpis(self, date):
        """Calculate KPIs for a given date"""
        # Total customers
        total_customers = Customer.objects.filter(
            is_active=True,
            created_at__date__lte=date
        ).count()
        
        # Previous period (30 days ago)
        prev_date = date - timedelta(days=30)
        prev_total = Customer.objects.filter(
            is_active=True,
            created_at__date__lte=prev_date
        ).count()
        
        total_change = 0
        if prev_total > 0:
            total_change = ((total_customers - prev_total) / prev_total) * 100
        
        # Retention rate (customers who purchased in last 90 days)
        ninety_days_ago = date - timedelta(days=90)
        active_customers = Customer.objects.filter(
            is_active=True,
            last_purchase_date__gte=ninety_days_ago
        ).count()
        
        retention_rate = 0
        if total_customers > 0:
            retention_rate = (active_customers / total_customers) * 100
        
        # Average lifetime value
        avg_ltv = Customer.objects.filter(is_active=True).aggregate(
            avg=Avg('lifetime_value')
        )['avg'] or 0
        
        # Churn risk
        at_risk_count = Customer.objects.filter(is_at_risk=True, is_active=True).count()
        churn_risk = 0
        if total_customers > 0:
            churn_risk = (at_risk_count / total_customers) * 100
        
        # Tier counts
        tier_counts = Customer.objects.filter(is_active=True).aggregate(
            vip=Count('id', filter=Q(loyalty_tier='VIP')),
            regular=Count('id', filter=Q(loyalty_tier='REGULAR')),
            new=Count('id', filter=Q(loyalty_tier='NEW')),
        )
        
        # Create KPI record
        kpi = CustomerKPI.objects.create(
            date=date,
            total_customers=total_customers,
            total_customers_change=round(Decimal(total_change), 2),
            retention_rate=round(Decimal(retention_rate), 2),
            retention_rate_change=Decimal('0'),  # Calculate separately if needed
            avg_lifetime_value=round(Decimal(avg_ltv), 2),
            avg_lifetime_value_change=Decimal('0'),
            churn_risk_percentage=round(Decimal(churn_risk), 2),
            churn_risk_change=Decimal('0'),
            vip_tier_count=tier_counts['vip'],
            regular_tier_count=tier_counts['regular'],
            new_signup_count=tier_counts['new'],
        )
        
        return kpi


class CustomerBehaviorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for customer behavior tracking
    """
    queryset = CustomerBehavior.objects.all()
    serializer_class = CustomerBehaviorSerializer
    
    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get behavior data for a specific customer"""
        customer_id = request.query_params.get('customer_id')
        if not customer_id:
            return Response(
                {'error': 'customer_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        behaviors = self.queryset.filter(customer_id=customer_id)
        serializer = self.get_serializer(behaviors, many=True)
        return Response(serializer.data)


class PurchaseRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for purchase records
    """
    queryset = PurchaseRecord.objects.all()
    serializer_class = PurchaseRecordSerializer
    
    def create(self, request, *args, **kwargs):
        """Create purchase record and update customer metrics"""
        response = super().create(request, *args, **kwargs)
        
        # Update customer metrics
        purchase = PurchaseRecord.objects.get(id=response.data['id'])
        purchase.customer.update_metrics()
        
        # Create activity
        RecentActivity.objects.create(
            customer=purchase.customer,
            activity_type='SALE',
            description=f"New sale: PKR {purchase.amount}"
        )
        
        return response


class RecentActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for recent activities (read-only)
    """
    queryset = RecentActivity.objects.all()
    serializer_class = RecentActivitySerializer
    
    def get_queryset(self):
        """Get recent activities with optional limit"""
        limit = self.request.query_params.get('limit', 10)
        return self.queryset[:int(limit)]


class CustomerInsightViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AI CRM insights
    """
    queryset = CustomerInsight.objects.filter(is_active=True)
    serializer_class = CustomerInsightSerializer
    
    @action(detail=False, methods=['get'])
    def active_insights(self, request):
        """Get all active insights for the dashboard"""
        insights = self.queryset.order_by('-priority', '-created_at')
        serializer = self.get_serializer(insights, many=True)
        return Response(serializer.data)


class CustomerKPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for historical KPI data
    """
    queryset = CustomerKPI.objects.all()
    serializer_class = CustomerKPISerializer
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get KPI trends over time"""
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        kpis = self.queryset.filter(date__gte=start_date, date__lte=end_date)
        serializer = self.get_serializer(kpis, many=True)
        return Response(serializer.data)
