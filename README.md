![SchemaSage Logo](assets/schemasage-logo.png)

SchemaSage is a Python-based schema inference engine for undocumented PostgreSQL databases. It connects to a database, extracts structural metadata, profiles columns statistically, ranks likely primary keys, infers foreign-key relationships, and flags suspicious or polymorphic references.

The goal of the project is to reduce the manual reverse-engineering work engineers face when inheriting messy or poorly documented databases.

---

## Why this project exists

Undocumented databases create real engineering problems:

- developers waste time figuring out what tables and columns mean
- migrations become risky because relationships are unclear
- reporting and analytics are harder when keys are not documented
- data quality issues like orphan references often go unnoticed
- application-level patterns like polymorphic references are hard to spot quickly

SchemaSage is designed to surface those patterns automatically using a combination of metadata inspection, profiling, and heuristic scoring.

---

## What SchemaSage does

SchemaSage currently supports the following features for PostgreSQL databases:

- extracts table and column metadata from the `public` schema
- profiles each column using row count, null ratio, distinct ratio, and sample values
- ranks likely primary-key candidates for each table
- infers likely foreign-key relationships using:
  - type compatibility
  - subset coverage
  - semantic name matching
  - target PK confidence
- identifies suspicious or orphan references where a column appears to be an FK but contains unmatched values
- detects likely polymorphic reference patterns such as `target_type + target_id`
- generates both:
  - a machine-readable JSON report
  - a human-readable Markdown report

---

## Current capabilities

Using the included messy sample dataset, SchemaSage is able to recover:

- clean relationships such as:
  - `projects.owner_id -> users.id`
  - `projects.organization_id -> organizations.id`
  - `subscriptions.organization_id -> organizations.id`
  - `users.organization_id -> organizations.id`
- suspicious / orphan references such as:
  - `invoices.org_id -> organizations.id` with incomplete coverage
- ambiguous polymorphic references such as:
  - `audit_logs.target_id`, which depends on `audit_logs.target_type`
- polymorphic reference patterns such as:
  - `audit_logs.target_type + audit_logs.target_id`

---

## Project structure

```text
schemasage/
├── .env
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── db_connect.py
│   ├── metadata.py
│   ├── profiler.py
│   ├── pk_detector.py
│   ├── fk_detector.py
│   └── reporting/
│       ├── __init__.py
│       ├── json_export.py
│       └── markdown_report.py
├── outputs/
│   ├── report.json
│   └── report.md
└── sample_data/
    ├── schema.sql
    └── seed_messy.sql
```

## Architecture Overview

SchemaSage follows a simple pipeline:

1. **Database connection**  
   The system reads database credentials from a `.env` file and connects to PostgreSQL using `psycopg`.

2. **Metadata extraction**  
   The engine queries PostgreSQL system metadata to collect:
   - table names
   - column names
   - data types
   - nullability

3. **Column profiling**  
   Each column is profiled using statistics such as:
   - total rows
   - null count / null ratio
   - distinct count / distinct ratio
   - sample non-null values

   These statistics are used later for inference.

4. **Primary key ranking**  
   SchemaSage scores columns as PK candidates using:
   - distinct ratio
   - non-null ratio
   - column naming patterns
   - data type patterns
   - penalties for descriptive fields
   - penalties for reference-style columns like `*_id`

5. **Foreign key inference**  
   The engine compares likely source columns against likely target keys using:
   - type matching
   - subset coverage
   - semantic name similarity
   - target PK confidence

6. **Reference categorization**  
   Detected relationships are grouped into:
   - Likely Foreign Keys
   - Suspicious / Orphan References
   - Ambiguous References
   - Polymorphic Reference Patterns

7. **Reporting**  
   The final analysis is exported as:
   - `outputs/report.json`
   - `outputs/report.md`

## Detection Categories

### Likely Foreign Keys

Relationships with strong semantic and structural evidence, typically with full or near-full coverage.

**Example:**

`projects.organization_id -> organizations.id`

