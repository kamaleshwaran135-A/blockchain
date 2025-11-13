from flask import Flask, render_template_string, request, jsonify
import hashlib

app = Flask(__name__)

# ----- Blockchain Data Structures -----
stack = []        # LIFO structure
hash_map = {}     # Key: hash, Value: data


# ----- Hash Function -----
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


# ----- HTML Template -----
html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blockchain Transaction Validator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef3f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: white;
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px #ccc;
            width: 420px;
            text-align: center;
        }
        input {
            padding: 8px;
            width: 70%;
            margin-right: 5px;
        }
        button {
            padding: 8px 15px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        ul { list-style: none; padding: 0; }
        li {
            background: #e9ecef;
            margin: 5px;
            padding: 8px;
            border-radius: 5px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Blockchain Validator</h1>

        <form id="transactionForm">
            <input type="text" id="transactionData" placeholder="Enter transaction (e.g., Alice pays Bob 10 BTC)" required>
            <button type="submit">Add</button>
        </form>

        <button id="validateBtn">Validate Blockchain</button>
        <button id="tamperBtn">Tamper Blockchain</button>
        <button id="resetBtn">Reset</button>

        <h3>Transaction Stack</h3>
        <ul id="transactionList"></ul>

        <h3>Validation Result:</h3>
        <p id="result"></p>
    </div>

    <script>
        const form = document.getElementById('transactionForm');
        const list = document.getElementById('transactionList');
        const result = document.getElementById('result');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = document.getElementById('transactionData').value;

            const response = await fetch('/add', {
                method: 'POST',
                body: new URLSearchParams({ transaction: data }),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            const res = await response.json();
            displayTransactions(res.transactions);
            result.textContent = res.message;
            document.getElementById('transactionData').value = '';
        });

        document.getElementById('validateBtn').addEventListener('click', async () => {
            const response = await fetch('/validate');
            const res = await response.json();
            result.textContent = res.valid ? "✅ Blockchain is VALID" : "❌ Blockchain is INVALID";
        });

        document.getElementById('tamperBtn').addEventListener('click', async () => {
            const response = await fetch('/tamper');
            const res = await response.json();
            displayTransactions(res.transactions);
            result.textContent = "⚠️ Blockchain data has been tampered!";
        });

        document.getElementById('resetBtn').addEventListener('click', async () => {
            const response = await fetch('/reset');
            const res = await response.json();
            list.innerHTML = '';
            result.textContent = res.message;
        });

        function displayTransactions(transactions) {
            list.innerHTML = '';
            transactions.forEach(tx => {
                const li = document.createElement('li');
                li.textContent = `Data: ${tx.data} | Hash: ${tx.hash.substring(0,15)}...`;
                list.appendChild(li);
            });
        }
    </script>
</body>
</html>
"""

# ----- Routes -----
@app.route('/')
def home():
    return render_template_string(html_page)


@app.route('/add', methods=['POST'])
def add_transaction():
    data = request.form['transaction']
    hash_val = generate_hash(data)
    stack.append({'data': data, 'hash': hash_val})
    hash_map[hash_val] = data
    return jsonify({
        'message': 'Transaction added successfully!',
        'transactions': list(reversed(stack))
    })


@app.route('/validate', methods=['GET'])
def validate_blockchain():
    # Check every transaction for integrity
    valid = True
    for tx in stack:
        recalculated_hash = generate_hash(tx['data'])
        if recalculated_hash != tx['hash']:
            valid = False
            break
    return jsonify({'valid': valid})


@app.route('/tamper', methods=['GET'])
def tamper_blockchain():
    # Simulate tampering (change one transaction)
    if stack:
        stack[0]['data'] = stack[0]['data'] + " (tampered)"
    return jsonify({'transactions': list(reversed(stack))})


@app.route('/reset', methods=['GET'])
def reset_blockchain():
    stack.clear()
    hash_map.clear()
    return jsonify({'message': 'Blockchain reset successfully!'})


# ----- Run App -----
if __name__ == '__main__':
    app.run(debug=True)
