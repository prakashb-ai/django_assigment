from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Vendor,PurchaseOrder,HistoricalPerformance
from .serializers import VendorSerializer,PurchaseOrderSerializer,HistoricalPerformanceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def create_vendor(request):
    if request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_vendor(request, vendor_id):
    if request.method == 'GET':
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

@api_view(['PUT'])
def update_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    if request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    if request.method == 'DELETE':
        vendor.delete()
        return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


def create_purchase_order(request):
    if request.method == 'POST':
        data = request.POST  
        purchase_order = PurchaseOrderSerializer.objects.create(
            po_number=data['po_number'],
            vendor_id=data['vendor_id'], 
            order_date=data['order_date'],
            delivery_date=data['delivery_date'],
            items=data['items'],
            quantity=data['quantity'],
            status=data['status'],
            quality_rating=data.get('quality_rating'),
            acknowledgment_date=data.get('acknowledgment_date')
        )
        return JsonResponse({'message': 'Purchase Order created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def list_purchase_orders(request):
    purchase_orders = PurchaseOrder.objects.all()
    data = [{'po_number': po.po_number, 'status': po.status} for po in purchase_orders]
    return JsonResponse(data, safe=False)

def get_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    data = {
        'po_number': purchase_order.po_number,
        'vendor': purchase_order.vendor.id,
        'order_date': purchase_order.order_date,
        'delivery_date': purchase_order.delivery_date,
        'items': purchase_order.items,
        'quantity': purchase_order.quantity,
        'status': purchase_order.status,
        'quality_rating': purchase_order.quality_rating,
        'issue_date': purchase_order.issue_date,
        'acknowledgment_date': purchase_order.acknowledgment_date
    }
    return JsonResponse(data)

def update_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'PUT':
        data = request.POST 
        purchase_order.po_number = data['po_number']
        purchase_order.vendor_id = data['vendor_id']
        purchase_order.order_date = data['order_date']
        purchase_order.delivery_date = data['delivery_date']
        purchase_order.items = data['items']
        purchase_order.quantity = data['quantity']
        purchase_order.status = data['status']
        purchase_order.quality_rating = data.get('quality_rating')
        purchase_order.acknowledgment_date = data.get('acknowledgment_date')
        purchase_order.save()
        return JsonResponse({'message': 'Purchase Order updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def delete_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    purchase_order.delete()
    return JsonResponse({'message': 'Purchase Order deleted successfully'}, status=204)



@api_view(['GET'])
def get_historical_performance(request, vendor_id):
    historical_performance = HistoricalPerformance.objects.filter(vendor_id=vendor_id)
    serializer = HistoricalPerformanceSerializer(historical_performance, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_historical_performance(request):
    serializer = HistoricalPerformanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_historical_performance(request, hp_id):
    historical_performance = get_object_or_404(HistoricalPerformance, id=hp_id)
    serializer = HistoricalPerformanceSerializer(historical_performance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_historical_performance(request, hp_id):
    historical_performance = get_object_or_404(HistoricalPerformance, id=hp_id)
    historical_performance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)