### Suspicious / Orphan References

Columns that appear to be intended as foreign keys, but whose values do not fully match the target table.

**Example:**

`invoices.org_id -> organizations.id` with incomplete coverage

This can indicate:

- orphaned rows
- bad data
- soft-deleted records
- stale application references

### Ambiguous References

Columns that partially match a likely target but are not clean enough to treat as standard foreign keys.

**Example:**

`audit_logs.target_id -> projects.id`

### Polymorphic Reference Patterns

Application-level patterns where a pair such as `target_type + target_id` determines the referenced entity.

**Example:**

`audit_logs.target_type + audit_logs.target_id`

## Example output

A typical run produces console output like this:
```
SchemaSage analysis complete.
JSON report written to: outputs\report.json
Markdown report written to: outputs\report.md

Top likely foreign keys:
- audit_logs.actor_user_id -> users.id (score=1.0)
- projects.owner_id -> users.id (score=1.0)
- projects.organization_id -> organizations.id (score=1.0)
- subscriptions.organization_id -> organizations.id (score=1.0)
- users.organization_id -> organizations.id (score=1.0)

Suspicious / orphan references:
- invoices.org_id -> organizations.id (coverage=0.8, score=0.91)

Polymorphic patterns:
- audit_logs: target_type + target_id
```
The Markdown report summarizes:

- likely PKs
- likely FKs
- suspicious / orphan references
- ambiguous references
- polymorphic patterns

## Installation

1. **Clone the repository**


   ```bash
   git clone <https://github.com/devbot6/SchemaSage>
   cd schemasage
   ```

2. **Create and activate virtual environment**

   **Windows**
   ```bash
   python -m venv venv
    venv\Scripts\activate
    ```
    **macOS / Linux**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**
    ```bash
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=schemasage
    DB_USER=postgres
    DB_PASSWORD=your_password_here
    ```
## Running the project

Run the analysis with:

```bash
python main.py
```
Output files will be written to:

- `outputs/report.json`
- `outputs/report.md`


## Sample Database Setup

This project includes a messy sample dataset meant to simulate real undocumented schemas.

### Recommended Setup Flow

1. Create a PostgreSQL database named `schemasage`
2. Load the schema from `sample_data/schema.sql`
3. Load the data from `sample_data/seed_messy.sql`
4. Run `python main.py`

The included sample data is intentionally imperfect. It contains:

- repeated business values
- nullable relationships
- orphan references
- polymorphic reference patterns

That makes it useful for stress-testing the inference engine.

## Tech Stack

- Python
- PostgreSQL
- `psycopg`
- `python-dotenv`

## Design Choices

A few deliberate design choices shaped this project:

### Heuristics Before LLMs

SchemaSage currently relies on deterministic logic and heuristic scoring rather than LLM-generated guesses. That keeps the system explainable and grounded in measurable evidence.

### PostgreSQL-First Scope

The project currently targets PostgreSQL only. That keeps the implementation focused and makes debugging easier.

### Report-First Interface

Before adding a UI or API layer, SchemaSage focuses on producing high-quality structured outputs. This helps validate the core inference engine first.

## Limitations

Current limitations include:

- PostgreSQL only
- heuristic scoring can still be biased by small datasets
- natural unique fields like `email` or `name` may sometimes score as strong PK candidates
- semantic matching is rule-based and limited to known aliases
- polymorphic detection is pattern-based, not full semantic reasoning
- no web UI or API yet
- no multi-schema support yet beyond `public`

## Future Improvements

Planned or possible next steps:

- add CLI arguments for database name and output path
- add a FastAPI endpoint that returns the JSON report
- support additional databases such as MySQL or SQLite
- improve semantic normalization for more naming conventions
- detect junction tables and many-to-many patterns
- generate ER-style relationship graphs
- add optional LLM-assisted documentation summaries on top of the deterministic engine
- build a lightweight UI for browsing findings interactively


## Author

Built by Devon Hulse.
