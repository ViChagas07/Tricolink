"""Initial schema: users, refresh_tokens, links and click_events.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-10-21
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", postgresql.CITEXT(), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=True),
        sa.Column("google_sub", sa.Text(), nullable=True),
        sa.Column("display_name", sa.String(length=80), nullable=True),
        sa.Column("locale", sa.String(length=8), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("char_length(email) <= 254", name="email_length"),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("google_sub", name="uq_users_google_sub"),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("family_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.Text(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_refresh_tokens_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_refresh_tokens"),
        sa.UniqueConstraint("token_hash", name="uq_refresh_tokens_token_hash"),
    )
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"])
    op.create_index("ix_refresh_tokens_family_id", "refresh_tokens", ["family_id"])
    op.create_index("ix_refresh_tokens_expires_at", "refresh_tokens", ["expires_at"])

    op.create_table(
        "links",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("original_url", sa.Text(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_custom_alias", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("click_count", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "char_length(original_url) <= 2048",
            name="original_url_length",
        ),
        sa.CheckConstraint(
            "char_length(original_url) > 0",
            name="original_url_not_empty",
        ),
        sa.CheckConstraint("code ~ '^[A-Za-z0-9_-]{3,32}$'", name="code_format"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_links_user_id_users",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_links"),
        sa.UniqueConstraint("code", name="uq_links_code"),
    )
    op.create_index(
        "ix_links_user_id_created_at",
        "links",
        ["user_id", sa.text("created_at DESC")],
    )
    op.create_index(
        "ix_links_expires_at",
        "links",
        ["expires_at"],
        postgresql_where=sa.text("expires_at IS NOT NULL"),
    )

    op.create_table(
        "click_events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("link_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "clicked_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("country", sa.CHAR(length=2), nullable=True),
        sa.Column(
            "device",
            sa.String(length=10),
            server_default=sa.text("'unknown'"),
            nullable=False,
        ),
        sa.Column("browser", sa.String(length=30), nullable=True),
        sa.Column("referrer_host", sa.String(length=255), nullable=True),
        sa.CheckConstraint(
            "device IN ('desktop', 'mobile', 'tablet', 'bot', 'unknown')",
            name="device_allowed",
        ),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["links.id"],
            name="fk_click_events_link_id_links",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_click_events"),
    )
    op.create_index(
        "ix_click_events_link_id_clicked_at",
        "click_events",
        ["link_id", "clicked_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_click_events_link_id_clicked_at", table_name="click_events")
    op.drop_table("click_events")
    op.drop_index("ix_links_expires_at", table_name="links")
    op.drop_index("ix_links_user_id_created_at", table_name="links")
    op.drop_table("links")
    op.drop_index("ix_refresh_tokens_expires_at", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_family_id", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
