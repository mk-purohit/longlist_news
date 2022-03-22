from django.db import models

# Create your models here.

# to store the new results.
class Newsitem(models.Model):   
    title = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    source = models.CharField(max_length=255)
    snippet = models.CharField(max_length=255)
    date_posted = models.DateField()

    def __str__(self):
        return self.title


# to store the search keys 
class Key(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# to store company names for framing the key to search
class Company(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name


# To store the News sources
class Postingsite(models.Model):
    name = models.CharField(max_length=255)
    quality = models.BooleanField(default=True)

    def __str__(self):
        return self.name
