import webview
import time
import threading

def inject_js(window):
    window.evaluate_js(
        r"""
        const DM_URL = 'https://www.instagram.com/direct/inbox/';

        function isAllowedUrl(url) {
            // Allow all external links but restrict Instagram navigation to DMs
            const isDMSection = url.startsWith('https://www.instagram.com/direct/');
            const isInstagram = url.startsWith('https://www.instagram.com/');
            return isDMSection || !isInstagram;  // Allow external or DM-related Instagram links
        }

        function forceRedirectToDMs() {
            if (!isAllowedUrl(window.location.href)) {
                window.location.href = DM_URL;
                return true;
            }
            return false;
        }

        function applyCustomStyles() {
            const htmlElement = document.querySelector('html');
            if (htmlElement) { 
                htmlElement.style.msOverflowStyle = 'none';
                htmlElement.style.scrollbarWidth = 'none';
            }

            if (!document.getElementById('hide-scrollbar-y-style')) {
                const style = document.createElement('style');
                style.id = 'hide-scrollbar-y-style';
                style.textContent = 'html::-webkit-scrollbar { display: none !important; }';
                document.head.appendChild(style);
            }

            const weirdBottomMargin = document.querySelector('div.html-div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa');
            if (weirdBottomMargin) { weirdBottomMargin.style.margin = '0'; }

            const frameWidthAndHeight = document.querySelector('div.html-div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa > section > main > section > div > div > div');
            if (frameWidthAndHeight) { frameWidthAndHeight.style.height = '100%'; frameWidthAndHeight.style.width = '100%'; }

            const charmsbar = document.querySelector('div.html-div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xixxii4.x1ey2m1c.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.xg7h5cd.xh8yej3.xhtitgo.x6w1myc.x1jeouym');
            if (charmsbar) { charmsbar.style.display = 'none'; }
        }

        function removeNonDMElements() {
            const navBar = document.querySelector('nav');
            if (navBar) navBar.remove();

            document.querySelectorAll('[href*="explore"], [aria-label*="explore"], [data-testid*="explore"]').forEach(el => el.remove());

            document.querySelectorAll('[href*="profile"], [aria-label*="profile"], [data-testid*="profile"], [href*="search"], [aria-label*="search"], [data-testid*="search"]').forEach(el => el.remove());
        }

        function enforceStrictControl() {
            if (forceRedirectToDMs()) return;
            applyCustomStyles();
            removeNonDMElements();
        }

        enforceStrictControl();

        const observer = new MutationObserver((mutations) => {
            enforceStrictControl();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            characterData: true
        });

        window.addEventListener('click', function(e) {
            const anchorTag = e.target.tagName === 'A' ? e.target : e.target.closest('a');
            if (anchorTag) {
                const href = anchorTag.href;
                if (!isAllowedUrl(href)) {
                    e.preventDefault();
                    e.stopPropagation();
                    forceRedirectToDMs();  // Redirect Instagram URLs that are not DMs
                } else if (!href.startsWith('https://www.instagram.com/')) {
                    // Allow external links
                    e.preventDefault();
                    e.stopPropagation();
                    window.open(href, '_blank'); // Open external links in new tab
                }
            }
        }, true);

        ['pushState', 'replaceState'].forEach(func => {
            const original = history[func];
            history[func] = function () {
                const result = original.apply(this, arguments);
                enforceStrictControl();
                return result;
            };
        });

        window.addEventListener('popstate', function() {
            enforceStrictControl();
        });

        window.addEventListener('hashchange', function(e) {
            e.preventDefault();
            enforceStrictControl();
        });

        setInterval(enforceStrictControl, 1000);

        window.checkDMContent = function() {
            const dmContent = document.querySelector('div[aria-label="Direct messaging"]');
            return !!dmContent;
        };
        """
    )

def is_allowed_url(url):
    return url.startswith('https://www.instagram.com/direct/')

def check_url_and_content(window):
    try:
        current_url = window.get_current_url()
        if not is_allowed_url(current_url):
            print(f"Redirecting from {current_url} to direct inbox")
            window.load_url("https://www.instagram.com/direct/inbox/")
        else:
            # Check if we're actually in the DM content
            is_dm_content = window.evaluate_js('window.checkDMContent()')
            if not is_dm_content:
                print("DM content not detected, redirecting")
                window.load_url("https://www.instagram.com/direct/inbox/")
    except Exception as e:
        print(f"Error checking URL and content: {str(e)}")

def load_url(window):
    window.load_url("https://www.instagram.com/direct/inbox/")
    time.sleep(5)  # Give some time for the page to load

    while not window.events.closing:
        check_url_and_content(window)
        time.sleep(1)  # Check every second

def on_loaded(window):
    inject_js(window)


if __name__ == "__main__":
    window = webview.create_window(
        "Instagram DMs",
        "https://www.instagram.com/direct/inbox/",
        width=600,
        height=800,
        resizable=False,
    )

    window.events.loaded += on_loaded

    url_thread = threading.Thread(target=load_url, args=(window,))
    url_thread.daemon = True
    url_thread.start()

    webview.start(
        private_mode=False,
        http_server=True,
        http_port=13377,
    )
