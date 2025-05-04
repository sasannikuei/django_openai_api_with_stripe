from django.db import models


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="usd")
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField()


class ShowTable(models.Model):
    phrase = models.CharField(max_length=100)
    ai_image = models.ImageField(upload_to='tables/')

    def __str__(self):
        return str(self.phrase)