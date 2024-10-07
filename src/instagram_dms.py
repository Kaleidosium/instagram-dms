import webview
import time


def inject_js(window):
    window.evaluate_js(
        r"""
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

        function redirectToInbox() {
            const directUrl = 'https://www.instagram.com/direct/';
            if (!window.location.href.includes(directUrl) && window.location.href.startsWith('https://www.instagram.com/')) {
                window.location.href = directUrl;
                return true;
            }
            return false;
        }

        // Run the functions immediately
        redirectToInbox();
        applyCustomStyles();

        // Use MutationObserver to watch for DOM changes
        const observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                if (mutation.type === 'childList' || mutation.type === 'subtree') {
                    if (redirectToInbox()) {
                        break;
                    }
                    applyCustomStyles();
                    break;
                }
            }
        });

        // Configure the observer to watch for changes in the body and its descendants
        if (document.body) {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        } else {
            console.error('Document body not found');
        }

        // Listen for URL changes (for single-page app navigation)
        let lastUrl = location.href; 
        const urlObserver = new MutationObserver(() => {
            const url = location.href;
            if (url !== lastUrl) {
                lastUrl = url;
                if (!redirectToInbox()) {
                    applyCustomStyles();
                }
            }
        });

        if (document.documentElement) {
            urlObserver.observe(document.documentElement, {childList: true, subtree: true});
        } else {
            console.error('Document element not found');
        }

        // Intercept link clicks
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (link && link.href.startsWith('https://www.instagram.com/') && !link.href.includes('/direct/')) {
                e.preventDefault();
                redirectToInbox();
            }
        }, true);


        """
    )


def check_url(window):
    try:
        current_url = window.evaluate_js("window.location.href")
        if (
            current_url
            and not current_url.startswith("https://www.instagram.com/direct/")
            and current_url.startswith("https://www.instagram.com/")
        ):
            window.load_url("https://www.instagram.com/direct/inbox/")
    except Exception as e:
        print(f"Error checking URL: {str(e)}")


def load_url(window):
    window.load_url("https://www.instagram.com/direct/inbox/")

    # Give some time for the page to load before starting the URL checking loop

    time.sleep(5)

    while True:
        check_url(window)
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

    # We need to explicitly set a http port to persist cookies between sessions

    webview.start(
        func=load_url,
        args=window,
        private_mode=False,
        http_server=True,
        http_port=13377,
    )
