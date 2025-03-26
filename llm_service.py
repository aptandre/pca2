import openai
import os
import json

class LLMService:
    def __init__(self, db):
        self.db = db
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def evaluate(self, id, text):
        print("\n\n\nTO AQUI NE NO EVALUATE\n\n\n")
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

        print("\n\n\nPREPARA QUE VOU MANDAR A REQUISIÇÃO\n\n\n")
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
