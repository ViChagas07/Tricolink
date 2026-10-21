from tricolink.infra.db.models import Base, ClickEvent, Link, RefreshToken, User


def test_all_context_tables_are_declared() -> None:
    assert set(Base.metadata.tables) == {
        "users",
        "refresh_tokens",
        "links",
        "click_events",
    }


def test_links_have_required_constraints_and_indexes() -> None:
    table = Link.__table__
    checks = {constraint.name for constraint in table.constraints if constraint.name}

    assert "ck_links_code_format" in checks
    assert "ck_links_original_url_length" in checks
    assert "uq_links_code" in checks
    assert "ix_links_user_id_created_at" in {index.name for index in table.indexes}
    assert "ix_links_expires_at" in {index.name for index in table.indexes}


def test_click_events_have_device_check_and_index() -> None:
    table = ClickEvent.__table__
    checks = {constraint.name for constraint in table.constraints if constraint.name}

    assert "ck_click_events_device_allowed" in checks
    assert "ix_click_events_link_id_clicked_at" in {index.name for index in table.indexes}


def test_users_and_refresh_tokens_have_required_uniques() -> None:
    user_uniques = {
        constraint.name
        for constraint in User.__table__.constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    }
    token_uniques = {
        constraint.name
        for constraint in RefreshToken.__table__.constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    }

    assert "uq_users_email" in user_uniques
    assert "uq_users_google_sub" in user_uniques
    assert "uq_refresh_tokens_token_hash" in token_uniques
