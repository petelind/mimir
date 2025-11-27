from django.conf import settings
from django.db import models
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


class UserOnboardingState(models.Model):
    """Persistent onboarding state for a user.

    Tracks whether onboarding is completed and current step index.

    Fields:
        user (OneToOneField): Related auth user. Example: User(username="maria")
        is_completed (bool): Onboarding completion flag. Example: True
        current_step (int): Current onboarding step index. Example: 0
        completed_at (datetime|None): When onboarding was completed. Example: 2025-01-01T10:00Z
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="onboarding_state",
    )
    is_completed = models.BooleanField(default=False)
    current_step = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"OnboardingState(user={self.user!s}, completed={self.is_completed}, step={self.current_step})"


def get_or_create_onboarding_state(user):
    """Return existing or newly created onboarding state for given user.

    :param user: Django auth user instance. Example: request.user
    :return: UserOnboardingState instance for user. Example: UserOnboardingState(...)
    """
    state, created = UserOnboardingState.objects.get_or_create(user=user)

    if created:
        logger.info("[ONBOARDING] Created onboarding state for user %s", user.username)
    else:
        logger.debug("[ONBOARDING] Retrieved existing onboarding state for user %s", user.username)

    return state


def mark_onboarding_completed(user, step=0):
    """Mark onboarding as completed for the given user.

    Side effects:
        - Ensures onboarding state row exists
        - Sets is_completed=True
        - Sets current_step to provided step (default 0)
        - Updates completed_at timestamp

    :param user: Django auth user instance. Example: request.user
    :param step: int - Final onboarding step index. Example: 0
    :return: Updated UserOnboardingState instance
    """
    state = get_or_create_onboarding_state(user)

    state.is_completed = True
    state.current_step = step
    state.completed_at = timezone.now()
    state.save(update_fields=["is_completed", "current_step", "completed_at"])

    logger.info(
        "[ONBOARDING] Marked onboarding completed for user %s (step=%s)",
        user.username,
        step,
    )

    return state

