function showPopup() {
    const popup = document.getElementById("auth-popup");
    if (popup) popup.classList.remove("hidden");
}

function closePopup() {
    const popup = document.getElementById("auth-popup");
    if (popup) popup.classList.add("hidden");
}

function getCSRFToken() {
    const name = "csrftoken";
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

/* =========================
   SCROLL-REVEAL (IntersectionObserver)
========================= */
function initScrollReveal() {
    const revealEls = document.querySelectorAll(".reveal, .reveal-scale, .reveal-left, .reveal-right");
    if (!revealEls.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("revealed");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: "0px 0px -40px 0px"
    });

    revealEls.forEach(el => observer.observe(el));
}

/* =========================
   NAVBAR SCROLL BEHAVIOR
========================= */
function initNavbarScroll() {
    const navbar = document.querySelector(".custom-navbar");
    if (!navbar) return;

    let lastScroll = 0;
    const scrollThreshold = 60;

    window.addEventListener("scroll", () => {
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > scrollThreshold) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }

        lastScroll = currentScroll;
    }, { passive: true });
}

/* =========================
   BACK-TO-TOP BUTTON
========================= */
function initBackToTop() {
    const btn = document.getElementById("back-to-top");
    if (!btn) return;

    const toggle = () => {
        if ((window.pageYOffset || document.documentElement.scrollTop) > 500) {
            btn.classList.add("visible");
        } else {
            btn.classList.remove("visible");
        }
    };

    window.addEventListener("scroll", toggle, { passive: true });

    btn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}

/* =========================
   MOBILE HAMBURGER TOGGLE
========================= */
function initMobileHamburger() {
    const toggler = document.querySelector(".custom-toggler");
    const drawer = document.getElementById("mobileMenu");
    if (!toggler || !drawer) return;

    drawer.addEventListener("show.bs.offcanvas", () => {
        toggler.classList.add("active");
    });

    drawer.addEventListener("hide.bs.offcanvas", () => {
        toggler.classList.remove("active");
    });
}

/* =========================
   BUTTON SPOTLIGHT EFFECT
========================= */
function initButtonSpotlight() {
    const buttons = document.querySelectorAll(".btn, .auth-btn, .view-btn, .login-btn, .signup-btn, .add-to-cart, .checkout-btn, .shop-btn");

    buttons.forEach(btn => {
        btn.addEventListener("mousemove", (e) => {
            const rect = btn.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            btn.style.setProperty("--x", x + "%");
            btn.style.setProperty("--y", y + "%");
        });
    });
}

/* =========================
   SCROLL PROGRESS TRACKER
========================= */
function initScrollProgress() {
    const progressBar = document.querySelector(".scroll-progress-bar");
    if (!progressBar) return;

    let ticking = false;
    window.addEventListener("scroll", () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
                progressBar.style.width = scrollPercent + "%";
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
}

/* =========================
   LAZY IMAGE LOADING
========================= */
function initLazyImages() {
    const lazyImages = document.querySelectorAll("img[data-src]");
    if (!lazyImages.length) return;

    const imgObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const src = img.dataset.src;
                if (src) {
                    const temp = new Image();
                    temp.src = src;
                    temp.onload = () => {
                        img.src = src;
                        img.classList.add("loaded");
                        img.removeAttribute("data-src");
                    };
                }
                imgObserver.unobserve(img);
            }
        });
    }, { rootMargin: "100px 0px" });

    lazyImages.forEach(img => imgObserver.observe(img));
}

/* =========================
   LAZY VIDEO LOADING & MOBILE AUTOPLAY ENFORCEMENT
 ========================= */
function initLazyVideos() {
    const lazyVideos = document.querySelectorAll("video.lazy-video");
    if (!lazyVideos.length) return;

    const playVideoElement = (video) => {
        if (video.paused) {
            video.play().catch(err => {
                // Retry play on first user interaction
                const forcePlay = () => {
                    video.play().catch(e => {});
                    document.removeEventListener("touchstart", forcePlay);
                    document.removeEventListener("click", forcePlay);
                };
                document.addEventListener("touchstart", forcePlay, { passive: true });
                document.addEventListener("click", forcePlay, { passive: true });
            });
        }
    };

    const videoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target;
                const source = video.querySelector("source");
                if (source && source.dataset.src) {
                    source.src = source.dataset.src;
                    video.load();
                    playVideoElement(video);
                    video.removeAttribute("preload");
                }
                videoObserver.unobserve(video);
            }
        });
    }, { rootMargin: "150px 0px" });

    lazyVideos.forEach(video => {
        videoObserver.observe(video);
        
        // Prevent manual or browser-enforced pausing
        video.addEventListener("pause", () => {
            if (video.dataset.userPaused !== "true") {
                video.play().catch(() => {});
            }
        });
    });
}

