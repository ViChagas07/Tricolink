"""Row Level Security for links and refresh_tokens.

Revision ID: 0002_row_level_security
Revises: 0001_initial_schema
Create Date: 2026-10-21
"""

from __future__ import annotations

from alembic import op

revision = "0002_row_level_security"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE links ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE links FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY links_select_owner ON links
        FOR SELECT USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY links_select_public ON links
        FOR SELECT USING (
            code = NULLIF(current_setting('app.current_link_code', true), '')
        )
        """
    )
    op.execute(
        """
        CREATE POLICY links_select_flusher ON links
        FOR SELECT USING (
            current_setting('app.click_flusher', true) = '1'
        )
        """
    )
    op.execute(
        """
        CREATE POLICY links_insert_owner_or_anonymous ON links
        FOR INSERT WITH CHECK (
            user_id IS NULL
            OR user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY links_update_owner ON links
        FOR UPDATE
        USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        WITH CHECK (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY links_update_flusher ON links
        FOR UPDATE
        USING (current_setting('app.click_flusher', true) = '1')
        WITH CHECK (current_setting('app.click_flusher', true) = '1')
        """
    )
    op.execute(
        """
        CREATE POLICY links_delete_owner ON links
        FOR DELETE USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )

    op.execute("ALTER TABLE refresh_tokens ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE refresh_tokens FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY refresh_tokens_select_owner ON refresh_tokens
        FOR SELECT USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_tokens_select_hash ON refresh_tokens
        FOR SELECT USING (
            token_hash = NULLIF(current_setting('app.refresh_token_hash', true), '')
        )
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_tokens_insert_owner ON refresh_tokens
        FOR INSERT WITH CHECK (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_tokens_update_owner ON refresh_tokens
        FOR UPDATE
        USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        WITH CHECK (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_tokens_update_family ON refresh_tokens
        FOR UPDATE
        USING (
            family_id = NULLIF(current_setting('app.refresh_family_id', true), '')::uuid
        )
        WITH CHECK (
            family_id = NULLIF(current_setting('app.refresh_family_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_tokens_update_hash ON refresh_tokens
        FOR UPDATE
        USING (
            token_hash = NULLIF(current_setting('app.refresh_token_hash', true), '')
        )
        WITH CHECK (
            token_hash = NULLIF(current_setting('app.refresh_token_hash', true), '')
        )
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_tokens_delete_owner ON refresh_tokens
        FOR DELETE USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY refresh_tokens_delete_family ON refresh_tokens
        FOR DELETE USING (
            family_id = NULLIF(current_setting('app.refresh_family_id', true), '')::uuid
        )
        """
    )


def downgrade() -> None:
    for policy in (
        "refresh_tokens_delete_family",
        "refresh_tokens_delete_owner",
        "refresh_tokens_update_hash",
        "refresh_tokens_update_family",
        "refresh_tokens_update_owner",
        "refresh_tokens_insert_owner",
        "refresh_tokens_select_hash",
        "refresh_tokens_select_owner",
    ):
        op.execute(f"DROP POLICY {policy} ON refresh_tokens")
    op.execute("ALTER TABLE refresh_tokens NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE refresh_tokens DISABLE ROW LEVEL SECURITY")

    for policy in (
        "links_delete_owner",
        "links_update_flusher",
        "links_update_owner",
        "links_insert_owner_or_anonymous",
        "links_select_flusher",
        "links_select_public",
        "links_select_owner",
    ):
        op.execute(f"DROP POLICY {policy} ON links")
    op.execute("ALTER TABLE links NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE links DISABLE ROW LEVEL SECURITY")
