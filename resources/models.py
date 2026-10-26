from django.db import models
from accounts.models import Student

class ResourceItem(models.Model):

                                    
              
                                    

    CATEGORY_CHOICES = [
        ('books', 'Books'),
        ('notes', 'Notes'),
        ('equipment', 'Equipment'),
        ('previous_questions', 'Previous Questions'),
        ('course_materials', 'Course Materials'),
    ]


                                    
                
                                    

    SHARE_TYPE_CHOICES = [
        ('share', 'Share'),
        ('rent', 'Rent'),
        ('sell', 'Sell'),
    ]


                                
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="resource_items",
        null=True,
        blank=True
    )


    title = models.CharField(
        max_length=200
    )


    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )


    description = models.TextField(
        blank=True
    )


    author = models.CharField(
        max_length=150,
        blank=True
    )


    department = models.CharField(
        max_length=100,
        blank=True
    )


    course_code = models.CharField(
        max_length=50,
        blank=True
    )


                                                
                         
     
                
                           
     
                       
                  
                                                

    share_type = models.CharField(
        max_length=20,
        choices=SHARE_TYPE_CHOICES,
        default='share'
    )


                                         
    price = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        null=True,
        blank=True
    )


    file = models.FileField(
        upload_to='resources/',
        blank=True,
        null=True
    )


    image = models.ImageField(
        upload_to='resource_images/',
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.title

class ResourceReview(models.Model):
    resource = models.ForeignKey(ResourceItem, on_delete=models.CASCADE, related_name="reviews")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="resource_reviews")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource.title} - {self.rating}/5"
