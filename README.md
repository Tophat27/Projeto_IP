# 🎮 Game UFPE_Alagada

<div align="center">

![Game UFPE_Alagada](https://img.shields.io/badge/Game-UFPE_Alagada-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-orange?style=for-the-badge&logo=pygame)
![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

*Um jogo de aventura 2D ambientado na UFPE com sistema de combate por turnos, coleta de itens e progressão por cenários*

</div>
## 🎓 Equipe
Vinícius S S Brandão<vssb>
Gabriel Marins Zarour <gmz>
Eduardo Lucas <elso>
Pedro Henrique Herculano da Silva<phhs>
Pedro Henrique Santana de Morais<phsm2>
Gabriel <jgcb>

---

## 📖 Sobre o Jogo

**Game UFPE_Alagada** é um jogo de aventura 2D desenvolvido em Python com Pygame, onde você controla um estudante que deve navegar pelos diferentes cenários da UFPE (Universidade Federal de Pernambuco) enfrentando desafios únicos em cada local.

### 🎯 Objetivo
Navegue pelos cenários da UFPE, colete itens úteis, derrote inimigos temáticos e sobreviva aos desafios de cada local. Cada cenário oferece uma experiência única com inimigos diferentes e mecânicas específicas.

---

## ✨ Características Principais

### 🎨 **Sistema de Cenários Dinâmicos**
- **4 Cenários Únicos**: Entrada UFPE, Biblioteca Central, RU e CIn
- **Transições Suaves**: Navegação fluida entre diferentes locais
- **Fundos Temáticos**: Cada cenário tem sua própria atmosfera visual

### ⚔️ **Sistema de Combate Avançado**
- **Combate por Turnos**: Sistema estratégico de batalha
- **Inimigos Únicos**: Cada cenário possui inimigos com características específicas
- **Partículas de Dano**: Sistema visual de feedback com animações
- **Orientação Inteligente**: Personagens mantêm direção durante o combate

### 🎭 **Sistema de Inimigos por Cenário**
- **Entrada UFPE**: Inimigo iniciante (20 HP, 3-15 dano)
- **Biblioteca**: Inimigo médio (35 HP, 7-20 dano) 
- **RU**: Inimigo forte (50 HP, 10-25 dano)
- **CIn**: Boss final (70 HP, 15-30 dano)

### 🎒 **Sistema de Inventário**
- **Botas**: Aumentam velocidade de movimento
- **Guarda-chuva**: Proteção contra dano
- **Gerenciamento Inteligente**: Uso limitado por turno

### 🎵 **Sistema de Áudio Completo**
- **Músicas Temáticas**: Diferentes trilhas para cada estado do jogo
- **Efeitos Sonoros**: Sons de ataque, vitória e derrota
- **Controle de Volume**: Sistema de áudio configurável

### 🎬 **Animações e Efeitos Visuais**
- **GIFs Animados**: Personagens e inimigos com animações fluidas
- **Partículas de Dano**: Sistema visual de feedback
- **Transições Suaves**: Animações entre estados do jogo

---

## 🚀 Instalação e Execução

### 📋 Pré-requisitos
- Python 3.7 ou superior
- Pygame 2.0 ou superior
- Pillow (PIL) para suporte a GIFs

### 🔧 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/Projeto_IP.git
cd Projeto_IP
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o jogo**
```bash
python jogo_ip.py
```

### 📦 Dependências
```bash
pip install pygame
pip install Pillow
```

---

## 🎮 Controles

### 🕹️ **Menu Principal**
- **Mouse**: Navegação pelos botões
- **Enter**: Seleção de opções

### 🚶 **Movimento do Jogador**
- **Setas/WASD**: Movimento em 4 direções
- **Limites de Movimento**: Restrito à área inferior da tela

### ⚔️ **Combate**
- **1**: Atacar
- **2**: Usar Bota (se disponível)
- **3**: Usar Guarda-chuva (se disponível)

### 🔧 **Funcionalidades Extras**
- **D**: Ativar/Desativar modo debug
- **ESC**: Sair do jogo

---

## 🏗️ Arquitetura do Projeto

### 📁 **Estrutura de Arquivos**
```
Projeto_IP/
├── jogo_ip.py          # Arquivo principal do jogo
├── enemy.py            # Sistema de inimigos
├── combat.py           # Sistema de combate
├── inventory.py        # Sistema de inventário
├── coleta.py           # Sistema de coleta de itens
├── items.py            # Definição dos itens
├── musica_config.py    # Configurações de áudio
├── variaveis.py        # Variáveis globais
├── tela.py             # Configurações de tela
├── storytelling.py     # Sistema de narrativa
├── images/             # Assets visuais
├── SFX/                # Efeitos sonoros
└── README.md           # Este arquivo
```

### 🧩 **Módulos Principais**

#### **`jogo_ip.py`**
- Loop principal do jogo
- Gerenciamento de estados
- Sistema de cenários
- Classe Player

#### **`enemy.py`**
- Sistema de inimigos por cenário
- Comportamentos únicos
- Animações GIF
- Estatísticas diferenciadas

#### **`combat.py`**
- Sistema de combate por turnos
- Partículas de dano
- Interface de batalha
- Gerenciamento de turnos

#### **`inventory.py`**
- Sistema de inventário
- Uso de itens
- Gerenciamento de recursos

---

## 🏛️ Arquitetura Modular e Orientação a Objetos

### 🧩 **Design Orientado a Objetos**

O projeto foi desenvolvido seguindo os princípios da **Programação Orientada a Objetos (POO)**, utilizando classes bem estruturadas para organizar o código de forma lógica e reutilizável.

#### **Principais Classes Implementadas:**

- **`Player`**: Gerencia o jogador, movimento, HP e dano
- **`Enemy`**: Sistema de inimigos com tipos específicos por cenário
- **`CombatSystem`**: Controla todo o sistema de combate por turnos
- **`Inventory`**: Gerencia itens e recursos do jogador
- **`DamageParticle`**: Sistema de partículas para feedback visual

### 📁 **Separação de Responsabilidades**

Cada arquivo possui uma responsabilidade específica, seguindo o princípio **Single Responsibility Principle**:

#### **`jogo_ip.py`** - Arquivo Principal
- **Responsabilidade**: Loop principal do jogo e gerenciamento de estados
- **Contém**: Classe Player, lógica de cenários, sistema de spawn de inimigos
- **Coordena**: Todos os outros sistemas através de instâncias das classes

#### **`enemy.py`** - Sistema de Inimigos
- **Responsabilidade**: Definição e comportamento dos inimigos
- **Contém**: Classe Enemy com tipos específicos por cenário
- **Implementa**: Animações GIF, estatísticas diferenciadas, comportamentos únicos

#### **`combat.py`** - Sistema de Combate
- **Responsabilidade**: Gerenciamento completo do combate
- **Contém**: Classe CombatSystem e DamageParticle
- **Implementa**: Turnos, interface de batalha, partículas de dano

#### **`inventory.py`** - Sistema de Inventário
- **Responsabilidade**: Gerenciamento de itens e recursos
- **Contém**: Classe Inventory
- **Implementa**: Adição, remoção e uso de itens

#### **`coleta.py`** - Sistema de Coleta
- **Responsabilidade**: Detecção e coleta de itens no mundo
- **Contém**: Lógica de colisão e spawn de itens
- **Implementa**: Sistema de coleta automática

#### **`items.py`** - Definição de Itens
- **Responsabilidade**: Configuração e propriedades dos itens
- **Contém**: Classes e constantes dos itens
- **Implementa**: Efeitos e comportamentos dos itens

#### **`musica_config.py`** - Sistema de Áudio
- **Responsabilidade**: Gerenciamento de músicas e efeitos sonoros
- **Contém**: Funções de controle de áudio
- **Implementa**: Transições musicais entre estados

#### **`variaveis.py`** - Configurações Globais
- **Responsabilidade**: Variáveis e constantes compartilhadas
- **Contém**: Configurações de tela, cores, dimensões
- **Implementa**: Centralização de configurações

#### **`tela.py`** - Configurações de Tela
- **Responsabilidade**: Inicialização e configuração da tela
- **Contém**: Configurações do Pygame
- **Implementa**: Setup da interface gráfica

### 🔄 **Benefícios da Arquitetura Modular**

#### **1. Manutenibilidade**
- **Código Organizado**: Cada funcionalidade em seu arquivo específico
- **Fácil Localização**: Problemas podem ser identificados rapidamente
- **Modificações Isoladas**: Mudanças não afetam outros sistemas

#### **2. Reutilização**
- **Classes Reutilizáveis**: Classes podem ser usadas em outros projetos
- **Módulos Independentes**: Cada arquivo pode ser testado isoladamente
- **Interfaces Claras**: APIs bem definidas entre os módulos

#### **3. Escalabilidade**
- **Fácil Extensão**: Novos sistemas podem ser adicionados sem modificar existentes
- **Modularidade**: Funcionalidades podem ser ativadas/desativadas
- **Testabilidade**: Cada módulo pode ser testado independentemente

#### **4. Colaboração**
- **Desenvolvimento Paralelo**: Diferentes desenvolvedores podem trabalhar em módulos diferentes
- **Conflitos Reduzidos**: Menos conflitos de merge no controle de versão
- **Documentação Clara**: Cada arquivo tem uma responsabilidade bem definida

### 🎯 **Padrões de Design Utilizados**

#### **Singleton Pattern**
- **`tela.py`**: Configuração única da tela do jogo
- **`variaveis.py`**: Configurações globais centralizadas

#### **Factory Pattern**
- **`enemy.py`**: Criação de inimigos baseada no tipo de cenário
- **`items.py`**: Criação de itens com propriedades específicas

#### **State Pattern**
- **`jogo_ip.py`**: Gerenciamento de estados do jogo (menu, jogo, combate)
- **`combat.py`**: Estados do combate (turno do jogador, turno do inimigo)

### 🐉 **Tipos de Inimigos**

| Cenário | Tipo | HP | Dano | Comportamento | Imagem |
|---------|------|----|------|---------------|---------|
| **Entrada** | `entrada` | 20 | 3-15 | Movimento simples | `inimigo 1.gif` |
| **Biblioteca** | `biblioteca` | 35 | 7-20 | Movimento suave | `clippy-microsoft.gif` |
| **RU** | `ru` | 50 | 10-25 | Movimento errático | `crocodile.gif` |
| **CIn** | `cin` | 70 | 15-30 | Movimento agressivo | `image-removebg-preview.png` |

### 🔄 **Progressão de Dificuldade**
- **Cenário 0**: Inimigo mais fraco para iniciantes
- **Cenário 1**: Dificuldade média para jogadores experientes
- **Cenário 2**: Desafio aumentado com inimigos mais fortes
- **Cenário 3**: Boss final com máxima dificuldade

### 🐛 **Modo Debug**
- Visualização de retângulos de colisão
- Informações de posição do jogador
- Estatísticas dos inimigos
- Limites de movimento

### 🎮 **Para Jogadores**
- **Variedade**: Cada cenário oferece uma experiência única
- **Progressão**: Dificuldade aumenta gradualmente
- **Imersão**: Inimigos temáticos para cada local
- **Balanceamento**: Estatísticas apropriadas para cada fase
- **Feedback Visual**: Sistema de partículas de dano para melhor experiência

<div align="center">

**🎮 Divirta-se jogando Game UFPE_Alagada! 🎮**

*Desenvolvido com ❤️ pela equipe do Projeto IP*

</div>
