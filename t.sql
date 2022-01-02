SELECT
  "payment_payment"."id",
  "payment_payment"."private_metadata",
  "payment_payment"."metadata",
  "payment_payment"."gateway",
  "payment_payment"."is_active",
  "payment_payment"."to_confirm",
  "payment_payment"."created",
  "payment_payment"."modified",
  "payment_payment"."charge_status",
  "payment_payment"."token",
  "payment_payment"."total",
  "payment_payment"."captured_amount",
  "payment_payment"."currency",
  "payment_payment"."checkout_id",
  "payment_payment"."order_id",
  "payment_payment"."store_payment_method",
  "payment_payment"."billing_email",
  "payment_payment"."billing_first_name",
  "payment_payment"."billing_last_name",
  "payment_payment"."billing_company_name",
  "payment_payment"."billing_address_1",
  "payment_payment"."billing_address_2",
  "payment_payment"."billing_city",
  "payment_payment"."billing_city_area",
  "payment_payment"."billing_postal_code",
  "payment_payment"."billing_country_code",
  "payment_payment"."billing_country_area",
  "payment_payment"."cc_first_digits",
  "payment_payment"."cc_last_digits",
  "payment_payment"."cc_brand",
  "payment_payment"."cc_exp_month",
  "payment_payment"."cc_exp_year",
  "payment_payment"."payment_method_type",
  "payment_payment"."customer_ip_address",
  "payment_payment"."extra_data",
  "payment_payment"."return_url",
  "payment_payment"."psp_reference"
FROM
  "payment_payment"
  LEFT OUTER JOIN "order_order" ON (
    "payment_payment"."order_id" = "order_order"."id"
  )
  LEFT OUTER JOIN "checkout_checkout" ON (
    "payment_payment"."checkout_id" = "checkout_checkout"."token"
  )
WHERE
  (
    (
      "order_order"."user_id" = 603
      OR "checkout_checkout"."user_id" = 603
    )
    AND "payment_payment"."id" = 1
  )
ORDER BY
  "payment_payment"."id" ASC
LIMIT
  1