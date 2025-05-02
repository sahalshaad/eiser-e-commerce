from django.db import models

# Create your models here.
class signup(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    pro_pic = models.FileField(upload_to='profile_pic/')
    
class Contact(models.Model):
    messege = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    user = models.ForeignKey(signup, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.category.name} > {self.name}"
    
class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='product/')
    
    def __str__(self):
        return self.name
    