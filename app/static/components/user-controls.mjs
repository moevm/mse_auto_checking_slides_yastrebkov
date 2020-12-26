import {AppContext} from "./app.mjs";
import {html, useContext} from '../preact.mjs';

export function UserControls(props) {
    const app = useContext(AppContext);

    let controls = !props.userName ?
        html`
            <button onclick=${() => app.relocate('/sign-in')}>Войти
            </button><button onclick=${() => app.relocate('/sign-up')}>Регистрация</button>
        `
        :
        html`
            <div class="user-name">${props.userName}</div>
            <button onclick=${() => app.logOut()}>Выйти</button>
        `;

    return html`<div id="user-controls">${controls}</div>`;
}