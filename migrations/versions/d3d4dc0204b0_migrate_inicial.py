"""migrate inicial

Revision ID: d3d4dc0204b0
Revises: 
Create Date: 2024-11-12 09:58:43.658390

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd3d4dc0204b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rastreio_de_patrimonios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('patrimonio_id', sa.Integer(), nullable=True),
    sa.Column('local_antigo', sa.String(length=100), nullable=True),
    sa.Column('local_novo', sa.String(length=100), nullable=True),
    sa.Column('data_mudanca', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['patrimonio_id'], ['patrimonios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=100), nullable=True))
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=100),
               nullable=True)
        batch_op.alter_column('cpf',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=11),
               nullable=True)
        batch_op.drop_index('cpf_UNIQUE')
        batch_op.drop_index('email_UNIQUE')
        batch_op.drop_index('id_UNIQUE')

    with op.batch_alter_table('cadastro_usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=100), nullable=True))
        batch_op.alter_column('nome',
               existing_type=mysql.VARCHAR(length=45),
               nullable=True)
        batch_op.alter_column('cpf',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=11),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=45),
               nullable=True)
        batch_op.alter_column('telefone',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=15),
               nullable=True)
        batch_op.drop_index('cpf_UNIQUE')
        batch_op.drop_index('email_UNIQUE')
        batch_op.drop_index('id_UNIQUE')
        batch_op.drop_index('telefone_UNIQUE')
        batch_op.drop_column('mensagem')

    with op.batch_alter_table('patrimonios', schema=None) as batch_op:
        batch_op.alter_column('numero_de_etiqueta',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('denominacao_de_imobiliario',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('data_de_chegada',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('local',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=100),
               nullable=False)

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=128), nullable=False))
        batch_op.alter_column('nome',
               existing_type=mysql.VARCHAR(length=45),
               nullable=True)
        batch_op.alter_column('cpf',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=11),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=45),
               nullable=True)
        batch_op.alter_column('telefone',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=15),
               nullable=True)
        batch_op.drop_index('cpf_UNIQUE')
        batch_op.drop_index('email_UNIQUE')
        batch_op.drop_index('telefone_UNIQUE')
        batch_op.drop_column('mensagem')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mensagem', mysql.VARCHAR(length=45), nullable=False))
        batch_op.create_index('telefone_UNIQUE', ['telefone'], unique=True)
        batch_op.create_index('email_UNIQUE', ['email'], unique=True)
        batch_op.create_index('cpf_UNIQUE', ['cpf'], unique=True)
        batch_op.alter_column('telefone',
               existing_type=sa.String(length=15),
               type_=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.alter_column('cpf',
               existing_type=sa.String(length=11),
               type_=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.alter_column('nome',
               existing_type=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.drop_column('password')

    with op.batch_alter_table('patrimonios', schema=None) as batch_op:
        batch_op.alter_column('local',
               existing_type=sa.String(length=100),
               type_=mysql.TEXT(),
               nullable=True)
        batch_op.alter_column('data_de_chegada',
               existing_type=sa.String(length=100),
               type_=mysql.TEXT(),
               nullable=True)
        batch_op.alter_column('denominacao_de_imobiliario',
               existing_type=sa.String(length=100),
               type_=mysql.TEXT(),
               nullable=True)
        batch_op.alter_column('numero_de_etiqueta',
               existing_type=sa.String(length=100),
               type_=mysql.TEXT(),
               nullable=True)

    with op.batch_alter_table('cadastro_usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mensagem', mysql.TEXT(), nullable=False))
        batch_op.create_index('telefone_UNIQUE', ['telefone'], unique=True)
        batch_op.create_index('id_UNIQUE', ['id'], unique=True)
        batch_op.create_index('email_UNIQUE', ['email'], unique=True)
        batch_op.create_index('cpf_UNIQUE', ['cpf'], unique=True)
        batch_op.alter_column('telefone',
               existing_type=sa.String(length=15),
               type_=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.alter_column('cpf',
               existing_type=sa.String(length=11),
               type_=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.alter_column('nome',
               existing_type=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.drop_column('password')

    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index('id_UNIQUE', ['id'], unique=True)
        batch_op.create_index('email_UNIQUE', ['email'], unique=True)
        batch_op.create_index('cpf_UNIQUE', ['cpf'], unique=True)
        batch_op.alter_column('cpf',
               existing_type=sa.String(length=11),
               type_=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=45),
               nullable=False)
        batch_op.drop_column('password')

    op.drop_table('rastreio_de_patrimonios')
    # ### end Alembic commands ###