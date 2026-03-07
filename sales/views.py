from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Sale
from .serializers import SaleSerializer


@api_view(['GET', 'POST'])
def sale_list(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    serializer = SaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    if request.method == 'GET':
        serializer = SaleSerializer(sale)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SaleSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    sale.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
