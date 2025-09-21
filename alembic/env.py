from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from app.models import Base  # 导入你的模型 Base
import os
from dotenv import load_dotenv

# Alembic 配置对象
config = context.config

load_dotenv()

# 从环境变量获取数据库信息
DB_USER = os.getenv("SQL_USER")
DB_PASS = os.getenv("SQL_PASSWORD")
DB_HOST = os.getenv("SQL_HOST")
DB_PORT = os.getenv("SQL_PORT")
DB_NAME = os.getenv("SQL_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# 设置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 指向 ORM 模型元数据
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """离线迁移（不连接数据库）"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """在线迁移（同步 engine）"""
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# 根据模式选择
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
