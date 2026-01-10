"""add role type to Enum

Revision ID: af2e81a7550f
Revises: eeae1ace2a08
Create Date: 2026-01-10 07:26:47.674166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'af2e81a7550f'
down_revision: Union[str, Sequence[str], None] = 'eeae1ace2a08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_roles_enum = postgresql.ENUM(
    "user",
    "admin",
    name="user_roles"
)

def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ Create enum type
    user_roles_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ DROP default BEFORE type change (CRITICAL)
    op.execute(
        "ALTER TABLE user_table ALTER COLUMN role DROP DEFAULT"
    )

    # 3️⃣ Convert column using explicit cast
    op.execute(
        """
        ALTER TABLE user_table
        ALTER COLUMN role
        TYPE user_roles
        USING role::user_roles
        """
    )

    # 4️⃣ Re-add default + NOT NULL
    op.alter_column(
        "user_table",
        "role",
        nullable=False,
        server_default="user"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop default first
    op.execute(
        "ALTER TABLE user_table ALTER COLUMN role DROP DEFAULT"
    )

    # Convert enum back to string
    op.alter_column(
        "user_table",
        "role",
        type_=sa.String(),
        nullable=True
    )

    # Drop enum type
    user_roles_enum.drop(op.get_bind(), checkfirst=True)
