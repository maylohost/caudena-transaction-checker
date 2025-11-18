#!/usr/bin/env python3
"""
Script CLI per verificare transazioni blockchain usando l'API Caudena
Uso:
    python check_transaction.py --hash <hash> --currency btc
    python check_transaction.py --address <address> --currency btc
"""

import os
import sys
import base64
import argparse
from datetime import datetime, timedelta
import jwt
import requests
from typing import Optional, Dict, Any

# Base URL dell'API
API_BASE_URL = "https://prism-api.caudena.com"

def load_env_file(filepath: str) -> Dict[str, str]:
    """Carica variabili da un file .env"""
    env_vars = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    # Ignora commenti e righe vuote
                    if not line or line.startswith('#'):
                        continue
                    
                    # Supporta diversi formati: KEY=value, KEY:value, KEY = value, export KEY=value
                    separator = '=' if '=' in line else ':' if ':' in line else None
                    if separator:
                        # Rimuovi 'export' se presente
                        line = line.replace('export ', '').strip()
                        parts = line.split(separator, 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            # Rimuovi quote se presenti
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            elif value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]
                            env_vars[key] = value
        except Exception as e:
            print(f"⚠️  Avviso: Errore nel leggere {filepath} (riga {line_num}): {e}")
    return env_vars

def get_api_credentials() -> tuple[str, str]:
    """Recupera le credenziali API da .env o variabili d'ambiente"""
    # Cerca file .env nella directory corrente
    env_files = ['.env', '.env.local', os.path.join(os.path.dirname(__file__), '.env')]
    env_vars = {}
    
    for env_file in env_files:
        if os.path.exists(env_file):
            env_vars = load_env_file(env_file)
            if env_vars:
                break
    
    # Prova diverse varianti di nomi delle chiavi
    kid = (os.getenv("CAUDENA_KID") or 
           env_vars.get("CAUDENA_KID") or 
           env_vars.get("id_caudena") or
           env_vars.get("KID") or
           env_vars.get("API_KID") or
           env_vars.get("CAUDENA_API_KID"))
    
    secret = (os.getenv("CAUDENA_SECRET") or 
              env_vars.get("CAUDENA_SECRET") or 
              env_vars.get("secret") or
              env_vars.get("SECRET") or
              env_vars.get("API_SECRET") or
              env_vars.get("CAUDENA_API_SECRET"))
    
    if not kid:
        print("❌ Errore: CAUDENA_KID non trovato")
        print("   Configura le credenziali in:")
        print("   - Variabili d'ambiente: CAUDENA_KID e CAUDENA_SECRET")
        print("   - File .env nella directory corrente")
        print("   - File .env.local nella directory corrente")
        sys.exit(1)
    
    if not secret:
        print("❌ Errore: CAUDENA_SECRET non trovato")
        print("   Configura le credenziali in:")
        print("   - Variabili d'ambiente: CAUDENA_KID e CAUDENA_SECRET")
        print("   - File .env nella directory corrente")
        print("   - File .env.local nella directory corrente")
        sys.exit(1)
    
    return kid, secret

def generate_jwt_token(kid: str, secret_b64: str) -> str:
    """Genera un token JWT per l'autenticazione"""
    try:
        # Decodifica il secret da base64
        secret = base64.b64decode(secret_b64)
    except Exception as e:
        print(f"❌ Errore nel decodificare il secret: {e}")
        sys.exit(1)
    
    # Crea il payload con exp di 5 minuti
    payload = {
        "kid": kid,
        "exp": int((datetime.now() + timedelta(minutes=5)).timestamp())
    }
    
    # Genera il token
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def make_api_request(method: str, endpoint: str, token: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Esegue una richiesta API"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    if data:
        headers["Content-Type"] = "application/json"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        else:
            raise ValueError(f"Metodo non supportato: {method}")
        
        # Mostra dettagli dell'errore se presente
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"❌ Errore HTTP {response.status_code}: {error_data}")
            except:
                print(f"❌ Errore HTTP {response.status_code}: {response.text}")
            sys.exit(1)
        
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ Errore HTTP: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Dettagli: {e.response.text}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore nella richiesta: {e}")
        sys.exit(1)

