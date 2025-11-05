from django.db import models


class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    certificate_hash = models.CharField(max_length=256)
    previous_hash = models.CharField(max_length=256)
    nonce = models.IntegerField()
    issuer = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Block {self.index} - {self.certificate_hash[:10]}..."


