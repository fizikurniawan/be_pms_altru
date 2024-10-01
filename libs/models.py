import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        # Soft delete: update `deleted_at` field
        return super().update(
            deleted_at=timezone.now(),
            deleted_at_timestamp=int(timezone.now().timestamp()),
        )

    def hard_delete(self):
        # Permanent delete (optional)
        return super().delete()

    def alive(self):
        # Return objects that are not soft-deleted
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        # Return only soft-deleted objects
        return self.filter(deleted_at__isnull=False)


class BaseModel(models.Model):
    # UUID as lookup field
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )

    created_at = models.DateTimeField()
    created_at_timestamp = models.IntegerField()
    updated_at = models.DateTimeField()
    updated_at_timestamp = models.IntegerField()

    # Soft delete fields
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_at_timestamp = models.IntegerField(null=True, blank=True)

    # Fields to track user actions
    created_by = models.ForeignKey(
        User,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    deleted_by = models.ForeignKey(
        User,
        related_name="%(class)s_deleted_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Custom queryset for soft delete
    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Set `created_at_timestamp` only on creation
        now = timezone.now()
        if not self.created_at:
            self.created_at = now
            self.created_at_timestamp = int(now.timestamp())

        # Always set `updated_at_timestamp`
        self.updated_at = now
        self.updated_at_timestamp = int(now.timestamp())

        # Save again if it's new or `created_at_timestamp` wasn't set
        super().save()

    def delete(self, *args, **kwargs):
        # Soft delete logic
        self.deleted_at = timezone.now()
        self.deleted_at_timestamp = int(self.deleted_at.timestamp())
        self.deleted_by = kwargs.get("deleted_by", None)  # Track who deleted
        self.save()

    def restore(self):
        # Clear deleted_at fields for restore
        self.deleted_at = None
        self.deleted_at_timestamp = None
        self.deleted_by = None
        self.save()
