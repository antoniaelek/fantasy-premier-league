! function(l, a) {
    if (l.PlotlyEmbeds) return l.PlotlyEmbeds.init();
    var o = l.PlotlyEmbeds = new function() {
        var r = this;
        r.minScreenWidth = 1024, r.minWidth = 400, r.version = "0.0.3", r.plots = {}, r.resizeInterval = null, r.processScriptTag = function(t) {
            var e = new i(t).init();
            e && (r.plots[e.getId()] = e)
        }, r.init = function() {
            var t = a.querySelectorAll("script[data-plotly]");
            Array.prototype.forEach.call(t, r.processScriptTag)
        }, r.resize = function() {
            for (var t in r.plots) r.plots[t].resize()
        }, r.onMessage = function(t) {
            var e = t.data,
                i = r.plots[e.id];
            i && t.origin === i.getBaseUrl() && e.initialSize && i.setInitialSize(e.initialSize)
        }
    };

    function i(t) {
        var e = this;
        e.script = t, e.fid = t.getAttribute("data-plotly"), e.fidurl = e.fid.replace(":", "/"), e.shareKey = t.getAttribute("sharekey-plotly"), e.iframe = null, e.isFluid = null, e.aspectRatio = null, e.initialWidth = null, e.initialHeight = null
    }
    var t = i.prototype;
    t.hasSupport = function() {
        return !(a.documentMode && a.documentMode <= 8) && !(l.screen.availWidth < o.minScreenWidth)
    }, t.getBaseUrl = function() {
        var t = this;
        if (t._baseUrl) return t._baseUrl;
        var e = t.getImage(),
            i = t.getLink(),
            r = t.script,
            n = l.location,
            a = (i.protocol || n.protocol) + "//" + (i.hostname || n.hostname);
        return 0 !== i.href.indexOf(a) ? null : 0 !== e.src.indexOf(a) ? null : 0 !== r.src.indexOf(a) ? null : t._baseUrl = a
    }, t.getId = function() {
        var t = this;
        if (t._id) return t._id;
        for (var e = t.fid, i = 1; a.getElementById("plotly-" + e);) e = t.fid + "-" + i, i++;
        return t._id = e
    }, t.generateIframe = function() {
        var t = a.createElement("iframe");
        return t.id = "plotly-" + this.getId(), t.width = 0, t.height = 0, t.frameBorder = 0, t.scrolling = "no", t.style.maxWidth = "100%",t.style.maxHeight = "50vh", t.style.visibility = "hidden", t.style.position = "absolute", t
    }, t.getUrl = function() {
        var t = this,
            e = t.getBaseUrl() + "/~" + t.fidurl + ".embed";
        return t.shareKey && (e += "?share_key=" + t.shareKey), e
    }, t.setInitialSize = function(t) {
        var e = this;
        e.isFluid = t.autosize || !t.width || !t.height, e.initialWidth = t.width, e.initialHeight = t.height, e.aspectRatio = e.getAspectRatio(t.height, t.width), e.resize()
    }, t.getAspectRatio = function(t, e) {
        var i = Math.round(100 * t / e);
        return (isNaN(i) ? 71 : i) / 100
    }, t.resize = function() {
        var t = this,
            e = t.wrapper.offsetWidth,
            i = o.minWidth;
        if (t.initialWidth <= i && (i = t.initialWidth + 1), e <= i) {
            var r = t.getImage();
            t.hideIframe(), r.style.maxWidth = "100%"
        } else if (null !== t.isFluid) {
            t.showIframe();
            var n = t.isFluid ? e : t.initialWidth,
                a = t.isFluid ? e * t.aspectRatio : t.initialHeight,
                l = Number(t.iframe.width),
                s = Number(t.iframe.height);
            n === l && a === s || (t.iframe.width = n, t.iframe.height = a, t.postMessage({
                task: "relayout",
                update: {
                    autosize: !1,
                    width: n,
                    height: a
                },
                sendData: !1
            }))
        }
    }, t.hideIframe = function() {
        this.getLink().style.display = "", this.getImage().style.maxWidth = "100%", this.iframe.style.display = "none"
    }, t.showIframe = function() {
        this.getLink().style.display = "none", this.iframe.style.position = "", this.iframe.style.visibility = "", this.iframe.style.display = ""
    }, t.postMessage = function(t) {
        this.iframe.contentWindow.postMessage(t, this.getBaseUrl())
    }, t.getLink = function() {
        var t = this;
        if (t._link) return t._link;
        var e, i, r, n = this.wrapper.firstElementChild;
        if ("A" === n.tagName && 0 < n.href.indexOf(this.fidurl)) return t._link = n;
        for (i = 0, r = (e = a.querySelectorAll('a[href*="~' + t.fidurl + '"]')).length; i < r; i += 1)
            if (!(n = e[i]).hasAttribute("data-plotly") && n.firstElementChild && "IMG" === n.firstElementChild.tagName) return t._link = n;
        return null
    }, t.getImage = function() {
        if (this._image) return this._image;
        var t = this.getLink();
        if (!t) return null;
        var e = t.firstElementChild;
        return e && "IMG" === e.tagName ? this._image = e : null
    }, t.initIframe = function() {
        var t = this;
        t.iframe = t.generateIframe(), t.wrapper.replaceChild(t.iframe, t.script), t.iframe.addEventListener("load", function() {
            t.postMessage({
                task: "getInitialSize",
                id: t.getId()
            })
        }), t.iframe.src = t.getUrl()
    }, t.initWrapper = function() {
        this.wrapper.style.textAlign = "center", this.wrapper.style.position = "relative"
    }, t.init = function() {
        var t = this;
        if (t.wrapper = t.script.parentNode, t.wrapper.getAttribute("data-plotly")) return null;
        var e = t.getLink(),
            i = t.getImage();
        if (!e || !i) {
            var r = t.script.src,
                n = r.substr(0, r.indexOf("/embed")),
                a = "Looks like the embed code for " + t.fid + " is incorrect. You can get the correct code here: " + n + "/~" + t.fidurl + ".html";
            if (l.console) return l.console.warn(a), null;
            throw new Error(a)
        }
        return t.wrapper.setAttribute("data-plotly", t.fidurl), e.setAttribute("data-plotly", t.fidurl), i.setAttribute("data-plotly", t.fidurl), t.initWrapper(), t.hasSupport() && t.initIframe(), t
    }, o.init(), l.addEventListener("message", o.onMessage), l.addEventListener("resize", function() {
        o.resizeInterval && l.clearTimeout(o.resizeInterval), o.resizeInterval = l.setTimeout(o.resize, 100)
    })
}(window, document);