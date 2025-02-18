from django.db import models

from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=120)
    ticker = models.CharField(max_length=20, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class StockQuote(models.Model):
    """
    POLYGON DATA

    "volume": result["v"],
    "vwap": result["vw"],
    "open": result["o"],
    "close": result["c"],
    "high": result["h"],
    "low": result["l"],
    "timestamp": utc_timestamp,  
    "no_of_transactions": result["n"]
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="stock_quote"
    )
    open = models.DecimalField(max_digits=10, decimal_places=4)
    close = models.DecimalField(max_digits=10, decimal_places=4)
    high = models.DecimalField(max_digits=10, decimal_places=4)
    low = models.DecimalField(max_digits=10, decimal_places=4)
    no_of_transactions = models.BigIntegerField(null=True, blank=True)
    volume = models.BigIntegerField()
    vwap = models.DecimalField(max_digits=10, decimal_places=4)
    time = TimescaleDateTimeField(interval="1 week")
    objects = TimescaleManager()
    timescale = TimescaleManager()

    class Meta:
        # combine fields and check the uniqueness
        unique_together = [("company", "time")]
    
    
