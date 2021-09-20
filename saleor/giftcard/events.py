from typing import Iterable, Optional, Tuple

from ..account.models import User
from ..app.models import App
from ..core.utils.validators import user_is_valid
from . import GiftCardEvents
from .models import GiftCard, GiftCardEvent

UserType = Optional[User]
AppType = Optional[App]


def gift_card_issued_event(
    gift_card: GiftCard,
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    balance_data = {
        "currency": gift_card.currency,
        "initial_balance": gift_card.initial_balance_amount,
        "current_balance": gift_card.current_balance_amount,
    }
    return GiftCardEvent.objects.create(
        gift_card=gift_card,
        user=user,
        app=app,
        type=GiftCardEvents.ISSUED,
        parameters={"balance": balance_data, "expiry_date": gift_card.expiry_date},
    )


def gift_card_sent_event(
    gift_card_id: int, user_id: Optional[int], app_id: Optional[int], email: str
):
    return GiftCardEvent.objects.create(
        gift_card_id=gift_card_id,
        user_id=user_id,
        app_id=app_id,
        type=GiftCardEvents.SENT_TO_CUSTOMER,
        parameters={"email": email},
    )


def gift_card_resent_event(
    gift_card_id: int, user_id: Optional[int], app_id: Optional[int], email: str
):
    return GiftCardEvent.objects.create(
        gift_card_id=gift_card_id,
        user_id=user_id,
        app_id=app_id,
        type=GiftCardEvents.RESENT,
        parameters={"email": email},
    )


def gift_card_balance_reset_event(
    gift_card: GiftCard,
    old_gift_card: GiftCard,
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    balance_data = {
        "currency": gift_card.currency,
        "initial_balance": gift_card.initial_balance_amount,
        "current_balance": gift_card.current_balance_amount,
        "old_currency": gift_card.currency,
        "old_initial_balance": old_gift_card.initial_balance_amount,
        "old_current_balance": old_gift_card.current_balance_amount,
    }
    return GiftCardEvent.objects.create(
        gift_card=gift_card,
        user=user,
        app=app,
        type=GiftCardEvents.BALANCE_RESET,
        parameters={"balance": balance_data},
    )


def gift_card_expiry_date_updated_event(
    gift_card: GiftCard,
    old_gift_card: GiftCard,
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    return GiftCardEvent.objects.create(
        gift_card=gift_card,
        user=user,
        app=app,
        type=GiftCardEvents.EXPIRY_DATE_UPDATED,
        parameters={
            "expiry_date": gift_card.expiry_date,
            "old_expiry_date": old_gift_card.expiry_date,
        },
    )


def gift_card_tag_updated_event(
    gift_card: GiftCard,
    old_gift_card: GiftCard,
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    return GiftCardEvent.objects.create(
        gift_card=gift_card,
        user=user,
        app=app,
        type=GiftCardEvents.TAG_UPDATED,
        parameters={
            "tag": gift_card.tag,
            "old_tag": old_gift_card.tag,
        },
    )


def gift_card_activated_event(
    gift_card: GiftCard,
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    return GiftCardEvent.objects.create(
        gift_card=gift_card,
        user=user,
        app=app,
        type=GiftCardEvents.ACTIVATED,
    )


def gift_card_deactivated_event(
    gift_card: GiftCard,
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    return GiftCardEvent.objects.create(
        gift_card=gift_card,
        user=user,
        app=app,
        type=GiftCardEvents.DEACTIVATED,
    )


def gift_cards_activated_event(
    gift_card_ids: Iterable[int],
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    events = [
        GiftCardEvent(
            gift_card_id=gift_card_id,
            user=user,
            app=app,
            type=GiftCardEvents.ACTIVATED,
        )
        for gift_card_id in gift_card_ids
    ]
    return GiftCardEvent.objects.bulk_create(events)


def gift_cards_deactivated_event(
    gift_card_ids: Iterable[int],
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    events = [
        GiftCardEvent(
            gift_card_id=gift_card_id,
            user=user,
            app=app,
            type=GiftCardEvents.DEACTIVATED,
        )
        for gift_card_id in gift_card_ids
    ]
    return GiftCardEvent.objects.bulk_create(events)


def gift_card_note_added_event(
    gift_card: GiftCard, user: UserType, app: AppType, message: str
) -> GiftCardEvent:
    if not user_is_valid(user):
        user = None
    return GiftCardEvent.objects.create(
        gift_card=gift_card,
        user=user,
        app=app,
        type=GiftCardEvents.NOTE_ADDED,
        parameters={"message": message},
    )


def gift_cards_used_in_order_event(
    balance_data: Iterable[Tuple[GiftCard, float]],
    order_id: int,
    user: UserType,
    app: AppType,
):
    if not user_is_valid(user):
        user = None
    events = [
        GiftCardEvent(
            gift_card=gift_card,
            user=user,
            app=app,
            type=GiftCardEvents.USED_IN_ORDER,
            parameters={
                "order_id": order_id,
                "balance": {
                    "currency": gift_card.currency,
                    "current_balance": gift_card.current_balance.amount,
                    "old_current_balance": previous_balance,
                },
            },
        )
        for gift_card, previous_balance in balance_data
    ]
    return GiftCardEvent.objects.bulk_create(events)


def gift_cards_bought_event(
    gift_cards: Iterable[GiftCard], order_id: int, user: UserType, app: AppType
):
    if not user_is_valid(user):
        user = None
    events = [
        GiftCardEvent(
            gift_card=gift_card,
            user=user,
            app=app,
            type=GiftCardEvents.BOUGHT,
            parameters={"order_id": order_id, "expiry_date": gift_card.expiry_date},
        )
        for gift_card in gift_cards
    ]
    return GiftCardEvent.objects.bulk_create(events)