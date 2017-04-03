from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields if field.name != "id"]
admin.site.register(UserProfile, UserProfileAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Address._meta.fields if field.name != "id"]
admin.site.register(Address, AddressAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.fields if field.name != "id"]
admin.site.register(Transaction, TransactionAdmin)

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PaymentMethod._meta.fields if field.name != "id"]
admin.site.register(PaymentMethod, PaymentMethodAdmin)



class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Advertisement._meta.fields if field.name != "id"]
admin.site.register(Advertisement, AdvertisementAdmin)

class AutomotiveMetaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AutomotiveMeta._meta.fields if field.name != "id"]
admin.site.register(AutomotiveMeta, AutomotiveMetaAdmin)

class RealEstateMetaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RealEstateMeta._meta.fields if field.name != "id"]
admin.site.register(RealEstateMeta, RealEstateMetaAdmin)

class EmploymentMetaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmploymentMeta._meta.fields if field.name != "id"]
admin.site.register(EmploymentMeta, EmploymentMetaAdmin)

class AdPackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AdPackage._meta.fields if field.name != "id"]
admin.site.register(AdPackage, AdPackageAdmin)

class AdMainCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AdMainCategory._meta.fields if field.name != "id"]
admin.site.register(AdMainCategory, AdMainCategoryAdmin)

class AdSubCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AdSubCategory._meta.fields if field.name != "id"]
admin.site.register(AdSubCategory, AdSubCategoryAdmin)



class BusinessAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Business._meta.fields if field.name != "id"]
admin.site.register(Business, BusinessAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Review._meta.fields if field.name != "id"]
admin.site.register(Review, ReviewAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields if field.name != "id"]
admin.site.register(Event, EventAdmin)

class BusinessPackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BusinessPackage._meta.fields if field.name != "id"]
admin.site.register(BusinessPackage, BusinessPackageAdmin)
