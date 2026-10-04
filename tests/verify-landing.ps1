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
  'contact_whatsapp_click',
  'og:image:alt',
  'og:image:width" content="1200"',
  'og:image:height" content="630"',
  '"founder"',
  'Eduardo Salas González',
  'role="img"',
  'Formato:',
  'menu-cta'
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

$visibleFaq = @(
  '¿Para qué tipo de empresas trabajan?',
  '¿Se puede comenzar por un problema puntual?',
  '¿Qué ocurre después de la primera conversación?',
  '¿Trabajan con sistemas que ya existen?'
)
$missingFaq = $visibleFaq | Where-Object { -not $html.Contains($_) }
if ($missingFaq) {
  $missingFaq | ForEach-Object { Write-Error "Missing visible FAQ contract: $_" }
  exit 1
}

if (-not $html.Contains('--muted:#36516e')) {
  Write-Error 'Secondary body text must use the approved high-contrast muted color.'
  exit 1
}

$root = Split-Path -Parent $PSScriptRoot
foreach ($asset in @('robots.txt', 'sitemap.xml', 'assets/og-es-tech-services.png')) {
  if (-not (Test-Path (Join-Path $root $asset))) {
    Write-Error "Missing deployed asset: $asset"
    exit 1
  }
}

if ((Get-Item (Join-Path $root 'assets/og-es-tech-services.png')).Length -gt 300KB) {
  Write-Error 'og:image asset exceeds 300KB.'
  exit 1
}
