from flask import Flask
from flask_login import LoginManager, current_user
from flask.views import MethodView
from flask import request, render_template, redirect, flash
from src.db import mysql
from hashlib import sha256
from src.methods.loginManager.manager import *
from datetime import timedelta
import json

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY="development"  #serve pras msg
)

app.secret_key = 'asijaiosjaoijs0o9ajd9821u3109380912830!!!!!asdsa!!sad' #serve pro flask login
app.permanent_session_lifetime = timedelta(minutes=30) #expirando a secao

login_manager = LoginManager(app)

#controller

def renovar_sessao():
    app.permanent_session_lifetime = timedelta(minutes=30)

class login_controller(MethodView):
    def get(self):
        if(current_user.is_authenticated == False):
            return render_template("login.html")
        else:
            renovar_sessao()
            return render_template("public/home.html")

    def post(self):
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        with mysql.cursor() as cur:
            cur.execute("SELECT * from usuario")
            pessoas = cur.fetchall()
            achou = 0

            for pessoa in pessoas:
                if pessoa[1] == usuario:
                    achou = 1
                    with mysql.cursor() as cur2:
                        try:
                            cur2.execute("select * from usuario where usrnome = %s", (usuario))
                            user = cur2.fetchone()
                            senha_bd = user[2]
                            senha_hash = sha256(senha.encode())
                            senha_cript = senha_hash.hexdigest()
                            

                            if(senha_cript == senha_bd):
                                user_obj = User(user[0], user[1], user[2])
                                login_user(user_obj)
                                return redirect("/")
                            else:
                                flash('Senha inválida', 'error')
                                
                        except:
                            flash('Erro na consulta', 'error')
    
            if(achou == 0):
                flash('Usuário não cadastrado', 'error')    
            return redirect("/")
    
class cadastro_produto_controller(MethodView):
    @login_required
    def get(self):
        renovar_sessao()
        with mysql.cursor() as cur:
            cur.execute("select * from produto")
            produtos = cur.fetchall()
            cur.execute("select * from secao")
            secoes = cur.fetchall()
            cur.execute("select * from tributacao")
            tributacoes = cur.fetchall()
            cur.execute("select * from ncm")
            ncms = cur.fetchall()
        return render_template("public/cadastro_produto.html", produtos=produtos, secoes=secoes, tributacoes=tributacoes, ncms=ncms)
    
    def post(self):
        prodes = request.form["prodes"]
        prosec = request.form["prosec"]
        proprc = request.form["proprc"]
        protrib = request.form["protrib"]
        proncm = request.form["proncm"]

        with mysql.cursor() as cur:
            cur.execute("INSERT INTO produto(procod, prodes, prosec, proprc, protrib, proncm) VALUES(null, %s, %s, %s, %s, %s)", (prodes, prosec, proprc, protrib, proncm))
            cur.connection.commit()
        return redirect("/cadastro/produto")
    
class cadastro_secao_controller(MethodView):
    def get(self):
        return render_template("public/cadastro_secao.html")
    def post(self):
        secdes = request.form["secdes"]

        with mysql.cursor() as cur:
            cur.execute("INSERT INTO secao VALUES(null, %s)", (secdes))
            cur.connection.commit()
        return redirect("/")

class get_secao_controller(MethodView):
    def get(self):
        with mysql.cursor() as cur:
            cur.execute("select * from secao")
            secoes = cur.fetchall()

            out_file = open("src/templates/json/secoes.json", "w")
            lista = []

            for secao in secoes:
                lista.append({
                    "seccod" : secao[0],
                    "secdes" : secao[1]
                })
                
            json.dump(lista, out_file, separators=(",", ": "), indent=2, sort_keys=True)
            out_file.close()

        return render_template("json/secoes.json")
    
class cadastro_usuario_controller(MethodView):
    @login_required
    def get(self):
        renovar_sessao()
        return render_template("public/cadastro_usuario.html")
    @login_required
    def post(self):
        usuario = request.form['usuario']
        senha = request.form['senha']

        senha_hash = sha256(senha.encode())
        senha_cript = senha_hash.hexdigest()

        try:
            with mysql.cursor() as cur:
                cur.execute("INSERT INTO usuario VALUES(null, %s, %s)", (usuario, senha_cript))
                cur.connection.commit()
                flash('Usuario cadastrado com sucesso!', 'success') 
        except:
            flash('Erro ao cadastrar usuário! Verifique se já existe um usuário com este nome', 'error')
        
        return redirect("/cadastro/usuario")
    
@login_manager.user_loader
def get_user(user_id):
    with mysql.cursor() as cur:
        cur.execute("select * from usuario where usrcod = %s", (user_id))
        usuario_slct = cur.fetchone()
        user_obj = User(usuario_slct[0], usuario_slct[1], usuario_slct[2])
    return user_obj

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect("/")

class logout(MethodView):
    @login_required
    def get(self):
        logout_user()
        return redirect("/")
    
'''@app.errorhandler(404)
def nao_encontrado(e):
    # Renderiza um template HTML customizado para a página não encontrada
    return render_template('nao_encontrado.html'), 404 '''

#fim do controller

#routes

routes = {
    "login": "/", "login_controller":login_controller.as_view("login"),
    "cadastro_produto":"/cadastro/produto", "cadastro_produto_controller":cadastro_produto_controller.as_view("cadastro_produto"),
    "get_secao":"/get/secao", "get_secao_controller":get_secao_controller.as_view("get_secao"),
    "cadastro_secao":"/cadastro/secao", "cadastro_secao_controller":cadastro_secao_controller.as_view("cadastro_secao"),
    "cadastro_usuario":"/cadastro/usuario", "cadastro_usuario_controller":cadastro_usuario_controller.as_view("cadastro_usuario"),
    "logout":"/logout","logout_controller":logout.as_view("logout")
    #"deletar_pessoa":"/delete/pessoa/<int:id>", "del_pessoa_controller":del_pessoa_controller.as_view("delete_pessoa"),
}

#fim do routes

app.add_url_rule(routes["login"], view_func=routes["login_controller"])
app.add_url_rule(routes["cadastro_produto"], view_func=routes["cadastro_produto_controller"])
app.add_url_rule(routes["get_secao"], view_func=routes["get_secao_controller"])
app.add_url_rule(routes["cadastro_secao"], view_func=routes["cadastro_secao_controller"])
app.add_url_rule(routes["cadastro_usuario"], view_func=routes["cadastro_usuario_controller"])
app.add_url_rule(routes["logout"], view_func=routes["logout_controller"])