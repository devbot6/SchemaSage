DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS organizations;

CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    industry TEXT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    organization_id UUID,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE projects (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id UUID,
    organization_id UUID,
    status TEXT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    organization_id UUID,
    plan_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL
);

CREATE TABLE invoices (
    id UUID PRIMARY KEY,
    org_id UUID,
    amount_cents INT NOT NULL,
    issued_at TIMESTAMP NOT NULL,
    paid_at TIMESTAMP
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    actor_user_id UUID,
    action TEXT NOT NULL,
    target_type TEXT,
    target_id UUID,
    created_at TIMESTAMP NOT NULL
);