/* =========================
   SMOOTH ANCHOR SCROLLING
========================= */
function initSmoothAnchors() {
    document.querySelectorAll('a').forEach(anchor => {
        const href = anchor.getAttribute("href");
        if (!href) return;

        let isSamePageAnchor = false;
        let targetId = "";

        if (href.startsWith("#") && href !== "#") {
            isSamePageAnchor = true;
            targetId = href;
        } else {
            try {
                const url = new URL(anchor.href, window.location.href);
                if (url.pathname === window.location.pathname && url.hash) {
                    isSamePageAnchor = true;
                    targetId = url.hash;
                }
            } catch (err) {
                // Ignore invalid URLs
            }
        }

        if (isSamePageAnchor) {
            anchor.addEventListener("click", function (e) {
                const target = document.querySelector(targetId);
                if (!target) return;
                e.preventDefault();

                const navbar = document.querySelector(".custom-navbar");
                const offset = navbar ? navbar.offsetHeight + 20 : 80;
                const targetTop = target.getBoundingClientRect().top + window.pageYOffset - offset;

                window.scrollTo({
                    top: targetTop,
                    behavior: "smooth"
                });

                // Update hash in address bar without scrolling
                history.pushState(null, null, targetId);
            });
        }
    });
}

function initPageTransition() {
    const transition = document.getElementById("page-transition");
    if (!transition) return;

    window.addEventListener("load", function () {
        setTimeout(() => {
            transition.classList.add("loaded");
            transition.classList.remove("active");
            const siteContent = document.getElementById("site-content");
            if (siteContent) siteContent.classList.add("loaded");

            // Defer scroll reveal until loader overlay fades out
            initScrollReveal();
        }, 200);

        // Handle initial page load with a hash (e.g. /about/#craftsmanship)
        if (window.location.hash) {
            setTimeout(() => {
                const target = document.querySelector(window.location.hash);
                if (target) {
                    const navbar = document.querySelector(".custom-navbar");
                    const offset = navbar ? navbar.offsetHeight + 20 : 80;
                    const targetTop = target.getBoundingClientRect().top + window.pageYOffset - offset;
                    window.scrollTo({
                        top: targetTop,
                        behavior: "smooth"
                    });
                }
            }, 250); // Trigger just as the loader screen starts fading out
        }
    });

    window.addEventListener("pageshow", function () {
        transition.classList.add("loaded");
        transition.classList.remove("active");
        const siteContent = document.getElementById("site-content");
        if (siteContent) siteContent.classList.add("loaded");

        // Defer scroll reveal
        initScrollReveal();
    });

    document.querySelectorAll("a").forEach(link => {
        const href = link.getAttribute("href");

        if (
            !href ||
            href.startsWith("#") ||
            href.startsWith("javascript:") ||
            href.startsWith("mailto:") ||
            href.startsWith("tel:") ||
            link.hasAttribute("target") ||
            link.classList.contains("no-transition")
        ) {
            return;
        }

        // Avoid page transitions for same-page anchor links (e.g. /about/#craftsmanship)
        try {
            const url = new URL(link.href, window.location.href);
            if (url.pathname === window.location.pathname && url.hash) {
                return;
            }
        } catch (err) {
            // Ignore
        }

        link.addEventListener("click", function (e) {
            if (e.ctrlKey || e.metaKey || e.shiftKey) return;

            e.preventDefault();

            transition.classList.remove("loaded");
            transition.classList.add("active");

            setTimeout(() => {
                window.location.href = href;
            }, 200);
        });
    });
}

function bumpCartBadge() {
    const badge = document.getElementById("cart-count");
    if (!badge) return;
    badge.classList.remove("bump");
    void badge.offsetWidth;
    badge.classList.add("bump");
    setTimeout(() => badge.classList.remove("bump"), 500);
}

function updateCart(product_id, qty) {

    $.post("/cart/update/", {
        product_id: product_id,
        quantity: qty
    }, function (response) {

        if (!response.success) return;

        $(`#qty-${product_id}`).text(qty);
        $(`#total-${product_id}`).text("₹" + response.item_total);

        $("#cart-count").text(response.cartq);
        bumpCartBadge();

        $("#cart-subtotal").text("₹" + response.cart_total);

        $("#cart-total").text(
            "₹" + (parseFloat(response.cart_total) + 250)
        );

    });

}

