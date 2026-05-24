/* AI Hub Local Console - app.js v20260505 */

let currentModalMarkdown = '';
let lastReviewData = null;

document.addEventListener('DOMContentLoaded', () => {
    // 탭 네비게이션
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => switchTab(item.dataset.tab, item));
    });

    // 헬스 체크
    checkHealth();
    document.getElementById('btnHealth').addEventListener('click', checkHealth);

    // Job Runner
    loadModels();
    loadRecentJobs();
    document.getElementById('btnRefreshModels').addEventListener('click', loadModels);
    document.getElementById('btnRun').addEventListener('click', runJob);
    document.getElementById('btnCopyResult')?.addEventListener('click', copyResult);

    // Instruction Review
    document.getElementById('irReviewerMode').addEventListener('change', onReviewerModeChange);
    document.getElementById('btnRunReview').addEventListener('click', runInstructionReview);
    document.getElementById('btnCopyFinalReview')?.addEventListener('click', copyFinalReview);

    // Developer Requests
    document.getElementById('btnRefreshRequests').addEventListener('click', loadDeveloperRequests);
    loadDeveloperRequests();

    // Evaluation Results
    document.getElementById('btnRefreshReviews').addEventListener('click', loadEvalResults);
    loadEvalResults();

    // Modal
    document.getElementById('btnCopyModal')?.addEventListener('click', copyModalMarkdown);
    document.getElementById('closeModal')?.addEventListener('click', closeModal);
    document.getElementById('jobModal')?.addEventListener('click', (e) => {
        if (e.target === document.getElementById('jobModal')) closeModal();
    });

    // OpenClaw
    document.getElementById('btnRefreshOpenClaw')?.addEventListener('click', loadOpenClawStatus);
    document.getElementById('btnOpenClawSend')?.addEventListener('click', sendOpenClawMessage);
    document.getElementById('openclawChatInput')?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendOpenClawMessage();
        }
    });
    
    loadOpenClawStatus();
});

// ─── Tab Navigation ────────────────────────────────────────────────────────

function switchTab(tabId, navItem) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.getElementById(tabId)?.classList.add('active');
    navItem?.classList.add('active');
}

// ─── Health Check ──────────────────────────────────────────────────────────

async function checkHealth() {
    const dot = document.getElementById('healthDot');
    const label = document.getElementById('healthLabel');
    dot.className = 'dot dot-checking';
    label.textContent = '확인 중...';
    try {
        const res = await fetch('/api/health');
        if (res.ok) {
            dot.className = 'dot dot-ok';
            label.textContent = 'Online';
        } else {
            throw new Error();
        }
    } catch {
        dot.className = 'dot dot-error';
        label.textContent = 'Offline';
    }
}

// ─── Model / Job Runner ────────────────────────────────────────────────────

async function loadModels() {
    const select = document.getElementById('modelSelect');
    select.innerHTML = '<option value="">로딩 중...</option>';
    try {
        const res = await fetch('/api/models');
        const data = await res.json();
        if (res.ok && data.models) {
            select.innerHTML = '';
            data.models.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m;
                opt.textContent = m;
                if (m.includes('qwen')) opt.selected = true;
                select.appendChild(opt);
            });
        } else {
            throw new Error(data.error || '로드 실패');
        }
    } catch (e) {
        select.innerHTML = `<option value="">Error: ${e.message}</option>`;
    }
}

