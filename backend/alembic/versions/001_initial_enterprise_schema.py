"""Create the normalized attendance schema.

Revision ID: 001_initial_enterprise_schema
"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial_enterprise_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cost_centers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(50), nullable=False, unique=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("cost_center_id", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["cost_center_id"], ["cost_centers.id"], ondelete="SET NULL"),
    )
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("ip", sa.String(50), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False, server_default="4370"),
        sa.Column("interval_seconds", sa.Integer(), nullable=False, server_default="300"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_sync_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "user_devices",
        sa.Column("user_id", sa.Integer(), primary_key=True),
        sa.Column("device_id", sa.Integer(), primary_key=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
    )
    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("user_external_id", sa.String(50), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint(
            "device_id",
            "user_external_id",
            "timestamp",
            name="uq_attendance_device_external_timestamp",
        ),
    )
    op.create_table(
        "sync_jobs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("attempt", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("scheduled_at", sa.DateTime(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("error_code", sa.String(80), nullable=True),
        sa.Column("error_message", sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("sync_jobs")
    op.drop_table("attendance")
    op.drop_table("user_devices")
    op.drop_table("devices")
    op.drop_table("users")
    op.drop_table("cost_centers")
