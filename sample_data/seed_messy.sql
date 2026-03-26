DELETE FROM audit_logs;
DELETE FROM invoices;
DELETE FROM subscriptions;
DELETE FROM projects;
DELETE FROM users;
DELETE FROM organizations;

INSERT INTO organizations (id, name, industry, created_at) VALUES
('11111111-1111-1111-1111-111111111111', 'Acme AI', 'Software', NOW()),
('22222222-2222-2222-2222-222222222222', 'Blue Ocean Robotics', 'Robotics', NOW()),
('33333333-3333-3333-3333-333333333333', 'Northwind Health', 'Healthcare', NOW()),
('44444444-4444-4444-4444-444444444444', 'Delta Data', 'Software', NOW()),
('55555555-5555-5555-5555-555555555555', 'Skyline Bio', 'Healthcare', NOW());

INSERT INTO users (id, email, full_name, organization_id, created_at) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'alice@acme.ai', 'Alice Carter', '11111111-1111-1111-1111-111111111111', NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'bob@acme.ai', 'Bob Smith', '11111111-1111-1111-1111-111111111111', NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3', 'cathy@blueocean.com', 'Cathy Lane', '22222222-2222-2222-2222-222222222222', NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa4', 'david@northwind.com', 'David Cole', '33333333-3333-3333-3333-333333333333', NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa5', 'erin@delta.com', 'Erin Hall', '44444444-4444-4444-4444-444444444444', NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa6', 'frank@delta.com', 'Frank Moore', '44444444-4444-4444-4444-444444444444', NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa7', 'gina@skyline.com', 'Gina West', '55555555-5555-5555-5555-555555555555', NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa8', 'harry@unknown.com', 'Harry Stone', NULL, NOW());

INSERT INTO projects (id, name, owner_id, organization_id, status, created_at) VALUES
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'Schema Mapper', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1', '11111111-1111-1111-1111-111111111111', 'active', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'VisionPilot', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3', '22222222-2222-2222-2222-222222222222', 'active', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb3', 'MedGraph', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa4', '33333333-3333-3333-3333-333333333333', 'paused', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb4', 'DeltaFlow', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa5', '44444444-4444-4444-4444-444444444444', 'active', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb5', 'SkyML', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa7', '55555555-5555-5555-5555-555555555555', 'planning', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb6', 'GhostProject', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa8', NULL, 'draft', NOW());

INSERT INTO subscriptions (id, organization_id, plan_name, status, started_at) VALUES
('cccccccc-cccc-cccc-cccc-ccccccccccc1', '11111111-1111-1111-1111-111111111111', 'pro', 'active', NOW()),
('cccccccc-cccc-cccc-cccc-ccccccccccc2', '22222222-2222-2222-2222-222222222222', 'enterprise', 'active', NOW()),
('cccccccc-cccc-cccc-cccc-ccccccccccc3', '33333333-3333-3333-3333-333333333333', 'starter', 'trialing', NOW()),
('cccccccc-cccc-cccc-cccc-ccccccccccc4', '44444444-4444-4444-4444-444444444444', 'pro', 'active', NOW()),
('cccccccc-cccc-cccc-cccc-ccccccccccc5', '55555555-5555-5555-5555-555555555555', 'starter', 'canceled', NOW());

INSERT INTO invoices (id, org_id, amount_cents, issued_at, paid_at) VALUES
('dddddddd-dddd-dddd-dddd-ddddddddddd1', '11111111-1111-1111-1111-111111111111', 5000, NOW(), NOW()),
('dddddddd-dddd-dddd-dddd-ddddddddddd2', '22222222-2222-2222-2222-222222222222', 12000, NOW(), NULL),
('dddddddd-dddd-dddd-dddd-ddddddddddd3', '33333333-3333-3333-3333-333333333333', 2500, NOW(), NOW()),
('dddddddd-dddd-dddd-dddd-ddddddddddd4', '44444444-4444-4444-4444-444444444444', 5000, NOW(), NULL),
('dddddddd-dddd-dddd-dddd-ddddddddddd5', '99999999-9999-9999-9999-999999999999', 5000, NOW(), NULL);

INSERT INTO audit_logs (id, actor_user_id, action, target_type, target_id, created_at) VALUES
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee1', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'created_project', 'project', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb1', NOW()),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee2', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3', 'updated_project', 'project', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb2', NOW()),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee3', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa4', 'paid_invoice', 'invoice', 'dddddddd-dddd-dddd-dddd-ddddddddddd3', NOW()),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee4', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa5', 'updated_project', 'project', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb4', NOW()),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeee5', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa8', 'viewed_dashboard', 'organization', '55555555-5555-5555-5555-555555555555', NOW());