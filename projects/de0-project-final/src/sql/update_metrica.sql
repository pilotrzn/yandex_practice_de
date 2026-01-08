MERGE INTO STV202504297__DWH.global_metrics gm
USING 
	(WITH transactions AS (
		SELECT 
			operation_id,
			account_number_from,
			account_number_to,
			currency_code,
			country,
			status,
			transaction_type,
			amount,
			transaction_dt::date,
		   ROW_NUMBER() OVER (PARTITION BY operation_id ORDER BY transaction_dt DESC) as rn
		FROM STV202504297__STAGING.transactions
		WHERE account_number_to >= 0 AND account_number_from >= 0
		  	  AND transaction_dt::date = '{{ ds }}'
	), currencies AS (	  
		SELECT 
			date_update::date,
			currency_code,
			currency_code_with,
			currency_with_div,
		   ROW_NUMBER() OVER (PARTITION BY currency_code, currency_code_with ORDER BY date_update DESC) as rn
		FROM STV202504297__STAGING.currencies
		WHERE date_update::date = '{{ ds }}'
	)
	SELECT tr.transaction_dt AS date_update,
		   tr.currency_code AS currency_from,
		   ROUND(SUM(tr.amount * cr.currency_with_div), 3) AS amount_total,
		   COUNT(DISTINCT tr.operation_id) AS cnt_transactions,
		   ROUND(COUNT(DISTINCT tr.operation_id)/COUNT(DISTINCT tr.account_number_from), 3) AS avg_transactions_per_account,
		   ROUND(COUNT(DISTINCT tr.account_number_from), 3) AS cnt_accounts_make_transactions
		FROM transactions tr
        LEFT JOIN currencies cr ON 
        tr.currency_code = cr.currency_code 
        AND tr.transaction_dt = cr.date_update
		WHERE tr.rn = 1 
		GROUP BY  1, 2
		ORDER BY 1) cte
ON gm.date_update = cte.date_update 
AND gm.currency_from = cte.currency_from
WHEN MATCHED THEN UPDATE
SET amount_total = cte.amount_total,
	cnt_transactions = cte.cnt_transactions,
	avg_transactions_per_account = cte.avg_transactions_per_account,
	cnt_accounts_make_transactions = cte.cnt_accounts_make_transactions
WHEN NOT MATCHED THEN
INSERT 
	(date_update, currency_from, amount_total, cnt_transactions, avg_transactions_per_account, cnt_accounts_make_transactions)
VALUES 
	 cte.date_update, cte.currency_from, cte.amount_total, cte.cnt_transactions, cte.avg_transactions_per_account, cte.cnt_accounts_make_transactions);