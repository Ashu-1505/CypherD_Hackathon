# CypherD Hackathon - Mock Web3 Wallet

A simple **Web3 wallet simulation** built with **React (frontend)**, **Flask (backend)**, and **Supabase (PostgreSQL)**.  
This project allows users to create/import wallets, view balances, send mock ETH, and see transaction history.

---

## 🛠 Tech Stack

- **Frontend:** React, Axios, TailwindCSS (optional)  
- **Backend:** Python, Flask, Flask-CORS  
- **Database:** Supabase PostgreSQL  
- **Extras:** Axios for API calls, Digital signatures simulated for transfers  

---

## 📦 Features

1. **Create Wallet**  
   - Generate a new 12-word mnemonic phrase.  
   - Derive a unique Ethereum address.  
   - Store wallet in Supabase with initial mock ETH balance.

2. **Import Wallet**  
   - Retrieve wallet using a known 12-word mnemonic phrase.  

3. **View Balance**  
   - Display current mock ETH balance for the wallet.

4. **Send Mock ETH**  
   - Send ETH to another wallet address.  
   - Supports ETH and USD input (ETH conversion can be added later).  
   - Simulates digital signature verification.

5. **Transaction History**  
   - View past transactions (sender, recipient, amount, timestamp).

---

## ⚡ Setup Instructions

### 1. Clone Repository


git clone https://github.com/<your-username>/CypherD_Hackathon.git
cd CypherD_Hackathon


# Creating the Wallet by 12 word mnemonic.
<img width="1440" height="900" alt="Screenshot 2025-10-05 at 2 10 10 PM" src="https://github.com/user-attachments/assets/e99e83a0-838c-4e80-8e6c-a1d7f29f3896" />
<img width="1440" height="900" alt="Screenshot 2025-10-05 at 2 09 55 PM" src="https://github.com/user-attachments/assets/49a9a4f9-1bcc-4589-8fa8-e4272ab19818" />
<img width="1440" height="900" alt="Screenshot 2025-10-05 at 2 09 46 PM" src="https://github.com/user-attachments/assets/9f61e847-7483-451c-add3-37d6c629e003" />
<img width="1440" height="813" alt="Screenshot 2025-10-05 at 2 09 38 PM" src="https://github.com/user-attachments/assets/4adc3ffa-67d1-4687-a5d7-aa8983a0b2b6" />

Chnages in the Supabase
<img width="1440" height="900" alt="Screenshot 2025-10-05 at 2 27 00 PM" src="https://github.com/user-attachments/assets/9993f739-726b-4cce-a52c-64885f9d0df7" />
