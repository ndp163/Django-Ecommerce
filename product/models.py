from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse

# Create your models here.

class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])
 
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']

    

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/',null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount = models.IntegerField(default=0)
    minamount = models.IntegerField(default=3)
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10,choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    image_tag.short_description = 'Image'



class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title