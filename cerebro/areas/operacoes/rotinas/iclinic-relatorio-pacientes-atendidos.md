# Rotina — iClinic: relatório diário de pacientes atendidos

## Objetivo

Automatizar a geração diária, às 23h, do relatório de pacientes atendidos no iClinic.

## Relatório

- Sistema: Afya iClinic
- Relatório: **Paciente por período**
- Formato de exportação: `.xls`
- Período desejado: data inicial = data final = dia corrente
- Recorrência nativa no iClinic: não disponível
- API: não disponível

## Caminho manual mapeado por prints

1. Acessar o iClinic após login.
2. No menu lateral, clicar em **Relatórios**.
3. Na tela de relatórios, clicar em **Paciente por período**.
4. Selecionar/preencher o período desejado.
5. Gerar/visualizar o relatório.
6. No canto inferior direito, clicar no botão de **Exportar**.
7. Baixar o arquivo `.xls`.

## Automação planejada

Criar rotina diária que:

1. Abre o iClinic em navegador automatizado do OpenClaw.
2. Confirma sessão logada.
3. Navega até **Relatórios → Paciente por período**.
4. Preenche período com a data do dia.
5. Exporta o `.xls`.
6. Salva o arquivo em pasta padronizada.
7. Opcionalmente analisa/resume/envia alerta.

## Pendência crítica

Ainda falta habilitar o login no navegador automatizado.

Recomendação: criar usuário dedicado para automação no iClinic, com permissões mínimas necessárias para visualizar/exportar o relatório.


## Campos do relatório

O relatório exportado em `.xls` contém os seguintes campos principais:

- **Data**
- **Horário**
- **Paciente**
- **Procedimento**
- **Convênio**

## Uso para follow-up

Os campos **Data**, **Horário**, **Paciente** e **Procedimento** serão usados para montar a rotina de acompanhamento pós-atendimento.

O campo **Convênio** pode ser usado como contexto adicional, por exemplo para diferenciar pacientes particulares, convênios ou regras comerciais específicas.

A regra principal de follow-up deve considerar:

- data do atendimento/procedimento;
- tipo de procedimento realizado;
- paciente atendido;
- prazo de contato definido para cada procedimento.

## Próxima definição necessária

Definir regras de follow-up por procedimento:

- quando acionar: D+1, D+3, D+7, D+15 etc.;
- canal: WhatsApp, ligação, tarefa para Paola, outro;
- texto/modelo de abordagem;
- se há exceções por tipo de procedimento.
