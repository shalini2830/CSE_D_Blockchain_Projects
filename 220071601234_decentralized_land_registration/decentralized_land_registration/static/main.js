async function postForm(url, formData) {
  const resp = await fetch(url, { method: 'POST', body: formData });
  return resp.json();
}

document.getElementById('regForm').addEventListener('submit', async e => {
  e.preventDefault();
  const formData = new FormData(document.getElementById('regForm'));
  document.getElementById('txResult').innerText = 'Submitting...';
  const resp = await postForm('/api/transactions/new', formData);
  document.getElementById('txResult').innerText = resp.message;
  const alertArea = document.getElementById('alertArea');
  alertArea.innerHTML = '';
  if (resp.flagged) {
    const div = document.createElement('div');
    div.className = 'warning-box';
    div.innerText = '⚠️ Duplicate Detected – Review Required. Reason: ' + resp.flag_reason;
    alertArea.appendChild(div);
  } else {
    const div = document.createElement('div');
    div.className = 'success-box';
    div.innerText = '✅ Submitted — No duplicates detected.';
    alertArea.appendChild(div);
  }
});

document.getElementById('mineBtn').addEventListener('click', async () => {
  document.getElementById('mineResult').innerText = 'Mining...';
  const resp = await fetch('/api/mine');
  const data = await resp.json();
  document.getElementById('mineResult').innerText = data.message + ' — Block ' + data.index;
});

document.getElementById('viewChainBtn').addEventListener('click', async () => {
  const resp = await fetch('/api/chain');
  const data = await resp.json();
  document.getElementById('chainResult').innerText = JSON.stringify(data, null, 2);
});
