```
███╗   ███╗ █████╗ ██╗   ██╗██╗      ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
████╗ ████║██╔══██╗╚██╗ ██╔╝██║     ██╔═══██╗██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
██╔████╔██║███████║ ╚████╔╝ ██║     ██║   ██║███████║██║   ██║███████╗   ██║   
██║╚██╔╝██║██╔══██║  ╚██╔╝  ██║     ██║   ██║██╔══██║██║   ██║╚════██║   ██║   
██║ ╚═╝ ██║██║  ██║   ██║   ███████╗╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   
╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
```
# Caudena Transaction Checker

**🇮🇹 [Italiano](#italiano) | 🇬🇧 [English](#english)**

---

## 🇮🇹 Italiano

# Caudena Transaction Checker

Script CLI Python per verificare transazioni blockchain e analizzare indirizzi usando l'API [Caudena](https://caudena.com).

## 🚀 Caratteristiche

- ✅ Verifica transazioni per hash
- ✅ Analisi completa di indirizzi blockchain
- ✅ Supporto per multiple blockchain (BTC, ETH, LTC, DOGE, TRX, BNB)
- ✅ Analisi di rischio con score dettagliati
- ✅ Rilevamento di contract sospetti/malevoli
- ✅ Analisi di token transfers (EVM)
- ✅ Statistiche complete degli indirizzi

## 📋 Requisiti

- Python 3.8+
- Account Caudena con API key
- Credenziali API (Key ID e Secret)

## 🔧 Installazione

1. **Clona il repository:**
```bash
git clone https://github.com/tuonome/caudena-transaction-checker.git
cd caudena-transaction-checker
```

2. **Installa le dipendenze:**
```bash
pip install -r requirements.txt
```

3. **Configura le credenziali API:**

Crea un file `.env` nella directory del progetto:

```bash
cp .env.example .env
```

Modifica il file `.env` con le tue credenziali:

```env
CAUDENA_KID=your-key-id-here
CAUDENA_SECRET=your-secret-base64-here
```

**Oppure** imposta le variabili d'ambiente:

```bash
export CAUDENA_KID="your-key-id-here"
export CAUDENA_SECRET="your-secret-base64-here"
```

### Come ottenere le credenziali API

1. Accedi al tuo account [Caudena](https://caudena.com)
2. Vai su **Settings → API**
3. Genera una nuova API key
4. Copia il **Key ID (kid)** e il **Secret** (in formato base64)

## 📖 Utilizzo

### Verifica transazione per hash

```bash
python check_transaction.py --hash <hash> --currency <currency>
```

**Esempi:**

```bash
# Bitcoin
python check_transaction.py --hash 0000000000000000000000000000000000000000000000000000000000000000 --currency btc

# Ethereum
python check_transaction.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000 --currency eth
```

### Verifica indirizzo

```bash
python check_transaction.py --address <address> --currency <currency>
```

**Esempi:**

```bash
# Bitcoin
python check_transaction.py --address xxxx --currency btc

# Ethereum
python check_transaction.py --address 0x0000000000000000000000000000000000000000 --currency eth
```

### Blockchain supportate

- `btc` - Bitcoin
- `eth` - Ethereum
- `ltc` - Litecoin
- `doge` - Dogecoin
- `trx` - Tron
- `bnb` - Binance Smart Chain

## 📊 Output

Lo script mostra informazioni dettagliate:

### Per le transazioni:
- Hash, status, timestamp, conferme
- Importi in crypto e USD
- Fee e gas (per EVM)
- Input e output con score di rischio
- Token transfers (per EVM)
- Analisi di contract sospetti

### Per gli indirizzi:
- Statistiche complete (balance, total in/out)
- Numero di transazioni
- Entity associata (se identificata)
- Score di rischio (1-10)
- Prime 5 transazioni recenti

## 🔍 Esempi di Output

### Transazione Bitcoin

```
================================================================================
📄 DETTAGLI TRANSAZIONE
================================================================================

🔹 Hash: 0000000000000000000000000000000000000000000000000000000000000000
🔹 Status: ✅ Confermata
🔹 Currency: BTC
🔹 Timestamp: 2024-01-01 00:00:00 UTC
🔹 Confirmations: 1000

💰 Importi:
   Amount: N/A
   Amount USD: $0.00
   Fee: 1000
   Fee USD: $0.50

📥 Inputs (2):
   1. bc1qxxxxxxxxxxxxxxxxxxxxx... | 100,000 | $50.00 | Score: 8.0 | None
   ...

📤 Outputs (1):
   1. bc1qyyyyyyyyyyyyyyyyyyyyy... | 99,000 | $49.50 | Score: 7.5 | None

⚠️  ANALISI CONTRACT:
   ✅ Nessun contract sospetto rilevato
```

### Indirizzo Ethereum

```
================================================================================
📊 STATISTICHE INDIRIZZO
================================================================================

🔹 Address: 0x0000000000000000000000000000000000000000

💰 Balance:
   Current: 0.00100000 ETH
   Total In: 1.00000000
   Total Out: 0.99900000

💰 Balance USD:
   Current: $2.50
   Total In: $2,500.00
   Total Out: $2,497.50

📊 Transazioni:
   Incoming: 5
   Outgoing: 3

🔹 Score: 7.5/10
🔹 First Seen: 2024-01-01 00:00:00 UTC
🔹 Last Seen: 2024-12-31 23:59:59 UTC
```

## 🛡️ Sicurezza

- ⚠️ **NON committare** il file `.env` nel repository
- ⚠️ **NON condividere** le tue credenziali API
- ✅ Il file `.env` è già incluso nel `.gitignore`
- ✅ Le credenziali vengono caricate solo localmente

## 📚 Documentazione API

Per maggiori informazioni sull'API Caudena, consulta la [documentazione ufficiale](https://docs.caudena.com).

## 🤝 Contribuire

Contributi sono benvenuti! Per favore:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## ⚠️ Disclaimer

Questo strumento è fornito "così com'è" senza garanzie di alcun tipo. L'uso di questo strumento è a proprio rischio.

## 🙏 Ringraziamenti

- [Caudena](https://caudena.com) per l'API e i servizi di analisi blockchain
- La comunità open source per il supporto

## 📧 Supporto

Per problemi o domande:
- Apri una [Issue](https://github.com/tuonome/caudena-transaction-checker/issues)
- Consulta la [documentazione Caudena](https://docs.caudena.com)

---

## 🇬🇧 English

# Caudena Transaction Checker

Python CLI script to verify blockchain transactions and analyze addresses using the [Caudena](https://caudena.com) API.

## 🚀 Features

- ✅ Verify transactions by hash
- ✅ Complete blockchain address analysis
- ✅ Support for multiple blockchains (BTC, ETH, LTC, DOGE, TRX, BNB)
- ✅ Risk analysis with detailed scores
- ✅ Detection of suspicious/malicious contracts
- ✅ Token transfers analysis (EVM)
- ✅ Complete address statistics

## 📋 Requirements

- Python 3.8+
- Caudena account with API key
- API credentials (Key ID and Secret)

## 🔧 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/tuonome/caudena-transaction-checker.git
cd caudena-transaction-checker
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API credentials:**

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```env
CAUDENA_KID=your-key-id-here
CAUDENA_SECRET=your-secret-base64-here
```

**Or** set environment variables:

```bash
export CAUDENA_KID="your-key-id-here"
export CAUDENA_SECRET="your-secret-base64-here"
```

### How to get API credentials

1. Log in to your [Caudena](https://caudena.com) account
2. Go to **Settings → API**
3. Generate a new API key
4. Copy the **Key ID (kid)** and **Secret** (base64 format)

## 📖 Usage

### Verify transaction by hash

```bash
python check_transaction.py --hash <hash> --currency <currency>
```

**Examples:**

```bash
# Bitcoin
python check_transaction.py --hash 0000000000000000000000000000000000000000000000000000000000000000 --currency btc

# Ethereum
python check_transaction.py --hash 0x0000000000000000000000000000000000000000000000000000000000000000 --currency eth
```

### Verify address

```bash
python check_transaction.py --address <address> --currency <currency>
```

**Examples:**

```bash
# Bitcoin
python check_transaction.py --address xxxx --currency btc

# Ethereum
python check_transaction.py --address 0x0000000000000000000000000000000000000000 --currency eth
```

### Supported blockchains

- `btc` - Bitcoin
- `eth` - Ethereum
- `ltc` - Litecoin
- `doge` - Dogecoin
- `trx` - Tron
- `bnb` - Binance Smart Chain

## 📊 Output

The script displays detailed information:

### For transactions:
- Hash, status, timestamp, confirmations
- Amounts in crypto and USD
- Fees and gas (for EVM)
- Inputs and outputs with risk scores
- Token transfers (for EVM)
- Suspicious contract analysis

### For addresses:
- Complete statistics (balance, total in/out)
- Number of transactions
- Associated entity (if identified)
- Risk score (1-10)
- Last 5 recent transactions

## 🔍 Output Examples

### Bitcoin Transaction

```
================================================================================
📄 TRANSACTION DETAILS
================================================================================

🔹 Hash: 0000000000000000000000000000000000000000000000000000000000000000
🔹 Status: ✅ Confirmed
🔹 Currency: BTC
🔹 Timestamp: 2024-01-01 00:00:00 UTC
🔹 Confirmations: 1000

💰 Amounts:
   Amount: N/A
   Amount USD: $0.00
   Fee: 1000
   Fee USD: $0.50

📥 Inputs (2):
   1. bc1qxxxxxxxxxxxxxxxxxxxxx... | 100,000 | $50.00 | Score: 8.0 | None
   ...

📤 Outputs (1):
   1. bc1qyyyyyyyyyyyyyyyyyyyyy... | 99,000 | $49.50 | Score: 7.5 | None

⚠️  CONTRACT ANALYSIS:
   ✅ No suspicious contracts detected
```

### Ethereum Address

```
================================================================================
📊 ADDRESS STATISTICS
================================================================================

🔹 Address: 0x0000000000000000000000000000000000000000

💰 Balance:
   Current: 0.00100000 ETH
   Total In: 1.00000000
   Total Out: 0.99900000

💰 Balance USD:
   Current: $2.50
   Total In: $2,500.00
   Total Out: $2,497.50

📊 Transactions:
   Incoming: 5
   Outgoing: 3

🔹 Score: 7.5/10
🔹 First Seen: 2024-01-01 00:00:00 UTC
🔹 Last Seen: 2024-12-31 23:59:59 UTC
```

## 🛡️ Security

- ⚠️ **DO NOT commit** the `.env` file to the repository
- ⚠️ **DO NOT share** your API credentials
- ✅ The `.env` file is already included in `.gitignore`
- ✅ Credentials are loaded only locally

## 📚 API Documentation

For more information about the Caudena API, see the [official documentation](https://docs.caudena.com).

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is released under the MIT License. See the `LICENSE` file for more details.

## ⚠️ Disclaimer

This tool is provided "as is" without warranty of any kind. Use of this tool is at your own risk.

## 🙏 Acknowledgments

- [Caudena](https://caudena.com) for the API and blockchain analysis services
- The open source community for support

## 📧 Support

For issues or questions:
- Open an [Issue](https://github.com/tuonome/caudena-transaction-checker/issues)
- Check the [Caudena documentation](https://docs.caudena.com)

---

**Made with ❤️ for the blockchain community**