def check_transaction_by_hash(currency: str, tx_hash: str, token: str):
    """Verifica una transazione tramite hash"""
    print(f"\n🔍 Verifica transazione: {tx_hash}")
    print(f"   Currency: {currency.upper()}\n")
    
    endpoint = f"/v2/{currency}/transaction/{tx_hash}"
    try:
        result = make_api_request("GET", endpoint, token)
        
        if result.get("status"):
            data = result.get("data", {})
            if data:
                print_transaction_details(data)
            else:
                print("❌ Nessun dato nella risposta")
                print(f"   Risposta completa: {result}")
        else:
            print("❌ Transazione non trovata o errore nella risposta")
            print(f"   Risposta: {result}")
    except SystemExit:
        pass
    except Exception as e:
        print(f"❌ Errore imprevisto: {e}")

def check_transaction_by_address(currency: str, address: str, token: str):
    """Verifica transazioni tramite indirizzo"""
    print(f"\n🔍 Verifica indirizzo: {address}")
    print(f"   Currency: {currency.upper()}\n")
    
    # Prima recupera le statistiche dell'indirizzo
    endpoint_stats = f"/v2/{currency}/address/stats/{address}"
    stats_result = make_api_request("GET", endpoint_stats, token)
    
    if stats_result.get("status"):
        print_address_stats(stats_result.get("data", {}))
    
    # Poi recupera le transazioni (prime 5)
    print("\n" + "="*80)
    print("📋 Ultime transazioni (prime 5):")
    print("="*80 + "\n")
    
    endpoint_tx = f"/v2/{currency}/address/transactions/{address}"
    tx_data = {
        "page": 1,
        "sort_by": "time",
        "sort_order": "desc"
    }
    tx_result = make_api_request("POST", endpoint_tx, token, tx_data)
    
    if tx_result.get("status"):
        transactions = tx_result.get("data", [])[:5]
        pagination = tx_result.get("pagination", {})
        
        print(f"Totale transazioni: {pagination.get('total_entries', 0)}\n")
        
        for i, tx in enumerate(transactions, 1):
            print(f"--- Transazione {i} ---")
            print_transaction_summary(tx)
            print()
    else:
        print("❌ Nessuna transazione trovata")

