import {html, useContext} from "../preact.mjs";
import {AppContext} from "./app.mjs";

export function Link(props) {
    let app = useContext(AppContext).app;

    const onClick = event => {
        event.preventDefault();
        app.relocate(event.currentTarget.href);
    };

    return html`<a ...${this.props} onclick=${onClick}>${props.children}</a>`;
}