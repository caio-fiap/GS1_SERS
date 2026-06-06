# ☄️ AETHER-1 -Space Energy Monitor

Sistema inteligente de monitoramento para missão espacial experimental. 
Desenvolvido para a Global Solution de **Soluções em Energias Renováveis e Sustentabilidade**

---

## 📋 Descrição

O **AETHER-1** simula o monitoramento em tempo real dos sistemas energéticos de uma estação espacial, incluindo:

- Geração de energia via **painéis solares**
- Gestão de **baterias** e consumo
- Controle da **temperatura** dos módulos
- Monitoramento do **sinal de comunicação** com a Central de Controle

O sistema aplica conceitos de **energia e potência** na análise dos dados simulados, gerando alertas e tomando decisões de forma automática.

---

## 📂 Estrutura do Projeto

```
aether1/  
│   
├── app.py              # aplicação principal
│   
├── modules/   
│   ├── simulador.py    # geração e simulação de dados dos sensores
│   └── alertas.py      # lógica de alertas e tomada de decisão
│
├── requisitos.txt   # dependências(bibliotecas) do python
└── README.md           # manual do projeto
```

---

## ⚙️ Como Rodar

### Clone o repositório
``` bash
git clone https://github.com/SEU-USER/aether1.git
cd aether1
```

### Instale as dependências
``` bash
pip install -r requisitos.txt
```

# Execute o sistema
```bash
streamlit run app.py
```
O dashboard abrirá automaticamente no navegador em `http://localhost:8501`;  
Se isso não acontecer, confira a resposta dada no terminal.

---

##  Funcionalidades

### Monitoramento de dados
Cada clique em **"Próximo ciclo"** simula um novo conjunto de leituras, com variação aleatória dentro de limites pré-definidos

| Sensor       | Faixa Normal | Unidade |
|--------------|:------------:|:-------:|
| Bateria      |   30 - 100   |    %    |
| Painel Solar |  1.5 - 5.0   |   kW    |
| Temperatura  |   -5 - 35    |   ºC    |
| Sinal        |   50 - 100   |   %     |

### Geração automática de alertas
O sistema classifica cada leitura em:
- 🟢 **NORMAL** - Dentro do esperado
- 🟡 **ALERTA** - atenção necessária
- 🔴 **CRÍTICO** - resposta imediata necessária

### Tomada de decisão
O sistema executa uma resposta automática para cada alerta. Por exemplo:
- Reduzir consumo de módulos não-essencias
- Ativar sistema de resfriamento de emrgência
- Redirecionar painéis solares

### Simulação de crise
O botão **⚠️ Crise** simula um evento catastrófico (como uma colisão com um meteoroide), degradando todos os sistemas simultaneamente.

---

## 🛠️ Tecnologias

- **Python 3.10**
- **Streamlit** &emsp;&emsp;&emsp;&emsp; -> interface web do dashboard
- **Plotly** &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp; -> gráficos interativos
- **Pandas** &emsp;&emsp;&emsp;&emsp;&emsp; -> manipulação de dados

---

## Screenshots

> Vou colocar imagens aqui depois de arrumar o programa :/

---

## 👥 Equipe

| Nome          |   RM    |
|---------------|:-------:|
| Caio Marinho  | 572873  |

---

## 🎥 Vídeo de demonstração

> link do youtube (quando tiver arrumado o programa :/)
