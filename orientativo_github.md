# Guia de Trabalho em Equipe no GitHub

Este documento é a nossa referência oficial para padronizar o trabalho em equipe usando o Git e o GitHub neste projeto. Como o repositório já está criado, o fluxo de trabalho será focado em clonar, ramificar (branch), modificar e integrar o código (Pull Request).

## 1. Clonar o repositório (Primeiro passo)
Como o repositório já existe, você **não** precisa usar `git init`. Você deve clonar (baixar) o projeto para a sua máquina:

```bash
git clone https://github.com/RAguiarEng/GenAI_Seguros.git
cd GenAI_Seguros
```

## 2. Configuração Inicial (Apenas uma vez)
Garanta que o Git saiba quem você é. No terminal, execute:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu_email@exemplo.com"
```

## 3. Fluxo de Trabalho Diário

Nunca trabalhe diretamente na branch `main` (nossa linha do tempo principal). Sempre crie uma cópia paralela chamada **branch** para a sua tarefa.

### Passo A: Atualize seu repositório
Antes de começar a trabalhar, garanta que você tem a versão mais recente do projeto:
```bash
git checkout main
git pull origin main
```

### Passo B: Crie uma Branch para a sua tarefa
Crie e entre em uma nova branch para a funcionalidade em que vai trabalhar:
```bash
git checkout -b feature/nome-da-tarefa
```
*Exemplos de nomes: `feature/faq-dataset`, `fix/erro-banco`, `docs/atualiza-readme`.*

### Passo C: Faça suas alterações e salve (Commit)
Trabalhe normalmente nos arquivos. Quando terminar ou quiser salvar um progresso:
```bash
# Adiciona os arquivos modificados para serem salvos
git add .

# Salva o estado atual com uma mensagem clara e descritiva
git commit -m "Adiciona dataset de FAQs do Kaggle"
```

### Passo D: Envie seu trabalho para o GitHub (Push)
Envie sua branch para o repositório remoto no GitHub:
```bash
git push -u origin feature/nome-da-tarefa
```
*(Nota: O `-u` só é necessário na primeira vez que enviar essa branch. Depois basta usar `git push`).*

## 4. Integração do Código (Pull Request - PR)
Após enviar sua branch para o GitHub, o código ainda não está na `main`. Para integrar:
1. Acesse a página do projeto no GitHub pelo navegador.
2. Você verá um botão verde dizendo **"Compare & pull request"**. Clique nele.
3. Adicione um título e uma descrição do que você fez.
4. Clique em **"Create pull request"**.
5. Peça para outro membro da equipe revisar seu código. Se tudo estiver certo, ele será aprovado e mesclado (Merged) à branch `main`.

## 5. Lidando com Conflitos
Se duas pessoas alterarem a mesma linha do mesmo arquivo, o Git acusará um **conflito**. 
- O Git vai marcar no arquivo onde está o conflito (com `<<<<<<<`, `=======`, `>>>>>>>`).
- Você precisará abrir o arquivo, decidir qual código manter (ou misturar os dois), apagar as marcações do Git e fazer um novo `git add` e `git commit`.
- Em caso de dúvidas, chame a equipe para ajudar na resolução.

## 6. Boas Práticas da Equipe
- **Commits frequentes e atômicos:** Faça commits pequenos e lógicos. Evite fazer um único commit no fim do dia com dezenas de arquivos alterados.
- **Mensagens claras:** Escreva mensagens de commit que expliquem *o que* foi feito (ex: "Corrige bug no fluxo de atendimento").
- **Comunicação:** Use a aba "Issues" do GitHub ou o grupo do WhatsApp/Discord da equipe para avisar no que você está trabalhando, evitando que duas pessoas façam a mesma coisa.
- **GitHub Desktop:** Se o terminal parecer muito complexo, sinta-se livre para usar a interface visual do [GitHub Desktop](https://desktop.github.com/). O fluxo lógico (Pull > Branch > Commit > Push > PR) é exatamente o mesmo!