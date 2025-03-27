import openai
import os
import json

class LLMService:
    def __init__(self, db):
        self.db = db
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def evaluate(self, id, text):
        prompt = (
            
                "Você é um classificador de feedbacks altamente competente e tem a tarefa de analisar o seguinte feedback\n"
                "produzido por um usuário. O seu objetivo é classificar o teor do comentário em 3 classes: \"POSITIVO\", \"NEGATIVO\" ou \"INCONCLUSIVO\".\n"
                "Cada feedback deverá ter apenas uma classificação. Além disso, você deverá retirar funcionalidades que o usuário pediu e dar uma\n"
                "justificativa pela qual ele quer aquela determinada funcionalidade. É muito importante que você extraia funcionalidades sempre que houver\n"
                "alguma solicitação dentro do texto e que você consiga determinar o motivo pelo qual o usuário quer aquela funcionalidade em específico.\n"

                "Abaixo, seguem alguns exemplos de classificação, separados por aspas triplas:"

                '''
                FEEDBACK RECEBIDO:
                {
                    "id": "4042f20a-45f4-4647-8050-139ac16f610b",
                    "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta"
                }

                RESPOSTA:
                {
                    "id": "4042f20a-45f4-4647-8050-139ac16f610b",
                    "sentiment": "POSITIVO",
                    "requested_features": [
                        {
                        "code": "EDITAR_PERFIL",
                        "reason": "O usuário gostaria de realizar a edição do próprio perfil"
                        }
                    ]
                }
                '''

                '''
                FEEDBACK RECEBIDO:
                {
                    "id": "4042f20a-45f4-4647-8050-139ac16f610c",
                    "feedback": "Não gostei da plataforma, ela poderia ser mais clara e ter pelo menos um assistente de IA integrado."
                }

                RESPOSTA:
                {
                    "id": "4042f20a-45f4-4647-8050-139ac16f610c",
                    "sentiment": "NEGATIVO",
                    "requested_features": [
                        {
                        "code": "ASSISTENTE_IA",
                        "reason": "O usuário gostaria de um assistente de IA para auxiliá-lo nos estudos."
                        }
                    ]
                }
                '''

                "Você deverá classificar o seguinte texto e retornar um json válido, sem texto adicional, assim como a RESPOSTA esperada acima:"
                "{"
                f"\"id\": \"{id}\""
                f"\"feedback\": \"{text}\""
                "}"
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            return {
                "id": parsed.get("id", id),
                "sentiment": parsed.get("sentiment", "unknown"),
                "features": parsed.get("requested_features", [])
            }

        except Exception as e:
            print("Erro na chamada OpenAI:", e)
            return {
                "erro": "Erro na chamada OpenAI",
                "detalhes": str(e)
            }

    def generate_email(self, feedback_data):
        prompt = (
        "Você é um assistente de emails muito competente em escrever emails corporativos para stakeholders da empresa AluMind.\n"
        "Esses stakeholders precisam ser informados sobre como a empresa está se saindo a partir dos feedbacks dos usuários.\n"
        "Assim sendo, você receberá, a seguir, separado por aspas triplas, os dados brutos dos dados coletados sobre os feedbacks\n"
        "mais recentes e deverá compor um email corporativo para os stakeholders da empresa AluMind.\n"
        "O email deverá conter as seguintes informações:\n"
        "1.porcentagem de feedbacks positivos"
        "2.porcentagem de feedbacks negativos"
        "3.Principais funcionalidades pedidas e o porquê cada uma seria importante de ter."
        "Componha o email a partir das seguintes informações:"
        f"'''{feedback_data}'''"
        "Você deve retornar apenas uma sting python formatada como um email corporativo."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            content = response.choices[0].message.content

            return content

        except Exception as e:
            print("Erro na chamada OpenAI:", e)
            return {
                "erro": "Erro na chamada OpenAI",
                "detalhes": str(e)
            }