from django.contrib import admin
from .models import Product, Order, Cart
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=("id","name","price")
    list_filter=("name",)
    list_editable=("price",)
    search_fields=("name",)
    ordering=("id",)
    actions=['Mark_Free']
    
    def Mark_Free(self,request,queryset):
        queryset.update(price=0)
        self.message_user(request,"Selected product has been marked as free")
        
    Mark_Free.short_description ="Mark selected product as free"

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
