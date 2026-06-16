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

## Credenciais e acesso automatizado

O acesso automatizado foi configurado via 1Password Service Account.

- Cofre: **Openclaw**
- Item: **Iclinic**
- Usuário: `draligiatoledo.dor@gmail.com`
- Token do Service Account salvo no servidor em: `/root/.openclaw/secrets/1password-service-account-token`
- Para ler a senha real pelo CLI, usar `--reveal`.

Comando-base para recuperar credenciais sem imprimir senha:

```bash
export OP_SERVICE_ACCOUNT_TOKEN="$(cat /root/.openclaw/secrets/1password-service-account-token)"
op item get 'Iclinic' --vault 'Openclaw' --fields username --reveal
op item get 'Iclinic' --vault 'Openclaw' --fields password --reveal
```

## Teste realizado

Em 2026-06-16, o fluxo foi testado com sucesso:

1. Login automático no iClinic com credenciais do 1Password.
2. Seleção da clínica **Clinica Dr. Ligia Toledo SP** quando solicitado.
3. Navegação para **Relatórios → Pacientes por período**.
4. Tela final confirmada em: `/v2/relatorios/atendimento/dia/`.
5. Botão **Exportar em .XLS** localizado.
6. Exportação testada com sucesso.
7. Arquivo gerado em:
   `/root/cerebro-minhaempresa/cerebro/areas/operacoes/relatorios/iclinic/downloads/pacientes_periodo_16_06_2026.xlsx`

## Observações técnicas

- O botão informa `.XLS`, mas o arquivo baixado no teste veio como `.xlsx`.
- O Chrome headless precisa ter a pasta de download liberada via CDP antes de clicar em exportar.
- Se a sessão expirar, a rotina deve refazer login usando 1Password.


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
