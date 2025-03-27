from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class EmailService:
    def __init__(self, database, stakeholders_list, metrics_service, llm_service):
        self.database = database
        self.stakeholders = stakeholders_list
        self.metrics_service = metrics_service
        self.llm_service = llm_service

    def generate_summary(self):
        requested_features = self.metrics_service.get_most_wanted_features()
        percentages = self.metrics_service.get_percentage_feedbacks()

        raw_data = f"top 10 requested_features: {requested_features}\npercentages: {percentages}"
        email_body = str(self.llm_service.generate_email(raw_data))

        for feature in requested_features:
            print(feature)
            email_body += f"- {feature[0]}: {feature[1]}\n"
        
        return email_body

    def send_report(self):
        email_body = self.generate_summary()

        sender_email = "andrewtxiz@gmail.com"
        subject = "Resumo dos Feedbacks da Semana - AluMind"

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login("andrewtxiz@gmail.com", "seegjwxnmbrnyxfn")

                for stakeholder in self.stakeholders:
                    message = MIMEMultipart()

                    message['From'] = sender_email

                    message['To'] = stakeholder

                    message['Subject'] = subject

                    message.attach(MIMEText(email_body, 'plain'))

                    server.sendmail(sender_email, stakeholder, message.as_string())

                print("E-mail enviado com sucesso para os stakeholders.")
        except Exception as e:
            print(f"Erro ao enviar o e-mail: {e}")