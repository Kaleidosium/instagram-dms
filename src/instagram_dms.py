"""
instagram_dms
A focused WebView wrapper that restricts Instagram access to Direct Messages only.

This module creates a desktop window that loads Instagram's DM interface while
preventing navigation to other Instagram sections.
"""

import threading
import time
import logging
import webview

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramDMClient:
    """Manages the Instagram DM WebView client and its behavior."""

    DM_URL = "https://www.instagram.com/direct/inbox/"
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 800

    def __init__(self):
        """Initialize the Instagram DM client."""
        self.window = None

    def _inject_control_script(self):
        """Inject JavaScript to control UI and navigation."""
        try:
            self.window.evaluate_js(self._get_control_script())
            logger.info("JavaScript injected successfully.")
        except Exception as e:
            logger.error(f"Error injecting control script: {e}")

    @staticmethod
    def _get_control_script():
        """Return the JavaScript code for controlling the Instagram interface."""
        return r"""
            try {
                const DM_URL = 'https://www.instagram.com/direct/inbox/';

                function isAllowedUrl(url) {
                    // Allow all external links but restrict Instagram navigation to DMs and Authentication
                    const isDMSection = url.startsWith('https://www.instagram.com/direct');
                    const isLoginPage = url.startsWith('https://www.instagram.com/accounts/login');
                    const isChallengePage = url.startsWith('https://www.instagram.com/challenge');
                    const isTwoFactorPage = url.startsWith('https://www.instagram.com/two_factor');
                    const isOneTapPage = url.startsWith('https://www.instagram.com/accounts/onetap');
                    const isInstagram = url.startsWith('https://www.instagram.com');
                    return isDMSection || isLoginPage || isChallengePage || isTwoFactorPage || isOneTapPage || !isInstagram;  // Allow external or DM-related Instagram links
                }

                function isLoggedIn() {
                    const sessionId = document.cookie.match(/sessionid=([^;]*)/);
                    const sessionKey = localStorage.getItem('ds_user_id');
                    return !!sessionId && !!sessionKey;  // True only if both cookie and local storage are valid.
                }

                function handleInitialSetup() {
                    // Only run setup clicks if we're not logged in
                    if (isLoggedIn()) {
                        return;
                    }
                    
                    // Handle "Not Now" on Notifications Modal
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const notNowButton = buttons.find(button => button.textContent === 'Not Now');
                    if (notNowButton) {
                        console.log('Found Not Now button, clicking...');
                        notNowButton.click();
                    }
                }

                function forceRedirectToDMs() {
                    if (!isAllowedUrl(window.location.href)) {
                        window.location.href = DM_URL;
                    }
                }

                function applyCustomStyles() {
                    try {
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
                    } catch (error) {
                        console.error('Error applying custom styles:', error);
                    }
                }

                function enforceStrictControl() {
                    handleInitialSetup();
                    forceRedirectToDMs();
                    applyCustomStyles();
                }

                enforceStrictControl();

                const observer = new MutationObserver(() => {
                    enforceStrictControl();
                });

                observer.observe(document.body, {
                    childList: true,
                    subtree: true,
                });

                window.addEventListener('beforeunload', () => {
                    observer.disconnect(); // Ensure the observer is disconnected when the window unloads
                });

                window.addEventListener('click', function (e) {
                    const anchorTag = e.target.tagName === 'A' ? e.target : e.target.closest('a');
                    if (anchorTag) {
                        const href = anchorTag.href;
                        if (isAllowedUrl(href)) {
                            // Allow external links
                            e.preventDefault();
                            e.stopPropagation();
                            window.open(href, '_blank'); // Open external links in new tab
                        } else {
                            e.preventDefault();
                            e.stopPropagation();
                            forceRedirectToDMs(); // Redirect Instagram URLs that are not DMs
                        }
                    }
                }, true);
        } catch (error) {
            console.error('Error in main script: ', error);
        }
        """

    def _monitor_url(self):
        """Monitor and enforce URL restrictions."""
        self.window.load_url(self.DM_URL)
        minimized = False
        last_check_time = 0
        check_interval_seconds = 1

        def handle_minimized():
            nonlocal minimized
            minimized = True
            logger.info("Window minimized, suspending activity.")

        def handle_restored():
            nonlocal minimized
            minimized = False
            logger.info("Window restored, resuming normal activity.")

        self.window.events.minimized += handle_minimized
        self.window.events.restored += handle_restored

        while not self.window.events.closing:
            try:
                current_time = time.time()
                if not minimized:
                    if current_time - last_check_time >= check_interval_seconds:
                        last_check_time = current_time
                        current_url = self.window.get_current_url()
                        if not current_url.startswith("https://www.instagram.com/direct/"):
                            self.window.load_url(self.DM_URL)
                
                # Use a short sleep to reduce CPU usage
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error monitoring URL: {e}")
                time.sleep(1)  # Wait a bit longer if an error occurs

    def _on_loaded(self):
        """Handle window loaded event."""
        self._inject_control_script()

    def start(self):
        """Start the Instagram DM client."""
        self.window = webview.create_window(
            title="Instagram DMs",
            url=self.DM_URL,
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
            resizable=False,
        )

        self.window.events.loaded += self._on_loaded

        url_monitor = threading.Thread(target=self._monitor_url, daemon=True)
        url_monitor.start()

        webview.start(private_mode=True, http_server=True, http_port=13377)


if __name__ == "__main__":
    client = InstagramDMClient()
    client.start()
