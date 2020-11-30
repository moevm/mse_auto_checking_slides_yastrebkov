import {Component, html, useContext} from "../preact.mjs";
import {AppContext} from "./app.mjs";
import {post} from "../ajax.mjs";

export class SignInUpFormBase extends Component {
    constructor(props) {
        super(props);
        this.state = { message: '', login: '', password: '' };
    }

    _onSubmit(submitEvent) {
        submitEvent.preventDefault();

        if (this._isGoodForm && !this._isGoodForm())
            return;

        post(this._signActionUrl, {
            login: this.state.login,
            password: this.state.password,
        })
        .then(result => {
            if (!result)
                return;

            if (result.success) {
                this._app.rememberSignIn(this.state.login, result.token);
                this._app.relocate('/');
            }
            else
                this.setState({message: this._failMessage});
        });
    }

    _inputSyncer(stateKey) {
        return event => this.setState({[stateKey]: event.currentTarget.value});
    }

    render() {
        this._app = useContext(AppContext);

        const controls = html`${
            this._controls.map(control => html`
                <input class="sign-in-out-input" placeholder=${control.placeholder} type=${control.type}
                    autocomplete=${control.autocomplete}
                    onchange=${this._inputSyncer(control.stateKey)} />
            `)
        }`;

        let message = null;
        if (this.state.message)
            message = html`<div class="error-message">${this.state.message}</div>`;

        return html`
            <form class="sign-in-out-form" onsubmit=${this._onSubmit.bind(this)}>
                ${controls}
                ${message}
                <button>${this._actionName}</button>
            </form>
        `;
    }
}