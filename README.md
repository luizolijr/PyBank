# Sistema de Gerenciamento Financeiro

Este é um projeto para controle financeiro que recebe as movimentações e as armazena em um arquivo JSON.

![image](https://github.com/luizolijr/PyBank/assets/42130256/4122a882-b998-46bb-879d-bd21c00bac41)


## Descrição

O objetivo deste projeto é ter um sistema funcional, com as operações básicas de CRUD (Create, Read, Update, Delete). Nesse contexto podemos adicionar novos registros, lêr os registros existentes, editá-los e deletá-los. Além disto, foi solicitado que pudessemos ter acesso aos investimentos do usuário e o rendimento com base no tempo decorrido.

Assim como no projeto do módulo 1, vale ressaltar que o objetivo deste projeto era implementar as funcionalidades com o mínimo de bibliotecas/módulos possíveis, sendo assim, teremos pouco ou quase nenhuma biblioteca complexa exercendo funções importantes no código, ex: pandas aparece minimamente no upgrade do projeto.

Informação importante sobre este repositório: O projeto desenvolvido pelo grupo está contido em "Projeto_LPII.ipynb", mas após o envio, decidi fazer um upgrade pra deixá-lo com uma interface visual utilizando Streamlit, que se encontra no arquivo "projeto_v2.py".

## Uso Projeto_LPII.ipynb

Para usar o projeto, siga estas etapas:

1. Caso não tenha as bibliotecas utilizadas instaladas, instale-as.
2. Execute o código Python.
3. O código irá pedir o ID do usuário, basta informar. Caso não exista, a unica função disponível seria "Criar novo Registro"
4. Basta seguir o menu e escolher as funcionalidades desejadas.

## Uso projeto_v2.py

Atualização: Adicionado parte "gráfica" com streamlit.

1. Instale as devidas bibliotecas
2. No windows, usei o terminal do anaconda e naveguei até a pasta do projeto.
3. Agora digite o comando "streamlit run projeto_v2.py" e o projeto abrirá em seu navegador.
3. O programa irá pedir o ID do usuário, basta informar.
4. Basta escolher as funcionalidades desejadas e aproveitar o sistema.

## Resultado

O projeto cumpre bem com o esperado, incluindo:

- Adicionar, Visualizar, Editar e Deletar registros.
- Exportar relatório em CSV ou JSON.
- Valor de capital do usuário com base nas despesas e receitas inseridas.
- Área de investimentos com valor total investido, rendimento e montante total.


## Meu Aprendizado

1 - Novamente achei um projeto desafiador, especialmente por não poder usar determinadas bibliotecas, saí com uma visão de que posso fazer funções pra qualquer coisa.  
2 - Aprendi mais sobre como trabalhar em grupo, pois os integrantes tinham muita incompatibilidade de horario, assim cada um produzia algo e ia comunicando com os demais, tendo algumas chamadas pontuais para terminar de alinhar/explicar o código.

## Requisitos

- Python
- Pandas
- Streamlit
- os
- datetime
- csv
- json

## Contribuição

Sinta-se à vontade para contribuir com este projeto, abrir problemas ou enviar solicitações de pull.


---

[Luiz Antônio]




