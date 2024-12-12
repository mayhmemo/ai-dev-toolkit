## Clonar o repositório

```bash
git clone https://github.com/Fguedes90/ai-dev-toolkit.git
```

## Navegar para o diretório do projeto

```bash
cd ai-dev-toolkit
```

## Instalar o UV

UV é um instalador rápido de pacotes Python e gerenciador de dependências escrito em Rust. Aqui está como instalar:

```bash
# Instalar UV usando curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instalando Python 3.10 usando UV

O UV pode gerenciar instalações Python. Aqui está como instalar o Python 3.10:

```bash
# Instalar Python 3.10
uv python install 3.10
```

## Instalando Poetry usando UV

Você pode instalar o Poetry como uma ferramenta usando UV:

```bash
# Instalar Poetry usando UV
uv tool install poetry
```

## Iniciar ambiente virtual do Poetry

```bash
poetry shell
```

## Instalar dependências

```bash
poetry install
```

## Executar a aplicação

### Tornar o script executável

```bash
chmod +x aitk
```

### Executar o script

```bash
./aitk --help
```
