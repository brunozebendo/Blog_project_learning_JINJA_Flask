"""O objetivo do código é criar um site que guarde as informações digitadas no formulário de um BLOG.
Primeiro, a sintaxe básica de importação e inicilização do flask e render_template para lidar com o html
Aula 60, segunda parte:
A ideia é aprimorar o código do blog para que passe e-mails para o dono do blog quando um usuário está tentando
entrar em contato, ou seja, quando ele preencha os dados e clique no botão
Primeiro, importa-se as bibliotecas necessárias, flask para trabalhar com web, render template
 para trabalhar com html, request para trabalhar com as requisições do site, smtplib para trabalhar
 com e-mails e requests para trabalhar com requisições de API
"""
"""no curso, o index é criado na mesma pasta do main, mas aqui só funcionou quando criei a pasta templates"""
from flask import Flask, render_template, request
import smtplib
import requests
"""aqui a sintaxe básica para pegar informações no site que cria posts automáticos e já trazê-los
no formato .json()"""
posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()
OWN_EMAIL = YOUR OWN EMAIL ADDRESS
OWN_PASSWORD = YOUR OWN EMAIL PASSWORD

app = Flask(__name__)
"""abaixo a sintaxe básica para acessar o html e usar os posts. """
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)

"""aqui o código para gerar um novo post a cada novo post trazido do json."""
@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

"""aqui é a rota para a página about, com o html equivalente"""
@app.route("/about")
def about():
    return render_template("about.html")

"""aqui a rota contact, com os métodos equivalentes para que a informação postada seja guardada.
Aqui é usado um método do FLASK explicado na documentação na parte de The Request Object, primeiro,
tem que importar o método  request, então é passada a função abaixo que usa o request.form 
(que é o nome da tag para formulários passados  no html, e o ["name"] e ["email"]....que são o nomes dos inputs
 estabelecidos no html, então o return volta uma string que será exibida quando o usuário preencher o formulário
  e for redirecionado  para o route. Acho que o msg_sent é o método que vai determinar se o e-mail é passado ou não,
   tendo como critério o preenchimento do formulário"""
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


"""aqui a sintaxe básica para criar a mensagem e passar o e-mail"""
def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == "__main__":
    #if you want your web server to run in repl.it, use the next line:
    app.run(host='0.0.0.0', port=8080)

    #If you want your web server to run locally on your computer, use this:
    # app.run(debug=True)