async function runJob() {
    const btn = document.getElementById('btnRun');
    const status = document.getElementById('runStatus');
    const output = document.getElementById('responseOutput');
    const resultCard = document.getElementById('jobResult');
    const pathsBox = document.getElementById('filePaths');
    const pathsList = document.getElementById('pathsList');

    const model = document.getElementById('modelSelect').value;
    const project = document.getElementById('projectSelect').value;
    const mode = document.getElementById('modeSelect').value;
    const task = document.getElementById('taskInput').value;
    const temperature = parseFloat(document.getElementById('temperatureInput').value);
    const dryRun = document.getElementById('dryRunCheck').checked;

    if (!model || !task) { alert('모델과 Task를 입력하세요.'); return; }

    btn.disabled = true;
    btn.textContent = '실행 중...';
    status.textContent = '처리 중...';
    status.className = 'badge';
    resultCard.classList.remove('hidden');
    pathsBox.classList.add('hidden');
    output.textContent = 'Ollama 응답 대기 중...';

    try {
        const res = await fetch('/api/jobs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model, project, mode, task, temperature, dry_run: dryRun })
        });
        const data = await res.json();
        if (res.ok) {
            status.textContent = data.status === 'success' ? 'Success' : 'Error';
            status.className = 'badge ' + (data.status === 'success' ? 'badge-ok' : 'badge-error');
            output.textContent = data.response;
            pathsList.innerHTML = `
                <li>Output: ${data.output_file}</li>
                <li>Meta: ${data.metadata_file}</li>
                <li>Session: ${data.history_files?.session || '-'}</li>
                <li>Ahnda: ${data.history_files?.ahnda || '-'}</li>
            `;
            pathsBox.classList.remove('hidden');
            loadRecentJobs();
        } else {
            throw new Error(data.error || '알 수 없는 오류');
        }
    } catch (e) {
        status.textContent = 'Failed';
        status.className = 'badge badge-error';
        output.textContent = `Error: ${e.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = '▶ Run Job';
    }
}

function copyResult() {
    const text = document.getElementById('responseOutput').innerText;
    navigator.clipboard.writeText(text).then(() => alert('복사 완료')).catch(() => alert('복사 실패'));
}

async function loadRecentJobs() {
    const list = document.getElementById('recentJobsList');
    try {
        const res = await fetch('/api/jobs');
        const data = await res.json();
        if (data.jobs?.length > 0) {
            list.innerHTML = '';
            data.jobs.forEach(job => {
                const li = document.createElement('li');
                li.textContent = job.name;
                li.onclick = () => openJobResult(job.job_id, job.name);
                list.appendChild(li);
            });
        } else {
            list.innerHTML = '<li style="color:var(--text-muted);cursor:default">최근 Job 없음</li>';
        }
    } catch {
        list.innerHTML = '<li style="color:var(--red);cursor:default">로드 실패</li>';
    }
}

// ─── Instruction Review ────────────────────────────────────────────────────

function onReviewerModeChange() {
    const mode = document.getElementById('irReviewerMode').value;
    const keyRow = document.getElementById('googleApiKeyRow');
    if (mode === 'google-eval-required-later') {
        keyRow.classList.remove('hidden');
    } else {
        keyRow.classList.add('hidden');
    }
}

function setStageProgress(stage, state) {
    // stage: 1-4 (4 = Developer Request 생성)
    const ids = ['stageProgress1', 'stageProgress2', 'stageProgress3', 'stageProgressFinal'];
    const el = document.getElementById(ids[stage - 1]);
    if (!el) return;
    const dot = el.querySelector('.stage-dot');
    dot.className = 'stage-dot';
    if (state === 'running') { dot.className = 'stage-dot stage-running'; dot.textContent = '◌'; }
    else if (state === 'done') { dot.className = 'stage-dot stage-done'; dot.textContent = '●'; }
    else { dot.className = 'stage-dot stage-waiting'; dot.textContent = '○'; }
}

async function runInstructionReview() {
    const btn = document.getElementById('btnRunReview');
    const title = document.getElementById('irTitle').value.trim();
    const targetProject = document.getElementById('irTargetProject').value;
    const requestType = document.getElementById('irRequestType').value;
    const reviewerMode = document.getElementById('irReviewerMode').value;
    const temperature = parseFloat(document.getElementById('irTemperature').value);
    const draft = document.getElementById('irDraftInstruction').value.trim();
    const googleApiKey = document.getElementById('irGoogleApiKey').value.trim() || null;

    if (!title || !draft) { alert('제목과 초안 지침을 입력하세요.'); return; }

    // 진행 상태 초기화
    const progress = document.getElementById('irProgress');
    const result = document.getElementById('irResult');
    progress.classList.remove('hidden');
    result.classList.add('hidden');
    [1, 2, 3, 4].forEach(i => setStageProgress(i, 'waiting'));

    btn.disabled = true;
    btn.textContent = '평가 실행 중...';

    // 단계적 UI 업데이트 (실제 API는 한 번에 처리되므로 순차 표시)
    setStageProgress(1, 'running');
    await sleep(300);
    setStageProgress(2, 'running');
    await sleep(300);
    setStageProgress(3, 'running');

    try {
        const body = { title, target_project: targetProject, request_type: requestType,
            draft_instruction: draft, reviewer_mode: reviewerMode, temperature };
        if (googleApiKey) body.google_api_key = googleApiKey;

        const res = await fetch('/api/instruction-reviews', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.error || '알 수 없는 오류');

        setStageProgress(1, 'done');
        setStageProgress(2, 'done');
        setStageProgress(3, 'done');
        setStageProgress(4, 'running');
        await sleep(200);
        setStageProgress(4, 'done');

        lastReviewData = data;

        // 결과 표시
        await showReviewResult(data);
        result.classList.remove('hidden');

        // Eval Results 탭도 갱신
        loadEvalResults();
        loadDeveloperRequests();

    } catch (e) {
        [1, 2, 3, 4].forEach(i => setStageProgress(i, 'waiting'));
        alert(`평가 실패: ${e.message}`);
    } finally {
        btn.disabled = false;
        btn.textContent = '◈ 3단계 평가 실행';
    }
}

async function showReviewResult(data) {
    const status = document.getElementById('irStatus');
    const googleLabel = document.getElementById('irGoogleAiLabel');
    const filePaths = document.getElementById('irFilePaths');

    status.textContent = 'completed';
    status.className = 'badge badge-ok';

    if (data.google_ai_used) {
        googleLabel.textContent = 'Google AI 사용됨';
        googleLabel.className = 'badge badge-blue';
        googleLabel.classList.remove('hidden');
    } else {
        googleLabel.textContent = 'local-only';
        googleLabel.className = 'badge';
        googleLabel.classList.remove('hidden');
    }

    filePaths.innerHTML = `
        <strong>생성된 파일:</strong>
        <ul>
            <li>Stage 1: ${data.stage1_file || '-'}</li>
            <li>Stage 2: ${data.stage2_file || '-'}</li>
            <li>Stage 3: ${data.stage3_file || '-'}</li>
            <li>Developer Request: ${data.developer_request_file || '-'}</li>
            <li>Metadata: ${data.metadata_file || '-'}</li>
        </ul>
    `;

    // 각 Stage 내용 가져오기
    try {
        const detailRes = await fetch(`/api/instruction-reviews/${data.review_id}`);
        if (detailRes.ok) {
            const detail = await detailRes.json();
            renderMarkdown('irStage1Content', detail.v2_stage1_content || '');
            renderMarkdown('irStage2Content', detail.v3_stage2_content || '');
            renderMarkdown('irStage3Content', detail.v4_stage3_content || '');
        }
    } catch {
        // 내용 로드 실패 시 무시
    }
}

function copyFinalReview() {
    const el = document.getElementById('irStage3Content');
    navigator.clipboard.writeText(el?.innerText || '').then(() => alert('최종 결과 복사 완료')).catch(() => alert('복사 실패'));
}

// ─── Developer Requests ────────────────────────────────────────────────────

async function loadDeveloperRequests() {
    const tbody = document.getElementById('drTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="empty-row">로딩 중...</td></tr>';
    try {
        const res = await fetch('/api/developer-requests');
        const data = await res.json();
        if (!data.requests?.length) {
            tbody.innerHTML = '<tr><td colspan="6" class="empty-row">Developer Request 없음</td></tr>';
            return;
        }
        tbody.innerHTML = '';
        data.requests.forEach(r => {
            const tr = document.createElement('tr');
            const statusBadge = statusToBadge(r.status);
            tr.innerHTML = `
                <td class="clickable" onclick="openDeveloperRequest('${r.request_id}')">${r.title || '-'}</td>
                <td>${r.target_project || '-'}</td>
                <td>${r.request_type || '-'}</td>
                <td>${statusBadge}</td>
                <td>${r.timestamp || '-'}</td>
                <td><button class="btn-ghost btn-sm" onclick="openDeveloperRequest('${r.request_id}')">보기</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="6" class="empty-row" style="color:var(--red)">로드 실패: ${e.message}</td></tr>`;
    }
}

async function openDeveloperRequest(requestId) {
    document.getElementById('modalTitle').textContent = `Developer Request: ${requestId}`;
    document.getElementById('modalBody').innerHTML = '로딩 중...';
    document.getElementById('jobModal').classList.remove('hidden');
    try {
        const res = await fetch(`/api/developer-requests/${requestId}`);
        const data = await res.json();
        currentModalMarkdown = data.doc_content || JSON.stringify(data, null, 2);
        renderMarkdown('modalBody', currentModalMarkdown);
    } catch (e) {
        document.getElementById('modalBody').innerHTML = `<p style="color:var(--red)">Error: ${e.message}</p>`;
    }
}

// ─── Evaluation Results ────────────────────────────────────────────────────

async function loadEvalResults() {
    const tbody = document.getElementById('irTableBody');
    tbody.innerHTML = '<tr><td colspan="6" class="empty-row">로딩 중...</td></tr>';
    try {
        const res = await fetch('/api/instruction-reviews');
        const data = await res.json();
        if (!data.reviews?.length) {
            tbody.innerHTML = '<tr><td colspan="6" class="empty-row">평가 결과 없음</td></tr>';
            return;
        }
        tbody.innerHTML = '';
        data.reviews.forEach(r => {
            const tr = document.createElement('tr');
            const gaiLabel = r.google_ai_used
                ? '<span class="badge badge-blue">Google AI</span>'
                : '<span class="badge">local-only</span>';
            tr.innerHTML = `
                <td class="clickable" onclick="openReviewResult('${r.review_id}')">${r.title || '-'}</td>
                <td>${r.target_project || '-'}</td>
                <td>${r.request_type || '-'}</td>
                <td>${gaiLabel}</td>
                <td>${r.timestamp || '-'}</td>
                <td><button class="btn-ghost btn-sm" onclick="openReviewResult('${r.review_id}')">보기</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="6" class="empty-row" style="color:var(--red)">로드 실패: ${e.message}</td></tr>`;
    }
}

async function openReviewResult(reviewId) {
    document.getElementById('modalTitle').textContent = `Review: ${reviewId}`;
    document.getElementById('modalBody').innerHTML = '로딩 중...';
    document.getElementById('jobModal').classList.remove('hidden');
    try {
        const res = await fetch(`/api/instruction-reviews/${reviewId}`);
        const data = await res.json();
        const combined = [
            `# ${data.title || reviewId}\n`,
            `**프로젝트**: ${data.target_project}  |  **유형**: ${data.request_type}  |  **모드**: ${data.reviewer_mode}\n`,
            `---\n## 1차 평가: 구조 정리\n${data.v2_stage1_content || ''}`,
            `---\n## 2차 평가: 실전 개발 검증\n${data.v3_stage2_content || ''}`,
            `---\n## 3차 평가: 최종 승인\n${data.v4_stage3_content || ''}`,
        ].join('\n\n');
        currentModalMarkdown = combined;
        renderMarkdown('modalBody', combined);
    } catch (e) {
        document.getElementById('modalBody').innerHTML = `<p style="color:var(--red)">Error: ${e.message}</p>`;
    }
}

