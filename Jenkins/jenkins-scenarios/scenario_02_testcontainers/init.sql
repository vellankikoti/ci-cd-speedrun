-- TestContainers Integration Demo Database Initialization
-- This file is used by Docker Compose to initialize the PostgreSQL database

-- Create database if it doesn't exist (this is handled by POSTGRES_DB)
-- But we can add any additional setup here

-- Enable extensions that might be useful
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- The actual table creation and sample data will be handled by the application
-- This file is mainly for any database-level configurations

-- Log that initialization is complete
DO $$
BEGIN
    RAISE NOTICE 'TestContainers Integration Demo database initialized successfully';
END $$;
