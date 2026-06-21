import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.runtime.migration')

# Pega os metadados das tabelas direto do app do flask
target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    # Roda as migracoes de modo offline
    url = current_app.config.get("SQLALCHEMY_DATABASE_URI")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Roda as migracoes online usando a conexao ativa do flask
    connectable = current_app.extensions['migrate'].db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()

def process_revision_directives(context, revision, directives):
    # Cancela a migracao se nao houver mudancas nos modelos
    if current_app.config.get('MIGRATE_AUTOGENERATE', True):
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            logger.info('Nenhuma alteração detectada nos modelos.')

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()