def print_transaction_details(data: Dict):
    """Stampa i dettagli completi di una transazione"""
    print("="*80)
    print("📄 DETTAGLI TRANSAZIONE")
    print("="*80)
    
    print(f"\n🔹 Hash: {data.get('hash', 'N/A')}")
    print(f"🔹 Status: {'✅ Confermata' if data.get('status') else '⏳ In attesa'}")
    print(f"🔹 Currency: {data.get('currency', 'N/A').upper()}")
    print(f"🔹 Timestamp: {format_timestamp(data.get('time', 0))}")
    print(f"🔹 Block Height: {data.get('height', 'N/A')}")
    print(f"🔹 Confirmations: {data.get('confirmations', 0):,}")
    
    print(f"\n💰 Importi:")
    print(f"   Amount: {data.get('amount', 'N/A')}")
    print(f"   Amount USD: ${data.get('amount_usd', 0):,.2f}")
    print(f"   Fee: {data.get('fee', 'N/A')}")
    print(f"   Fee USD: ${data.get('fee_usd', 0):,.2f}")
    
    if data.get('gas'):
        print(f"   Gas: {data.get('gas', 'N/A')}")
        print(f"   Gas Used: {data.get('gas_used', 'N/A')}")
        print(f"   Gas Price: {data.get('gas_price', 'N/A')}")
    
    # Inputs
    if 'inputs' in data and data['inputs']:
        print(f"\n📥 Inputs ({len(data['inputs'])}):")
        for i, inp in enumerate(data['inputs'][:3], 1):
            addr = inp.get('address', 'N/A')
            amount = inp.get('amount', 0)
            amount_usd = inp.get('amount_usd', 0)
            score = inp.get('score', 'N/A')
            entity = inp.get('name', 'Unidentified')
            print(f"   {i}. {addr[:20]}... | {amount:,} | ${amount_usd:,.2f} | Score: {score} | {entity}")
        if len(data['inputs']) > 3:
            print(f"   ... e altri {len(data['inputs']) - 3} input")
    
    # Outputs
    if 'outputs' in data and data['outputs']:
        print(f"\n📤 Outputs ({len(data['outputs'])}):")
        for i, out in enumerate(data['outputs'][:3], 1):
            addr = out.get('address', 'N/A')
            amount = out.get('amount', 0)
            amount_usd = out.get('amount_usd', 0)
            score = out.get('score', 'N/A')
            entity = out.get('name', 'Unidentified')
            print(f"   {i}. {addr[:20]}... | {amount:,} | ${amount_usd:,.2f} | Score: {score} | {entity}")
        if len(data['outputs']) > 3:
            print(f"   ... e altri {len(data['outputs']) - 3} output")
    
    # Token transfers (per EVM)
    if 'tokens' in data and data['tokens']:
        print(f"\n🪙 Token Transfers ({len(data['tokens'])}):")
        for token in data['tokens'][:5]:
            token_info = token.get('token', {})
            value = token.get('value', 0)
            usd = token.get('usd', 0)
            symbol = token_info.get('symbol', 'N/A')
            name = token_info.get('name', 'N/A')
            scam = token_info.get('scam', False)
            spam = token_info.get('spam', False)
            
            warning = ""
            if scam or spam:
                warning = " ⚠️  SCAM/SPAM!"
            
            print(f"   {symbol} ({name}): {value:,} (${usd:,.2f}){warning}")
            
            sender = token.get('sender', {})
            receiver = token.get('receiver', {})
            if sender.get('address'):
                sender_addr = sender.get('address', 'N/A')
                sender_score = sender.get('score', 'N/A')
                sender_entity = sender.get('entity', {}).get('name', 'Unidentified') if sender.get('entity') else 'Unidentified'
                print(f"      From: {sender_addr[:20]}... (Score: {sender_score}, {sender_entity})")
            if receiver.get('address'):
                receiver_addr = receiver.get('address', 'N/A')
                receiver_score = receiver.get('score', 'N/A')
                receiver_entity = receiver.get('entity', {}).get('name', 'Unidentified') if receiver.get('entity') else 'Unidentified'
                print(f"      To: {receiver_addr[:20]}... (Score: {receiver_score}, {receiver_entity})")
    
    # Evidenzia contract malevoli
    print(f"\n⚠️  ANALISI CONTRACT:")
    malicious_found = False
    
    if 'inputs' in data and data['inputs']:
        for inp in data['inputs']:
            if inp.get('contract'):
                addr = inp.get('address', 'N/A')
                score = inp.get('score', 'N/A')
                entity = inp.get('name', 'Unidentified')
                if score and score < 4:
                    print(f"   ⚠️  CONTRACT SOSPETTO (Input): {addr}")
                    print(f"      Score: {score}/10 | Entity: {entity}")
                    malicious_found = True
    
    if 'outputs' in data and data['outputs']:
        for out in data['outputs']:
            if out.get('contract'):
                addr = out.get('address', 'N/A')
                score = out.get('score', 'N/A')
                entity = out.get('name', 'Unidentified')
                if score and score < 4:
                    print(f"   ⚠️  CONTRACT SOSPETTO (Output): {addr}")
                    print(f"      Score: {score}/10 | Entity: {entity}")
                    malicious_found = True
    
    if not malicious_found:
        print("   ✅ Nessun contract sospetto rilevato")
    
    print("\n" + "="*80)

