let currentModalMarkdown = '';

document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    loadModels();
    loadRecentJobs();

    document.getElementById('btnHealth').addEventListener('click', checkHealth);
    document.getElementById('btnRefreshModels').addEventListener('click', loadModels);
    document.getElementById('btnRun').addEventListener('click', runJob);
    
    document.getElementById('btnCopyResult')?.addEventListener('click', copyResult);
    document.getElementById('btnCopyModal')?.addEventListener('click', copyModalMarkdown);
    document.querySelector('.close-modal')?.addEventListener('click', closeModal);
    
    document.getElementById('btnPreviewAhnda')?.addEventListener('click', previewAhndaMvp);
    document.getElementById('btnApplyAhnda')?.addEventListener('click', applyAhndaMvp);
});

function copyResult() {
    const text = document.getElementById('responseOutput').innerText;
    navigator.clipboard.writeText(text).then(() => alert('결과 복사 완료')).catch(() => alert('복사 실패'));
}

function copyModalMarkdown() {
    navigator.clipboard.writeText(currentModalMarkdown).then(() => alert('Markdown 복사 완료')).catch(() => alert('복사 실패'));
}

function closeModal() {
    document.getElementById('jobModal').classList.add('hidden');
}

async function checkHealth() {
    const badge = document.getElementById('healthStatus');
    badge.textContent = 'Checking...';
    badge.className = 'badge';
    
    try {
        const res = await fetch('/api/health');
        if (res.ok) {
            badge.textContent = 'Online';
            badge.classList.add('ok');
        } else {
            throw new Error('Not OK');
        }
    } catch (e) {
        badge.textContent = 'Offline';
        badge.classList.add('error');
    }
}

async function loadModels() {
    const select = document.getElementById('modelSelect');
    select.innerHTML = '<option value="">Loading...</option>';
    
    try {
        const res = await fetch('/api/models');
        const data = await res.json();
        
        if (res.ok && data.models) {
            select.innerHTML = '';
            data.models.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m;
                opt.textContent = m;
                // pre-select qwen if available
                if(m.includes('qwen')) opt.selected = true;
                select.appendChild(opt);
            });
        } else {
            throw new Error(data.error || 'Failed to load');
        }
    } catch (e) {
        select.innerHTML = `<option value="">Error: ${e.message}</option>`;
    }
}

async function runJob() {
    const btn = document.getElementById('btnRun');
    const status = document.getElementById('runStatus');
    const output = document.getElementById('responseOutput');
    const pathsBox = document.getElementById('filePaths');
    const pathsList = document.getElementById('pathsList');
    
    const model = document.getElementById('modelSelect').value;
    const project = document.getElementById('projectSelect').value;
    const mode = document.getElementById('modeSelect').value;
    const task = document.getElementById('taskInput').value;
    const temperature = parseFloat(document.getElementById('temperatureInput').value);
    const dryRun = document.getElementById('dryRunCheck').checked;
    
    if (!model || !task) {
        alert('Please select a model and enter a task.');
        return;
    }
    
    btn.disabled = true;
    btn.textContent = 'Running...';
    status.textContent = 'Processing...';
    status.className = 'badge';
    status.classList.remove('hidden');
    pathsBox.classList.add('hidden');
    output.textContent = 'Waiting for response from Ollama...';
    
    try {
        const res = await fetch('/api/jobs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model, project, mode, task, temperature, dry_run: dryRun })
        });
        
        const data = await res.json();
        
        if (res.ok) {
            status.textContent = data.status === 'success' ? 'Success' : 'Completed with Errors';
            status.classList.add(data.status === 'success' ? 'ok' : 'error');
            output.textContent = data.response;
            
            pathsList.innerHTML = `
                <li>Output: ${data.output_file}</li>
                <li>Meta: ${data.metadata_file}</li>
                <li>Session: ${data.history_files.session}</li>
                <li>Ahnda: ${data.history_files.ahnda}</li>
                <li>BomTS Ref: ${data.history_files.bomts_reference}</li>
                <li>BomTS Pub: ${data.history_files.bomts_publish}</li>
            `;
            pathsBox.classList.remove('hidden');
            document.getElementById('btnCopyResult')?.classList.remove('hidden');
            
            loadRecentJobs();
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (e) {
        status.textContent = 'Failed';
        status.classList.add('error');
        output.textContent = `Error: ${e.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = '▶ Run Job';
    }
}

async function loadRecentJobs() {
    const list = document.getElementById('recentJobsList');
    try {
        const res = await fetch('/api/jobs');
        const data = await res.json();
        
        if (data.jobs && data.jobs.length > 0) {
            list.innerHTML = '';
            data.jobs.forEach(job => {
                const li = document.createElement('li');
                li.textContent = job.name;
                li.className = 'job-item';
                li.onclick = () => openJobResult(job.job_id, job.name);
                list.appendChild(li);
            });
        } else {
            list.innerHTML = '<li>No recent jobs found.</li>';
        }
    } catch (e) {
        list.innerHTML = '<li>Failed to load recent jobs.</li>';
    }
}

async function openJobResult(job_id, title) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').innerHTML = 'Loading...';
    document.getElementById('jobModal').classList.remove('hidden');
    
    try {
        const res = await fetch(`/api/jobs/${job_id}/result`);
        if (!res.ok) throw new Error('Failed to load result');
        const text = await res.text();
        currentModalMarkdown = text;
        
        // Render using marked.js
        if(typeof marked !== 'undefined') {
            document.getElementById('modalBody').innerHTML = marked.parse(text);
        } else {
            const pre = document.createElement('pre');
            pre.textContent = text;
            document.getElementById('modalBody').innerHTML = '';
            document.getElementById('modalBody').appendChild(pre);
        }
    } catch (e) {
        document.getElementById('modalBody').innerHTML = `<p class="error">Error: ${e.message}</p>`;
    }
}

async function previewAhndaMvp() {
    const resultsBox = document.getElementById('safeApplyResults');
    const output = document.getElementById('safeApplyOutput');
    resultsBox.classList.remove('hidden');
    output.textContent = '미리보기 불러오는 중...';
    
    try {
        const res = await fetch('/api/apply/site-ahnda-static-mvp/preview');
        const data = await res.json();
        if(res.ok) {
            output.textContent = JSON.stringify(data, null, 2);
        } else {
            output.textContent = `Error: ${data.error || '알 수 없는 오류'}`;
        }
    } catch(e) {
        output.textContent = `Error: ${e.message}`;
    }
}

async function applyAhndaMvp() {
    if(!confirm("/project/site/ahnda에 정적 MVP 파일을 생성합니다. 진행할까요?")) {
        return;
    }
    
    const resultsBox = document.getElementById('safeApplyResults');
    const output = document.getElementById('safeApplyOutput');
    resultsBox.classList.remove('hidden');
    output.textContent = '적용 중...';
    
    try {
        const res = await fetch('/api/apply/site-ahnda-static-mvp', { method: 'POST' });
        const data = await res.json();
        if(res.ok) {
            output.textContent = JSON.stringify(data, null, 2);
        } else {
            output.textContent = `Error: ${data.error || '알 수 없는 오류'}`;
        }
    } catch(e) {
        output.textContent = `Error: ${e.message}`;
    }
}
