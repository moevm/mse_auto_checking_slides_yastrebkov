import {SignInUpFormBase} from "./sign-in-up-form-base.mjs";

export class SignUpForm extends SignInUpFormBase {
    constructor(props) {
        super(props);
        this._actionName = 'Зарегистрироваться';
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
                autocomplete: 'new-password',
                stateKey: 'password',
            },
            {
                placeholder: 'Пароль ещё раз',
                type: 'password',
                autocomplete: 'new-password',
                stateKey: 'passwordAgain',
            },
        ];
        this._signActionUrl = '/api/sign-up';
        this._failMessage = 'Пользователь с таким логином существует';
    }

    _isGoodForm() {
        if (this.state.login.length < 2) {
            this.setState({message: "Слишком короткий логин"});
            return false;
        }
        if (this.state.password.length < 2) {
            this.setState({message: "Слишком короткий пароль"});
            return false;
        }
        if (this.state.password !== this.state.passwordAgain) {
            this.setState({message: "Пароли не совпадают"});
            return false;
        }
        return true;
    }
}