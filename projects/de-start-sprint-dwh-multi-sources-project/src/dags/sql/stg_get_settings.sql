SELECT id, workflow_key, workflow_settings
FROM   stg.srv_wf_settings
WHERE  workflow_key = %(etl_key)s;