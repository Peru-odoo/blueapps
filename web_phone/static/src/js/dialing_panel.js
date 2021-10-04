odoo.define('web_phone.DialingPanel', function (require) {
    "use strict";

    const config = require('web.config');
    const core = require('web.core');
    const Widget = require('web.Widget');
    const session = require('web.session');

    const {_t} = core;
    const HEIGHT_OPEN = '480px';
    const HEIGHT_FOLDED = '0px';

    const DialingPanel = Widget.extend({
        template: 'web_phone.DialingPanel',
        events: {
            'click .o_dial_call_button': '_onClickCallButton',
            'click .o_dial_accept_button': '_onClickAcceptButton',
            'click .o_dial_reject_button': '_onClickRejectButton',
            'click .o_dial_fold': '_onClickFold',
            'click .o_dial_hangup_button': '_onClickHangupButton',
            'click .o_dial_keypad_backspace': '_onClickKeypadBackspace',
            'click .o_dial_number': '_onClickDialNumber',
            'click .o_dial_window_close': '_onClickWindowClose',
            'keyup .o_dial_keypad_input': '_onKeyupKeypadInput',
        },

        /**
         * @constructor
         */
        init() {
            this._super(...arguments);

            this.title = _t("VOIP");
            this.user = session.user_id;

            this._isFolded = false;
            this._isInCall = false;
            this._isShow = false;
            this._active = true;

            this.dialPlayer = document.createElement("audio");
            this.dialPlayer.volume = 1;
            this.dialPlayer.setAttribute("src", "web_phone/static/src/sounds/outgoing-call2.ogg");

            this.incomingPlayer = document.createElement("audio");
            this.incomingPlayer.volume = 1;
            this.incomingPlayer.setAttribute("src", "web_phone/static/src/sounds/incomingcall.mp3");


            this.web_phone_configs = {
                web_phone_sip_protocol: '',
                web_phone_sip_proxy: '',
                web_phone_sip_secret: '',
                web_phone_sip_user: '',
                web_phone_stun_server: '',
                web_phone_websocket: '',
            }

            this._userAgent = null;
            this.session = null;

        },
        /**
         * @override
         */
        async start() {
            this._$callButton = this.$('.o_dial_call_button');
            this._$keypadInput = this.$('.o_dial_keypad_input');
            this._$mainButton = this.$('.o_dial_main_buttons');
            this._$incomingButtons = this.$('.o_dial_incoming_buttons')
            this._$keypad = this.$('.o_dial_keypad');
            this._$dialPanel = this.$('.o_dial_panel');
            this._$dialPhone = this.$('#dial_phone')


            this.$el.css('bottom', 0);
            this.$el.hide();

            const [web_phone_configs] = await this._rpc({
                model: 'res.users',
                method: 'search_read',
                domain: [
                    ['id', '=', this.user],
                ],
                fields: [
                    'web_phone_sip_user',
                    'web_phone_sip_secret',
                    'web_phone_sip_protocol',
                    'web_phone_sip_proxy',
                    'web_phone_websocket',
                    'web_phone_stun_server'
                ],
                limit: 1,

            });
            delete web_phone_configs['id'];
            this.web_phone_configs = web_phone_configs;

            for (let key in web_phone_configs) {
                if (!web_phone_configs[key]) {
                    console.error(`Missing config: "${key}" for Web Phone!`);
                    this._active = false;
                }
            }

            this._initUserAgent();

            core.bus.on('voip_onToggleDisplay', this, function () {
                if (this._active) {
                    this._onToggleDisplay();
                } else {
                    this.do_notify('Missing configs! Check "User / Preferences"!');
                }
            });
        },

        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        _initUserAgent() {
            const self = this;
            if (!self._active) {
                console.error('return')
                return
            }
            const {
                web_phone_sip_user,
                web_phone_sip_secret,
                web_phone_sip_proxy,
                web_phone_sip_protocol,
                web_phone_websocket,
                web_phone_stun_server
            } = self.web_phone_configs;

            try {
                self.socket = new JsSIP.WebSocketInterface(web_phone_websocket);
            } catch (e) {
                console.error(e);
                this._active = false;
                return
            }
            self.socket.via_transport = web_phone_sip_protocol;
            self.configuration = {
                sockets: [self.socket],
                ws_servers: web_phone_websocket,
                realm: 'OdooPBX',
                display_name: web_phone_sip_user,
                uri: `sip:${web_phone_sip_user}@${web_phone_sip_proxy}`,
                password: web_phone_sip_secret,
                contact_uri: `sip:${web_phone_sip_user}@${web_phone_sip_proxy}`,
                register: true,
                stun_server: web_phone_stun_server,
            };
            self._userAgent = new JsSIP.UA(self.configuration);
            // JsSIP.debug.enable('JsSIP:*');
            JsSIP.debug.disable('JsSIP:*');
            self._userAgent.start();

            self._userAgent.on('connected', function (e) {
                // console.log('SIP Connected')
            });

            // HANDLE RTCSession
            self._userAgent.on("newRTCSession", function ({session}) {
                if (session.direction === "outgoing") {
                    session.connection.addEventListener("track", (e) => {
                        const remoteAudio = document.createElement('audio');
                        remoteAudio.srcObject = e.streams[0];
                        remoteAudio.play();
                    });
                }

                if (session.direction === "incoming") {
                    session.on('peerconnection', function (data) {
                        data.peerconnection.addEventListener('addstream', function (e) {
                            const remoteAudio = document.createElement('audio');
                            remoteAudio.srcObject = e.stream;
                            remoteAudio.play();
                        });
                    });
                    if (self._isInCall) {
                        session.terminate();
                        return;
                    }
                    self.session = session;
                    if (!self._isShow) {
                        self._onToggleDisplay();
                    }
                    self._$keypad.hide();
                    self._$dialPanel.show();
                    self._$dialPhone.text(self.session._request.from._uri._user);
                    self._$keypadInput.val(self.session._request.from._uri._user);
                    self._$mainButton.hide();
                    self._$incomingButtons.show();

                    self.incomingPlayer.play();
                    self.incomingPlayer.loop = true;

                    // incoming call here
                    self.session.on("accepted", function (data) {
                        // console.log('incoming -> accepted: ', data);
                        self.incomingPlayer.pause();
                        self.incomingPlayer.currentTime = 0;
                        self._$keypad.show();
                        self._$dialPanel.hide();
                        console.log(self._isInCall);
                    });
                    self.session.on("confirmed", function (data) {
                        // console.log('incoming -> confirmed: ', data);
                        // this handler will be called for incoming calls too
                    });
                    self.session.on("ended", function (data) {
                        // console.log('incoming -> ended: ', data);
                        self.do_notify(data.cause);
                        self._cancelCall();
                        self._$keypad.show();
                        self._$dialPanel.hide();
                    });
                    self.session.on("failed", function (data) {
                        // console.log('incoming -> failed: ', data);
                        self.do_notify(data.cause);
                        self._cancelCall();
                        self._$keypad.show();
                        self._$dialPanel.hide();

                        self.incomingPlayer.pause();
                        self.incomingPlayer.currentTime = 0;
                    });
                }
            });

        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _cancelCall() {
            this.$el.css('zIndex', '');
            this._isInCall = false;
            this._showCallButton();
            this._resetMainButton();
            this._$keypad.show();
            this._$dialPanel.hide();
            this._$keypadInput.val("");
        },

        /**
         * @private
         */
        async _makeCall(number) {
            const self = this;
            if (!self._isInCall) {
                if (!number) {
                    self.do_notify(false, _t("The phonecall has no number"));
                    return;
                }
                if (!self._isShow || this._isFolded) {
                    await self._toggleDisplay();
                }
                self._isInCall = true;

                self.eventHandlers = {
                    'connecting': function (data) {
                        // console.log('connecting: ', data)
                        self.dialPlayer.play();
                        self.dialPlayer.loop = true;
                    },
                    'confirmed': function (data) {
                        // console.log('confirmed: ', data);
                    },
                    'accepted': function (data) {
                        // console.log('accepted: ', data)
                        self.dialPlayer.pause();
                        self.dialPlayer.currentTime = 0;
                        self._$keypad.show();
                        self._$dialPanel.hide();
                    },
                    'ended': function (data) {
                        // console.log('ended: ', data);
                        self.do_notify(data.cause);
                        self._cancelCall();
                        self.dialPlayer.pause();
                        self.dialPlayer.currentTime = 0;
                    },
                    'failed': function (data) {
                        // console.log('failed: ', data);
                        self.do_notify(data.cause);
                        self._cancelCall();
                        self.dialPlayer.pause();
                        self.dialPlayer.currentTime = 0;
                    }
                };

                var options = {
                    'eventHandlers': self.eventHandlers,
                    'mediaConstraints': {'audio': true, 'video': false}
                };
                self.session = self._userAgent.call(`sip:${number}`, options);


                this._showHangupButton()
            } else {
                this.do_notify(YOUR_ARE_ALREADY_IN_A_CALL);
            }
        },
        /**
         * start a call on ENTER keyup
         *
         * @private
         * @param {KeyEvent} ev
         */
        _onKeyupKeypadInput(ev) {
            if (ev.keyCode === $.ui.keyCode.ENTER) {
                this._onClickCallButton();
            }
        },

        /**
         * @private
         * @return {Promise}
         */
        async _toggleDisplay() {
            if (this._isShow) {
                if (!this._isFolded) {
                    this.$el.hide();
                    this._isShow = false;
                } else {
                    return this._toggleFold({isFolded: false});
                }
            } else {
                this.$el.show();
                this._isShow = true;

                if (this._isFolded) {
                    await this._toggleFold();
                }
                this._isFolded = false;

            }
        },

        /**
         * @private
         */
        _fold(animate = true) {
            if (animate) {
                this.$el.animate({
                    height: this._isFolded ? HEIGHT_FOLDED : HEIGHT_OPEN,
                });
            } else {
                this.$el.height(this._isFolded ? HEIGHT_FOLDED : HEIGHT_OPEN);
            }
            if (this._isFolded) {
                this.$('.o_dial_fold').css("bottom", "23px");
                this.$('.o_dial_main_buttons').hide();
                this.$('.o_dial_incoming_buttons').hide();
            } else {
                this.$('.o_dial_fold').css("bottom", 0);
                this.$('.o_dial_main_buttons').show();
            }
        },


        /**
         * @private
         * @param {Object} [param0={}]
         * @param {boolean} [param0.isFolded]
         * @return {Promise}
         */
        async _toggleFold({isFolded} = {}) {
            if (!config.device.isMobile) {
                this._isFolded = _.isBoolean(isFolded) ? isFolded : !this._isFolded;
                this._fold();
            }
        },

        /**
         * @private
         */
        _resetMainButton() {
            this._$mainButton.show();
            this._$incomingButtons.hide();
        },

        /**
         * @private
         */
        _showCallButton() {
            this._resetMainButton();
            this._$callButton.addClass('o_dial_call_button');
            this._$callButton.removeClass('o_dial_hangup_button');
            this._$callButton[0].setAttribute('aria-label', _t('Call'));
            this._$callButton[0].title = _t('Call');
        },
        /**
         * @private
         */
        _showHangupButton() {
            this._resetMainButton();
            this._$callButton.removeClass('o_dial_call_button');
            this._$callButton.addClass('o_dial_hangup_button');
            this._$callButton[0].setAttribute('aria-label', _t('End Call'));
            this._$callButton[0].title = _t('End Call');
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * Method handeling the click on the call button.
         * If a phonecall detail is displayed, then call its first number.
         * If there is a search value, we call it.
         * If we are on the keypad and there is a value, we call it.
         *
         * @private
         * @return {Promise}
         */
        async _onClickCallButton() {
            if (!this._active) {
                this.do_notify('Missing configs');
            } else if (this._isInCall) {
                return;
            } else {
                const number = this._$keypadInput.val();
                if (!number) {
                    return;
                }
                this._$keypad.hide();
                this._$dialPanel.show();
                this._$dialPhone.text(number);

                await this._makeCall(number);
            }
        },

        /**
         * @private
         * @return {Promise}
         */
        async _onClickAcceptButton() {
            if (this._isInCall) {
                return;
            } else {
                const callOptions = {mediaConstraints: {audio: true, video: false}};

                this._isInCall = true;
                this._resetMainButton();
                this._showHangupButton();

                this.session.answer(callOptions);
            }
        },

        /**
         * @private
         * @return {Promise}
         */
        async _onClickRejectButton() {
            if (this._isInCall) {
                return;
            } else {
                this.session.terminate();
                this._$keypad.show();
                this._$dialPanel.hide();
                this._$keypadInput.val("");
                this._resetMainButton();
            }
        },

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onClickDialNumber(ev) {
            ev.preventDefault();
            this._$keypadInput.focus();
            this._onKeypadButtonClick(ev.currentTarget.textContent);
        },
        /**
         * @private
         * @return {Promise}
         */
        async _onClickFold() {
            return this._toggleFold();
        },
        /**
         * @private
         */
        _onClickHangupButton() {
            this._cancelCall();
            this.session.terminate();
        },
        /**
         * @private
         */
        _onClickKeypadBackspace() {
            this._$keypadInput.val(this._$keypadInput.val().slice(0, -1));
        },

        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onClickWindowClose(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            this.$el.hide();
            this._isShow = false;
        },

        /**
         * @private
         * @param {string} number the keypad number clicked
         */
        _onKeypadButtonClick(number) {
            if (this._isInCall) {
                this.session.sendDTMF(number);
            } else {
                this._$keypadInput.val(this._$keypadInput.val() + number);
            }
        },

        /**
         * @private
         */
        async _onToggleDisplay() {
            await this._toggleDisplay();
        },
    });

    return DialingPanel;

});
