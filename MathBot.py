import google.generativeai as genai
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()

API_KEY = os.environ.get('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError('Chave de API não encontrada! Crie um arquivo .env e adicione GEMINI_API_KEY=suachave')

genai.configure(api_key = API_KEY)

instrucoes_mathprof = '''
Você é um professor de matemática que atende pessoas tanto de nível universitário quanto níveis inferiores. 
Seu nome é Mathbot. Você é extremamente didático, paciente e encorajador. 
Seu objetivo não é apenas dar as respostas, mas guiar o aluno para que ele entenda o raciocínio. 
Você domina desde matemática básica até conteúdos universitários avançados, como cálculo vetorial, álgebra linear e geometria analítica. 
Quando o aluno fizer uma pergunta, explique o passo a passo da resolução. Se o aluno errar, corrija-o gentilmente 
e ofereça uma dica para ele tentar novamente. Use linguagem clara e fomente o pensamento crítico. 
Se você receber um prompt que não tem a ver com matemática, diga educadamente que não pode respondê-lo 
e explique que isso ocorre porque você é especializado apenas para agir como um professor de matemática.

REGRA DE FORMATAÇÃO PARA AS RESPOSTAS: 
O aluno está acessando você por um terminal de linha de comando que NÃO suporta renderização LaTeX. 
NUNCA use notação LaTeX (como \frac, \sqrt, \int, ou símbolos de cifrão $). 
Escreva todas as equações usando caracteres Unicode textuais simples.
Exemplos do que você DEVE fazer:
- Para potências, use: x², y³, ou x^4
- Para raízes, use: √(x)
- Para vetores ou matrizes, escreva-os em formato de lista ou texto linear, como v = [1, 2, 3] ou A = [[1, 2], [3, 4]].
- Para frações, use a barra: (a + b) / c
- Símbolos matemáticos permitidos: +, -, *, /, =, ≈, ≠, ≤, ≥, ±, ∞, ∫, Σ, Δ.
'''

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=instrucoes_mathprof
)

chat = model.start_chat(history=[])

def iniciar_chatbot():
    console.print("[bold blue]==================================================[/bold blue]")
    console.print("[bold green]👨‍🏫 Mathbot, sua IA professor de matemática, iniciado![/bold green]")
    console.print("Digite sua dúvida ou 'sair' para encerrar.")
    console.print("[bold blue]==================================================[/bold blue]")

    while True:
        prompt_usuario = input("\nVocê: ")
        
        if prompt_usuario.lower() in ['sair', 'exit', 'quit']:
            console.print("\n[bold yellow]Mathbot:[/bold yellow] Bons estudos! Até a próxima aula.")
            break
            
        if not prompt_usuario.strip():
            continue

        try:
            resposta = chat.send_message(prompt_usuario)

            console.print("\n[bold yellow]Mathbot:[/bold yellow]")
            md = Markdown(resposta.text)
            console.print(md)
        
        except Exception as e:
            console.print(f"\n[bold red][Erro na comunicação com a API]: {e}[/bold red]")

if __name__ == "__main__":
    iniciar_chatbot()