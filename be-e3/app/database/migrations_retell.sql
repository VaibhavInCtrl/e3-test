ALTER TABLE agents ADD COLUMN retell_agent_id TEXT;
ALTER TABLE agents ADD COLUMN system_prompt TEXT;
ALTER TABLE agents ADD COLUMN scenario_description TEXT;

ALTER TABLE conversations ADD COLUMN retell_call_id TEXT UNIQUE;
ALTER TABLE conversations ADD COLUMN retell_access_token TEXT;
ALTER TABLE conversations ADD COLUMN call_type TEXT DEFAULT 'web_call';
ALTER TABLE conversations ADD COLUMN recording_url TEXT;
ALTER TABLE conversations ADD COLUMN transcript TEXT;
ALTER TABLE conversations ADD COLUMN duration_ms INTEGER;
ALTER TABLE conversations ADD COLUMN disconnection_reason TEXT;
ALTER TABLE conversations ADD COLUMN structured_data JSONB;
ALTER TABLE conversations ADD COLUMN call_analysis JSONB;

CREATE INDEX idx_conversations_retell_call_id ON conversations(retell_call_id);

