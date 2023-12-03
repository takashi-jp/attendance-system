import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app import db
from app.models import Employee

@click.command('create-user')
@click.argument('name')
@click.argument('email')
@click.argument('password')
@click.option('--admin', is_flag=True, help='Create an admin user.')
@with_appcontext
def create_user(name, email, password, admin):
    hashed_password = generate_password_hash(password)
    user = Employee(name=name, email=email, password_hash=hashed_password, is_admin=admin)
    db.session.add(user)
    db.session.commit()
    user_type = 'admin' if admin else 'employee'
    click.echo(f'Type:{user_type} Name:{name} created successfully!')