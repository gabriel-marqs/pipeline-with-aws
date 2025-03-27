# Usa a imagem base da AWS para Lambda em Python
FROM public.ecr.aws/lambda/python:3.12

# Instala dependências do sistema (se necessário)
# RUN yum install -y algum-pacote

# Copia o arquivo de dependências do Python para o container
COPY src/requirements.txt ${LAMBDA_TASK_ROOT}

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do Lambda para o container
COPY src/lambda_function.py ${LAMBDA_TASK_ROOT}

# Define o comando padrão (handler do Lambda)
CMD ["lambda_function.lambda_handler"]