def print_transaction_summary(tx: Dict):
    """Stampa un riepilogo breve di una transazione"""
    print(f"Hash: {tx.get('hash', 'N/A')[:20]}...")
    print(f"Time: {format_timestamp(tx.get('time', 0))}")
    print(f"Direction: {tx.get('direction', 'N/A')}")
    print(f"Amount: {tx.get('total_out' if tx.get('direction') == 'out' else 'total_in', 0):,}")
    print(f"Amount USD: ${tx.get('total_out_usd' if tx.get('direction') == 'out' else 'total_in_usd', 0):,.2f}")
    print(f"Fee: {tx.get('fee', 0):,} (${tx.get('fee_usd', 0):,.2f})")
    print(f"Confirmations: {tx.get('confirmations', 0):,}")

def print_address_stats(data: Dict):
    """Stampa le statistiche di un indirizzo"""
    print("="*80)
    print("📊 STATISTICHE INDIRIZZO")
    print("="*80)
    
    address = data.get('address', 'N/A')
    print(f"\n🔹 Address: {address}")
    
    balance = data.get('balance', {})
    print(f"\n💰 Balance:")
    print(f"   Current: {balance.get('balance', 0):,.8f} {data.get('blockchain', '').upper()}")
    print(f"   Total In: {balance.get('total_in', 0):,.8f}")
    print(f"   Total Out: {balance.get('total_out', 0):,.8f}")
    
    balance_usd = data.get('balance_usd', {})
    print(f"\n💰 Balance USD:")
    print(f"   Current: ${balance_usd.get('balance', 0):,.2f}")
    print(f"   Total In: ${balance_usd.get('total_in', 0):,.2f}")
    print(f"   Total Out: ${balance_usd.get('total_out', 0):,.2f}")
    
    trx_count = data.get('trx_count', {})
    print(f"\n📊 Transazioni:")
    print(f"   Incoming: {trx_count.get('in', 0):,}")
    print(f"   Outgoing: {trx_count.get('out', 0):,}")
    
    entity = data.get('entity')
    if entity:
        print(f"\n🏢 Entity:")
        print(f"   Name: {entity.get('name', 'N/A')}")
        print(f"   Category: {entity.get('category', 'N/A')}")
    
    print(f"\n🔹 Score: {data.get('score', 'N/A')}/10")
    print(f"🔹 First Seen: {format_timestamp(data.get('first_seen', 0))}")
    print(f"🔹 Last Seen: {format_timestamp(data.get('last_seen', 0))}")

def format_timestamp(timestamp: int) -> str:
    """Formatta un timestamp Unix in formato leggibile"""
    if not timestamp:
        return "N/A"
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        return str(timestamp)

def main():
    parser = argparse.ArgumentParser(
        description="Verifica transazioni blockchain usando l'API Caudena",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  # Verifica transazione per hash
  python check_transaction.py --hash 0000000000000000000000000000000000000000000000000000000000000000 --currency btc

  # Verifica indirizzo
  python check_transaction.py --address xxxxxx --currency btc

Per maggiori informazioni, visita: https://docs.caudena.com
        """
    )
    
    parser.add_argument(
        "--hash",
        type=str,
        help="Hash della transazione da verificare"
    )
    
    parser.add_argument(
        "--address",
        type=str,
        help="Indirizzo blockchain da verificare"
    )
    
    parser.add_argument(
        "--currency",
        type=str,
        default="btc",
        choices=["btc", "eth", "ltc", "doge", "trx", "bnb"],
        help="Currency/blockchain (default: btc). Supportate: btc, eth, ltc, doge, trx, bnb"
    )
    
    args = parser.parse_args()
    
    if not args.hash and not args.address:
        parser.error("Devi fornire --hash o --address")
    
    if args.hash and args.address:
        parser.error("Fornisci solo --hash O --address, non entrambi")
    
    print("🔐 Autenticazione...")
    kid, secret = get_api_credentials()
    token = generate_jwt_token(kid, secret)
    print("✅ Token generato con successo\n")
    
    if args.hash:
        check_transaction_by_hash(args.currency, args.hash, token)
    elif args.address:
        check_transaction_by_address(args.currency, args.address, token)

if __name__ == "__main__":
    main()

