function initTheme() {
    const storedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    const theme = storedTheme || systemTheme;

    document.documentElement.setAttribute('data-theme', theme);
    // Wait for DOM to update icon
    setTimeout(() => updateIcon(theme), 50);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateIcon(next);
}

function updateIcon(theme) {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    const icon = btn.querySelector('i');
    if (theme === 'dark') {
        icon.className = 'fas fa-moon';
    } else {
        icon.className = 'fas fa-sun';
    }
}

// Inject Toggle Button into Navbar if not present
function injectThemeToggle() {
    const nav = document.querySelector('.nav-links');
    if (nav && !document.getElementById('theme-toggle')) {
        const btn = document.createElement('button');
        btn.id = 'theme-toggle';
        btn.className = 'nav-btn';
        btn.innerHTML = '<i class="fas fa-moon"></i>'; // Default icon
        btn.onclick = toggleTheme;
        btn.setAttribute('aria-label', 'Toggle theme');
        nav.appendChild(btn);

        const current = document.documentElement.getAttribute('data-theme');
        updateIcon(current);
    }
}

async function loadReadme(path) {
    const container = document.getElementById("md");
    if (!container) return;

    try {
        container.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--text-secondary);">Loading documentation...</div>';

        const res = await fetch(path, { cache: "no-store" });
        if (!res.ok) throw new Error(`Could not load ${path} (Status: ${res.status})`);

        const md = await res.text();

        // Configure Marked
        marked.setOptions({
            breaks: true,
            gfm: true,
            headerIds: true
        });

        const html = marked.parse(md);
        container.innerHTML = html;

        // Apply syntax highlighting and add copy buttons
        document.querySelectorAll("pre code").forEach((block) => {
            hljs.highlightElement(block);
            addCopyButton(block);
        });

    } catch (err) {
        container.innerHTML = `
            <div style="text-align:center; padding: 40px; color: #e5534b;">
                <h3 style="color:inherit">Error Loading Documentation</h3>
                <pre style="background:rgba(229,83,75,0.1); color:inherit; border-color: rgba(229,83,75,0.3);">${err.message}</pre>
                <p style="color:var(--text-secondary)">Please check that <code>README.md</code> exists in this directory.</p>
            </div>
        `;
    }
}

function addCopyButton(codeBlock) {
    const pre = codeBlock.parentNode;

    // Wrap pre in relative container
    const wrapper = document.createElement('div');
    wrapper.className = 'code-wrapper';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    // Create Button
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.innerHTML = '<i class="far fa-copy"></i>';
    btn.onclick = () => {
        navigator.clipboard.writeText(codeBlock.textContent).then(() => {
            btn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => btn.innerHTML = '<i class="far fa-copy"></i>', 2000);
        });
    };

    wrapper.appendChild(btn);
}

// Initialize
initTheme();
document.addEventListener('DOMContentLoaded', () => {
    injectThemeToggle();
});
