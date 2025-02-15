# 🎬 Sistema de Recomendação Inteligente de Filmes

Este projeto é uma API que recomenda um filme com base na similaridade de gêneros entre dois filmes escolhidos pelo usuário. Além disso, a aplicação também analisa o sentimento das avaliações de filmes utilizando modelos de aprendizado de máquina para delimitar se o filme tem avaliações positivas, negativas ou neutras.


## 🚀 Funcionalidades

✅ **Recomendação de Filmes**:
- O sistema compara dois filmes e sugere um terceiro filme com base nos gêneros em comum.
- Utiliza a API do TMDb para obter os dados dos filmes.
- Calcula a similaridade entre os filmes utilizando a métrica de cosseno.

✅ **Análise de Sentimento**:
- Utiliza o modelo de NLP da biblioteca `transformers` para classificar avaliações de filmes como **positivas, negativas ou neutras**.
- Mede a confiança da análise de sentimento.

## 🛠️ Tecnologias Utilizadas

- **Python**
- **NumPy** (para manipulação de arrays)
- **scikit-learn** (para cálculo de similaridade)
- **requests** (para consumo da API do TMDb)
- **Hugging Face Transformers** (para análise de sentimento)

## 📦 Instalação e Configuração

### 🔹 1. Clone o Repositório
```bash
git clone https://github.com/DaniOrze/movie-recommendation-api.git
cd movie-recommendation-api
```

### 🔹 2. Crie um Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate    # Para Windows
```

### 🔹 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 🔹 4. Configuração da API Key
Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API TMDb:
```env
TMDB_API_KEY=sua_api_key_aqui
```

## 📌 Uso

### 🔹 Executar a Aplicação FastAPI

```bash
fastapi dev main.py
```

### 🔹 Testar os Endpoints via Swagger

Após iniciar a aplicação, abra o navegador e acesse:

```
http://127.0.0.1:8000/docs
```

Isso abrirá a interface do Swagger, onde você pode testar os endpoints da API de forma interativa.

## 🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para usá-lo e modificá-lo.