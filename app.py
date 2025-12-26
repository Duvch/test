#!/usr/bin/env python3
"""
Web interface to execute Slashy keyboard shortcut tests
"""

from flask import Flask, render_template_string, jsonify
import subprocess
import json
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slashy Test Runner</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #fff;
            border-radius: 16px;
            padding: 40px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #1a1a2e;
            margin-bottom: 10px;
            font-size: 2rem;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .run-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 16px 40px;
            font-size: 1.1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        .run-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .run-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .results {
            margin-top: 30px;
            display: none;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #1a1a2e;
        }
        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }
        .stat.passed .stat-value { color: #28a745; }
        .stat.failed .stat-value { color: #dc3545; }
        .stat.partial .stat-value { color: #ffc107; }
        .test-list {
            background: #1a1a2e;
            border-radius: 8px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
        }
        .test-item {
            display: flex;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #2a2a4e;
            color: #fff;
        }
        .test-item:last-child {
            border-bottom: none;
        }
        .test-status {
            width: 30px;
            font-size: 1.2rem;
        }
        .test-shortcut {
            width: 120px;
            font-family: monospace;
            color: #667eea;
        }
        .test-desc {
            flex: 1;
            color: #aaa;
        }
        .test-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .badge-pass { background: #28a745; color: white; }
        .badge-fail { background: #dc3545; color: white; }
        .badge-partial { background: #ffc107; color: #1a1a2e; }
        .status-bar {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .status-ready { background: #d4edda; color: #155724; }
        .status-functional { background: #fff3cd; color: #856404; }
        .status-needs-work { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Slashy Test Runner</h1>
        <p class="subtitle">Automated keyboard shortcut testing for Slashy Mail</p>

        <button class="run-btn" onclick="runTests()">
            <span class="spinner" id="spinner"></span>
            <span id="btn-text">Run Tests</span>
        </button>

        <div class="results" id="results">
            <div class="status-bar" id="status-bar"></div>

            <div class="summary" id="summary"></div>

            <div class="test-list" id="test-list"></div>
        </div>
    </div>

    <script>
        async function runTests() {
            const btn = document.querySelector('.run-btn');
            const spinner = document.getElementById('spinner');
            const btnText = document.getElementById('btn-text');
            const results = document.getElementById('results');

            btn.disabled = true;
            spinner.style.display = 'block';
            btnText.textContent = 'Running...';

            try {
                const response = await fetch('/run-tests');
                const data = await response.json();

                displayResults(data);
                results.style.display = 'block';
            } catch (error) {
                alert('Error running tests: ' + error.message);
            } finally {
                btn.disabled = false;
                spinner.style.display = 'none';
                btnText.textContent = 'Run Tests Again';
            }
        }

        function displayResults(data) {
            const summary = data.summary;
            const tests = data.test_results;

            // Status bar
            const statusBar = document.getElementById('status-bar');
            let statusClass, statusText;
            if (summary.pass_rate >= 80) {
                statusClass = 'status-ready';
                statusText = '✓ PRODUCTION READY';
            } else if (summary.pass_rate >= 60) {
                statusClass = 'status-functional';
                statusText = '⚠ MOSTLY FUNCTIONAL';
            } else {
                statusClass = 'status-needs-work';
                statusText = '✗ NEEDS IMPROVEMENT';
            }
            statusBar.className = 'status-bar ' + statusClass;
            statusBar.textContent = statusText + ' - ' + summary.pass_rate.toFixed(1) + '% Pass Rate';

            // Summary stats
            document.getElementById('summary').innerHTML = `
                <div class="stat">
                    <div class="stat-value">${summary.total_tests}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat passed">
                    <div class="stat-value">${summary.passed}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat failed">
                    <div class="stat-value">${summary.failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat partial">
                    <div class="stat-value">${summary.partial}</div>
                    <div class="stat-label">Partial</div>
                </div>
            `;

            // Test list
            const testList = document.getElementById('test-list');
            testList.innerHTML = tests.map(test => {
                let icon, badgeClass;
                if (test.status === 'PASS') {
                    icon = '✓';
                    badgeClass = 'badge-pass';
                } else if (test.status === 'FAIL') {
                    icon = '✗';
                    badgeClass = 'badge-fail';
                } else {
                    icon = '⚠';
                    badgeClass = 'badge-partial';
                }
                return `
                    <div class="test-item">
                        <span class="test-status">${icon}</span>
                        <span class="test-shortcut">${test.shortcut}</span>
                        <span class="test-desc">${test.description}</span>
                        <span class="test-badge ${badgeClass}">${test.status}</span>
                    </div>
                `;
            }).join('');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run-tests')
def run_tests():
    # Run the test script
    script_path = os.path.join(os.path.dirname(__file__), 'slashy_test.py')
    subprocess.run(['python3', script_path], capture_output=True)

    # Read the generated report
    report_path = os.path.join(os.path.dirname(__file__), 'slashy_test_report.json')
    with open(report_path, 'r') as f:
        report = json.load(f)

    return jsonify(report)

if __name__ == '__main__':
    print("Starting Slashy Test Runner...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
