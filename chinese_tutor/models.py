from django.db import models


class FlashCard(models.Model):
    stimulus = models.CharField(max_length=200)
    response = models.CharField(max_length=200)
    response_type = models.CharField(max_length=200)

    def __str__(self):
        return str((self.id, self.stimulus, self.response_type, self.response))


class UserAttempt(models.Model):
    user = models.CharField(max_length=200)
    flash_card = models.ForeignKey(FlashCard, related_name="flash_card")
    user_response = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((self.user, self.flash_card.stimulus, self.user_response,
                    self.user_response == self.flash_card.response))
