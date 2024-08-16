# Kibana/Elastic Network Scanner

![Banner]([Kibana Script](https://prnt.sc/A9zLQtJeFKF4)) <!-- Substitua com um link para um banner ou imagem relevante -->

## Descrição

Este repositório contém um poderoso script de varredura de rede projetado para detectar serviços Kibana e Elastic rodando em uma infraestrutura específica. O script verifica blocos de IPs configuráveis, identifica portas abertas, e tenta acessar serviços via HTTP para confirmar sua operacionalidade. Ao final, exibe um resumo dos resultados, incluindo o total de IPs verificados e URLs dos serviços encontrados.

> **Nota:** Este script foi projetado para uso em ambientes controlados e com autorização explícita. Utilize-o de forma responsável.

## Funcionalidades

- **Varredura de Blocos de IPs:** Varre endereços IP em blocos configuráveis para detectar serviços específicos.
- **Verificação de Portas Abertas:** Identifica portas abertas em hosts e tenta acessar serviços Kibana/Elastic.
- **Relatório Detalhado:** Gera um resumo da varredura, listando URLs dos serviços encontrados e outras estatísticas relevantes.
- **Performance Otimizada:** Utiliza múltiplas threads para realizar varreduras rápidas e eficientes.

## Pré-requisitos

Antes de executar o script, você precisará instalar as seguintes bibliotecas Python:

- `socket`
- `requests`
- `ipaddress`
- `concurrent.futures`
- `queue`
- `colorama`
- `logging`
- `datetime`
- `tqdm`

## Instalação

Para instalar as bibliotecas necessárias, execute o seguinte comando:

```bash
pip install requests colorama tqdm
```

## Uso

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/ailtonrocha/kibana-elastic-network-scanner.git
   cd kibana-elastic-network-scanner
   ```

2. **Configure os Blocos de IPs:**

   Edite o script `scanner.py` e configure os blocos de IPs que você deseja escanear:

   ```python
   blocks_of_ips = [
       ip_network("10.0.0.0/8"),  # Exemplo de bloco /8
   ]
   ```

3. **Execute o Script:**

   ```bash
   python scanner.py
   ```

   O script exibirá um banner informativo e iniciará a varredura dos IPs configurados, verificando as portas abertas e testando a acessibilidade dos serviços Kibana/Elastic.

4. **Verifique os Resultados:**

   Ao final da varredura, o script mostrará um resumo com o total de IPs verificados, serviços encontrados e as URLs dos serviços acessíveis.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar um pull request ou abrir uma issue se encontrar algum problema ou tiver sugestões de melhorias.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Créditos

Criado por: **Ailton Rocha**

---

**Divirta-se escaneando com responsabilidade!**
