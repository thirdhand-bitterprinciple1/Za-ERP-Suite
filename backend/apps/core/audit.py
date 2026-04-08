from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save, post_delete
from django.forms.models import model_to_dict
from django.dispatch import receiver

from apps.core.context import get_current_user
from apps.core.models import AuditLog


def _is_auditable_instance(instance) -> bool:
    app_label = instance._meta.app_label
    if app_label not in {
        "accounting",
        "billing",
        "commerce",
        "crm",
        "hr",
        "inventory",
        "orgs",
        "partners",
        "projects",
        "purchasing",
        "reports",
        "website",
    }:
        return False
    return instance.__class__.__name__ != "AuditLog"


def _snapshot(instance):
    return model_to_dict(instance)


def _company_for(instance):
    return getattr(instance, "company", None)


@receiver(pre_save)
def capture_old_values(sender, instance, **kwargs):
    if not _is_auditable_instance(instance) or not instance.pk:
        return

    prior = sender.objects.filter(pk=instance.pk).first()
    if prior:
        instance._audit_old_values = _snapshot(prior)


@receiver(post_save)
def write_save_audit(sender, instance, created, **kwargs):
    if not _is_auditable_instance(instance):
        return

    user = get_current_user()
    old_values = getattr(instance, "_audit_old_values", {}) if not created else {}
    new_values = _snapshot(instance)

    AuditLog.objects.create(
        company=_company_for(instance),
        user=user if getattr(user, "is_authenticated", False) else None,
        action=AuditLog.Action.CREATE if created else AuditLog.Action.UPDATE,
        content_type=ContentType.objects.get_for_model(instance.__class__),
        object_id=str(instance.pk),
        old_values=old_values,
        new_values=new_values,
    )


@receiver(post_delete)
def write_delete_audit(sender, instance, **kwargs):
    if not _is_auditable_instance(instance):
        return

    user = get_current_user()
    old_values = _snapshot(instance)

    AuditLog.objects.create(
        company=_company_for(instance),
        user=user if getattr(user, "is_authenticated", False) else None,
        action=AuditLog.Action.DELETE,
        content_type=ContentType.objects.get_for_model(instance.__class__),
        object_id=str(instance.pk),
        old_values=old_values,
        new_values={},
    )
