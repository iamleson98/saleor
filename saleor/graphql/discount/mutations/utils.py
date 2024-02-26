from collections import defaultdict

import graphene
from django.db.models import QuerySet

from ....discount.models import Promotion, PromotionRule
from ....discount.utils import CatalogueInfo, update_rule_variant_relation
from ....product.models import ProductVariant

CATALOGUE_FIELD_TO_TYPE_NAME = {
    "categories": "Category",
    "collections": "Collection",
    "products": "Product",
    "variants": "ProductVariant",
}


def convert_catalogue_info_to_global_ids(
    catalogue_info: CatalogueInfo,
) -> defaultdict[str, set[str]]:
    converted_catalogue_info: defaultdict[str, set[str]] = defaultdict(set)

    for catalogue_field, type_name in CATALOGUE_FIELD_TO_TYPE_NAME.items():
        converted_catalogue_info[catalogue_field].update(
            graphene.Node.to_global_id(type_name, id_)
            for id_ in catalogue_info[catalogue_field]
        )
    return converted_catalogue_info


def clear_promotion_old_sale_id(promotion: Promotion, *, save=False):
    """Clear the promotion `old_sale_id` if set."""
    if promotion.old_sale_id:
        promotion.old_sale_id = None
        if save:
            promotion.save(update_fields=["old_sale_id"])


def update_variants_for_promotion(
    variants: QuerySet["ProductVariant"], promotion: "Promotion"
):
    PromotionRuleVariant = PromotionRule.variants.through
    rules = PromotionRule.objects.filter(promotion_id=promotion.id)
    promotion_rule_variants = []
    for rule_id in promotion.rules.values_list("id", flat=True):
        promotion_rule_variants.extend(
            [
                PromotionRuleVariant(
                    promotionrule_id=rule_id, productvariant_id=variant.pk
                )
                for variant in variants
            ]
        )
    update_rule_variant_relation(rules, promotion_rule_variants)
