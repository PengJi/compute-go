webpackJsonp([1], {
    "4M7i": function(t, e) {},
    BuVq: function(t, e) {},
    D4uH: function(t, e, n) {
        "use strict";
        var r = n("Gu7T"),
            i = n.n(r),
            s = n("bOdI"),
            o = n.n(s),
            a = {},
            l = {
                name: "fa-icon",
                props: {
                    name: {
                        type: String,
                        validator: function(t) {
                            return !t || t in a || (console.warn('Invalid prop: prop "name" is referring to an unregistered icon "' + t + '".\nPlease make sure you have imported this icon before using it.'), !1)
                        }
                    },
                    title: String,
                    scale: [Number, String],
                    spin: Boolean,
                    inverse: Boolean,
                    pulse: Boolean,
                    flip: {
                        validator: function(t) {
                            return "horizontal" === t || "vertical" === t
                        }
                    },
                    label: String,
                    tabindex: [Number, String]
                },
                data: function() {
                    return {
                        id: h(),
                        x: !1,
                        y: !1,
                        childrenWidth: 0,
                        childrenHeight: 0,
                        outerScale: 1
                    }
                },
                computed: {
                    normalizedScale: function() {
                        var t = this.scale;
                        return t = void 0 === t ? 1 : Number(t), isNaN(t) || t <= 0 ? (console.warn('Invalid prop: prop "scale" should be a number over 0.', this), this.outerScale) : t * this.outerScale
                    },
                    klass: function() {
                        return o()({
                            "fa-icon": !0,
                            "fa-spin": this.spin,
                            "fa-flip-horizontal": "horizontal" === this.flip,
                            "fa-flip-vertical": "vertical" === this.flip,
                            "fa-inverse": this.inverse,
                            "fa-pulse": this.pulse
                        }, this.$options.name, !0)
                    },
                    icon: function() {
                        return this.name ? a[this.name] : null
                    },
                    box: function() {
                        return this.icon ? "0 0 " + this.icon.width + " " + this.icon.height : "0 0 " + this.width + " " + this.height
                    },
                    ratio: function() {
                        if (!this.icon) return 1;
                        var t = this.icon,
                            e = t.width,
                            n = t.height;
                        return Math.max(e, n) / 16
                    },
                    width: function() {
                        return this.childrenWidth || this.icon && this.icon.width / this.ratio * this.normalizedScale || 0
                    },
                    height: function() {
                        return this.childrenHeight || this.icon && this.icon.height / this.ratio * this.normalizedScale || 0
                    },
                    style: function() {
                        return 1 !== this.normalizedScale && {
                            fontSize: this.normalizedScale + "em"
                        }
                    },
                    raw: function() {
                        if (!this.icon || !this.icon.raw) return null;
                        var t = this.icon.raw,
                            e = {};
                        return t = t.replace(/\s(?:xml:)?id=(["']?)([^"')\s]+)\1/g, function(t, n, r) {
                            var i = h();
                            return e[r] = i, ' id="' + i + '"'
                        }), t = t.replace(/#(?:([^'")\s]+)|xpointer\(id\((['"]?)([^')]+)\2\)\))/g, function(t, n, r, i) {
                            var s = n || i;
                            return s && e[s] ? "#" + e[s] : t
                        }), t
                    },
                    focusable: function() {
                        var t = this.tabindex;
                        return null == t ? "false" : ("string" == typeof t ? parseInt(t, 10) : t) >= 0 ? null : "false"
                    }
                },
                mounted: function() {
                    this.updateStack()
                },
                updated: function() {
                    this.updateStack()
                },
                methods: {
                    updateStack: function() {
                        var t = this;
                        if (this.name || null === this.name || 0 !== this.$children.length) {
                            if (!this.icon) {
                                var e = 0,
                                    n = 0;
                                this.$children.forEach(function(r) {
                                    r.outerScale = t.normalizedScale, e = Math.max(e, r.width), n = Math.max(n, r.height)
                                }), this.childrenWidth = e, this.childrenHeight = n, this.$children.forEach(function(t) {
                                    t.x = (e - t.width) / 2, t.y = (n - t.height) / 2
                                })
                            }
                        } else console.warn('Invalid prop: prop "name" is required.')
                    }
                },
                render: function(t) {
                    if (null === this.name) return t();
                    var e = {
                        class: this.klass,
                        style: this.style,
                        attrs: {
                            role: this.$attrs.role || (this.label || this.title ? "img" : null),
                            "aria-label": this.label || null,
                            "aria-hidden": String(!(this.label || this.title)),
                            tabindex: this.tabindex,
                            x: this.x,
                            y: this.y,
                            width: this.width,
                            height: this.height,
                            viewBox: this.box,
                            focusable: this.focusable
                        }
                    },
                        n = "vat-" + this.id;
                    if (this.title && (e.attrs["aria-labelledby"] = n), this.raw) {
                        var r = this.raw;
                        this.title && (r = '<title id="' + n + '">' + function(t) {
                            return t.replace(/[<>"&]/g, function(t) {
                                return d[t] || t
                            })
                        }(this.title) + "</title>" + r), e.domProps = {
                            innerHTML: r
                        }
                    }
                    var s = this.title ? [t("title", {
                        attrs: {
                            id: n
                        }
                    }, this.title)] : [];
                    return t("svg", e, this.raw ? null : s.concat(this.$slots.default || [].concat(i()(this.icon.paths.map(function(e, n) {
                        return t("path", {
                            attrs: e,
                            key: "path-" + n
                        })
                    })), i()(this.icon.polygons.map(function(e, n) {
                        return t("polygon", {
                            attrs: e,
                            key: "polygon-" + n
                        })
                    })))))
                },
                register: function(t) {
                    for (var e in t) {
                        var n = t[e],
                            r = n.paths,
                            i = void 0 === r ? [] : r,
                            s = n.d,
                            o = n.polygons,
                            l = void 0 === o ? [] : o,
                            c = n.points;
                        s && i.push({
                            d: s
                        }), c && l.push({
                            points: c
                        }), a[e] = u({}, n, {
                            paths: i,
                            polygons: l
                        })
                    }
                },
                icons: a
            };

        function u(t) {
            for (var e = arguments.length, n = Array(e > 1 ? e - 1 : 0), r = 1; r < e; r++) n[r - 1] = arguments[r];
            return n.forEach(function(e) {
                for (var n in e) e.hasOwnProperty(n) && (t[n] = e[n])
            }), t
        }
        var c = 870711;

        function h() {
            return "va-" + (c++).toString(16)
        }
        var d = {
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "&": "&amp;"
        };
        var m = n("VU/8")(l, null, !1, function(t) {
            n("BuVq")
        }, null, null);
        e.a = m.exports
    },
    NHnr: function(t, e, n) {
        "use strict";
        Object.defineProperty(e, "__esModule", {
            value: !0
        });
        var r = n("7+uW"),
            i = n("go35"),
            s = n.n(i),
            o = {
                data: function() {
                    return {
                        menu: s.a
                    }
                },
                methods: {
                    handleOpen: function(t, e) {
                        console.log(t, e)
                    },
                    handleClose: function(t, e) {
                        console.log(t, e)
                    }
                }
            },
            a = {
                render: function() {
                    var t = this,
                        e = t.$createElement,
                        n = t._self._c || e;
                    return n("el-row", {
                        staticClass: "tac"
                    }, [n("el-col", {
                        attrs: {
                            span: 24
                        }
                    }, [n("el-menu", {
                        staticClass: "el-menu-vertical-demo",
                        attrs: {
                            "default-active": "2",
                            router: ""
                        },
                        on: {
                            open: t.handleOpen,
                            close: t.handleClose
                        }
                    }, t._l(t.menu, function(e) {
                        return n("el-menu-item", {
                            key: e.id,
                            attrs: {
                                index: e.path
                            }
                        }, [n("template", {
                            slot: "title"
                        }, [n("icon", {
                            attrs: {
                                name: e.icon
                            }
                        }), t._v(" "), n("span", {
                            domProps: {
                                textContent: t._s(e.name)
                            }
                        })], 1)], 2)
                    }), 1)], 1)], 1)
                },
                staticRenderFns: []
            };
        var l = {
            render: function() {
                var t = this.$createElement,
                    e = this._self._c || t;
                return e("el-row", [e("div", {
                    staticClass: "head-wrap"
                }, [this._v("Web Shell")])])
            },
            staticRenderFns: []
        };
        var u = {
                name: "App",
                components: {
                    navmenu: n("VU/8")(o, a, !1, function(t) {
                        n("YvoH")
                    }, "data-v-28ac6478", null).exports,
                    vheader: n("VU/8")(null, l, !1, function(t) {
                        n("PEjQ")
                    }, "data-v-f79b580a", null).exports
                }
            },
            c = {
                render: function() {
                    var t = this.$createElement,
                        e = this._self._c || t;
                    return e("div", {
                        attrs: {
                            id: "app"
                        }
                    }, [e("el-container", [e("el-header", {
                        staticClass: "header"
                    }, [e("vheader")], 1), this._v(" "), e("el-container", [e("el-aside", {
                        staticClass: "aside",
                        attrs: {
                            width: "200px"
                        }
                    }, [e("navmenu")], 1), this._v(" "), e("el-main", [e("router-view")], 1)], 1)], 1)], 1)
                },
                staticRenderFns: []
            };
        var h = n("VU/8")(u, c, !1, function(t) {
            n("4M7i")
        }, null, null).exports,
            d = n("zL8q"),
            m = n.n(d),
            p = (n("tvR6"), n("/ocq")),
            f = n("RRo+"),
            v = n.n(f),
            g = {
                name: "AddNode",
                data: function() {
                    return {
                        ruleForm: {
                            pass: "",
                            checkPass: "",
                            port: 22,
                            ipaddress: "192.168.35.141",
                            username: "jipeng"
                        },
                        rules: {
                            port: [{
                                validator: function(t, e, n) {
                                    if (!e) return n(new Error("端口不能为空"));
                                    setTimeout(function() {
                                        v()(e) ? e < 20 ? n(new Error("必须大于20")) : n() : n(new Error("请输入数字值"))
                                    }, 1e3)
                                },
                                trigger: "blur"
                            }]
                        }
                    }
                },
                methods: {
                    submitForm: function(t) {
                        this.$refs[t].validate(function(t) {
                            if (!t) return console.log("error submit!!"), !1;
                            alert("submit!")
                        })
                    },
                    resetForm: function(t) {
                        this.$refs[t].resetFields()
                    },
                    goToWebssh: function() {
                        var t = '{"username":"' + this.ruleForm.username + '", "ipaddress":"' + this.ruleForm.ipaddress + '", "port":' + this.ruleForm.port + ', "password":"' + this.ruleForm.pass + '"}',
                            e = window.btoa(t);
                        this.$router.push({
                            path: "/webssh",
                            name: "WebSSH",
                            params: {
                                msg: "msg",
                                dataObj: e
                            }
                        })
                    }
                }
            },
            w = {
                render: function() {
                    var t = this,
                        e = t.$createElement,
                        n = t._self._c || e;
                    return n("div", [n("el-form", {
                        ref: "ruleForm",
                        staticClass: "demo-ruleForm",
                        attrs: {
                            model: t.ruleForm,
                            "status-icon": "",
                            rules: t.rules,
                            "label-width": "100px",
                            "label-position": "left"
                        }
                    }, [n("el-form-item", {
                        attrs: {
                            label: "ip地址",
                            prop: "ipaddress",
                            required: ""
                        }
                    }, [n("el-input", {
                        attrs: {
                            type: "text"
                        },
                        model: {
                            value: t.ruleForm.ipaddress,
                            callback: function(e) {
                                t.$set(t.ruleForm, "ipaddress", e)
                            },
                            expression: "ruleForm.ipaddress"
                        }
                    })], 1), t._v(" "), n("el-form-item", {
                        attrs: {
                            label: "用户名",
                            prop: "username",
                            required: ""
                        }
                    }, [n("el-input", {
                        attrs: {
                            type: "text"
                        },
                        model: {
                            value: t.ruleForm.username,
                            callback: function(e) {
                                t.$set(t.ruleForm, "username", e)
                            },
                            expression: "ruleForm.username"
                        }
                    })], 1), t._v(" "), n("el-form-item", {
                        attrs: {
                            label: "密码",
                            prop: "pass",
                            required: ""
                        }
                    }, [n("el-input", {
                        attrs: {
                            type: "password",
                            autocomplete: "off"
                        },
                        model: {
                            value: t.ruleForm.pass,
                            callback: function(e) {
                                t.$set(t.ruleForm, "pass", e)
                            },
                            expression: "ruleForm.pass"
                        }
                    })], 1), t._v(" "), n("el-form-item", {
                        attrs: {
                            label: "端口",
                            prop: "port",
                            required: ""
                        }
                    }, [n("el-input", {
                        model: {
                            value: t.ruleForm.port,
                            callback: function(e) {
                                t.$set(t.ruleForm, "port", t._n(e))
                            },
                            expression: "ruleForm.port"
                        }
                    })], 1), t._v(" "), n("el-form-item", [n("el-button", {
                        attrs: {
                            type: "primary",
                            plain: ""
                        },
                        on: {
                            click: function(e) {
                                return t.goToWebssh()
                            }
                        }
                    }, [t._v("连接")]), t._v(" "), n("el-button", {
                        on: {
                            click: function(e) {
                                return t.resetForm("ruleForm")
                            }
                        }
                    }, [t._v("重置")])], 1)], 1)], 1)
                },
                staticRenderFns: []
            },
            b = n("VU/8")(g, w, !1, null, null, null).exports,
            S = n("13sD"),
            x = n("6x4x"),
            y = n("AaoT");
        S.Terminal.applyAddon(x), S.Terminal.applyAddon(y);
        var F = S.Terminal,
            _ = {
                name: "Console",
                props: {
                    msg: {
                        type: String
                    },
                    username: {
                        type: String
                    },
                    password: {
                        type: String
                    }
                },
                data: function() {
                    return {
                        term: null,
                        terminalSocket: null
                    }
                },
                methods: {
                    runRealTerminal: function() {
                        console.log("webSocket is finished")
                    },
                    errorRealTerminal: function() {
                        console.log("error")
                    },
                    closeRealTerminal: function() {
                        console.log("close")
                    }
                },
                mounted: function() {
                    var t = window.screen.height,
                        e = (window.screen.width, Math.floor((t - 30) / 9)),
                        n = Math.floor(window.innerHeight / 17) - 2;
                    if (void 0 === this.username) var r = ("http:" === location.protocol ? "ws" : "wss") + "://" + location.hostname + ":5001/ws?msg=" + this.msg + "&rows=" + n + "&cols=" + e;
                    else r = ("http:" === location.protocol ? "ws" : "wss") + "://" + location.hostname + ":5001/ws?msg=" + this.msg + "&rows=" + n + "&cols=" + e + "&username=" + this.username + "&password=" + this.password;
                    var i = document.getElementById("terminal");
                    this.term = new F, this.term.open(i), this.terminalSocket = new WebSocket(r), this.terminalSocket.onopen = this.runRealTerminal, this.terminalSocket.onclose = this.closeRealTerminal, this.terminalSocket.onerror = this.errorRealTerminal, this.term.attach(this.terminalSocket), this.term._initialized = !0, console.log("mounted is going on")
                },
                beforeDestroy: function() {
                    this.terminalSocket.close(), this.term.destroy()
                }
            },
            k = {
                render: function() {
                    var t = this.$createElement;
                    return (this._self._c || t)("div", {
                        staticClass: "console",
                        attrs: {
                            id: "terminal"
                        }
                    })
                },
                staticRenderFns: []
            },
            $ = {
                name: "WebSSH",
                data: function() {
                    return {
                        msg: "",
                        username: "",
                        password: ""
                    }
                },
                components: {
                    "my-terminal": n("VU/8")(_, k, !1, null, null, null).exports
                },
                methods: {
                    getParams: function() {
                        this.msg = this.$route.params.dataObj, this.username = this.$route.params.username, this.password = this.$route.params.password
                    }
                },
                created: function() {
                    this.getParams()
                }
            },
            T = {
                render: function() {
                    var t = this.$createElement,
                        e = this._self._c || t;
                    return e("div", {
                        staticClass: "container"
                    }, [e("my-terminal", {
                        attrs: {
                            msg: this.msg,
                            username: this.username,
                            password: this.password
                        }
                    })], 1)
                },
                staticRenderFns: []
            };
        var R = n("VU/8")($, T, !1, function(t) {
            n("Qxdp")
        }, "data-v-ff0a9434", null).exports;
        r.default.use(p.a);
        var E = [{
                name: "AddNode",
                id: "addnode",
                icon: "desktop",
                path: "/",
                component: b,
                meta: {
                    title: "AddNode"
                }
            },
            {
                name: "WebSSH",
                id: "webssh",
                path: "/webssh",
                component: R,
                meta: {
                    title: "WebSSH"
                }
            }
        ],
            H = new p.a({
                routes: E
            }),
            P = (n("uMhA"), n("D4uH"));
        n("D/PP"), n("fIPj");
        r.default.use(m.a), r.default.config.productionTip = !1, r.default.component("icon", P.a), new r.default({
            el: "#app",
            router: H,
            components: {
                App: h
            },
            template: "<App/>"
        })
    },
    PEjQ: function(t, e) {},
    Qxdp: function(t, e) {},
    YvoH: function(t, e) {},
    fIPj: function(t, e) {},
    go35: function(t, e) {
        t.exports = [{
            name: "主机",
            id: "addnode",
            icon: "desktop",
            path: "/"
        }]
    },
    tvR6: function(t, e) {},
    uMhA: function(t, e) {}
}, ["NHnr"]);
