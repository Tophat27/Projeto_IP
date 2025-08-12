# Sistema de Inimigos por Cenário - Instruções de Implementação

## Visão Geral
O sistema foi implementado para que cada cenário tenha um tipo específico de inimigo com características únicas.

## Tipos de Inimigos Implementados

### 1. **Entrada UFPE** - Tipo: "entrada"
- **Imagem**: `images/inimigo 1.gif` (GIF animado)
- **HP**: 30
- **Dano**: 8-20
- **Comportamento**: Movimento simples + animação GIF
- **Características**: Ideal para jogadores iniciantes, com animação

### 2. **Biblioteca Central** - Tipo: "biblioteca"
- **Imagem**: `images/clippy-microsoft.gif` (GIF animado)
- **HP**: 45
- **Dano**: 12-25
- **Comportamento**: Movimento suave com variação sutil + animação GIF
- **Características**: Inimigo de dificuldade média, com animação

### 3. **RU** - Tipo: "ru"
- **Imagem**: `images/crocodile.gif` (GIF animado)
- **HP**: 60
- **Dano**: 15-30
- **Comportamento**: Movimento errático e imprevisível + animação GIF
- **Características**: Inimigo mais desafiador, com animação

### 4. **CIn** - Tipo: "cin"
- **Imagem**: `images/image-removebg-preview.png`
- **HP**: 80
- **Dano**: 20-35
- **Comportamento**: Movimento agressivo com variação horizontal
- **Características**: Boss final, inimigo mais forte

## Como Criar as Imagens dos Inimigos

### Opção 1: Usar o Inimigo Padrão
Se você não criar as imagens específicas, o sistema usará `images/enemy.png` como fallback.

### Opção 2: Criar Imagens Personalizadas
1. **inimigo 1.gif**: Inimigo relacionado à entrada da UFPE (ex: guarda, estudante perdido) - **JÁ IMPLEMENTADO**
2. **clippy-microsoft.gif**: Inimigo relacionado à biblioteca (ex: bibliotecário zangado, livro voador) - **JÁ IMPLEMENTADO**
3. **crocodile.gif**: Inimigo relacionado ao RU (ex: cozinheiro, comida estragada) - **JÁ IMPLEMENTADO**
4. **image-removebg-preview.png**: Inimigo relacionado ao CIn (ex: professor, computador malicioso) - **JÁ IMPLEMENTADO**

## Características do Sistema

### Progressão de Dificuldade
- **Cenário 0 (Entrada)**: Inimigo mais fraco (30 HP, 8-20 dano)
- **Cenário 1 (Biblioteca)**: Inimigo médio (45 HP, 12-25 dano)
- **Cenário 2 (RU)**: Inimigo forte (60 HP, 15-30 dano)
- **Cenário 3 (CIn)**: Boss final (80 HP, 20-35 dano)

### Comportamentos Únicos
- **Entrada**: Movimento simples e previsível
- **Biblioteca**: Movimento suave com variação mínima
- **RU**: Movimento errático e imprevisível
- **CIn**: Movimento agressivo com variação horizontal

### Sistema de Fallback
Se alguma imagem não for encontrada, o sistema:
1. Tenta carregar `images/enemy.png`
2. Se falhar, cria um inimigo vermelho padrão
3. Mantém as estatísticas apropriadas para o cenário

## Benefícios da Implementação

1. **Variedade**: Cada cenário oferece uma experiência única
2. **Progressão**: Dificuldade aumenta gradualmente
3. **Imersão**: Inimigos temáticos para cada local
4. **Balanceamento**: Estatísticas apropriadas para cada fase
5. **Robustez**: Sistema de fallback para evitar erros

## Testando o Sistema

1. Execute o jogo
2. Ative o modo debug (tecla D)
3. Observe as mensagens no console mostrando o tipo de inimigo spawnado
4. Verifique as estatísticas diferentes de cada inimigo
5. Teste a progressão de dificuldade entre cenários

## Personalização

Para adicionar novos tipos de inimigos:
1. Adicione o novo tipo na lista `tipos_inimigos`
2. Crie a lógica correspondente na classe `Enemy`
3. Adicione as estatísticas e comportamentos desejados
4. Crie a imagem correspondente na pasta `images/`
