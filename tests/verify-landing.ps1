param([string]$Path = "index.html")

$html = Get-Content -Raw -LiteralPath $Path
$required = @(
  '<title>Consultoría tecnológica para pymes y empresas medianas | ES Tech Services</title>',
  'Convierte la tecnología en una ventaja para tu operación.',
  'id="roadmap"',
  'id="capacidades"',
  'id="faq"',
  'Conversemos sobre tu operación',
  'aria-controls="site-menu"',
  'aria-expanded="false"',
  'scroll-margin-top:',
  'prefers-reduced-motion: reduce',
  'prefers-reduced-transparency: reduce',
  'https://eduardosalasg.dev/assets/og-es-tech-services.png',
  'FAQPage',
  'contact_whatsapp_click'
)

$failed = $required | Where-Object { -not $html.Contains($_) }
if ($failed) {
  $failed | ForEach-Object { Write-Error "Missing required landing contract: $_" }
  exit 1
}

if ($html -match 'world-class|P0</b>|KPI</b>|SLA</b>') {
  Write-Error 'Legacy unsupported or unexplained jargon remains in page content.'
  exit 1
}