/* =========================
   LUXURY INTRO SPLASH SCREEN
========================= */
function initLuxuryIntro() {
    const intro = document.getElementById("luxury-intro");
    if (!intro) return;

    if (sessionStorage.getItem("luxury_intro_played") === "true") {
        intro.style.display = "none";
        document.body.classList.remove("intro-active");
        return;
    }

    const hanger = intro.querySelector(".hanger-3d");

    // 3D Parallax Mouse Move Listener
    let ticking = false;
    intro.addEventListener("mousemove", function (e) {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const rect = intro.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                // Calculate tilt angles (max tilt around 15 degrees)
                const tiltX = -(y / (rect.height / 2)) * 15;
                const tiltY = (x / (rect.width / 2)) * 15;

                if (hanger) {
                    hanger.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
                }
                ticking = false;
            });
            ticking = true;
        }
    });

    // Reset rotation on mouse leave
    intro.addEventListener("mouseleave", function () {
        if (hanger) {
            hanger.style.transform = `rotateX(0deg) rotateY(0deg)`;
        }
    });

    intro.addEventListener("click", function () {
        intro.classList.add("exit-active");
        document.body.classList.remove("intro-active");
        sessionStorage.setItem("luxury_intro_played", "true");

        // Wait for exit transitions to finish before removing from DOM
        setTimeout(() => {
            intro.remove();
        }, 1200);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    initLuxuryIntro();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {

            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            }

        }
    });

    initPageTransition();
    if (!document.getElementById("page-transition")) {
        initScrollReveal();
    }
    initNavbarScroll();
    initBackToTop();
    initMobileHamburger();
    initButtonSpotlight();
    initScrollProgress();
    initLazyImages();
    initLazyVideos();
    initSmoothAnchors();

    /* AUTH POPUP */
    window.addEventListener("click", function (event) {

        const popup = document.getElementById("auth-popup");

        if (popup && event.target === popup) {
            closePopup();
        }

    });

    const profileBtn = document.getElementById("profile-trigger");

    if (profileBtn) {

        profileBtn.addEventListener("click", function (e) {

            e.preventDefault();

            if (this.dataset.auth === "true") {
                window.location.href = this.dataset.profileUrl;
            } else {
                showPopup();
            }

        });

    }

    /* ADD TO CART */
    $(document).on("click", ".add-to-cart, #add-cart", function (e) {

        e.preventDefault();

        const btn = $(this);

        const product_id = btn.data("product-id");

        const quantity = parseInt($("#qty").text()) || 1;

        $.post("/cart/add/", {
            product_id,
            quantity
        }, function (response) {

            if (response.login_required) {
                showPopup();
                return;
            }

            $("#cart-count").text(response.cartq || 0);
            bumpCartBadge();

            btn.text("Added ✓")
                .prop("disabled", true);

            setTimeout(() => {

                btn.text("ADD TO CART")
                    .prop("disabled", false);

            }, 1200);

        });

    });

    /* QTY PLUS */
    $(document).on("click", ".qty-plus", function () {

        const product_id = $(this).data("product-id");

        const qtyDisplay = $(`#qty-${product_id}`);

        let qty = parseInt(qtyDisplay.text()) || 1;

        qty++;

        updateCart(product_id, qty);

    });

    /* QTY MINUS */
    $(document).on("click", ".qty-minus", function () {

        const product_id = $(this).data("product-id");

        const qtyDisplay = $(`#qty-${product_id}`);

        let qty = parseInt(qtyDisplay.text()) || 1;

        if (qty <= 1) return;

        qty--;

        updateCart(product_id, qty);

    });

    /* DELETE */
    $(document).on("click", ".remove-item", function () {

        const product_id = $(this).data("product-id");

        const row = $(this).closest(".cart-item");

        $.post("/cart/delete/", {
            product_id
        }, function (response) {

            if (!response.success) return;

            row.fadeOut(250, function () {

                $(this).remove();

                $("#cart-count").text(response.cartq);
                bumpCartBadge();

                $("#cart-subtotal").text("₹" + response.cart_total);

                $("#cart-total").text(
                    "₹" + (parseFloat(response.cart_total) + 250)
                );

                if (response.cartq <= 0) {
                    location.reload();
                }

            });

        });

    });

});