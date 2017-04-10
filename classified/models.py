from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator


CLASSIFIED_CATEGORIES = (('Automotive', 'Automotive'),
                        ('Real Estate', 'Real Estate'),
                        ('Employment', 'Employment'),
                        ('Merchandise', 'Merchandise'),
                        ('Pets & Animals', 'Pets & Animals'),
                        ('Tuition & Lessons', 'Tuition & Lessons'),
                        ('Services', 'Services'),
                        ('Community', 'Community'),)



class Address(models.Model):
    user = models.OneToOneField(User)
    street_no = models.CharField(max_length=5)
    street_name = models.CharField(max_length=100)
    unit_no = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=7, validators=[RegexValidator(r'^[ABCEGHJKLMNPRSTVXYabceghjklmnprstvxy][0-9][ABCEGHJKLMNPRSTVWXYZabceghjklmnprstvxy] ?[0-9][ABCEGHJKLMNPRSTVWXYZabceghjklmnprstvxy][0-9]$', "Invalid Postal Code")])
    country = models.CharField(max_length=20, default="Canada")
    updated_at = models.DateTimeField(auto_now=True)


class PaymentMethod(models.Model):
    user = models.ForeignKey(User)
    card_no = models.CharField(max_length=20)
    card_type = models.CharField(max_length=20)
    cvc_no = models.CharField(max_length=3)
    billing_address = models.OneToOneField(Address)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone =  models.CharField(max_length=15, blank=True, null=True)
    photo = models.TextField(validators=[URLValidator()], blank=True, null=True)
    facebook = models.CharField(max_length=25, blank=True, null=True)
    twitter = models.CharField(max_length=25, blank=True, null=True)
    google = models.CharField(max_length=25, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class AdPackage(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    days_valid = models.IntegerField()

    def __str__(self):
        return self.name



class AdMainCategory(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField()
    image = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


class AdSubCategory(models.Model):
    name = models.CharField(max_length=1000)
    parent_category = models.ForeignKey(AdMainCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField()

    def __str__(self):
        return self.name



class Advertisement(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    main_category = models.ForeignKey(AdMainCategory)
    sub_category = models.ForeignKey(AdSubCategory)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=50)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=7, validators=[RegexValidator(r'^[ABCEGHJKLMNPRSTVXYabceghjklmnprstvxy][0-9][ABCEGHJKLMNPRSTVWXYZabceghjklmnprstvxy] ?[0-9][ABCEGHJKLMNPRSTVWXYZabceghjklmnprstvxy][0-9]$', "Invalid Postal Code")])
    package = models.ForeignKey(AdPackage)
    photos = models.TextField(blank=True, null=True)
    video = models.TextField(blank=True, null=True)
    visits = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    thumbnail = models.CharField(max_length=1000, blank=True, null=True)
    website = models.CharField(max_length=1000, blank=True, null=True)
    favourited_by = models.ManyToManyField(User, related_name="favorited_users")

    def __str__(self):
        return self.title


class AdvertisementMeta(models.Model):
    advertisement = models.OneToOneField(Advertisement)
    condition = models.CharField(max_length=25, blank=True, null=True)
    make = models.CharField(max_length=25, blank=True, null=True)
    model = models.CharField(max_length=25, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    mileage = models.CharField(max_length=25, blank=True, null=True)
    transmission = models.CharField(max_length=25, blank=True, null=True)
    body_type = models.CharField(max_length=25, blank=True, null=True)
    colour = models.CharField(max_length=25, blank=True, null=True)
    building_type = models.CharField(max_length=25, blank=True, null=True)
    size = models.CharField(max_length=25, blank=True, null=True)
    no_bedrooms = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    no_bathrooms = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    is_pet_friendly = models.BooleanField(default=False)
    no_parking_spaces = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    avaiable_move_in = models.DateTimeField(blank=True, null=True)
    job_type = models.CharField(max_length=25, blank=True, null=True)
    company = models.CharField(max_length=25, blank=True, null=True)
    salary = models.CharField(max_length=25, blank=True, null=True)
    location = models.CharField(max_length=25, blank=True, null=True)
    






class Transaction(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.OneToOneField(PaymentMethod)
    item = models.CharField(max_length=25)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.item


class BusinessPackage(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    days_valid = models.IntegerField()

    def __str__(self):
        return self.name


class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    main_category = models.CharField(max_length=50)
    address = models.OneToOneField(Address)
    description = models.TextField(blank=True, null=True)
    photos = ArrayField(models.TextField(validators=[URLValidator()]), blank=True, null=True)
    video = models.TextField(validators=[URLValidator()], blank=True, null=True)
    open_hours = models.TextField(blank=True, null=True)
    biz_email = models.EmailField(blank=True, null=True)
    biz_website = models.TextField(validators=[URLValidator()], blank=True, null=True)
    facebook = models.CharField(max_length=25, blank=True, null=True)
    twitter = models.CharField(max_length=25, blank=True, null=True)
    google = models.CharField(max_length=25, blank=True, null=True)    
    package = models.ForeignKey(BusinessPackage)
    visits = models.IntegerField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=1000, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    business = models.ForeignKey(Business)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    location = models.OneToOneField(Address)
    photos = ArrayField(models.TextField(validators=[URLValidator()]), blank=True, null=True)
    video = models.TextField(validators=[URLValidator()], blank=True, null=True)
    page_link = models.TextField(validators=[URLValidator()], blank=True, null=True)
    packages = models.ForeignKey(AdPackage, on_delete=models.CASCADE)
    visits = models.IntegerField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name