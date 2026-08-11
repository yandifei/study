/* ============================================================================
   MongoDB Service — Admin Panel JavaScript
   ============================================================================ */

const app = (() => {
    /* ── State ─────────────────────────────────────────────────────────────── */
    let currentLogType = null;       // 'error' | 'running'
    let autoRefreshTimer = null;
    let autoRefreshInterval = 5000;  // 5 seconds
    let serverStartTime = Date.now();
    let uptimeInterval = null;

    /* ── DOM Refs ──────────────────────────────────────────────────────────── */
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    const dom = {
        clock: $('#clock'),
        serverStatus: $('#serverStatus'),
        statusDot: $('.status-dot'),
        statusText: $('.status-text'),
        statusUptime: $('#statusUptime'),
        infoHost: $('#infoHost'),
        infoPort: $('#infoPort'),
        infoUptime: $('#infoUptime'),
        logPreview: $('#logPreview'),
        logModal: $('#logModal'),
        logModalIcon: $('#logModalIcon'),
        logModalTitle: $('#logModalTitle'),
        logModalSize: $('#logModalSize'),
        logContent: $('#logContent'),
        logLineCount: $('#logLineCount'),
        autoScrollCheckbox: $('#autoScroll'),
        btnAutoRefresh: $('#btnAutoRefresh'),
        stopModal: $('#stopModal'),
        stopPassword: $('#stopPassword'),
        stopError: $('#stopError'),
        btnConfirmStop: $('#btnConfirmStop'),
        btnErrorLog: $('#btnErrorLog'),
        btnRunLog: $('#btnRunLog'),
        toastContainer: $('#toastContainer'),
        previewTabs: $$('.log-tab'),
    };

    /* ── Utils ──────────────────────────────────────────────────────────────── */
    const formatBytes = (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / 1048576).toFixed(2) + ' MB';
    };

    const formatUptime = (ms) => {
        const totalSec = Math.floor(ms / 1000);
        const d = Math.floor(totalSec / 86400);
        const h = Math.floor((totalSec % 86400) / 3600);
        const m = Math.floor((totalSec % 3600) / 60);
        const s = totalSec % 60;
        const parts = [];
        if (d > 0) parts.push(`${d}d`);
        if (h > 0) parts.push(`${h}h`);
        if (m > 0) parts.push(`${m}m`);
        parts.push(`${s}s`);
        return parts.join(' ');
    };

    const highlightLog = (text) => {
        if (!text) return '<span class="log-placeholder">（空）</span>';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            // Timestamps: 2026-06-13 14:30:00 or similar
            .replace(/(\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?)/g, '<span class="log-timestamp">$1</span>')
            // Log levels
            .replace(/\b(CRITICAL|FATAL)\b/gi, '<span class="log-critical">$&</span>')
            .replace(/\b(ERROR|ERR)\b/g, '<span class="log-error">$&</span>')
            .replace(/\b(WARNING|WARN)\b/g, '<span class="log-warning">$&</span>')
            .replace(/\b(INFO|SUCCESS)\b/g, '<span class="log-info">$&</span>')
            .replace(/\b(DEBUG|TRACE)\b/g, '<span class="log-debug">$&</span>');
    };

    /* ── Toast ──────────────────────────────────────────────────────────────── */
    const showToast = (message, type = 'success', duration = 3500) => {
        const icons = {
            success: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
            error: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
            info: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        };
        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        toast.innerHTML = `${icons[type] || icons.info}<span>${message}</span>`;
        dom.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('toast--out');
            toast.addEventListener('transitionend', () => toast.remove());
        }, duration);
    };

    /* ── Clock ──────────────────────────────────────────────────────────────── */
    const updateClock = () => {
        const now = new Date();
        dom.clock.textContent = now.toLocaleTimeString('zh-CN', { hour12: false });
    };
    setInterval(updateClock, 1000);
    updateClock();

    /* ── Uptime ──────────────────────────────────────────────────────────────── */
    const updateUptime = () => {
        const elapsed = Date.now() - serverStartTime;
        const str = formatUptime(elapsed);
        dom.statusUptime.textContent = `运行 ${str}`;
        dom.infoUptime.textContent = str;
    };
    uptimeInterval = setInterval(updateUptime, 1000);
    updateUptime();

    /* ── Server Info ────────────────────────────────────────────────────────── */
    const fetchServerInfo = async () => {
        try {
            const resp = await fetch('/api/admin/info');
            if (resp.ok) {
                const data = await resp.json();
                dom.infoHost.textContent = data.host || '--';
                dom.infoPort.textContent = data.port || '--';
                if (data.start_time) {
                    serverStartTime = new Date(data.start_time).getTime();
                    updateUptime();
                }
            }
        } catch { /* silent */ }
    };
    fetchServerInfo();

    /* ── Log Preview ────────────────────────────────────────────────────────── */
    const switchPreviewTab = async (tab) => {
        dom.previewTabs.forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
        try {
            const resp = await fetch(`/api/admin/logs/preview?type=${tab}&lines=15`);
            if (resp.ok) {
                const data = await resp.json();
                dom.logPreview.innerHTML = data.content
                    ? highlightLog(data.content)
                    : '<span class="log-placeholder">（空）</span>';
            }
        } catch {
            dom.logPreview.innerHTML = '<span class="log-placeholder">加载失败</span>';
        }
    };
    // Load initial preview
    switchPreviewTab('error');

    /* ── Log Viewer ─────────────────────────────────────────────────────────── */
    const loadLogContent = async () => {
        if (!currentLogType) return;
        dom.logContent.innerHTML = '<span class="log-placeholder">加载中...</span>';

        try {
            const resp = await fetch(`/api/admin/logs/full?type=${currentLogType}`);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            const data = await resp.json();
            dom.logContent.innerHTML = highlightLog(data.content);
            dom.logLineCount.textContent = `${data.line_count || 0} 行`;
            dom.logModalSize.textContent = formatBytes(data.size || 0);

            if (dom.autoScrollCheckbox.checked) {
                requestAnimationFrame(() => {
                    dom.logContent.scrollTop = dom.logContent.scrollHeight;
                });
            }
        } catch (err) {
            dom.logContent.innerHTML = `<span class="log-placeholder">加载失败: ${err.message}</span>`;
            dom.logLineCount.textContent = '错误';
        }
    };

    const openLogViewer = (type) => {
        currentLogType = type;
        const titles = { error: '错误日志', running: '运行日志' };
        const icons = {
            error: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
            running: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
        };

        dom.logModalTitle.textContent = titles[type] || '日志查看器';
        dom.logModalIcon.innerHTML = icons[type] || '';
        dom.logModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        loadLogContent();

        // Focus trap
        setTimeout(() => dom.logModal.querySelector('.modal-btn-icon')?.focus(), 100);
    };

    const closeLogViewer = () => {
        dom.logModal.classList.remove('active');
        document.body.style.overflow = '';
        stopAutoRefresh();
        currentLogType = null;
    };

    const refreshLog = () => { if (currentLogType) loadLogContent(); };

    const toggleAutoRefresh = () => {
        if (autoRefreshTimer) {
            stopAutoRefresh();
            showToast('自动刷新已关闭', 'info', 2000);
        } else {
            autoRefreshTimer = setInterval(refreshLog, autoRefreshInterval);
            dom.btnAutoRefresh.classList.add('active');
            showToast(`每 ${autoRefreshInterval / 1000}s 自动刷新`, 'info', 2000);
        }
    };

    const stopAutoRefresh = () => {
        if (autoRefreshTimer) {
            clearInterval(autoRefreshTimer);
            autoRefreshTimer = null;
        }
        dom.btnAutoRefresh.classList.remove('active');
    };

    const downloadLog = () => {
        if (!currentLogType) return;
        const endpoints = {
            error: '/outputs/logs/error.log',
            running: '/outputs/logs/日志记录.log',
        };
        const url = endpoints[currentLogType];
        if (url) {
            const a = document.createElement('a');
            a.href = url;
            a.download = currentLogType === 'error' ? 'error.log' : '运行日志.log';
            a.click();
        }
    };

    /* ── Stop Server ────────────────────────────────────────────────────────── */
    const showStopDialog = () => {
        dom.stopModal.classList.add('active');
        dom.stopPassword.value = '';
        dom.stopError.textContent = '';
        dom.btnConfirmStop.disabled = false;
        document.body.style.overflow = 'hidden';
        setTimeout(() => dom.stopPassword.focus(), 100);
    };

    const closeStopDialog = () => {
        dom.stopModal.classList.remove('active');
        document.body.style.overflow = '';
    };

    const stopServer = async () => {
        const password = dom.stopPassword.value.trim();
        if (!password) {
            dom.stopError.textContent = '请输入密码';
            return;
        }

        dom.btnConfirmStop.disabled = true;
        dom.btnConfirmStop.textContent = '正在停止...';
        dom.stopError.textContent = '';

        try {
            const resp = await fetch(`/${encodeURIComponent(password)}`, { method: 'DELETE' });
            const data = await resp.json();

            if (resp.ok) {
                showToast('服务已停止', 'success');
                dom.statusDot.classList.add('danger');
                dom.statusText.textContent = '已停止';
                closeStopDialog();
                // Start polling to detect when server is gone
                let attempts = 0;
                const check = setInterval(async () => {
                    attempts++;
                    try {
                        await fetch('/api/admin/info');
                    } catch {
                        dom.statusText.textContent = '离线';
                        dom.statusUptime.textContent = '服务已停止';
                        clearInterval(check);
                        clearInterval(uptimeInterval);
                        showToast('服务器已离线', 'info', 5000);
                    }
                    if (attempts > 30) clearInterval(check);
                }, 1000);
            } else {
                dom.stopError.textContent = data.error || data.detail || '密码错误或服务拒绝';
                dom.btnConfirmStop.disabled = false;
                dom.btnConfirmStop.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>确认停止`;
            }
        } catch (err) {
            dom.stopError.textContent = '网络错误：无法连接到服务器';
            dom.btnConfirmStop.disabled = false;
            dom.btnConfirmStop.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>确认停止`;
        }
    };

    /* ── Keyboard Shortcuts ─────────────────────────────────────────────────── */
    const handleKeyboard = (e) => {
        // Esc: close modals
        if (e.key === 'Escape') {
            if (dom.logModal.classList.contains('active')) {
                closeLogViewer();
            } else if (dom.stopModal.classList.contains('active')) {
                closeStopDialog();
            }
        }
        // Enter: confirm stop
        if (e.key === 'Enter' && dom.stopModal.classList.contains('active')) {
            stopServer();
        }
        // R: refresh log when viewer is open
        if (e.key === 'r' && e.ctrlKey && dom.logModal.classList.contains('active')) {
            e.preventDefault();
            refreshLog();
        }
    };
    document.addEventListener('keydown', handleKeyboard);

    /* ── Modal Backdrop Click ────────────────────────────────────────────────── */
    dom.logModal.addEventListener('click', (e) => {
        if (e.target === dom.logModal) closeLogViewer();
    });
    dom.stopModal.addEventListener('click', (e) => {
        if (e.target === dom.stopModal) closeStopDialog();
    });

    /* ── Stop Password Enter Key ─────────────────────────────────────────────── */
    dom.stopPassword.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            stopServer();
        }
    });

    /* ── Public API ─────────────────────────────────────────────────────────── */
    return {
        openLogViewer,
        closeLogViewer,
        refreshLog,
        toggleAutoRefresh,
        downloadLog,
        showStopDialog,
        closeStopDialog,
        stopServer,
        switchPreviewTab,
    };
})();

// Global function bridge for onclick handlers
const openLogViewer = (type) => app.openLogViewer(type);
const closeLogViewer = () => app.closeLogViewer();
const refreshLog = () => app.refreshLog();
const toggleAutoRefresh = () => app.toggleAutoRefresh();
const downloadLog = () => app.downloadLog();
const showStopDialog = () => app.showStopDialog();
const closeStopDialog = () => app.closeStopDialog();
const stopServer = () => app.stopServer();
const switchPreviewTab = (tab) => app.switchPreviewTab(tab);
