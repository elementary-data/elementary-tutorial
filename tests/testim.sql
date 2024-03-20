{{
    config(
        severity='error',
        meta={'owner': ['noy@elementary-data.com']}
    )
}}

SELECT
  *
FROM {{ ref('elementary_test_results') }} AS "ETR"
LEFT JOIN {{ ref('test_result_rows') }} AS "TRR"
  ON "ETR"."ID" = "TRR"."ELEMENTARY_TEST_RESULTS_ID"
WHERE
  NOT "ETR"."COLUMN_NAME" IS NULL
ORDER BY
  "ETR"."TEST_TYPE" DESC NULLS FIRST
