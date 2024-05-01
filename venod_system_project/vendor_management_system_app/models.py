from django.db import models
from django.db.models import Avg, Count, F, ExpressionWrapper, fields

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfilment_rate = models.FloatField(default=0)

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50)
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    items = models.TextField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update Vendor's On-Time Delivery Rate
        if self.status == 'completed':
            completed_pos_count = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed').count()
            on_time_deliveries_count = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed', delivery_date__lte=self.delivery_date).count()
            if completed_pos_count > 0:
                self.vendor.on_time_delivery_rate = (on_time_deliveries_count / completed_pos_count) * 100
                self.vendor.save()

        # Update Vendor's Quality Rating Average
        if self.quality_rating is not None and self.status == 'completed':
            completed_pos = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed', quality_rating__isnull=False)
            total_rating = sum([pos.quality_rating for pos in completed_pos])
            if completed_pos.count() > 0:
                self.vendor.quality_rating_avg = total_rating / completed_pos.count()
                self.vendor.save()

        # Update Vendor's Average Response Time
        if self.acknowledgment_date is not None:
            response_time_expr = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())
            avg_response_time = PurchaseOrder.objects.filter(vendor=self.vendor, acknowledgment_date__isnull=False).annotate(response_time=response_time_expr).aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
            if avg_response_time is not None:
                self.vendor.average_response_time = avg_response_time.total_seconds() / 60  # Convert to minutes
                self.vendor.save()

        # Update Vendor's Fulfilment Rate
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed').count()
        total_pos = PurchaseOrder.objects.filter(vendor=self.vendor).count()
        if total_pos > 0:
            self.vendor.fulfilment_rate = (fulfilled_pos / total_pos) * 100
            self.vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfilment_rate = models.FloatField()
