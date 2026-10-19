#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import os, re, subprocess, sys, zipfile, xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

SP_DATE=os.environ.get('SP_DATE','2026-06-30')
dt=datetime.strptime(SP_DATE,'%Y-%m-%d')
br=dt.strftime('%d/%m/%Y')
outdir=Path('/root/cerebro-minhaempresa/cerebro/areas/operacoes/relatorios/iclinic/downloads')
outdir.mkdir(parents=True,exist_ok=True)
final=outdir/f'pacientes_periodo_{dt.strftime("%d_%m_%Y")}.xlsx'
tmp=outdir/f'.tmp_pacientes_periodo_{dt.strftime("%d_%m_%Y")}.xlsx'
url=f'https://app.iclinic.com.br/v2/relatorios/atendimento/dia/?physician=58268&date=custom&date__gte={SP_DATE}&date__lte={SP_DATE}'

def log(s): print(s, flush=True)

def get_secret(field):
    token=Path('/root/.openclaw/secrets/1password-service-account-token').read_text().strip()
    env=os.environ.copy(); env['OP_SERVICE_ACCOUNT_TOKEN']=token
    p=subprocess.run(['op','item','get','Iclinic','--vault','Openclaw','--fields',field,'--reveal'], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
    if p.returncode!=0:
        raise RuntimeError('1Password lookup failed for '+field+': '+p.stderr[:300])
    return p.stdout.strip()

def read_xlsx_rows(path: Path):
    NS={"a":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            root=ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall('a:si',NS):
                shared.append(''.join((t.text or '') for t in si.findall('.//a:t',NS)))
        sheet=[n for n in z.namelist() if n.startswith('xl/worksheets/sheet')][0]
        root=ET.fromstring(z.read(sheet))
        rows=[]
        for row in root.findall('.//a:row',NS):
            vals=[]
            for cell in row.findall('a:c',NS):
                v=cell.find('a:v',NS); val=''
                if v is not None:
                    raw=v.text or ''
                    val=shared[int(raw)] if cell.get('t')=='s' and raw.isdigit() and int(raw)<len(shared) else raw
                vals.append(val)
            if any(str(x).strip() for x in vals): rows.append(vals)
        return rows

username=get_secret('username')
password=get_secret('password')
if not username: username='draligiatoledo.dor@gmail.com'

with sync_playwright() as p:
    # A coleta roda por cron, sem garantia de que exista um Chrome já aberto
    # expondo CDP em 127.0.0.1:18800. Tenta reaproveitar esse navegador quando
    # disponível, mas inicia uma instância isolada quando não estiver — assim a
    # rotina não depende de uma sessão gráfica local para funcionar.
    try:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:18800')
        ctx = browser.contexts[0] if browser.contexts else browser.new_context(
            accept_downloads=True, locale='pt-BR', timezone_id='America/Sao_Paulo'
        )
        log('browser: connected to local CDP')
    except Exception:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            accept_downloads=True, locale='pt-BR', timezone_id='America/Sao_Paulo'
        )
        log('browser: launched isolated Chromium')
    page=ctx.new_page()
    page.set_default_timeout(18000)
    log('goto '+url)
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(2000)
    if page.get_by_placeholder(re.compile('Email|E-mail|email',re.I)).count():
        log('login required')
        page.get_by_placeholder(re.compile('Email|E-mail|email',re.I)).first.fill(username)
        page.get_by_placeholder(re.compile('senha',re.I)).first.fill(password)
        page.get_by_role('button', name=re.compile('^Entrar$',re.I)).click()
        page.wait_for_timeout(7000)
    log('post-login-url '+page.url)
    try:
        if page.get_by_text('Clinica Dr. Ligia Toledo SP', exact=False).count():
            log('selecting clinic')
            page.get_by_text('Clinica Dr. Ligia Toledo SP', exact=False).first.click()
            page.wait_for_timeout(5000)
    except Exception as e:
        log('clinic selection note '+type(e).__name__)
    log('goto report target')
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=60000)
    page.wait_for_timeout(3000)
    body=page.locator('body').inner_text(timeout=20000)
    log('report-url '+page.url)
    if page.get_by_placeholder(re.compile('Email|E-mail|email',re.I)).count() or 'Sua sessão expirou' in body:
        raise SystemExit('blocked: login/session did not complete')
    if 'Exportar' not in body:
        Path('/tmp/iclinic_no_export_body.txt').write_text(body, encoding='utf-8')
        raise SystemExit('blocked: export not available')
    exp=page.get_by_role('button', name=re.compile('Exportar.*XLS|Exportar',re.I))
    if not exp.count(): exp=page.get_by_text(re.compile('Exportar.*XLS|Exportar',re.I))
    log('export count '+str(exp.count()))
    if not exp.count(): raise SystemExit('blocked: export button not found')
    if tmp.exists(): tmp.unlink()
    with page.expect_download(timeout=90000) as di:
        exp.first.click()
    dl=di.value
    dl.save_as(str(tmp))
    log('downloaded tmp size='+str(tmp.stat().st_size))
    if tmp.stat().st_size==0: raise SystemExit('blocked: empty download')

rows=read_xlsx_rows(tmp)
if rows:
    header=rows[0]
    expected=['Data','Horario','Paciente','Procedimento','Convênio']
    missing=[x for x in expected if x not in header]
    if missing: raise SystemExit('blocked: missing columns '+','.join(missing)+' header='+repr(header))
    records=[dict(zip(header,row)) for row in rows[1:]]
    bad=[r.get('Data') for r in records if r.get('Data')!=br]
    if bad:
        raise SystemExit('blocked: downloaded report contains dates outside '+br+': '+repr(bad[:10]))
else:
    # O iClinic exporta uma planilha sem cabeçalho quando não há atendimentos.
    # Isso é um resultado válido do dia, não falha de coleta.
    records=[]
    log('validated empty report: no appointments for '+br)
if final.exists():
    bak=final.with_suffix(final.suffix+'.bak_'+datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'))
    final.rename(bak); log('backup '+str(bak))
tmp.rename(final)
log('final '+str(final))
log(f'validated records={len(records)} date={br}')
