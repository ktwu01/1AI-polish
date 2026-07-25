(() => {
    "use strict";

    const translations = {
        en: {
            title: "AI Academic Polisher",
            skip: "Skip to writing workspace",
            languageLabel: "中文",
            languageHref: "index_cn.html",
            headline: "Make every sentence earn its place.",
            subhead: "Refine academic prose while preserving your argument and voice.",
            workspaceLabel: "Academic polishing workspace",
            draft: "Draft",
            inputLabel: "Text to polish",
            placeholder: "Paste an academic paragraph, abstract, or research note…",
            characterUnit: "characters",
            shortcut: "⌘ / Ctrl + Enter to polish",
            modeLegend: "Polishing mode",
            modes: {
                academic: "Academic",
                formal: "Formal",
                casual: "Clear",
                creative: "Creative"
            },
            polish: "Polish draft",
            detect: "Check AI signals",
            clear: "Clear",
            output: "Polished version",
            waiting: "Waiting for draft",
            workingPolish: "Polishing…",
            workingDetect: "Analyzing…",
            ready: "Ready to copy",
            analysisReady: "Analysis ready",
            copy: "Copy text",
            copied: "Copied",
            emptyTitle: "Your revision will appear here.",
            emptyText: "Add a draft, choose a mode, and polish when you are ready.",
            loadingPolishTitle: "Refining your draft",
            loadingPolishText: "DeepSeek-R1 is reviewing structure, clarity, and voice.",
            loadingDetectTitle: "Reading for AI signals",
            loadingDetectText: "The analysis may take a few moments.",
            reasoning: "Review editorial notes",
            demoTitle: "Demo response",
            demoText: "This result is simulated. Configure an API key on the backend to use DeepSeek-R1.",
            metaSignal: "AI signal",
            metaTime: "Time",
            metaMode: "Mode",
            metaService: "Service",
            secondUnit: "sec",
            unknown: "Unknown",
            requiredPolish: "Add some text before polishing your draft.",
            requiredDetect: "Add some text before checking AI signals.",
            processError: "The draft could not be polished",
            detectError: "The AI signal check could not be completed",
            clipboardError: "Copying was blocked by the browser. Select the result and copy it manually.",
            emptyResult: "The service returned an empty result.",
            detectionTitle: "AI signal check",
            confidence: "Confidence",
            confidenceLevels: {
                low: "Low",
                medium: "Medium",
                high: "High"
            },
            detectionSummary: "This is a probabilistic signal, not proof of authorship.",
            patternScore: "Pattern score",
            complexityScore: "Complexity score",
            semanticScore: "Semantic score",
            note: "DeepSeek-R1 processing through FastAPI",
            railLabels: ["structure", "clarity", "voice"]
        },
        zh: {
            title: "AI 学术润色",
            skip: "跳转到写作工作区",
            languageLabel: "English",
            languageHref: "index.html",
            headline: "让每一句话都有分量。",
            subhead: "在保留论点与个人表达的同时，让学术写作更准确、更清晰。",
            workspaceLabel: "学术润色工作区",
            draft: "原始文本",
            inputLabel: "需要润色的文本",
            placeholder: "粘贴论文段落、摘要或研究笔记…",
            characterUnit: "字符",
            shortcut: "⌘ / Ctrl + Enter 开始润色",
            modeLegend: "润色模式",
            modes: {
                academic: "学术",
                formal: "正式",
                casual: "清晰",
                creative: "创意"
            },
            polish: "润色文本",
            detect: "检测 AI 痕迹",
            clear: "清空",
            output: "润色结果",
            waiting: "等待输入",
            workingPolish: "正在润色…",
            workingDetect: "正在分析…",
            ready: "可以复制",
            analysisReady: "分析完成",
            copy: "复制文本",
            copied: "已复制",
            emptyTitle: "润色结果会显示在这里。",
            emptyText: "输入文本并选择模式，准备好后即可开始润色。",
            loadingPolishTitle: "正在精炼文本",
            loadingPolishText: "DeepSeek-R1 正在检查结构、清晰度和表达方式。",
            loadingDetectTitle: "正在分析 AI 痕迹",
            loadingDetectText: "分析可能需要一点时间。",
            reasoning: "查看编辑说明",
            demoTitle: "演示结果",
            demoText: "当前结果为模拟数据。请在后端配置 API 密钥以使用 DeepSeek-R1。",
            metaSignal: "AI 痕迹",
            metaTime: "用时",
            metaMode: "模式",
            metaService: "服务",
            secondUnit: "秒",
            unknown: "未知",
            requiredPolish: "请先输入需要润色的文本。",
            requiredDetect: "请先输入需要检测的文本。",
            processError: "无法完成文本润色",
            detectError: "无法完成 AI 痕迹检测",
            clipboardError: "浏览器阻止了复制操作，请选中结果后手动复制。",
            emptyResult: "服务未返回润色结果。",
            detectionTitle: "AI 痕迹检测",
            confidence: "置信度",
            confidenceLevels: {
                low: "低",
                medium: "中",
                high: "高"
            },
            detectionSummary: "该结果仅为概率信号，不能作为作者身份的确定证据。",
            patternScore: "模式得分",
            complexityScore: "复杂度得分",
            semanticScore: "语义得分",
            note: "由 FastAPI 调用 DeepSeek-R1 处理",
            railLabels: ["结构", "清晰", "表达"]
        }
    };

    const icon = (name) => {
        const icons = {
            feather: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M20.2 3.8c-3.9-.7-7.4.3-10.1 3-2.8 2.8-3.8 6.4-3.1 10.5 4 .7 7.6-.4 10.3-3.2 2.7-2.8 3.7-6.3 2.9-10.3Z" stroke="currentColor" stroke-width="1.7"/>
                    <path d="M4 21 17.5 7.4M8.2 16.7h4.1M11.2 13.7l.1-4.2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                </svg>`,
            globe: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.6"/>
                    <path d="M3.8 12h16.4M12 3.5c2.2 2.3 3.2 5.1 3.2 8.5S14.2 18.2 12 20.5C9.8 18.2 8.8 15.4 8.8 12S9.8 5.8 12 3.5Z" stroke="currentColor" stroke-width="1.6"/>
                </svg>`,
            book: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M4 5.8c2.7-.7 5.3-.2 8 1.4v12c-2.7-1.6-5.3-2.1-8-1.4v-12Zm16 0c-2.7-.7-5.3-.2-8 1.4v12c2.7-1.6 5.3-2.1 8-1.4v-12Z" stroke="currentColor" stroke-linejoin="round"/>
                </svg>`,
            formal: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="m3 9 9-5 9 5H3Zm2 2h14M6 11v6m4-6v6m4-6v6m4-6v6M4 20h16" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>`,
            sparkles: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M12 3c.4 3.6 2.4 5.6 6 6-3.6.4-5.6 2.4-6 6-.4-3.6-2.4-5.6-6-6 3.6-.4 5.6-2.4 6-6Zm6 11.5c.2 1.7 1.2 2.7 3 3-1.8.3-2.8 1.3-3 3-.2-1.7-1.2-2.7-3-3 1.8-.3 2.8-1.3 3-3ZM5.2 15c.2 1.2.9 1.9 2.1 2.1-1.2.2-1.9.9-2.1 2.1C5 18 4.3 17.3 3.1 17.1c1.2-.2 1.9-.9 2.1-2.1Z" stroke="currentColor" stroke-linejoin="round"/>
                </svg>`,
            bulb: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M8.3 15.6A7 7 0 1 1 15.7 15.6c-.8.6-1.2 1.5-1.2 2.4h-5c0-.9-.4-1.8-1.2-2.4ZM9.5 21h5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>`,
            wand: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="m4 20 10.2-10.2m-3-3 3 3m-4.9 3.9 3 3M17 3v3m-1.5-1.5h3M20 10v2m-1-1h2M8 3v2M7 4h2" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>`,
            pulse: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M2.5 12h4l2-6 3.4 12 2.5-8 1.8 2h5.3" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>`,
            copy: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <rect x="8" y="7" width="11" height="13" rx="1.8" stroke="currentColor"/>
                    <path d="M16 7V5.8C16 4.8 15.2 4 14.2 4H5.8C4.8 4 4 4.8 4 5.8v10.4C4 17.2 4.8 18 5.8 18H8" stroke="currentColor"/>
                </svg>`,
            alert: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M12 3 2.8 20h18.4L12 3Z" stroke="currentColor" stroke-linejoin="round"/>
                    <path d="M12 9v5m0 3.2v.1" stroke="currentColor" stroke-linecap="round"/>
                </svg>`,
            arrow: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M3 12h17m-5-5 5 5-5 5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>`,
            chart: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M4 20V10h4v10m2 0V4h4v16m2 0v-7h4v7M2.5 20.5h19" stroke="currentColor" stroke-linejoin="round"/>
                </svg>`,
            clock: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <circle cx="12" cy="12" r="9" stroke="currentColor"/>
                    <path d="M12 7v5l3.2 2" stroke="currentColor" stroke-linecap="round"/>
                </svg>`,
            branch: `
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <circle cx="6" cy="5" r="2" stroke="currentColor"/>
                    <circle cx="18" cy="8" r="2" stroke="currentColor"/>
                    <circle cx="18" cy="18" r="2" stroke="currentColor"/>
                    <path d="M6 7v8a3 3 0 0 0 3 3h7M6 11h7a3 3 0 0 0 3-3" stroke="currentColor"/>
                </svg>`
        };
        return icons[name] || "";
    };

    const language = document.documentElement.lang.toLowerCase().startsWith("zh") ? "zh" : "en";
    const t = translations[language];
    const root = document.querySelector(".container");

    if (!root) {
        document.documentElement.classList.remove("redesign-pending");
        return;
    }

    document.title = t.title;

    const modes = [
        ["academic", "book"],
        ["formal", "formal"],
        ["casual", "sparkles"],
        ["creative", "bulb"]
    ];

    root.className = "app-root";
    root.innerHTML = `
        <a class="skip-link" href="#writing-workspace">${t.skip}</a>
        <header class="topbar">
            <a class="brand" href="#" aria-label="${t.title}">
                <span class="brand-mark">${icon("feather")}</span>
                <span class="brand-name">${t.title}</span>
            </a>
            <a class="language-link" href="${t.languageHref}" hreflang="${language === "en" ? "zh" : "en"}">
                ${icon("globe")}
                <span>${t.languageLabel}</span>
            </a>
        </header>

        <main class="page-shell" id="main-content">
            <section class="intro" aria-labelledby="page-title">
                <h1 id="page-title">${t.headline}</h1>
                <p>${t.subhead}</p>
            </section>

            <div class="error-banner" id="errorBanner" role="alert" tabindex="-1" hidden>
                ${icon("alert")}
                <span id="errorText"></span>
            </div>

            <section class="workspace" id="writing-workspace" aria-label="${t.workspaceLabel}">
                <form class="workspace-panel draft-panel" id="polishForm" novalidate>
                    <div class="panel-header">
                        <h2>${t.draft}</h2>
                    </div>

                    <div class="editor-frame">
                        <label class="sr-only" for="textInput">${t.inputLabel}</label>
                        <textarea id="textInput" name="content" maxlength="10000" placeholder="${t.placeholder}" spellcheck="true"></textarea>
                        <div class="editor-meta">
                            <span id="characterCount">0 / 10,000 ${t.characterUnit}</span>
                            <span class="shortcut">${t.shortcut}</span>
                        </div>
                    </div>

                    <fieldset class="mode-fieldset">
                        <legend>${t.modeLegend}</legend>
                        <div class="mode-grid">
                            ${modes.map(([value, iconName], index) => `
                                <div class="mode-option">
                                    <input type="radio" name="style" id="style-${value}" value="${value}" ${index === 0 ? "checked" : ""}>
                                    <label for="style-${value}">
                                        ${icon(iconName)}
                                        <span>${t.modes[value]}</span>
                                    </label>
                                </div>
                            `).join("")}
                        </div>
                    </fieldset>

                    <div class="action-row">
                        <button class="action-button action-primary" id="processBtn" type="submit">
                            ${icon("wand")}
                            <span>${t.polish}</span>
                        </button>
                        <button class="action-button action-secondary" id="detectBtn" type="button">
                            ${icon("pulse")}
                            <span>${t.detect}</span>
                        </button>
                        <button class="action-button action-quiet" id="clearBtn" type="button">${t.clear}</button>
                    </div>
                </form>

                <div class="proof-rail" aria-hidden="true">
                    ${t.railLabels.map((label) => `
                        <div class="proof-mark">
                            <span class="proof-line"></span>
                            <span>${label}</span>
                            ${icon("arrow")}
                        </div>
                    `).join("")}
                </div>

                <article class="workspace-panel output-panel" aria-labelledby="outputTitle">
                    <div class="panel-header">
                        <h2 id="outputTitle">${t.output}</h2>
                        <div class="output-actions">
                            <span class="result-status" id="resultStatus" data-state="idle">${t.waiting}</span>
                            <button class="copy-button" id="copyBtn" type="button" disabled>
                                ${icon("copy")}
                                <span data-copy-label>${t.copy}</span>
                            </button>
                        </div>
                    </div>

                    <div class="output-stage" id="outputStage" aria-live="polite" aria-busy="false">
                        <div class="empty-state" id="emptyState">
                            <div class="empty-state-inner">
                                <span class="empty-state-icon">${icon("feather")}</span>
                                <h3>${t.emptyTitle}</h3>
                                <p>${t.emptyText}</p>
                            </div>
                        </div>

                        <div class="loading-state" id="loadingState" hidden>
                            <div class="loading-state-inner">
                                <div class="spinner" aria-hidden="true"></div>
                                <h3 id="loadingTitle">${t.loadingPolishTitle}</h3>
                                <p id="loadingText">${t.loadingPolishText}</p>
                            </div>
                        </div>

                        <div class="demo-notice" id="demoNotice" hidden>
                            ${icon("alert")}
                            <span><strong>${t.demoTitle}.</strong> ${t.demoText}</span>
                        </div>

                        <div class="result-prose" id="resultText" hidden></div>
                    </div>

                    <details class="reasoning-disclosure" id="reasoningSection" hidden>
                        <summary>${t.reasoning}</summary>
                        <div class="reasoning-content" id="reasoningContent"></div>
                    </details>
                </article>
            </section>

            <dl class="result-meta" id="resultMeta" hidden>
                <div class="meta-item">
                    ${icon("chart")}
                    <dt>${t.metaSignal}</dt>
                    <dd id="aiProbability">—</dd>
                </div>
                <div class="meta-item">
                    ${icon("clock")}
                    <dt>${t.metaTime}</dt>
                    <dd id="processingTime">—</dd>
                </div>
                <div class="meta-item">
                    ${icon("book")}
                    <dt>${t.metaMode}</dt>
                    <dd id="styleUsed">—</dd>
                </div>
                <div class="meta-item">
                    ${icon("branch")}
                    <dt>${t.metaService}</dt>
                    <dd id="apiUsed">—</dd>
                </div>
            </dl>

            <p class="page-note">${t.note}</p>
        </main>
    `;

    document.documentElement.classList.remove("redesign-pending");

    const defaultApiUrl = "https://oneai-polish.onrender.com";
    const previewApiUrl = new URLSearchParams(window.location.search).get("api");
    const isLocalPreview = ["127.0.0.1", "localhost", "::1"].includes(window.location.hostname);
    const WORKSPACE_API_URL = isLocalPreview && previewApiUrl
        ? previewApiUrl.replace(/\/+$/, "")
        : defaultApiUrl;
    const textInput = document.getElementById("textInput");
    const polishForm = document.getElementById("polishForm");
    const processBtn = document.getElementById("processBtn");
    const detectBtn = document.getElementById("detectBtn");
    const clearBtn = document.getElementById("clearBtn");
    const copyBtn = document.getElementById("copyBtn");
    const copyLabel = copyBtn.querySelector("[data-copy-label]");
    const characterCount = document.getElementById("characterCount");
    const errorBanner = document.getElementById("errorBanner");
    const errorText = document.getElementById("errorText");
    const outputStage = document.getElementById("outputStage");
    const emptyState = document.getElementById("emptyState");
    const loadingState = document.getElementById("loadingState");
    const loadingTitle = document.getElementById("loadingTitle");
    const loadingText = document.getElementById("loadingText");
    const demoNotice = document.getElementById("demoNotice");
    const resultText = document.getElementById("resultText");
    const resultStatus = document.getElementById("resultStatus");
    const reasoningSection = document.getElementById("reasoningSection");
    const reasoningContent = document.getElementById("reasoningContent");
    const resultMeta = document.getElementById("resultMeta");
    const aiProbability = document.getElementById("aiProbability");
    const processingTime = document.getElementById("processingTime");
    const styleUsed = document.getElementById("styleUsed");
    const apiUsed = document.getElementById("apiUsed");
    let activeController = null;
    let lastCopyText = "";

    const selectedStyle = () => polishForm.elements.style.value || "academic";

    const formatPercentage = (value) => {
        const number = Number(value);
        return Number.isFinite(number) ? `${(number * 100).toFixed(1)}%` : t.unknown;
    };

    const formatSeconds = (value) => {
        const number = Number(value);
        return Number.isFinite(number) ? `${number.toFixed(1)} ${t.secondUnit}` : t.unknown;
    };

    const setStatus = (text, state = "idle") => {
        resultStatus.textContent = text;
        resultStatus.dataset.state = state;
    };

    const updateCounter = () => {
        const length = textInput.value.length;
        characterCount.textContent = `${length.toLocaleString(language === "zh" ? "zh-CN" : "en-US")} / 10,000 ${t.characterUnit}`;
    };

    const showError = (heading, detail = "") => {
        errorText.textContent = detail ? `${heading}: ${detail}` : heading;
        errorBanner.hidden = false;
        errorBanner.focus({ preventScroll: true });
        errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
    };

    const clearError = () => {
        errorBanner.hidden = true;
        errorText.textContent = "";
    };

    const safeMarkdown = (element, source) => {
        const value = String(source || "");
        if (window.marked && window.DOMPurify) {
            element.innerHTML = window.DOMPurify.sanitize(window.marked.parse(value), {
                USE_PROFILES: { html: true }
            });
        } else {
            element.textContent = value;
        }
    };

    const setBusy = (busy, action = "polish") => {
        outputStage.setAttribute("aria-busy", String(busy));
        processBtn.disabled = busy;
        detectBtn.disabled = busy;

        if (!busy) {
            return;
        }

        emptyState.hidden = true;
        resultText.hidden = true;
        demoNotice.hidden = true;
        reasoningSection.hidden = true;
        reasoningSection.open = false;
        resultMeta.hidden = true;
        copyBtn.disabled = true;
        loadingState.hidden = false;

        const detecting = action === "detect";
        loadingTitle.textContent = detecting ? t.loadingDetectTitle : t.loadingPolishTitle;
        loadingText.textContent = detecting ? t.loadingDetectText : t.loadingPolishText;
        setStatus(detecting ? t.workingDetect : t.workingPolish, "working");
    };

    const resetOutput = () => {
        lastCopyText = "";
        copyBtn.disabled = true;
        copyLabel.textContent = t.copy;
        loadingState.hidden = true;
        resultText.hidden = true;
        resultText.textContent = "";
        resultText.classList.remove("detection-result");
        demoNotice.hidden = true;
        emptyState.hidden = false;
        reasoningSection.hidden = true;
        reasoningSection.open = false;
        reasoningContent.textContent = "";
        resultMeta.hidden = true;
        setStatus(t.waiting, "idle");
        outputStage.setAttribute("aria-busy", "false");
    };

    const getContent = (action) => {
        const content = textInput.value.trim();
        if (content) {
            return content;
        }

        showError(action === "detect" ? t.requiredDetect : t.requiredPolish);
        textInput.focus();
        return null;
    };

    const requestJson = async (endpoint, payload, signal) => {
        const response = await fetch(`${WORKSPACE_API_URL}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload),
            signal
        });

        let result = null;
        try {
            result = await response.json();
        } catch {
            result = null;
        }

        if (!response.ok) {
            const detail = result?.message || result?.detail || `${response.status} ${response.statusText}`;
            throw new Error(detail);
        }

        return result || {};
    };

    const setMeta = ({ signal, time, mode, service }) => {
        aiProbability.textContent = signal;
        processingTime.textContent = time;
        styleUsed.textContent = mode;
        apiUsed.textContent = service;
        resultMeta.hidden = false;
    };

    const renderPolishResult = (result) => {
        const processedText = String(result.processed_text || t.emptyResult);
        const mode = result.style_used || selectedStyle();
        const service = result.api_used || "DeepSeek-R1";
        const reasoning = result.reasoning_content || result.reasoning || "";

        loadingState.hidden = true;
        emptyState.hidden = true;
        resultText.classList.remove("detection-result");
        safeMarkdown(resultText, processedText);
        resultText.hidden = false;
        lastCopyText = resultText.innerText.trim();
        copyBtn.disabled = !lastCopyText;
        copyLabel.textContent = t.copy;

        if (reasoning) {
            safeMarkdown(reasoningContent, reasoning);
            reasoningSection.hidden = false;
        } else {
            reasoningSection.hidden = true;
            reasoningContent.textContent = "";
        }

        const isDemo = /Demo Mode|演示模式/i.test(service);
        demoNotice.hidden = !isDemo;

        setMeta({
            signal: formatPercentage(result.ai_probability),
            time: formatSeconds(result.processing_time),
            mode: t.modes[mode] || mode || t.unknown,
            service
        });
        setStatus(t.ready, "ready");
        outputStage.setAttribute("aria-busy", "false");
    };

    const renderDetectionResult = (result) => {
        const signal = formatPercentage(result.ai_probability);
        const confidenceKey = String(result.confidence_level || "low").toLowerCase();
        const confidence = t.confidenceLevels[confidenceKey] || result.confidence_level || t.unknown;
        const analysis = result.analysis || {};
        const scores = [
            [t.patternScore, Number(analysis.pattern_score)],
            [t.complexityScore, Number(analysis.complexity_score)],
            [t.semanticScore, Number(analysis.semantic_score)]
        ];

        loadingState.hidden = true;
        emptyState.hidden = true;
        demoNotice.hidden = true;
        reasoningSection.hidden = true;
        resultText.classList.add("detection-result");
        resultText.innerHTML = `
            <div class="detection-heading">
                <h3>${t.detectionTitle}</h3>
                <span class="signal-value"></span>
            </div>
            <p class="detection-summary"></p>
            <dl class="score-list">
                ${scores.map(([label, score]) => {
                    const percentage = Number.isFinite(score) ? Math.max(0, Math.min(100, score * 100)) : 0;
                    return `
                        <div class="score-row">
                            <dt>${label}</dt>
                            <dd class="score-bar" aria-hidden="true"><span style="--score: ${percentage.toFixed(1)}%"></span></dd>
                            <dd class="score-number">${Number.isFinite(score) ? `${percentage.toFixed(1)}%` : "—"}</dd>
                        </div>
                    `;
                }).join("")}
            </dl>
        `;
        resultText.querySelector(".signal-value").textContent = signal;
        resultText.querySelector(".detection-summary").textContent = `${t.confidence}: ${confidence}. ${t.detectionSummary}`;
        resultText.hidden = false;
        lastCopyText = resultText.innerText.trim();
        copyBtn.disabled = false;
        copyLabel.textContent = t.copy;

        setMeta({
            signal,
            time: formatSeconds(result.processing_time),
            mode: t.detect,
            service: "DeepSeek-R1"
        });
        setStatus(t.analysisReady, "ready");
        outputStage.setAttribute("aria-busy", "false");
    };

    const runAction = async (action) => {
        const content = getContent(action);
        if (!content) {
            return;
        }

        clearError();
        activeController?.abort();
        activeController = new AbortController();
        setBusy(true, action);

        try {
            if (action === "detect") {
                const result = await requestJson("/api/v1/detect", { content }, activeController.signal);
                renderDetectionResult(result);
            } else {
                const result = await requestJson(
                    "/api/v1/process",
                    { content, style: selectedStyle() },
                    activeController.signal
                );
                renderPolishResult(result);
            }
        } catch (error) {
            if (error.name === "AbortError") {
                return;
            }
            resetOutput();
            showError(action === "detect" ? t.detectError : t.processError, error.message);
        } finally {
            setBusy(false);
            activeController = null;
        }
    };

    polishForm.addEventListener("submit", (event) => {
        event.preventDefault();
        runAction("polish");
    });

    detectBtn.addEventListener("click", () => runAction("detect"));

    clearBtn.addEventListener("click", () => {
        activeController?.abort();
        activeController = null;
        textInput.value = "";
        updateCounter();
        clearError();
        resetOutput();
        processBtn.disabled = false;
        detectBtn.disabled = false;
        textInput.focus();
    });

    copyBtn.addEventListener("click", async () => {
        if (!lastCopyText) {
            return;
        }

        try {
            await navigator.clipboard.writeText(lastCopyText);
            copyLabel.textContent = t.copied;
            window.setTimeout(() => {
                copyLabel.textContent = t.copy;
            }, 1800);
        } catch {
            showError(t.clipboardError);
        }
    });

    textInput.addEventListener("input", updateCounter);
    textInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
            event.preventDefault();
            polishForm.requestSubmit();
        }
    });

    updateCounter();
})();
