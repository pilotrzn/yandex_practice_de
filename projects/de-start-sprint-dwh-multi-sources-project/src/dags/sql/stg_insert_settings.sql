INSERT INTO stg.srv_wf_settings(workflow_key, workflow_settings)
VALUES (%(etl_key)s, %(etl_setting)s)
ON CONFLICT (workflow_key) DO UPDATE
SET workflow_settings = EXCLUDED.workflow_settings;