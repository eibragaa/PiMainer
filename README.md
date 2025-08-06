# PiMainer 🚀

Um painel visual para mineração de Bitcoin em modo "loteria", projetado para rodar em um Raspberry Pi com DietPi. Este projeto combina um minerador de CPU de linha de comando com uma interface de terminal rica e moderna, construída em Python com a biblioteca `rich`.

![PiMainer Screenshot](httpss://i.imgur.com/link_para_sua_nova_screenshot.png)
*(Instrução: Tire uma foto/screenshot do seu painel final funcionando, faça upload para um site como o [Imgur](https://imgur.com/) e substitua o link acima).*

## Sobre o Projeto

O PiMainer nasceu como um projeto de aprendizado para explorar a mineração de Bitcoin, o gerenciamento de sistemas Linux e a criação de interfaces de usuário no terminal (TUI). Ele não foi projetado para ser lucrativo, mas sim para ser uma ferramenta educacional e um gadget de dados divertido.

### Funcionalidades

* **Painel Visual Moderno:** Exibe estatísticas em tempo real, incluindo:
    * Hashrate dinâmico (via API do minerador)
    * Temperatura da CPU do Raspberry Pi
    * Uptime do serviço
    * Altura do bloco atual da rede Bitcoin
* **Backend de Mineração:** Utiliza o `cpuminer-opt` com sua API JSON ativada.
* **Serviço Automatizado:** Roda como um serviço `systemd`, iniciando automaticamente com o sistema e garantindo persistência.

## Instalação

Testado em um Raspberry Pi 3B+ com DietPi (baseado em Debian Bookworm).

### 1. Clonando o Repositório
```bash
git clone [https://github.com/eibragaa/PiMainer.git](https://github.com/eibragaa/PiMainer.git)
cd PiMainer
```

### 2. Instalando Dependências

**a) Dependências do sistema e de compilação:**
```bash
sudo apt-get update
sudo apt-get install -y git build-essential automake autoconf pkg-config libcurl4-openssl-dev libjansson-dev libssl-dev libgmp-dev zlib1g-dev python3-rich tmux
```

**b) O Minerador `cpuminer-opt`:**
O projeto usa um diretório irmão para o minerador.
```bash
cd .. # Volta para /root
git clone [https://github.com/JayDDee/cpuminer-opt.git](https://github.com/JayDDee/cpuminer-opt.git)
cd cpuminer-opt
./build.sh
cd ../PiMainer # Volta para o diretório do nosso projeto
```

### 3. Configuração

**a) Configure seu endereço de carteira:**
Edite o script de inicialização para inserir seu endereço de carteira Bitcoin.
```bash
nano start_pimainer.sh
```
Na linha `MINER_CMD`, substitua `SEU_ENDERECO_DE_CARTEIRA_BTC_AQUI` pelo seu endereço real. Salve e saia.

**b) Torne os scripts executáveis:**
```bash
chmod +x start_pimainer.sh
chmod +x pimainer_display.py 
```

**c) Configure o serviço `systemd`:**
Copie o arquivo de serviço para o diretório do systemd, recarregue e habilite.
```bash
sudo cp pimainer.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pimainer.service
```

### 4. Uso

Inicie o serviço (ou reinicie o Pi):
```bash
sudo systemctl start pimainer.service
```
Para visualizar o painel, anexe-se à sessão `tmux`:
```bash
tmux attach -t nerdminer
```
* `CTRL+B` + `N` para alternar para a janela do painel.
* `CTRL+B` + `D` para desanexar e deixar rodando em segundo plano.

## Agradecimentos
* **cpuminer-opt** por JayDDee e contribuidores.
* Biblioteca **Rich** por Will McGugan.
* APIs públicas de **mempool.space** e **CoinGecko**.
