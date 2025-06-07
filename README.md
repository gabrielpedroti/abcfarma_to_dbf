<h1 align="left">💊 Gerador de Preços ABCFARMA (.DBF)</h1>

<p align="left">
Este projeto foi desenvolvido para gerar um arquivo utilizado na atualização de preços de medicamentos tabelados. Essa foi a minha primeira oportunidade de criar uma aplicação para resolver um problema real, que surgiu através da necessidade de um amigo, dono de uma rede de farmácias, que enfrentava dificuldades para encontrar uma solução compatível com o sistema que utiliza, e não havia opções no mercado.
</p>

##

<h3 align="left">🚀 Tecnologias utilizadas</h3>

<ul align="left">
  <li><strong>Python 3</strong></li>
  <li><strong>API ABCFARMA</strong> (requisições com <code>requests</code>)</li>
  <li><strong>Geração de arquivos .DBF</strong> com <code>dbf</code></li>
  <li><strong>Variáveis de ambiente</strong> com <code>dotenv</code></li>
  <li><strong>Criação de executável</strong> com <code>PyInstaller</code> (para rodar fora do terminal)</li>
</ul>

##

<h3 align="left">🖥️ Como funciona</h3>

<ol align="left">
  <li>Faz requisições à API da ABCFARMA com as credenciais da farmácia</li>
  <li>Processa os dados retornados (cerca de 17 mil produtos)</li>
  <li>Filtra os produtos com base em regras configuráveis (ex: ignorar medicamentos que não são tabelados)</li>
  <li>Gera um arquivo <code>.DBF</code> padronizado e compatível com sistemas legados</li>
  <li>Cria um log da execução e salva o arquivo com um nome dinâmico, como: <code>PRECO_280525.dbf</code></li>
</ol>

##

<h3 align="left">⚠️ Observações</h3>

<ul align="left">
  <li>Os dados sensíveis (CNPJ e senha) são armazenados em um arquivo <code>.env</code>, que por questões de privacidade <strong>não está incluído no repositório</strong>.</li>
  <li>O acesso à API funciona apenas para farmácias com <strong>assinatura ativa na ABCFARMA</strong> e com um <strong>CNPJ de software autorizado</strong>.</li>
</ul>

##

<h3 align="left">🚧 Status</h3>

<ul align="left">
  <li>✅ O sistema está funcional e cumprindo seu propósito!</li>
  <li>🛠️ Futuramente, pretendo implementar melhorias como:
    <ul>
      <li>Interface gráfica (GUI)</li>
      <li>Verificação automática de atualizações antes de gerar o <code>.DBF</code></li>
      <li>Envio automático do <code>.DBF</code> por e-mail</li>
      <li>Opção de alterar o diretório de salvamento dos arquivos</li>
      <li>Definição dos dados que serão incluídos no <code>.DBF</code>, prevendo necessidades futuras</li>
    </ul>
  </li>
</ul>
