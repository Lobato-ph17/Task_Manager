from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Caminho do banco de dados
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, '..', 'instance', 'tarefas.db')

    # Configuração do banco
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Modelo importado depois da inicialização
    from .models import Tarefa

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            titulo = request.form['titulo']
            nova_tarefa = Tarefa(titulo=titulo)
            db.session.add(nova_tarefa)
            db.session.commit()

        tarefas = Tarefa.query.all()
        return render_template('home.html', tarefas=tarefas)
    
    @app.route('/delete/<int:id>', methods=['POST'])
    def excluir_tarefa(id): 

        tarefa = Tarefa.query.get_or_404(id)
        db.session.delete(tarefa)
        db.session.commit()
        return redirect('/')



    return app
