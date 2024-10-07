import webview


def inject_js(window):
    window.evaluate_js(
        r"""
        function applyCustomStyles() {
            if (!window.location.href.includes('/direct/inbox')) {
                return;  // Exit if not on the inbox page
            }

            console.log('Applying custom styles...');


            var htmlElement = document.querySelector('html');
            if (htmlElement) { 
                htmlElement.style.msOverflowStyle = 'none';
                htmlElement.style.scrollbarWidth = 'none';
            }
            
            const style = document.createElement('style');
            style.textContent = 'html::-webkit-scrollbar { display: none !important; }';
            document.head.appendChild(style);

            var weirdBottomMargin = document.querySelector('div.html-div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa');
            if (weirdBottomMargin) { weirdBottomMargin.style.margin = '0'; }

            var frameWidthAndHeight = document.querySelector('div.html-div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x1v4esvl.x8vgawa > section > main > section > div > div > div');
            if (frameWidthAndHeight) { frameWidthAndHeight.style.height = '100%'; frameWidthAndHeight.style.width = '100%'; }

            var charmsbar = document.querySelector('div.html-div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xixxii4.x1ey2m1c.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.xg7h5cd.xh8yej3.xhtitgo.x6w1myc.x1jeouym');
            if (charmsbar) { charmsbar.style.display = 'none'; }
        }

        // Run the function immediately
        applyCustomStyles();

        // Set up an interval to run the function every second
        setInterval(applyCustomStyles, 1000);
        """
    )


def load_url(window):
    window.load_url("https://www.instagram.com/direct/inbox/")


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
