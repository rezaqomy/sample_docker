const donateBtn = document.getElementById('donateBtn');
const amountInput = document.getElementById('amount');
const totalAmountElement = document.getElementById('totalAmount');
const messageElement = document.getElementById('message');

function formatNumber(num) {
    return new Intl.NumberFormat('fa-IR'). format(num);
}

async function loadTotal() {
    try {
        const response = await fetch('/api/total');
        const data = await response.json();
        totalAmountElement.textContent = `${formatNumber(data.total)} ریال`;
    } catch (error) {
        console. error('Error loading total:', error);
    }
}

function showMessage(text, type) {
    messageElement.textContent = text;
    messageElement. className = `message ${type}`;
    messageElement.style.display = 'block';
}

function checkUrlParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const status = urlParams.get('status');
    const refId = urlParams.get('ref_id');
    const message = urlParams.get('message');
    
    if (status === 'success') {
        showMessage(`✅ پرداخت با موفقیت انجام شد! کد پیگیری: ${refId}`, 'success');
        loadTotal();
    } else if (status === 'error') {
        showMessage(`❌ پرداخت ناموفق بود. ${message || ''}`, 'error');
    }
    
    if (status) {
        window.history.replaceState({}, document.title, '/');
    }
}

donateBtn.addEventListener('click', async () => {
    const amount = parseInt(amountInput.value);
    
    if (! amount || amount < 10000) {
        showMessage('مبلغ باید حداقل ۱۰,۰۰۰ ریال باشد', 'error');
        return;
    }

        if (! amount || amount > 2000000000) {
        showMessage('مبلغ باید حداکثر ۲,۰۰۰,۰۰۰,۰۰۰ ریال باشد  ', 'error');
        return;
    }

    
    donateBtn.disabled = true;
    donateBtn.textContent = '⏳ در حال انتقال...';
    
    try {
        const response = await fetch('/api/donate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: amount.toString() 
        });
        
        const data = await response.json();
        
        if (response.ok && data.payment_url) {
            window.location.href = data.payment_url;
        } else {
            showMessage('خطا در ایجاد درخواست پرداخت', 'error');
            donateBtn.disabled = false;
            donateBtn.textContent = '💸 پول زور بدید';
        }
    } catch (error) {
        showMessage('خطا در برقراری ارتباط', 'error');
        donateBtn.disabled = false;
        donateBtn.textContent = '💸 پول زور بدید';
    }
});

loadTotal();
checkUrlParams();