// ─── Job Modal (Job Runner) ────────────────────────────────────────────────

async function openJobResult(job_id, title) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').innerHTML = '로딩 중...';
    document.getElementById('jobModal').classList.remove('hidden');
    try {
        const res = await fetch(`/api/jobs/${job_id}/result`);
        if (!res.ok) throw new Error('로드 실패');
        const text = await res.text();
        currentModalMarkdown = text;
        renderMarkdown('modalBody', text);
    } catch (e) {
        document.getElementById('modalBody').innerHTML = `<p style="color:var(--red)">Error: ${e.message}</p>`;
    }
}

// ─── Utilities ─────────────────────────────────────────────────────────────

function renderMarkdown(elementId, text) {
    const el = document.getElementById(elementId);
    if (!el) return;
    if (typeof marked !== 'undefined' && text) {
        el.innerHTML = marked.parse(text);
    } else {
        el.textContent = text;
    }
}

function closeModal() {
    document.getElementById('jobModal').classList.add('hidden');
}

function copyModalMarkdown() {
    navigator.clipboard.writeText(currentModalMarkdown).then(() => alert('복사 완료')).catch(() => alert('복사 실패'));
}

function statusToBadge(status) {
    const map = {
        draft: '<span class="badge">draft</span>',
        reviewed: '<span class="badge badge-warn">reviewed</span>',
        ready_for_opai: '<span class="badge badge-ok">ready_for_opai</span>',
        sent_to_opai: '<span class="badge badge-blue">sent_to_opai</span>',
        completed: '<span class="badge badge-ok">completed</span>',
        failed: '<span class="badge badge-error">failed</span>',
    };
    return map[status] || `<span class="badge">${status || '-'}</span>`;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ─── OpenClaw Console ──────────────────────────────────────────────────────

async function loadOpenClawStatus() {
    const display = document.getElementById('openclawHealthDisplay');
    const lblWebUrl = document.getElementById('lblOpenClawWebUrl');
    const lblApiUrl = document.getElementById('lblOpenClawApiUrl');
    const btnWeb = document.getElementById('btnOpenClawWeb');
    
    if (!display) return;
    display.textContent = '상태 확인 중...';
    
    try {
        // 1. 설정 로드
        const confRes = await fetch('/api/openclaw/config');
        const conf = await confRes.json();
        
        lblWebUrl.textContent = conf.web_url;
        lblApiUrl.textContent = conf.api_url;
        btnWeb.href = conf.web_url;
        
        // 2. Health Check (Bridge Server로 직접 접근)
        const healthUrl = `${conf.api_url}/api/health`;
        const hRes = await fetch(healthUrl);
        if (!hRes.ok) throw new Error('Health Check API 호출 실패');
        const hData = await hRes.json();
        
        display.innerHTML = `
            <strong>API Health:</strong> <span style="color:var(--vscode-charts-green)">Online</span><br>
            <strong>Ollama:</strong> ${hData.ollama ? '<span style="color:var(--vscode-charts-green)">Online</span>' : '<span style="color:var(--vscode-charts-red)">Offline</span>'}<br>
            <strong>Chat Model:</strong> ${hData.models?.chat} (${hData.models?.chat_available ? '사용 가능' : '사용 불가'})<br>
            <strong>Code Model:</strong> ${hData.models?.code} (${hData.models?.code_available ? '사용 가능' : '사용 불가'})<br>
            <br>
            <small style="color:var(--vscode-descriptionForeground)">Timestamp: ${hData.timestamp}</small>
        `;
    } catch (e) {
        display.innerHTML = `<span style="color:var(--vscode-charts-red)">Offline 또는 통신 오류 (${e.message})</span><br>
        <small style="color:var(--vscode-descriptionForeground)">OpenClaw Bridge Server가 실행 중인지 확인하세요.</small>`;
    }
}

async function sendOpenClawMessage() {
    const input = document.getElementById('openclawChatInput');
    const log = document.getElementById('openclawChatLog');
    const lblApiUrl = document.getElementById('lblOpenClawApiUrl');
    
    const message = input.value.trim();
    if (!message) return;
    
    const apiUrl = lblApiUrl.textContent;
    if (!apiUrl || apiUrl === '-') {
        alert('API URL을 로드하지 못했습니다. 상태 확인을 다시 해주세요.');
        return;
    }

    // 사용자 메시지 추가
    input.value = '';
    const userMsg = document.createElement('div');
    userMsg.style.cssText = 'align-self: flex-end; background: var(--vscode-button-background); color: var(--vscode-button-foreground); padding: 10px 15px; border-radius: 8px 8px 0 8px; max-width: 80%; word-break: break-word;';
    userMsg.textContent = message;
    log.appendChild(userMsg);
    log.scrollTop = log.scrollHeight;

    // 로딩 표시 (Thinking 애니메이션)
    const aiMsg = document.createElement('div');
    aiMsg.style.cssText = 'align-self: flex-start; background: var(--vscode-editorWidget-background); padding: 10px 15px; border-radius: 8px 8px 8px 0; max-width: 80%; border: 1px solid var(--vscode-widget-border); font-style: italic; min-width: 120px;';
    aiMsg.textContent = 'Thinking .';
    log.appendChild(aiMsg);
    log.scrollTop = log.scrollHeight;

    let dotCount = 1;
    const thinkingInterval = setInterval(() => {
        dotCount = (dotCount % 4) + 1;
        aiMsg.textContent = 'Thinking ' + '.'.repeat(dotCount);
    }, 400);

    try {
        const res = await fetch(`${apiUrl}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                workspaceRoot: '/project',
                message: message,
                mode: 'chat'
            })
        });
        
        clearInterval(thinkingInterval);
        aiMsg.style.fontStyle = 'normal';
        
        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `HTTP ${res.status}`);
        }
        
        const data = await res.json();
        const aiResponseText = data.answer || data.response || '';
        if (typeof marked !== 'undefined') {
            aiMsg.innerHTML = marked.parse(aiResponseText);
        } else {
            aiMsg.textContent = aiResponseText;
        }
    } catch (e) {
        clearInterval(thinkingInterval);
        aiMsg.style.fontStyle = 'normal';
        aiMsg.textContent = `Error: ${e.message}`;
        aiMsg.style.color = 'var(--vscode-charts-red)';
    } finally {
        log.scrollTop = log.scrollHeight;
    }
}

// Safe Apply 함수 (하위 호환)
async function previewAhndaMvp() {
    try {
        const res = await fetch('/api/apply/site-ahnda-static-mvp/preview');
        const data = await res.json();
        alert(JSON.stringify(data, null, 2));
    } catch (e) { alert(`Error: ${e.message}`); }
}

async function applyAhndaMvp() {
    if (!confirm('/project/site/ahnda에 정적 MVP 파일을 생성합니다. 진행할까요?')) return;
    try {
        const res = await fetch('/api/apply/site-ahnda-static-mvp', { method: 'POST' });
        const data = await res.json();
        alert(JSON.stringify(data, null, 2));
    } catch (e) { alert(`Error: ${e.message}`); }
}

// ─── Lostway Sim/Eval Tab ───────────────────────────────────────────────────

function lwSimInit() {
    lwSimLoadFiles();
}

async function lwSimGenerate() {
    const count = parseInt(document.getElementById('lwSimCount').value || '20', 10);
    const btn = document.getElementById('btnLwSimGenerate');
    const resultEl = document.getElementById('lwSimGenResult');
    
    btn.disabled = true;
    btn.textContent = '생성 중...';
    resultEl.classList.remove('hidden');
    resultEl.textContent = '생성 중입니다. 잠시만 기다려주세요...';

    try {
        const res = await fetch('/api/lostway/simulation/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ count })
        });
        const data = await res.json();
        if (data.ok) {
            resultEl.textContent = `✅ 생성 완료!\n\n${data.output}`;
            lwSimLoadFiles();
        } else {
            resultEl.textContent = `❌ 오류 발생:\n${data.error}`;
        }
    } catch (e) {
        resultEl.textContent = `❌ 네트워크 오류: ${e.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = '▶ 데이터 생성 실행';
    }
}

async function lwSimEvaluate() {
    const percent = parseInt(document.getElementById('lwSimPercent').value || '1', 10);
    const btn = document.getElementById('btnLwSimEvaluate');
    const resultEl = document.getElementById('lwSimEvalResult');
    
    btn.disabled = true;
    btn.textContent = '검증 중...';
    resultEl.classList.remove('hidden');
    resultEl.textContent = '검증 스크립트 실행 중입니다. 잠시만 기다려주세요...';

    try {
        const res = await fetch('/api/lostway/simulation/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ percent })
        });
        const data = await res.json();
        if (data.ok) {
            resultEl.textContent = `✅ 검증 완료!\n\n${data.output}`;
            lwSimLoadFiles();
        } else {
            resultEl.textContent = `❌ 오류 발생:\n${data.error}`;
        }
    } catch (e) {
        resultEl.textContent = `❌ 네트워크 오류: ${e.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = '✔ n% 검증 추출 실행';
    }
}

async function lwSimLoadFiles() {
    const tbody = document.getElementById('lwSimFilesTableBody');
    if (!tbody) return;
    try {
        const res = await fetch('/api/lostway/simulation/files');
        const data = await res.json();
        if (!data.files || data.files.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="empty-row">파일이 없습니다.</td></tr>';
            return;
        }
        tbody.innerHTML = data.files.map(item => `
            <tr>
                <td style="font-family: monospace; font-size: 0.85em;">${item.name}</td>
                <td>${item.size.toLocaleString()}</td>
                <td>
                    <button class="btn-ghost btn-sm" onclick="lwSimViewFile('${item.name}')">열기 (Top 100줄)</button>
                    <a href="/api/lostway/simulation/files/${encodeURIComponent(item.name)}/download" download class="btn-ghost btn-sm" style="text-decoration:none; padding: 4px 8px; font-size: 11px;">다운로드</a>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="3" class="empty-row">로드 실패: ${e.message}</td></tr>`;
    }
}

async function lwSimViewFile(filename) {
    try {
        const res = await fetch(`/api/lostway/simulation/files/${encodeURIComponent(filename)}`);
        if (!res.ok) {
            const err = await res.text();
            alert(`파일 읽기 실패: ${err}`);
            return;
        }
        const text = await res.text();
        const modal = document.getElementById('jobModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        
        if (modal && modalTitle && modalBody) {
            modalTitle.textContent = filename;
            
            // JSON/JSONL 파싱 시도
            let items = [];
            try {
                if (text.trim().startsWith('[')) {
                    items = JSON.parse(text);
                } else {
                    items = text.trim().split('\n').map(line => {
                        try { return JSON.parse(line); } catch(e) { return null; }
                    }).filter(Boolean);
                }
            } catch(e) {
                // 파싱 실패 시 원문 표시
                modalBody.innerHTML = `<pre style="white-space: pre-wrap; font-size: 13px;">${text.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>`;
                modal.classList.remove('hidden');
                return;
            }
            
            const isDark = document.body.classList.contains('dark-theme') || window.matchMedia('(prefers-color-scheme: dark)').matches;
            const darkClass = isDark ? 'dark-theme' : '';

            let html = `
<style>
.chat-list { max-height: 70vh; overflow-y: auto; padding-right: 10px; }
.chat-container { display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px; padding: 16px; background: #f9fafb; border-radius: 8px; border: 1px solid #e5e7eb; }
.dark-theme .chat-container { background: var(--bg-card, #1e1e2e); border-color: var(--border, #2a2a35); }
.chat-meta { font-size: 12px; color: #6b7280; margin-bottom: 8px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px; display: flex; justify-content: space-between; }
.dark-theme .chat-meta { color: #a1a1aa; border-color: var(--border, #3f3f46); }
.risk-high { color: #ef4444; font-weight: bold; }
.risk-medium { color: #f59e0b; font-weight: bold; }
.risk-low { color: #10b981; font-weight: bold; }
.chat-bubble-wrapper { display: flex; width: 100%; }
.chat-bubble-wrapper.user { justify-content: flex-end; }
.chat-bubble-wrapper.assistant { justify-content: flex-start; }
.chat-bubble-wrapper.notice { justify-content: center; }
.chat-bubble { max-width: 80%; padding: 10px 14px; border-radius: 12px; font-size: 14px; line-height: 1.5; white-space: pre-wrap; }
.chat-bubble-wrapper.user .chat-bubble { background: #6366f1; color: white; border-bottom-right-radius: 2px; }
.chat-bubble-wrapper.assistant .chat-bubble { background: #e5e7eb; color: #111827; border-bottom-left-radius: 2px; }
.dark-theme .chat-bubble-wrapper.assistant .chat-bubble { background: #3f3f46; color: #f4f4f5; }
.chat-bubble-wrapper.notice .chat-bubble { background: transparent; color: #9ca3af; font-size: 12px; text-align: center; font-style: italic; border: 1px dashed #d1d5db; border-radius: 6px; padding: 6px 12px; }
.dark-theme .chat-bubble-wrapper.notice .chat-bubble { border-color: #52525b; }
.chat-ending { margin-top: 8px; padding: 12px; background: #e0e7ff; border-radius: 8px; color: #4338ca; font-size: 13px; font-weight: 500; text-align: center; }
.dark-theme .chat-ending { background: rgba(67, 56, 202, 0.2); color: #c7d2fe; }
</style>
<div class="chat-list ${darkClass}">
            `;

            if (items.length === 0) {
                html += `<div style="padding:20px; text-align:center;">데이터가 없습니다.</div>`;
            }

            items.forEach((item, index) => {
                const riskColor = item.risk_level === 'crisis' || item.risk_level === 'high' ? 'risk-high' 
                                : item.risk_level === 'medium' ? 'risk-medium' : 'risk-low';
                
                html += `<div class="chat-container">
                    <div class="chat-meta">
                        <span><strong>ID:</strong> ${item.id}</span>
                        <span><strong>Risk:</strong> <span class="${riskColor}">${item.risk_level?.toUpperCase() || 'UNKNOWN'}</span></span>
                    </div>`;
                    
                if (item.conversation && Array.isArray(item.conversation)) {
                    item.conversation.forEach(msg => {
                        let cls = msg.role === 'user' ? 'user' : 'assistant';
                        if (msg.type === 'notice') cls = 'notice';
                        
                        const msgText = (msg.text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                        
                        html += `
                        <div class="chat-bubble-wrapper ${cls}">
                            <div class="chat-bubble">${msgText}</div>
                        </div>`;
                    });
                }
                
                if (item.ending && item.ending.save_question) {
                    const eq = item.ending.save_question.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    html += `<div class="chat-ending">${eq}</div>`;
                }
                
                html += `</div>`;
            });

            html += `</div>`;
            modalBody.innerHTML = html;
            modal.classList.remove('hidden');
        } else {
            alert(text);
        }
    } catch (e) {
        alert(`오류: ${e.message}`);
    }
}

// 이벤트 바인딩
document.addEventListener('DOMContentLoaded', () => {
    const btnGen = document.getElementById('btnLwSimGenerate');
    if (btnGen) btnGen.addEventListener('click', lwSimGenerate);

    const btnEval = document.getElementById('btnLwSimEvaluate');
    if (btnEval) btnEval.addEventListener('click', lwSimEvaluate);

    const btnRefresh = document.getElementById('btnRefreshLwSimFiles');
    if (btnRefresh) btnRefresh.addEventListener('click', lwSimLoadFiles);

    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            if (item.dataset.tab === 'tab-lostway-sim') {
                lwSimInit();
            }
        });
    });
});
