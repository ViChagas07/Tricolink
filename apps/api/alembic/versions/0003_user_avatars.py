"""User avatars and Google profile picture.

Revision ID: 0003_user_avatars
Revises: 0002_row_level_security
Create Date: 2026-10-23
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0003_user_avatars"
down_revision = "0002_row_level_security"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("google_avatar_url", sa.Text(), nullable=True))
    op.add_column(
        "users",
        sa.Column("avatar_updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_check_constraint(
        "google_avatar_url_length",
        "users",
        "google_avatar_url IS NULL OR char_length(google_avatar_url) <= 2048",
    )

    op.create_table(
        "user_avatars",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("content_type", sa.String(length=16), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "content_type IN ('image/jpeg', 'image/png', 'image/webp')",
            name="avatar_content_type",
        ),
        sa.CheckConstraint(
            "octet_length(content) BETWEEN 1 AND 8192",
            name="avatar_content_size",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_user_avatars_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", name="pk_user_avatars"),
    )

    op.execute("ALTER TABLE user_avatars ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE user_avatars FORCE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE POLICY user_avatars_select_owner ON user_avatars
        FOR SELECT USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY user_avatars_insert_owner ON user_avatars
        FOR INSERT WITH CHECK (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )
    op.execute(
        """
        CREATE POLICY user_avatars_update_owner ON user_avatars
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
        CREATE POLICY user_avatars_delete_owner ON user_avatars
        FOR DELETE USING (
            user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
        )
        """
    )


def downgrade() -> None:
    op.drop_table("user_avatars")
    op.drop_constraint("google_avatar_url_length", "users", type_="check")
    op.drop_column("users", "avatar_updated_at")
    op.drop_column("users", "google_avatar_url")
