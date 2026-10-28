from typing import Any
from django.utils import timezone

from core.models import ClientReview, Order
from core.errors import (
    ClientReviewNotFoundError,
    InvalidScoreError,
    InvalidReviewDateError,
    OrderNotFoundError,
)
from users.models import Client
from users.errors import ClientNotFoundError

def create_client_review(current_client: Client, params: dict[str, Any]) -> ClientReview:
    if current_client is None:
        raise ClientNotFoundError

    score = params["score"]
    if score < 1 or score > 5:
        raise InvalidScoreError

    order = params.get("order")
    order_id = params.get("order_id")
    if order is None:
        if order_id is None:
            raise OrderNotFoundError
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise OrderNotFoundError

    new_review = ClientReview(
        score=score,
        notes=params.get("notes"),
        client=current_client,
        order=order,
    )
    new_review.save()

    return new_review


def list_client_reviews(params: dict[str, Any]):
    minimum_date = params.get("minimum_date")
    maximum_date = params.get("maximum_date")
    minimum_score = params.get("minimum_score")
    maximum_score = params.get("maximum_score")

    if (minimum_date is not None) and (maximum_date is not None):
        if minimum_date > maximum_date:
            raise InvalidReviewDateError

    if (minimum_score is not None) and (maximum_score is not None):
        if minimum_score > maximum_score:
            raise InvalidScoreError

    if (minimum_score is not None) and (minimum_score < 1 or minimum_score > 5):
        raise InvalidScoreError

    if (maximum_score is not None) and (maximum_score < 1 or maximum_score > 5):
        raise InvalidScoreError

    reviews = ClientReview.objects.all()

    review_id = params.get("id")
    if review_id is not None:
        reviews = reviews.filter(pk=review_id)

    if minimum_date is not None:
        reviews = reviews.filter(created_at__gte=minimum_date)

    if maximum_date is not None:
        reviews = reviews.filter(created_at__lte=maximum_date)

    if minimum_score is not None:
        reviews = reviews.filter(score__gte=minimum_score)

    if maximum_score is not None:
        reviews = reviews.filter(score__lte=maximum_score)

    notes = params.get("notes")
    if notes is not None:
        reviews = reviews.filter(notes__icontains=notes)

    client_id = params.get("client_id")
    if client_id is not None:
        reviews = reviews.filter(client__id=client_id)

    order_id = params.get("order_id")
    if order_id is not None:
        reviews = reviews.filter(order__id=order_id)

    if not reviews.exists():
        raise ClientReviewNotFoundError

    return reviews


def update_client_review(current_client: Client, params: dict[str, Any]) -> ClientReview:
    if current_client is None:
        raise ClientNotFoundError

    try:
        target_review = ClientReview.objects.get(pk=params["id"], client=current_client)
    except ClientReview.DoesNotExist:
        raise ClientReviewNotFoundError

    score = params.get("score")
    if score is not None:
        if score < 1 or score > 5:
            raise InvalidScoreError
        target_review.score = score

    notes = params.get("notes")
    if notes is not None:
        target_review.notes = notes

    target_review.last_edited_at = timezone.now()
    target_review.save()

    return target_review


def delete_client_review(current_client: Client, target_review_id: int) -> None:
    if current_client is None:
        raise ClientNotFoundError

    try:
        target_review = ClientReview.objects.get(pk=target_review_id, client=current_client)
    except ClientReview.DoesNotExist:
        raise ClientReviewNotFoundError

    target_review.delete()

