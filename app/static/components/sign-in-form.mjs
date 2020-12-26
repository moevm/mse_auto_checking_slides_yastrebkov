import {SignInUpFormBase} from "./sign-in-up-form-base.mjs";

export class SignInForm extends SignInUpFormBase {
    constructor(props) {
        super(props);
        this._actionName = 'Войти';
        this._controls = [
            {
                placeholder: 'Логин',
                type: 'text',
                autocomplete: 'username',
                stateKey: 'login',
            },
            {
                placeholder: 'Пароль',
                type: 'password',
                autocomplete: 'current-password',
                stateKey: 'password',
            },
        ];
        this._signActionUrl = '/api/sign-in';
        this._failMessage = 'Неверный логин или пароль';
    }
}