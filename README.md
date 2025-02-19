# 📚 Sistema de Gerenciamento de Estudos para o ENEM

## 🎯 Objetivo do Projeto
Nosso projeto busca solucionar um dos principais desafios enfrentados pelos estudantes que se preparam para o ENEM: a falta de organização e planejamento de estudos. A ideia surgiu a partir da nossa própria experiência e da realidade de muitas pessoas próximas, que enfrentam dificuldades para estruturar uma rotina eficiente de estudos.

Com esse projeto, pretendemos desenvolver um cronograma de estudos semanal personalizado, baseado em dados coletados por meio de um formulário. Isso ajudará o usuário a organizar melhor sua jornada de preparação para o ENEM. Além disso, planejamos incluir seções específicas com os conteúdos de cada disciplina exigida na prova, facilitando o acesso às matérias e otimizando o aprendizado.

---

## 🚀 Funcionalidades

### 📌 Funcionalidades Principais
- **Formulário de coleta** (sem possibilidade de edição pelo usuário após envio)
- **Geração de cronograma de estudos personalizado**
- **Listagem das matérias e seus conteúdos**
- **Acompanhamento de progresso através de gráfico**
- **Marcação de conteúdos concluídos (check no cronograma)**
- **Revisão ativa com o mecanismo de check**
- **Barra de pesquisa para busca de conteúdos específicos**
- **Área administrativa para gestão de usuários e conteúdos**
  - O administrador pode visualizar todos os usuários cadastrados
  - O administrador pode excluir usuários
  - O administrador pode adicionar novos conteúdos ou assuntos

### 🔍 Detalhamento das Funcionalidades
- O cronograma será estruturado em **3 semanas de estudo e 1 semana de revisão**
- Enquanto o usuário não marcar um conteúdo como estudado, ele continuará aparecendo no cronograma nas semanas seguintes
- O tempo disponível será distribuído de forma estratégica, equilibrando revisão e aprofundamento
- O sistema calculará a média de tempo necessário para o aprendizado de cada assunto
- O cronograma será atualizado dinamicamente conforme o progresso do usuário
- O menu interativo permitirá que o usuário visualize os conteúdos de cada disciplina
- O dashboard apresentará os conteúdos semanais e o progresso do usuário

---

## 🔮 Futuras Implementações
- **Encaminhamento para listas de exercícios** (via API ou IA)
- **Recomendações de videoaulas e materiais de estudo** (via API ou IA)
- **Prova de nivelamento** para medir o conhecimento do usuário antes da montagem do cronograma
- **Edição dos dados informados no formulário** (permitindo ajuste de tempo de estudo)
- **Fórum para interação entre usuários**
- **Sugestão de novos conteúdos pelos usuários, com aprovação do administrador**

---

## 🛠️ Especificações Técnicas
### 📋 Coleta de Dados
- O formulário solicitará as seguintes informações:
  - Horas disponíveis para estudo
  - Matérias que o usuário deseja estudar
  - Matérias que o usuário deseja dar maior foco
- Atribuição de pesos às matérias conforme a importância indicada pelo usuário
- Distribuição do cronograma com base nesses pesos, priorizando matérias mais relevantes
- Cálculo estimado do tempo necessário para estudo de cada assunto
- Planejamento do cronograma com continuidade baseada no cumprimento das horas recomendadas

### 📌 Organização do Sistema
- **Menu interativo:** Ao clicar em uma disciplina, serão exibidos os conteúdos relacionados
- **Dashboard:** Exibição dos conteúdos semanais e progresso do usuário

---

## 📅 Problemas que o Projeto Resolve
✅ Falta de organização nos estudos<br>
✅ Otimização do tempo de preparação para o ENEM

---

### ✉️ Contato
Caso tenha dúvidas ou sugestões, entre em contato conosco! 😊
