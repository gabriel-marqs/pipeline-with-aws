FROM public.ecr.aws/lambda/python:3.12

# Copia o requirements.txt da raiz do projeto para a imagem
COPY ../requirements.txt .

# Copia o código da pasta src (fora da pasta docker)
COPY ../src/lambda_function.py ${LAMBDA_TASK_ROOT}

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

CMD ["lambda_function.lambda_handler"]