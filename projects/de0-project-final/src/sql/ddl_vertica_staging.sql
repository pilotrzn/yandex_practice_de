CREATE TABLE IF NOT EXISTS STV202504297__STAGING.currencies (
	date_update timestamp, 
    currency_code int,
    currency_code_with int,
    currency_with_div numeric(5,3)
)
ORDER BY date_update
SEGMENTED BY hash(currency_code,date_update) ALL NODES
PARTITION BY date_update::date
GROUP BY calendar_hierarchy_day(date_update::date, 3, 2);

CREATE TABLE IF NOT EXISTS STV202504297__STAGING.transactions (
	operation_id varchar(60),
	account_number_from int,
	account_number_to int,
	currency_code int,
	country varchar(30),
	status varchar(30),
	transaction_type varchar(30),
	amount int,
	transaction_dt timestamp
)
ORDER BY transaction_dt
SEGMENTED BY hash(operation_id, transaction_dt) ALL NODES
PARTITION BY transaction_dt::date
GROUP BY calendar_hierarchy_day(transaction_dt::date, 3, 2);


CREATE PROJECTION STV202504297__STAGING.currencies
(
 date_update,
 currency_code,
 currency_code_with,
 currency_with_div
)
AS
 SELECT currencies.date_update,
        currencies.currency_code,
        currencies.currency_code_with,
        currencies.currency_with_div
 FROM STV202504297__STAGING.currencies
 ORDER BY currencies.date_update
 SEGMENTED BY hash(currency_code,date_update) ALL NODES KSAFE 1;

CREATE PROJECTION STV202504297__STAGING.transactions 
(
operation_id,
account_number_from,
account_number_to,
currency_code,
country,
status,
transaction_type,
amount,
transaction_dt
)
AS
SELECT transactions.operation_id,
        transactions.account_number_from,
        transactions.account_number_to,
        transactions.currency_code,
        transactions.country,
        transactions.status,
        transactions.transaction_type,
        transactions.amount,
        transactions.transaction_dt
FROM STV202504297__STAGING.transactions
ORDER BY transactions.operation_id
SEGMENTED BY hash(transactions.operation_id) ALL NODES KSAFE 1;
