from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


class SystemClock:
    def now(self) -> datetime:
        return utc_now()
