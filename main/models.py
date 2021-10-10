from django.db import models, IntegrityError


class Candidate(models.Model):
    name = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)
    frontend = models.IntegerField(default=1)
    backend = models.IntegerField(default=1)
    fullstack = models.IntegerField(default=1)
    devOps = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Vote(models.Model):
    ip_address = models.CharField(
        max_length=50,
        default="None",
        unique=True
    )
    candidate = models.ForeignKey(
        to=Candidate,
        on_delete=models.CASCADE,
        related_name='vote'
    )

    def save(self, commit=True, *args, **kwargs):

        if commit:
            try:
                self.candidate.votes += 1
                self.candidate.save()
                super(Vote, self).save(*args, **kwargs)

            except IntegrityError:
                self.candidate.votes -= 1
                self.candidate.save()
                raise IntegrityError

        else:
            raise IntegrityError

    def __str__(self):
        return self.candidate.name
