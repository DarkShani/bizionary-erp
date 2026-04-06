"""
Dashboard Views - Analytics and Reporting Engine
================================================

This module implements the dashboard's aggregation service.
All data is computed dynamically from existing tables using Django ORM.

Architecture:
    MySQL Database → Django Models → Aggregation Queries → JSON Response

Performance Strategy:
    - Database-level aggregations (Sum, Count, Avg)
    - annotate() for grouping
    - select_related() for foreign keys
    - Avoid Python-level loops
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, F, Q, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from decimal import Decimal

from products.models import Product
from sales.models import Sale
from invoices.models import Invoice
from purchases.models import Purchase

from .serializers import (
    DashboardKPISerializer,
    MonthlyRevenueSerializer,
    TopProductSerializer,
    LowStockProductSerializer,
    RecentSaleSerializer
)


@api_view(['GET'])
def dashboard_kpis(request):
    """
    Main Dashboard KPIs Endpoint
    
    Returns all primary KPIs in a single response
    
    Method: GET
    Endpoint: /api/dashboard/kpis/
    
    Response:
        {
            "total_products": <dynamic_count>,
            "total_inventory_value": "<decimal_as_string>",
            "total_revenue": "<decimal_as_string>",
            "total_purchases_value": "<decimal_as_string>",
            "total_invoices": <dynamic_count>,
            "unpaid_invoices": <dynamic_count>,
            "low_stock_count": <dynamic_count>
        }
    """
    try:
        # Normalize decimal precision to keep serializer validation consistent.
        to_2dp = lambda value: (value or Decimal('0.00')).quantize(Decimal('0.01'))

        # KPI 1: Total Products Count
        total_products = Product.objects.count()

        # KPI 2: Total Inventory Value (sum of stock_quantity * unit_price)
        # Using ExpressionWrapper for calculation at database level
        inventory_value_aggregate = Product.objects.aggregate(
            total_value=Sum(
                ExpressionWrapper(
                    F('stock_quantity') * F('unit_price'),
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                )
            )
        )
        total_inventory_value = to_2dp(inventory_value_aggregate['total_value'])

        # KPI 3: Total Revenue (sum of sales.total_price)
        revenue_aggregate = Sale.objects.aggregate(
            total=Sum('total_price')
        )
        total_revenue = to_2dp(revenue_aggregate['total'])

        # KPI 5: Total Purchases Value
        purchases_aggregate = Purchase.objects.aggregate(
            total=Sum('total_cost')
        )
        total_purchases_value = to_2dp(purchases_aggregate['total'])

        # KPI 6: Total Invoices Count
        total_invoices = Invoice.objects.count()

        # KPI 7: Unpaid Invoices Count
        unpaid_invoices = Invoice.objects.filter(
            Q(status='UNPAID') | Q(status='PARTIALLY_PAID')
        ).count()

        # KPI 8: Low Stock Products Count (stock_quantity < reorder_level)
        low_stock_count = Product.objects.filter(
            stock_quantity__lt=F('reorder_level')
        ).count()

        # Note: Account balance removed - Screen 4 (Accounts) is independent

        # Prepare response data
        kpi_data = {
            'total_products': total_products,
            'total_inventory_value': total_inventory_value,
            'total_revenue': total_revenue,
            'total_purchases_value': total_purchases_value,
            'total_invoices': total_invoices,
            'unpaid_invoices': unpaid_invoices,
            'low_stock_count': low_stock_count,
        }

        serializer = DashboardKPISerializer(data=kpi_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch KPIs: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def monthly_revenue(request):
    """
    Monthly Revenue Breakdown
    
    Groups sales by month and calculates total revenue per month
    
    Method: GET
    Endpoint: /api/dashboard/monthly-revenue/
    
    Query Parameters:
        - year (optional): Filter by specific year
    
    Response:
        [
            {"month": "January", "year": 2023, "revenue": 20000.00},
            {"month": "February", "year": 2023, "revenue": 15000.00}
        ]
    """
    try:
        year_filter = request.query_params.get('year', None)
        
        # Base queryset
        queryset = Sale.objects.all()
        
        # Apply year filter if provided
        if year_filter:
            queryset = queryset.filter(sale_date__year=year_filter)

        # Group by month and year, calculate revenue
        monthly_data = queryset.annotate(
            month_num=ExtractMonth('sale_date'),
            year_num=ExtractYear('sale_date')
        ).values('month_num', 'year_num').annotate(
            revenue=Sum('total_price')
        ).order_by('year_num', 'month_num')

        # Convert month numbers to names
        month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        result = []
        for item in monthly_data:
            result.append({
                'month': month_names[item['month_num'] - 1],
                'year': item['year_num'],
                'revenue': item['revenue']
            })

        serializer = MonthlyRevenueSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch monthly revenue: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def top_products(request):
    """
    Top Selling Products
    
    Returns top N products by quantity sold
    
    Method: GET
    Endpoint: /api/dashboard/top-products/
    
    Query Parameters:
        - limit (optional): Number of products to return (default: 5)
    
    Response:
        [
            {
                "product_id": 1,
                "product_name": "A4 Copy Paper 80 GSM",
                "product_sku": "PAP-A4-80",
                "quantity_sold": 500,
                "total_revenue": 25000.00
            }
        ]
    """
    try:
        limit = int(request.query_params.get('limit', 5))

        # Aggregate sales by product using select_related for performance
        top_products_data = Sale.objects.select_related('product').values(
            'product__id',
            'product__name',
            'product__sku'
        ).annotate(
            quantity_sold=Sum('quantity_sold'),
            total_revenue=Sum('total_price')
        ).order_by('-quantity_sold')[:limit]

        # Format the data
        result = []
        for item in top_products_data:
            result.append({
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'product_sku': item['product__sku'],
                'quantity_sold': item['quantity_sold'],
                'total_revenue': item['total_revenue']
            })

        serializer = TopProductSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch top products: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def low_stock_products(request):
    """
    Low Stock Products Alert
    
    Returns products where stock_quantity < reorder_level
    
    Method: GET
    Endpoint: /api/dashboard/low-stock-products/
    
    Response:
        [
            {
                "product_id": 5,
                "product_name": "Office Supplies",
                "sku": "OFF-SUP-001",
                "stock_quantity": 15,
                "reorder_level": 20,
                "unit_price": 150.00
            }
        ]
    """
    try:
        # Primary set: products below reorder level.
        low_stock = Product.objects.filter(
            stock_quantity__lt=F('reorder_level')
        ).values(
            'id',
            'name',
            'sku',
            'stock_quantity',
            'reorder_level',
            'unit_price'
        ).order_by('stock_quantity')

        # If nothing is currently below reorder level, return lowest-stock products
        # so the dashboard summary is still informative instead of empty.
        if not low_stock.exists():
            low_stock = Product.objects.values(
                'id',
                'name',
                'sku',
                'stock_quantity',
                'reorder_level',
                'unit_price'
            ).order_by('stock_quantity')[:10]

        # Format the data
        result = []
        for item in low_stock:
            result.append({
                'product_id': item['id'],
                'product_name': item['name'],
                'sku': item['sku'],
                'stock_quantity': item['stock_quantity'],
                'reorder_level': item['reorder_level'],
                'unit_price': item['unit_price'],
                'inventory_value': (item['unit_price'] or Decimal('0.00')) * (item['stock_quantity'] or 0),
                'isReorder': (item['stock_quantity'] or 0) < (item['reorder_level'] or 0),
            })

        serializer = LowStockProductSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch low stock products: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def recent_sales(request):
    """
    Recent Sales Transactions
    
    Returns the most recent sales transactions
    
    Method: GET
    Endpoint: /api/dashboard/recent-sales/
    
    Query Parameters:
        - limit (optional): Number of sales to return (default: 10)
    
    Response:
        [
            {
                "sale_id": 125,
                "product_name": "Laptop",
                "customer_name": "John Doe",
                "quantity_sold": 2,
                "total_price": 150000.00,
                "sale_date": "2023-10-15",
                "created_at": "2023-10-15T10:30:00Z"
            }
        ]
    """
    try:
        limit = int(request.query_params.get('limit', 10))

        # Use only stable sale fields so this endpoint works across schema variants.
        recent_sales_data = Sale.objects.select_related('product').values(
            'id',
            'product__name',
            'quantity_sold',
            'total_price',
            'sale_date',
            'created_at'
        ).order_by('-created_at')[:limit]

        # Format the data
        result = []
        for item in recent_sales_data:
            result.append({
                'sale_id': item['id'],
                'product_name': item['product__name'],
                'customer_name': 'Customer',
                'quantity_sold': item['quantity_sold'],
                'total_price': item['total_price'],
                'sale_date': item['sale_date'],
                'created_at': item['created_at']
            })

        serializer = RecentSaleSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch recent sales: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def outstanding_invoices(request):
    """
    Outstanding Invoices Details
    
    Returns detailed list of unpaid and partially paid invoices
    
    Method: GET
    Endpoint: /api/dashboard/outstanding-invoices/
    
    Response:
        [
            {
                "invoice_id": 10,
                "invoice_number": "INV-0010",
                "customer_name": "ABC Corp",
                "total_amount": 50000.00,
                "amount_paid": 20000.00,
                "balance_due": 30000.00,
                "due_date": "2023-11-01",
                "status": "PARTIALLY_PAID"
            }
        ]
    """
    try:
        # Get unpaid and partially paid invoices
        outstanding = Invoice.objects.filter(
            Q(status='UNPAID') | Q(status='PARTIALLY_PAID')
        ).annotate(
            balance=ExpressionWrapper(
                F('total_amount') - F('amount_paid'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        ).values(
            'id',
            'invoice_number',
            'customer_name',
            'total_amount',
            'amount_paid',
            'balance',
            'due_date',
            'status'
        ).order_by('due_date')

        return Response(list(outstanding), status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch outstanding invoices: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def sales_performance(request):
    """
    Sales Performance Over Time
    
    Returns aggregated sales data for performance analysis
    Useful for charts and graphs
    
    Method: GET
    Endpoint: /api/dashboard/sales-performance/
    
    Query Parameters:
        - period (optional): 'daily', 'weekly', 'monthly' (default: 'monthly')
        - year (optional): Filter by specific year
    
    Response:
        [
            {"period": "2023-10", "total_sales": 50, "revenue": 125000.00},
            {"period": "2023-11", "total_sales": 65, "revenue": 180000.00}
        ]
    """
    try:
        period = request.query_params.get('period', 'monthly')
        year_filter = request.query_params.get('year', None)

        queryset = Sale.objects.all()
        
        if year_filter:
            queryset = queryset.filter(sale_date__year=year_filter)

        if period == 'monthly':
            # Group by month
            performance_data = queryset.annotate(
                period_date=TruncMonth('sale_date')
            ).values('period_date').annotate(
                total_sales=Count('id'),
                revenue=Sum('total_price')
            ).order_by('period_date')
        else:
            # Default to monthly
            performance_data = queryset.annotate(
                period_date=TruncMonth('sale_date')
            ).values('period_date').annotate(
                total_sales=Count('id'),
                revenue=Sum('total_price')
            ).order_by('period_date')

        result = []
        for item in performance_data:
            result.append({
                'period': item['period_date'].strftime('%Y-%m') if item['period_date'] else 'N/A',
                'total_sales': item['total_sales'],
                'revenue': item['revenue']
            })

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch sales performance: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
