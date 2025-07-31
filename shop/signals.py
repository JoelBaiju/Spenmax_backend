from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import Branch


@receiver(post_save, sender=Branch)
def increment_company_branch_count(sender, instance, created, **kwargs):
    if created: # Check if a new Branch instance was created
        company = instance.company # Get the associated Company instance
        company.branch_count += 1 # Increment the branch_count
        company.save()